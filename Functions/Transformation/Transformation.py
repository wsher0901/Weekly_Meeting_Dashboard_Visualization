import pandas as pd
import numpy as np
from datetime import timedelta, datetime, date 
from Functions.Visualization.utility import remove_columns
from Files.common_list import test_list_concise_map, hla_removal_list, nonhla_removal_list, comment_category, gene_list, nonhla_gene_list, client_removal_list, hla_extension_list

def high_volume_transform(list_of_dataframe):
    
    def split_gene(df):
        df.Gene = df.apply(lambda row: row['Gene'].split(','),axis=1)
        df = df.explode('Gene')
        return df

    def edit_country_name(df):
        df.Country = df.apply(lambda row: row['Country'].strip() if row['Country'] not in ['UK','USA'] \
                                else ('United Kingdom' if row['Country'] == 'UK' else 'United States of America'),axis=1)
        return df

    def truncate_gene_name(df):
        df.Gene = df.apply(lambda row: test_list_concise_map[row['Gene']] if row['Gene'] in test_list_concise_map else row['Gene'],axis=1)
        return df

    def distinguish_old_and_new_sample(df):
        df.ClientProjectName = df.apply(lambda row: row['ClientProjectName'] if row['RequestType'] == 'New' \
                                        else row['ClientProjectName'] + ' (Rerequest)',axis=1)
        df.ClientName = df.apply(lambda row: row['ClientName'] if row['RequestType'] == 'New' else row['ClientName']+' (ReRequest)',axis=1)
        return df

    def rename_first_table_columns(df):
        df = df.rename(columns={'ClientName':'Client','ClientProjectName':'Project','ReceivedDate':'Date','ClientSampleID':'Sample ID','RequestType':'Request Type'})
        return df

    def rename_second_table_columns(df):
        df = df.rename(columns={'DNAType':'Type','GeneGroupName':'Gene','DateofUsage':'Date','DNADay':'Day','SampleCount':'Sample Count'})
        return df

    def rename_thrid_table_columns(df):
        df = df.rename(columns={'DNAType':'Type','SampleCount':'Sample Count'})
        return df[['Type','Sample Count']]
    
    output = []
    df1 = list_of_dataframe[0]
    df1 = split_gene(df1)
    df1 = edit_country_name(df1)
    df1 = truncate_gene_name(df1)
    #df1 = distinguish_old_and_new_sample(df1)
    df1 = rename_first_table_columns(df1)

    df2 = list_of_dataframe[1]
    df2 = rename_second_table_columns(df2)

    df3 = list_of_dataframe[2]
    df3 = rename_thrid_table_columns(df3)

    output.extend([df1,df2,df3])

    return output

def cmv_transform(list_of_dataframe):
    column_rename = {'CMVType':'Type','ExperimentName':'Experiment Names','ClientName':'Client Names','CMVDate':'Experiment Date',
                     'CMVDay':'Day','UserName':'Experiment By','StatsDay':'Elisa Date','NoOfSample':'Total Number of Samples',
                     'NoOfPositive':'Number of Positive','NoOfNegative':'Number of Negative','NoOfEquivocal':'Number of Equivocal',
                     '%OfPositive':'Rate of Positive','%OfNegative':'Rate of Negative','%OfEquivocal':'Rate of Equivocal',
                     'ClientNames':'Client Names','ClientSampleID':'Sample ID','OODValue':'Observed OD Value','AdjustedODValue':'Adjusted OD Value',
                     'RI':'RI (Relative Index)'}
    
    output = []
    list_of_dataframe = [i.rename(columns=column_rename) for i in list_of_dataframe]
    
    def aggregation(df):
        return df.groupby(['Type','Experiment Date','Day']).agg({'SampleID':'count',
                                                               'Experiment By':lambda x: ','.join(x),
                                                               'Experiment Names': lambda x: ','.join(x),
                                                               'Client Names': lambda x: ','.join(x)}).reset_index()
    
    def leave_only_unique_values(df):
        def remove_redundancy(*args):
            return [', '.join(set(i.split(','))) for i in args]

        df[['Experiment By','Experiment Names','Client Names']] = df.apply(lambda row: pd.Series(remove_redundancy(row['Experiment By'],row['Experiment Names'],row['Client Names'])),axis=1)
        return df
    
    def rename_and_order_first_table(df):
        df = df.rename(columns={'SampleID':'Sample Count'})
        df = df[['Type','Experiment Names','Client Names', 'Experiment Date','Day','Experiment By','Sample Count']]
        return df 
    
    def rename_and_order_second_table(df):
        return df[['Elisa Date','Experiment Names','Client Names','Experiment By','Total Number of Samples',
                          'Number of Negative','Number of Positive','Number of Equivocal','Rate of Negative','Rate of Positive','Rate of Equivocal']]
    
    def rename_and_order_remaining_table(df):
        return df[['Elisa Date','Experiment Names','Sample ID','Position','Observed OD Value','Adjusted OD Value','RI (Relative Index)']]

    df1 = list_of_dataframe[0]
    df1 = aggregation(df1)
    df1 = leave_only_unique_values(df1)
    df1 = rename_and_order_first_table(df1)
    output.append(df1)

    df2 = list_of_dataframe[2]
    df2 = rename_and_order_second_table(df2)
    output.append(df2)

    for df in list_of_dataframe[4:]:
        output.append(rename_and_order_remaining_table(df))
    
    for i in output:
        i.index += 1 

    return output

def low_volume_transform(list_of_dataframe):

    def reorder_second_table(df):
        return df[['Type','Project','A','B','C','DRB1','DRB345','DQB1','DQA1','DPB1','DPA1']]
    
    def edit_country_name(df):
        df['Country'] = df.apply(lambda row: row['Country'].strip().capitalize() if row['Country'] not in ['UK','USA'] \
                                else ('United Kingdom' if row['Country'] == 'UK' else 'United States of America'),axis=1)
        return df
    
    def truncate_gene_name(df):
        df['Gene'] = df.apply(lambda row: test_list_concise_map[row['Gene']] if row['Gene'] in test_list_concise_map else row['Gene'],axis=1)
        return df 

    column_rename = {'ClientProjectName':'Project','ClientType':'Type','ClientProjectType':'Type','GeneGroupName':'Gene','ReceivedDate':'Date','SampleCount':'Sample Count'}
    list_of_dataframe = [i.rename(columns=column_rename) for i in list_of_dataframe]
    
    df1 = remove_columns(list_of_dataframe[0],['ID'])

    df2 = remove_columns(list_of_dataframe[1],['ClientID','ClientProjectID','ParentID'])
    df2 = reorder_second_table(df2)

    df3 = remove_columns(list_of_dataframe[2],['ID'])

    df4 = remove_columns(list_of_dataframe[3],['ParentID'])
    
    df5 = remove_columns(list_of_dataframe[5],['ParentID'])
    df5 = edit_country_name(df5)
    df5 = df5.groupby('Country')['Sample Count'].sum().reset_index()

    df6 = remove_columns(list_of_dataframe[6],['ID'])
    df6 = truncate_gene_name(df6)

    df7 = remove_columns(list_of_dataframe[7],['RowID','ParentID','ClientID'])
    df7 = truncate_gene_name(df7)

    return [df1,df2,df3,df4,df5,df6,df7]

def pcr_transform(list_of_dataframe):
    column_rename = {'PCRType':'Type','GeneGroupName':'Gene','BlotCount':'Blot Count',
                        'SampleCount':'Sample Count','PlateCount':'Plate Count','BlotNames':'Blot Names',
                        'PlateNames':'Plate Names','DateofUsage':'Date'}

    def merge_first_and_second_table(df1,df2):
        temp = df1[['PCRType','ExperimentProjectTypeID']].merge(df2,'left',left_on='ExperimentProjectTypeID',right_on='ParentID')
        temp = temp[['PCRType','ExperimentProjectTypeID','ID','GeneGroupName']]
        return temp
    
    def merge_second_and_third_table(df1,df2):
        temp = df1.merge(df2,'left',left_on = ['ExperimentProjectTypeID','ID'],right_on = ['ExperimentProjectTypeID','ParentID'])
        return temp
    
    def rename_columns(df):
        return df.rename(columns=column_rename)

    def remove_duplicate(df):
        return df[['Type','Gene','Date','Blot Count','Sample Count','Plate Count','Blot Names','Plate Names']].drop_duplicates()
    
    def truncate_gene_name(df):
        df.Gene = df.apply(lambda row: test_list_concise_map[row['Gene']] if row['Gene'] in test_list_concise_map else row['Gene'],axis=1)
        return df

    output = merge_first_and_second_table(list_of_dataframe[0],list_of_dataframe[1])
    output = merge_second_and_third_table(output,list_of_dataframe[2])
    output = rename_columns(output)
    output = remove_duplicate(output)
    output = truncate_gene_name(output)
    return output

def gel_transform(list_of_dataframe):
    id_to_type = {1:'Illumina',2:'Pacbio'}
    column_rename = {'GelType':'Type','GelCount':'Gel Count','AmpliconCount':'Amplicon Count','ReRunCount':'Rerun Count',
                     'RepeatCount':'Repeat Count','TotalAmplicons':'Total Amplicons','GelRowCount':'Gel Row Count',
                     'DateofUsage':'Date','BlotCount':'Blot Count','BlotCategory':'Category','PCRBarcode':'Barcode',
                     'PlateName':'Plate Name','ReviewrComments':'Comment','ReviewedonStringFormat':'Date',
                     'RejectionType':'Rejection Type','ImageDetailId':'Image ID','GelExperimentID':'Gel Experiment ID'}
    
    def convert_id_to_type(df,column_name):
        df[column_name] = df.apply(lambda row: id_to_type[row[column_name]],axis=1)
        return df.rename(columns={column_name:'Type'})
    
    list_of_dataframe = [i.rename(columns=column_rename) for i in list_of_dataframe]

    list_of_dataframe[0] = remove_columns(list_of_dataframe[0],'ID')

    list_of_dataframe[1] = remove_columns(list_of_dataframe[1],['RowID','ID'])
    list_of_dataframe[1] = convert_id_to_type(list_of_dataframe[1],'ParentID')

    list_of_dataframe[2] = remove_columns(list_of_dataframe[2],'ID')

    list_of_dataframe[3] = remove_columns(list_of_dataframe[3],['RowID','ID'])
    list_of_dataframe[3] = convert_id_to_type(list_of_dataframe[3],'ParentID')

    list_of_dataframe[5] = remove_columns(list_of_dataframe[5],'RowID')

    return [list_of_dataframe[0],list_of_dataframe[1],list_of_dataframe[2],list_of_dataframe[3],list_of_dataframe[5]]

def illumina_transform(list_of_dataframe):
    list_of_dataframe[0] = remove_columns(list_of_dataframe[0],['ID','SampleCount','AmpliconCount','TotalCells','PoolThreshold'])
    list_of_dataframe[0] = list_of_dataframe[0].rename(columns={'NGSType':'NGS Type','RunCount':'Run Count'})

    list_of_dataframe[1] = remove_columns(list_of_dataframe[1],'ID')
    list_of_dataframe[1] = list_of_dataframe[1].rename(columns={'NGSType':'NGS Type','DateofUsage':'Date','NGSExperimentName':'Experiment','TotalCells':'Total Cells',
                                                                'PoolThreshold':'Pool Threshold','ExperimentID':'Experiment ID','ReagentKitVersion':'Kit Version'})

    list_of_dataframe[2] = remove_columns(list_of_dataframe[2],['RowID','ExperimentID','PlateNumber','CreatedOn','CreatedBy','GeneID','GeneGroupID','ParentID','NGSExperimentName'])

    return list_of_dataframe

def pacbio_transform(list_of_dataframe):
    list_of_dataframe[0] = remove_columns(list_of_dataframe[0],['ID','SampleCount','AmpliconCount','TotalCells'])
    list_of_dataframe[0] = list_of_dataframe[0].rename(columns={'PacbioType':'Pacbio Type','RunCount':'Run Count'})

    list_of_dataframe[1] = remove_columns(list_of_dataframe[1],['RowID','ParentID','ID','MachineNumber','MachineTypeID','RunCount','SampleCount','AmpliconCount'])
    list_of_dataframe[1] = list_of_dataframe[1].rename(columns={'DateofUsage':'Date','MachineType':'Machine Type','TotalCells':'Total Cells','JobName':'Job Name',
                                                                'RunName':'Run Name','JobType':'Job Type'})
    return list_of_dataframe

def repeats_transform(data,protocol_type,lw):
    repeat_list = gene_list + ['Overall']
    column_list = [f"{cat} {stat}" for cat in repeat_list for stat in ['Total','Repeat','%']]

    def remove_client(data):
        return [i for i in data if i[0] not in client_removal_list]

    def convert_gene_list(genes):
        total = []
        for i in gene_list:
            if i not in genes.split(', '):
                total.append(0)
            else:
                total.append(1)
        return total

    def sort_by(data,category):
        index = 1 if category == 'Experiment' else 0
        output = {}
        for i in data:
            if i[index] not in output:
                output[i[index]] = [i]
            else:
                output[i[index]].append(i)
        return output

    def aggregate_statistics(data):
        output = {}
        for experiment in data.keys():
            output[experiment] = {}
            total = [sum(column) for column in zip(*[i[3] for i in data[experiment]])]
            repeat = [sum(column) for column in zip(*[i[4] for i in data[experiment]])]
            output[experiment]['Total'] = total
            output[experiment]['Repeat'] = repeat
            output[experiment]['Repeat Rate'] = [round(repeat/total*100,2) if total != 0 else np.nan for repeat, total in zip(repeat, total)]
            overall = len(data[experiment])
            overall_repeat = len([i for i in data[experiment] if sum(i[4]) != 0])
            output[experiment]['Total'].append(overall)
            output[experiment]['Repeat'].append(overall_repeat)
            output[experiment]['Repeat Rate'].append(round(overall_repeat/overall*100,2))
        return output        

    def reorganize(data,date):
        date = date
        temp = []
        for i in data:
            t = [i,date]
            for j in range(0,10,1):
                for k in ['Total','Repeat','Repeat Rate']:
                    t.append(data[i][k][j])
            temp.append(t)
        return pd.DataFrame(temp,columns=['Experiment','Date']+column_list)
    
    data = remove_client(data)
    data = [list(i[0:3]) + [convert_gene_list(i[3])] + [convert_gene_list(i[4])] + list(i[5:]) + [protocol_type[i[-1]]] if i[-1] in protocol_type \
        else list(i[0:3]) + [convert_gene_list(i[3])] + [convert_gene_list(i[4])] + list(i[5:]) + ['NA'] for i in data]
    
    ngs, pac = sort_by([x for x in data if x[6] == 'NGS' or x[-1] == '1KB'],'Experiment'), sort_by([x for x in data if x[6] == 'Pacbio' and x[-1] == '4XALL'],'Experiment')
    ngs, pac = aggregate_statistics(ngs), aggregate_statistics(pac)

    ngs_by_client, pac_by_client = sort_by([x for x in data if x[6] == 'NGS' or x[-1] == '1KB'],'Client'), sort_by([x for x in data if x[6] == 'Pacbio' and x[-1] == '4XALL'],'Client')
    ngs_by_client, pac_by_client = aggregate_statistics(ngs_by_client), aggregate_statistics(pac_by_client)

    return reorganize(ngs,lw), reorganize(pac,lw), reorganize(ngs_by_client,lw), reorganize(pac_by_client,lw)

def reagents_transform(list_of_dataframe):
    column_rename = {'BufferName':'Buffer Name','LotNumber':'Lot #','MakeDate':'Make Date','ExpDate':'Expiry Date','CreatedBy':'Prepared By','BufferLotID':'Buffer Lot ID',
                     'BufferProcess':'Buffer Process','QtyMade':'Qty Made','AlliquotedQty':'Aliquoted Qty','ReactionsCnt':'# of Reactions','PrimerMixName':'Primer Name',
                     'PrimerMixLotID':'Primer Mix Lot ID','PrimerMixProcess':'Primer Mix Process','StorageLocationName':'Storage Location','PrimerName':'Primer Name',
                     'DispensingDate':'Dispense Date','UserName':'Dispensed By','TotalPlates':'# of Plates','DispensingMachine':'Dispensing Machine','MasterMixName':'Master Mix Name'}
    
    def align_unit(df,unit):
        def convert(row):
            quantity, metric = row.split(' ')
            if unit == 'L':
                if metric in ['L','Litre']:
                    return quantity + ' L'
                else:
                    return str(float(quantity)/1000) + ' L'
            else:
                if metric in ['L','Litre']:
                    return str(float(quantity) * 1000) + ' ml'
                else:
                    return quantity + ' ml'
        if len(df) != 0:
            df['Qty Made'] = df.apply(lambda row: convert(row['Qty Made']),axis=1)
        return df 

            
    list_of_dataframe = [i.rename(columns=column_rename) for i in list_of_dataframe]
    list_of_dataframe[0] = align_unit(list_of_dataframe[0],'L')[['Buffer Name','Lot #','Make Date','Expiry Date','Prepared By','Qty Made','Aliquoted Qty','# of Reactions']]
    list_of_dataframe[1] = align_unit(list_of_dataframe[1],'ml')[['Primer Name','Lot #','Make Date','Expiry Date','Prepared By','Qty Made','Aliquoted Qty','# of Reactions','Storage Location']]
    list_of_dataframe[2] = list_of_dataframe[2][['Primer Name','Lot #','Dispense Date','Dispensed By','Dispensing Machine','# of Plates','Storage Location']]
    list_of_dataframe[4] = align_unit(list_of_dataframe[4],'L')[['Master Mix Name','Lot #','Make Date','Expiry Date','Prepared By','Qty Made','Aliquoted Qty','# of Reactions','Storage Location']]

    return [list_of_dataframe[0],list_of_dataframe[1],list_of_dataframe[2],list_of_dataframe[4]]

def hla_tat_transform(list_of_dataframe,lw,tw):
    column_rename = {'ClientProjectID':'Client Project ID','ClientProjectName':'Project Name','ShipmentDate':'Shipment Date','SampleCount':'Sample Count','Class1TAT':'Class I TAT',
                     'Class2TAT':'Class II TAT','C1ReportCount':'C1 Report','C2ReportCount':'C2 Report','C1QueueCount':'C1 Queue','C2QueueCount':'C2 Queue','C1NotReportCount':'C1 Not Reported',
                     'C2NotReportCount':'C2 Not Reported','C1ReqCount':'C1 Requested','C2ReqCount':'C2 Requested','C1C2QueueCount':'C1&C2 Queue','HoldReportStatus':'Hold STatus',
                     'ClientID':'Client ID','C1Resolution':'C1 Resolution','C2Resolution':'C2 Resolution','HeaderComment':'Header','FinalDue':'Final Due','ReceivedDate':'Received Date',
                     'ReportCommentCategoryID':'Comment Category','ReportSubcomments':'Sub Comment','FullName':'Made by'}
        
    def add_label(df,label):
        df['Type'] = label
        return df 
    
    def turn_date_into_datetime(df):
        df['ShipmentDate'] = df.apply(lambda row: row['ShipmentDate'].date(),axis=1) 
        return df 
    
    def merge_data(data,extension,comment):
        df = pd.merge(data,extension.drop_duplicates(subset=['ClientProjectID']),on='ClientProjectID',how='left')
        df = pd.merge(df,comment,on=['ClientProjectID','Type','ShipmentDate'],how='left')
        return df 
    
    def edit_final_due(df):
        def add_final_due(row):
            if row['ClientProjectName'] != 'NatKidneyRegistry STAT HLA ABORH':
                return row['FinalDue']
            else:
                if row['FinalDue'] != None:
                    return row['FinalDue']
                else:
                    if row['Class1TAT'].weekday() == 1:
                        return row['Class1TAT'] + timedelta(days=3)
                    else:
                        return row['Class1TAT'] + timedelta(days=4)
                    
        df['FinalDue'] = df.apply(lambda row: add_final_due(row),axis=1)
        return df 
    
    def remove_client(df,remove_list):
        return df[~df['ClientProjectName'].isin(remove_list)]
    
    def filter_with_date(df,column,lw,tw):
        if date.today() >= lw and date.today() <= tw:
            if date.today().weekday() == 3:
                return df[(df[column] >= lw) & (df[column] <= tw)]
            else:
                return df[(df[column] >= lw) & (df[column] <= date.today())]
        else:
            return df[(df[column] >= lw) & (df[column] <= tw)] 
        
    def add_new_columns(df,by_TAT):
        def determine_delay(row, filter_list, by_TAT):
            c1,c2 = ['C1ReportWithinTATCount','C2ReportWithinTATCount'] if by_TAT else ['C1ReportWithinFinalCount','C2ReportWithinFinalCount']
            rate = 90
            if by_TAT:
                if (row['ClientProjectName'] in filter_list and row['Type'] == 'Non-Clinical') or row['Type'] == 'Clinical':
                    rate = 100
            else:
                rate = 100
            if row['C1ReqCount'] == 0:
                if row[c2]/row['C2ReqCount']*100 < rate:
                    return 'Delayed'
                else:
                    return 'Completed'
            
            elif row['C2ReqCount'] == 0:
                if row[c1]/row['C1ReqCount']*100 < rate:
                    return 'Delayed'
                else:
                    return 'Completed'

            elif row['C1ReqCount'] != 0 and row['C2ReqCount'] != 0:
                if row[c1]/row['C1ReqCount']*100 >= rate and row[c2]/row['C2ReqCount']*100 >= rate:
                    return 'Completed'
                else:
                    return 'Delayed'
                
        def modify_comment_category(row):
            if row['Delay Status'] == 'Delayed':
                if pd.isnull(row['ReportCommentCategoryID']) == True:
                    if pd.isnull(row['IsMultipleExtensionRequestAllowed']) == True:
                        return 'Not Commented'
                    else:
                        if row['ClientProjectName'] not in hla_extension_list:
                            return 'Extended'
                        else:
                            return 'Not Commented'
                else:
                    return comment_category[row['ReportCommentCategoryID']]
            else:
                return ''
            
        def calculate_percentage(column1: pd.Series,column2: pd.Series,percent: bool)-> str:
            if percent:
                if column2 != 0:
                    return str(round(column1/column2*100,2))+'%'
                else:
                    return 'NaN'
            else:
                if column2 != 0:
                    return str(int(column1))+'/'+str(int(column2))
                else:
                    return 'NaN'

        if by_TAT:
            df['Delay Status'] = df.apply(lambda row: determine_delay(row,hla_removal_list,by_TAT),axis=1)
            df['ReportCommentCategoryID'] = df.apply(lambda row: modify_comment_category(row),axis=1)
            df['C1 by TAT'] = df.apply(lambda row: calculate_percentage(row['C1ReportWithinTATCount'],row['C1ReqCount'],False),axis=1)
            df['C1% by TAT'] = df.apply(lambda row: calculate_percentage(row['C1ReportWithinTATCount'],row['C1ReqCount'],True),axis=1)
            df['C2 by TAT'] = df.apply(lambda row: calculate_percentage(row['C2ReportWithinTATCount'],row['C2ReqCount'],False),axis=1)
            df['C2% by TAT'] = df.apply(lambda row: calculate_percentage(row['C2ReportWithinTATCount'],row['C2ReqCount'],True),axis=1)
            df['C1 by Today'] = df.apply(lambda row: calculate_percentage(row['C1ReportCount'],row['C1ReqCount'],False),axis=1)
            df['C1% by Today'] = df.apply(lambda row: calculate_percentage(row['C1ReportCount'],row['C1ReqCount'],True),axis=1)
            df['C2 by Today'] = df.apply(lambda row: calculate_percentage(row['C2ReportCount'],row['C2ReqCount'],False),axis=1)
            df['C2% by Today'] = df.apply(lambda row: calculate_percentage(row['C2ReportCount'],row['C2ReqCount'],True),axis=1)
            df['By TAT'] = df.apply(lambda row: f"({row['C1ReportWithinTATCount']}/{row['C1ReqCount']}), ({row['C2ReportWithinTATCount']}/{row['C2ReqCount']})",axis=1)
            df['By Today'] = df.apply(lambda row: f"({row['C1ReportCount']}/{row['C1ReqCount']}), ({row['C2ReportCount']}/{row['C2ReqCount']})",axis=1)
            df = df.drop_duplicates(subset=['ClientProjectID','ShipmentDate','Class1TAT','SampleCount','C1% by TAT','C2% by TAT','C1 by TAT','C2 by TAT','Type'])
        else:
            df['Delay Status'] = df.apply(lambda row: determine_delay(row,hla_removal_list,by_TAT),axis=1)
            df['ReportCommentCategoryID'] = df.apply(lambda row: modify_comment_category(row),axis=1)
            df['C1 by Final'] = df.apply(lambda row: calculate_percentage(row['C1ReportWithinFinalCount'],row['C1ReqCount'],False),axis=1)
            df['C1% by Final'] = df.apply(lambda row: calculate_percentage(row['C1ReportWithinFinalCount'],row['C1ReqCount'],True),axis=1)
            df['C2 by Final'] = df.apply(lambda row: calculate_percentage(row['C2ReportWithinFinalCount'],row['C2ReqCount'],False),axis=1)
            df['C2% by Final'] = df.apply(lambda row: calculate_percentage(row['C2ReportWithinFinalCount'],row['C2ReqCount'],True),axis=1)
            df['C1 by Today'] = df.apply(lambda row: calculate_percentage(row['C1ReportCount'],row['C1ReqCount'],False),axis=1)
            df['C1% by Today'] = df.apply(lambda row: calculate_percentage(row['C1ReportCount'],row['C1ReqCount'],True),axis=1)
            df['C2 by Today'] = df.apply(lambda row: calculate_percentage(row['C2ReportCount'],row['C2ReqCount'],False),axis=1)
            df['C2% by Today'] = df.apply(lambda row: calculate_percentage(row['C2ReportCount'],row['C2ReqCount'],True),axis=1)
            df['By Final'] = df.apply(lambda row: f"({row['C1ReportWithinFinalCount']}/{row['C1ReqCount']}), ({row['C2ReportWithinFinalCount']}/{row['C2ReqCount']})",axis=1)
            df['By Today'] = df.apply(lambda row: f"({row['C1ReportCount']}/{row['C1ReqCount']}), ({row['C2ReportCount']}/{row['C2ReqCount']})",axis=1)
            df = df.drop_duplicates(subset=['ClientProjectID','ShipmentDate','FinalDue','SampleCount','C1% by Final','C2% by Final','C1 by Final','C2 by Final','Type'])
        return df
    
    def add_time(df,due_date):
        columns_to_check = ['ClientProjectName', due_date,'Type']
        temp = df[df.duplicated(subset=columns_to_check, keep=False)]
        temp = temp.groupby(['ClientProjectName',due_date])['Type'].count()
        temp = temp.reset_index().values.tolist()
        duplicates = {}
        for i in temp:
            if i[0] not in duplicates:
                duplicates[i[0]] = {i[1]:[i[2], datetime.combine(i[1],datetime.min.time()) - timedelta(hours=11)]}
            else:
                duplicates[i[0]][i[1]] = [i[2], datetime.combine(i[1],datetime.min.time()) - timedelta(hours=11)]

        start = []
        end = []
        for index,row in df.iterrows():
            if row['ClientProjectName'] not in duplicates:
                start.append(datetime.combine(row[due_date], datetime.min.time()) - timedelta(hours=11))
                end.append(datetime.combine(row[due_date], datetime.min.time()) + timedelta(hours=11))
            else:
                if row[due_date] not in duplicates[row['ClientProjectName']]:
                    start.append(datetime.combine(row[due_date], datetime.min.time()) - timedelta(hours=11))
                    end.append(datetime.combine(row[due_date], datetime.min.time()) + timedelta(hours=11))
                else:
                    divide = duplicates[row['ClientProjectName']][row[due_date]][0]
                    individual_hour = (22 - (divide-1)*0.5)/ divide
                    begin_time = duplicates[row['ClientProjectName']][row[due_date]][1]
                    start.append(begin_time)
                    end.append(begin_time+timedelta(hours=individual_hour))
                    duplicates[row['ClientProjectName']][row[due_date]][1] = begin_time + timedelta(hours=individual_hour) + timedelta(hours=0.5)

        df['Start'] = start
        df['Finish'] = end
        return df
    
    non_clinical = add_label(list_of_dataframe[0],'Non-Clinical')
    non_clinical_comment = add_label(list_of_dataframe[1],'Non-Clinical')
    clinical = add_label(list_of_dataframe[2],'Clinical')
    clinical_comment = add_label(list_of_dataframe[3],'Clinical')

    data = pd.concat([non_clinical,clinical],ignore_index=True)
    data = turn_date_into_datetime(data)

    comment = pd.concat([non_clinical_comment,clinical_comment],ignore_index=True)
    comment = turn_date_into_datetime(comment)

    df = merge_data(data,list_of_dataframe[4],comment)
    df = df[pd.isna(df.ClientProjectName) == False]
    df = edit_final_due(df)
    df = df.drop_duplicates()
    df = remove_client(df,['HISTO QC'])
    df_tat, df_final = filter_with_date(df,'Class1TAT',lw,tw), filter_with_date(df,'FinalDue',lw,tw)
    df_tat, df_final = add_new_columns(df_tat,True), add_new_columns(df_final,False)
    df_tat, df_final = add_time(df_tat,'Class1TAT'), add_time(df_final,'FinalDue')
    df_tat, df_final = df_tat.rename(columns=column_rename), df_final.rename(columns=column_rename)
    return df_tat, df_final

def non_hla_tat_transform(list_of_dataframe,lw,tw):
    column_rename = {'ClientDisplayName':'Client Name','ClientProjectID':'Client Project ID','ClientProjectName':'Project Name','ClientProjectCode':'Project Code',
                     'ShipmentDate':'Shipment Date','GeneGroupName':'Gene','FinalDue':'Final Due','DateAdded':'Commented Date'}
    
    def remove_client(df):
        return df[~df['ClientProjectName'].isin(nonhla_removal_list)]
    
    def merge_data(data,extension,comment):
        df = pd.merge(data,extension.drop_duplicates(subset=['ClientProjectID']),on='ClientProjectID',how='left')
        df = pd.merge(df,comment,on=['ClientProjectID','ShipmentDate'],how='left')
        return df 
    
    def pipeline(df,col,lw,tw):
        def filter_data_with_date(df,col,lw,tw):
            if date.today() >= lw and date.today() <= tw:
                if date.today().weekday() == 3:
                    return df[(df[col] >= lw) & (df[col] <= tw)]
                else:
                    return df[(df[col] >= lw) & (df[col] <= date.today())]
            else:
                return df[(df[col] >= lw) & (df[col] <= tw)]
        
        def calculate_delay(df,col):
            if col == 'TAT':
                df['TAT Report %'] = df.apply(lambda row: str(round(100*row['ReportWithinTATCount']/row['Total'],2))+'%',axis=1)
                df['Today Report %'] = df.apply(lambda row: str(round(100*row['Reported']/row['Total'],2))+'%',axis=1)
                df['Delay Status'] = df.apply(lambda row: 'Completed' if float(row['TAT Report %'][:-1]) >= 90 else 'Delayed',axis=1)
            else:
                df['Final Report %'] = df.apply(lambda row: str(round(100*row['ReportWithinFinalCount']/row['Total'],2))+'%',axis=1)
                df['Today Report %'] = df.apply(lambda row: str(round(100*row['Reported']/row['Total'],2))+'%',axis=1)
                df['Delay Status'] = df.apply(lambda row: 'Completed' if float(row['Final Report %'][:-1]) == 100 else 'Delayed',axis=1)
            return df
    
        def add_display_text(df,col):
            if col == 'TAT':
                df['Display Text'] = df.apply(lambda row: f"{row['ReportWithinTATCount']}/{row['Total']} ({row['TAT Report %']})",axis=1)
            else:
                df['Display Text'] = df.apply(lambda row: f"{row['ReportWithinFinalCount']}/{row['Total']} ({row['Final Report %']})",axis=1)
            return df
        
        df = filter_data_with_date(df,col,lw,tw)
        df = calculate_delay(df,col)
        df = add_display_text(df,col)
        df = df.drop_duplicates(subset=['ClientProjectName','ClientProjectID','ShipmentDate','TotalinShipment','GeneGroupName',col],keep='first')
        return df 

    def modify_comment_category(df):
        def modify(row):
            exception_list = ['NatKidneyRegistry STAT HLA ABORH']
            if row['Delay Status'] == 'Delayed':
                if pd.isnull(row['ReportCommentCategoryID']) == True:
                    if pd.isnull(row['IsMultipleExtensionRequestAllowed']) == True:
                        return 'Not Commented'
                    else:
                        if row['ClientProjectName'] not in hla_extension_list:
                            return 'Extended'
                        else:
                            return 'Not Commented'
                else:
                    return comment_category[row['ReportCommentCategoryID']]
            else:
                return 'Completed'
        df['Comment Category'] = df.apply(lambda row: modify(row),axis=1)
        return df
    
    def group_data(df):
        df_dict = {}
        for i in nonhla_gene_list:
            if i in df.Gene.unique():
                df_dict[i] = df[df['Gene'] == i]
            
        return df_dict
        
    df = list_of_dataframe[0]
    df['TAT'] = df.apply(lambda row: row['TAT'].date(),axis=1)
    df['ShipmentDate'] = df.apply(lambda row: row['ShipmentDate'].date(),axis=1)

    comment = list_of_dataframe[1]
    comment['ShipmentDate'] = comment.apply(lambda row: row['ShipmentDate'].date(),axis=1)
    comment['DateAdded'] = comment.apply(lambda row: row['DateAdded'].date(),axis=1)
    comment = comment.sort_values(by=['ClientProjectID','ShipmentDate','isHLAComment'])

    temp = merge_data(df,list_of_dataframe[2],comment)
    temp = temp.drop_duplicates()
    temp = remove_client(temp)
    df_not_final, df_final = pipeline(temp,'TAT',lw,tw), pipeline(temp,'FinalDue',lw,tw)
    df_not_final, df_final = modify_comment_category(df_not_final), modify_comment_category(df_final)
    df_not_final, df_final = df_not_final.rename(columns=column_rename), df_final.rename(columns=column_rename)
    
    df_not_final = group_data(df_not_final)
    df_final = df_final[df_final['Final Due'] != None]
    df_not_final['Final Due'] = df_final
    return df_not_final
