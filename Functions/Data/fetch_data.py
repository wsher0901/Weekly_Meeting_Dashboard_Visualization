import os, glob, shutil, pickle, pyodbc
import pandas as pd
from pytz import timezone
import streamlit as st
from datetime import timedelta, datetime, date, time
from dateutil.relativedelta import relativedelta
from Functions.Transformation.Transformation import high_volume_transform, cmv_transform, low_volume_transform, pcr_transform, gel_transform, illumina_transform, \
pacbio_transform, repeats_transform, reagents_transform, hla_tat_transform, non_hla_tat_transform
from Functions.Data.generate_data import generate_high_volume, generate_cmv, generate_low_volume, generate_pcr, generate_gel, generate_illumina, \
generate_pacbio, generate_repeats, generate_hla
tz = timezone('EST')

def connect():
    SERVER = st.secrets["SERVER"]
    DATABASE = st.secrets["DATABASE"]
    USERNAME = st.secrets["USERNAME"]
    PASSWORD = st.secrets["PASSWORD"]
    conn = pyodbc.connect(f'DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={SERVER};DATABASE={DATABASE};UID={USERNAME};PWD={PASSWORD};Encrypt=No;') 
    cursor = conn.cursor()
    return cursor

def disconnect(cursor):
    cursor.close()

def high_volume_load(cursor, lw, tw):       
    # output = []
    # cursor.execute(f"EXEC GetDashBoardPrePCRHVSummary '{lw.strftime('%Y/%m/%d')}','{tw.strftime('%Y/%m/%d')}',NULL")
    
    # while True:
    #     output.append(pd.DataFrame([list(i) for i in cursor.fetchall()],columns=[column[0] for column in cursor.description]))
    #     if not cursor.nextset():
    #         break

    #return high_volume_transform(output)
    return generate_high_volume()

def cmv_load(cursor,lw,tw):
    # output= []
    # cursor.execute('use HistoSDB')
    # cursor.execute(f"declare @MeetingDetails varchar(max) exec GetDashBoardPrePCRHVCMVSummary '{lw.strftime('%Y/%m/%d')}','{tw.strftime('%Y/%m/%d')}',NULL,@MeetingDetails output")
    # while True:
    #     output.append(pd.DataFrame([list(i) for i in cursor.fetchall()],columns=[column[0] for column in cursor.description]))
    #     if not cursor.nextset():
    #         break

    #return cmv_transform(output)
    return generate_cmv()

def low_volume_load(cursor,lw,tw):
    # output = []
    # query = f"declare @MeetingDetails varchar(max) EXEC GetDashBoardPrePCRClinicalSummary '{lw.strftime('%Y/%m/%d')}' ,'{tw.strftime('%Y/%m/%d')}',0,@MeetingDetails output"
    # cursor.execute(query)
    
    # while True:
    #     output.append(pd.DataFrame([list(i) for i in cursor.fetchall()],columns=[column[0] for column in cursor.description]))
    #     if not cursor.nextset():
    #         break

    #return low_volume_transform(output)
    return generate_low_volume()

def pcr_load(cursor,lw,tw):
    # output = []
    # query = f"declare @MeetingDetails varchar(max) exec GetDashBoardPCRSummary  '{lw.strftime('%m/%d/%Y')}' ,'{tw.strftime('%m/%d/%Y')}',0,@MeetingDetails output"
    # cursor.execute(query)
    
    # while True:
    #     output.append(pd.DataFrame([list(i) for i in cursor.fetchall()],columns=[column[0] for column in cursor.description]))
    #     if not cursor.nextset():
    #         break

    #return pcr_transform(output)
    return generate_pcr()

def gel_load(cursor,lw,tw):
    # output = []
    # query = f"declare @MeetingDetails varchar(max) exec GetDashBoardGelSummary'{lw.strftime('%Y/%m/%d')}' ,'{tw.strftime('%Y/%m/%d')}',0,@MeetingDetails output"
    # cursor.execute(query)
    
    # while True:
    #     output.append(pd.DataFrame([list(i) for i in cursor.fetchall()],columns=[column[0] for column in cursor.description]))
    #     if not cursor.nextset():
    #         break

    #return gel_transform(output)
    return generate_gel()

def illumina_load(cursor,lw,tw):
    # output = []
    # query = f"declare @MeetingDetails varchar(max) exec GetDashBoardNextGenSummary '{lw.strftime('%Y/%m/%d')}' ,'{tw.strftime('%Y/%m/%d')}',0,@MeetingDetails output --,1,100"
    # cursor.execute(query)
    # while True:
    #     output.append(pd.DataFrame([list(i) for i in cursor.fetchall()],columns=[column[0] for column in cursor.description]))
    #     if not cursor.nextset():
    #         break

    #return illumina_transform(output)
    return generate_illumina()

def pacbio_load(cursor,lw,tw):
    # output = []
    # query = f"declare @MeetingDetails varchar(max) exec GetDashBoardPacbioSummary '{lw.strftime('%Y/%m/%d')}' ,'{tw.strftime('%Y/%m/%d')}',0,@MeetingDetails output --,1,100"
    # cursor.execute(query)
    # while True:
    #     output.append(pd.DataFrame([list(i) for i in cursor.fetchall()],columns=[column[0] for column in cursor.description]))
    #     if not cursor.nextset():
    #         break

    #return pacbio_transform(output)
    return generate_pacbio()

def repeats_load(cursor,lw,tw):
    # cursor.execute('use HistoSDB')
    # cursor.execute(f"EXEC GetDashboardRepeatExperiments '{tw.strftime('%m/%d/%Y')}'")
    # protocol_dict = {i:j for i,j,k in cursor.fetchall()}
    
    # Previous SP
    #cursor.execute(f"EXEC GetExperimentAndSampleDetails '{lw.strftime('%m/%d/%Y')}', '{tw.strftime('%m/%d/%Y')}'")
    # New SP
    # cursor.execute(f"EXEC GetDashBoardRepeatsSamplesSummary '{lw.strftime('%m/%d/%Y')}', '{tw.strftime('%m/%d/%Y')}'")
    #return repeats_transform([list(i) for i in cursor.fetchall()],protocol_dict,lw)
    return generate_repeats()

def reagents_load(cursor,lw,tw):
    # output = []
    # query = f"declare @MeetingDetails varchar(max) exec GetDashBoardReagentSummary '{lw.strftime('%Y/%m/%d')}' ,'{tw.strftime('%Y/%m/%d')}',0,@MeetingDetails output"
    # cursor.execute(query)
    # while True:
    #     output.append(pd.DataFrame([list(i) for i in cursor.fetchall()],columns=[column[0] for column in cursor.description]))
    #     if not cursor.nextset():
    #         break
    return
    #return reagents_transform(output)
    
def new_allele_load(cursor,lw,tw,today):
    def get_gene_index():
        cursor.execute("select GenomeSegmentName, d.ClassID, c.Name, a.NucleotideStart, NucleotideEnd, a.AminoAcidStart, a.AminoAcidEnd, a.CodonStart from ProbemapallelesHistos.dbo.genometrics a,ProbemapallelesHistos.dbo.genomesegments b,ProbemapallelesHistos.dbo.genes c, Histosdb.dbo.genes d where a.GenomeSegmentID = b.GenomeSegmentID and a.GeneID = C.GeneID and c.MethodTypeID = 2 and c.name = d.genename and d.GeneGroupID = 1 and d.Status = 'A' and NucleotideStart <> 0 and AnalysisGeneOrder is not null order by c.Name, NucleotideStart")
        temp = cursor.fetchall()
        return temp
    def gene_info(data):
        gene_codon_index = {}
        gene_location_index = {}
        for i in data:
            if i[2] not in gene_location_index:
                if i[0] == 'E1' and i[2] == 'DQB1':
                    gene_location_index[i[2]] = {i[0]:[i[3],i[4]+1]}
                elif i[0] == 'I1' and i[2] == 'DQB1':
                    gene_location_index[i[2]] = {i[0]:[i[3]+1,i[4]]}
                else:
                    gene_location_index[i[2]] = {i[0]:[i[3],i[4]]}
                gene_codon_index[i[2]] = {i[0]:i[5:]}
            else:
                if i[0] == 'E1' and i[2] == 'DQB1':
                    gene_location_index[i[2]][i[0]] = [i[3],i[4]+1]

                elif i[0] == 'I1' and i[2] == 'DQB1':
                    gene_location_index[i[2]][i[0]] = [i[3]+1,i[4]]
                else:
                    gene_location_index[i[2]][i[0]] = [i[3],i[4]]
                gene_codon_index[i[2]][i[0]] = i[5:]

        return gene_location_index, gene_codon_index
    def get_new_allele(lw,tw,today):
        def get_query(lw,tw,today):
            last_week = "'"+lw.strftime('%m/%d/%Y')+"'"
            this_week = "'"+datetime.combine(tw, datetime.max.time()).strftime('%m/%d/%Y %H:%M:%S.%f')[:-3]+"'"
            query = "Exec Pacbio_analysis.dbo.GetNewAllelePatternMutationdetails_Period_PositionWise 20240101, "+ last_week + ',' + this_week + ',' + "'" + (tw- relativedelta(days=90)).strftime('%m/%d/%Y') + "'" + ',' + this_week + ',' + "'" + today.strftime('%m/%d/%Y %H:%M:%S.%f')[:-3] + "'"
            return query
        def position_extract(position):
            new_ind = position.split('$')
            if '' in new_ind:
                new_ind.remove('')
            mut_list = []
            for j in new_ind:
                b = j.split('-')
                mut_type = b[0]
                ind = b[1].split(',')
                for k in ind:
                    mut_list.append(mut_type+'-'+k)
                    
            mut_list = sorted(mut_list,key=lambda x: int(x[2:]))
                    
            return mut_list
        def name_shorten(name):
            if name[0] == 'E':
                return 'E' + name[-1]
            elif name[0] == 'I':
                return 'I' + name[-1]
            else:
                return name
        query = get_query(lw,tw,today)
        data, temp = [], []
        for i in cursor.execute(query).fetchall():
            temp.append(list(i))
        data.append(temp)
        while cursor.nextset():
            temp = []
            for i in cursor.fetchall():
                temp.append(list(i))
            data.append(temp)
        
        uno = {}
        for i in pd.DataFrame(data[0]).drop_duplicates().values.tolist():
            if i[1] not in uno:
                uno[i[1]] = {i[2]:[i[0]]}
            else:
                if i[2] not in uno[i[1]]:
                    uno[i[1]][i[2]] = [i[0]]
                else:
                    uno[i[1]][i[2]].append(i[0])
                    
        dos = {}
        for i in pd.DataFrame(data[1]).drop_duplicates(subset=[0,1,2,3,4,5,7,8,9,10,11,12,13,14,15,16,17,18,19]).values.tolist():
            sub_type = i[18]
            if sub_type != None:
                sub_type = sub_type.split(',')
                if '' in sub_type:
                    sub_type.remove('')
            area = name_shorten(i[5])
            temp = [position_extract(i[17]),i[1],i[0].replace('-',''),i[2].replace('-',''),i[8],
                    i[9],i[10],i[11],sub_type,i[7],i[14]]
            
            if i[4] not in dos:
                dos[i[4]] = {i[3]:{area:temp}}
            else:
                if i[3] not in dos[i[4]]:
                    dos[i[4]][i[3]] = {area:temp}
                else:
                    if area not in dos[i[4]][i[3]]:
                        dos[i[4]][i[3]][area] = temp

        tres = {}
        for i in pd.DataFrame(data[2]).drop_duplicates(subset=[0,1,2,3,5,6,7,8,9,10,11,12,13,14,15]).values.tolist():
            t = dos[i[2]][i[0]][name_shorten(i[3])][0]
            mut_type = ''
            for j in t:
                if j[2:] == str(i[8]):
                    mut_type = j[0]
            temp = [mut_type,int(i[8]),i[5],i[6],i[7],i[9],i[14],i[15]]
            if i[2] not in tres:
                tres[i[2]] = {i[0]:{name_shorten(i[3]):[temp]}}
            else:
                if i[0] not in tres[i[2]]:
                    tres[i[2]][i[0]] = {name_shorten(i[3]):[temp]}
                else:
                    if name_shorten(i[3]) not in tres[i[2]][i[0]]:
                        tres[i[2]][i[0]][name_shorten(i[3])] = [temp]
                    else:
                        tres[i[2]][i[0]][name_shorten(i[3])].append(temp)
                        
            tres[i[2]][i[0]][name_shorten(i[3])].sort(key=lambda x: x[1])
                        
        return uno,dos,tres
    def load_stop_codon(lw,tw,type):
        before = (tw-timedelta(days=90)).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        today = (datetime.now(tz) + timedelta(hours=1)).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        lw = lw.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        tw = tw.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        cursor.execute('use HistoSDB')
        query = f"exec Pacbio_analysis.dbo.GetSegmentMutationDetails @DetailType=N'{type}StopCodons',@GeneName=N'C1 & C11',@ClientProjectCode=N'All',@NewAlleleStart='{lw}',@NewAlleleEnd='{tw}',@ShipmentStart='{before}',@ShipmentEnd='{tw}',@TimeStamp='{today}',@sourceType=N'PacBio'"
        data = []
        temp = []
        for i in cursor.execute(query).fetchall():
            temp.append(list(i))
        data.append(temp)
        while cursor.nextset():
            temp = []
            for i in cursor.fetchall():
                temp.append(list(i))
            data.append(temp)
        
        return data
    def load_table(lw,tw):
        before = (tw-timedelta(days=90)).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        today = (datetime.now(tz) + timedelta(hours=1)).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        lw = lw.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        tw = tw.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        cursor.execute('use HistoSDB')
        query = f"Pacbio_analysis.dbo.GetUniquepatterns @sourceType=N'PacBio',@GeneName=N'C1 & C11',@Segments=N'ARS,Non-ARS Exons,All Exons,Exons & Introns',@ClientProjectCode=N'All',@NewAllelestart='{lw}',@NewAlleleEnd='{tw}',@ShipmentStart='{before}',@ShipmentEnd='{tw}',@TimeStamp='{today}',@PCName=N'10.202.22.105',@ProcessID=1500"
        data = []
        temp = []
        for i in cursor.execute(query).fetchall():
            temp.append(list(i))
        data.append(temp)
        while cursor.nextset():
            temp = []
            for i in cursor.fetchall():
                temp.append(list(i))
            data.append(temp)
        
        return data
    data_0 = get_gene_index()
    gene_location,gene_codon = gene_info(data_0)
    data = get_new_allele(lw,tw,today)
    border = load_stop_codon(lw,tw,'Border')
    non_border = load_stop_codon(lw,tw,'Non-Border')
    table = load_table(lw,tw)

    return gene_location,gene_codon,data,border,non_border,table

def hla_tat_load(cursor,lw,tw):
    # output = []
    # before = tw-timedelta(days=90)
    # non_clinical_query = f"EXEC GetClientProjectsWithStatistics_Visualization '{before.strftime('%Y/%m/%d')}','{tw.strftime('%Y/%m/%d')}','N',1" 
    # clinical_query = f"EXEC GetClientProjectsWithStatistics_Visualization '{before.strftime('%Y/%m/%d')}','{tw.strftime('%Y/%m/%d')}','C',1"
    # extension_query = "select * from AutoExtensionRequestClientProjects"
    # for i in [non_clinical_query,clinical_query,extension_query]:
    #     cursor.execute(i)
    #     while True:
    #         output.append(pd.DataFrame([list(i) for i in cursor.fetchall()],columns=[column[0] for column in cursor.description]))
    #         if not cursor.nextset():
    #             break

    # return hla_tat_transform(output,lw,tw)
    return generate_hla()

def non_hla_tat_load(cursor,lw,tw):
    output = []
    before = tw-relativedelta(months=6)
    gene_list = 'ABO-RH,CCR,CMV,DRA,E,FCGR3A,G,HPA,KIR,MICA,MICB'
    query = f"EXEC GetNonHLAReportStatisticsWorkflow_Visualization '{before.strftime('%Y/%m/%d')}','{tw.strftime('%Y/%m/%d')}','{gene_list}',1"
    extension_query = "select * from AutoExtensionRequestClientProjects"
    for i in [query,extension_query]:
        cursor.execute(i)
        while True:
            output.append(pd.DataFrame([list(i) for i in cursor.fetchall()],columns=[column[0] for column in cursor.description]))
            if not cursor.nextset():
                break
    
    return non_hla_tat_transform(output,lw,tw)

def get_date():
    today = date.today()
    this_week = last_week = ''
    if today.weekday() == 3:
        this_week = (today - timedelta(days=1))
        last_week = (today - timedelta(days=7))
    else:
        if today.weekday() <= 2:
            this_week = today + timedelta(days=(2-today.weekday()))
            last_week = (today - timedelta(days=(4+today.weekday())))
        else:
            this_week = (today + timedelta(days=(9-today.weekday())))
            last_week = (today - timedelta(days=(today.weekday()-3)))

    return last_week, this_week

page_list = ['Pre PCR (High Vol)','Pre PCR (CMV)','Pre PCR (Low Vol)','PCR','Gel','Illumina','Pacbio','Repeats','HLA TAT','Non-HLA TAT','New Allele']
page_dict = {'Pre PCR (High Vol)':high_volume_load,
             'Pre PCR (CMV)':cmv_load,
             'Pre PCR (Low Vol)':low_volume_load,
             'PCR':pcr_load,
             'Gel':gel_load,
             'Illumina':illumina_load,
             'Pacbio':pacbio_load,
             'Repeats':repeats_load,
             'HLA TAT':hla_tat_load,
             'Non-HLA TAT':non_hla_tat_load,
             'New Allele':new_allele_load}

def load_data(lw,tw,choice):
    cursor = None
    today = datetime.now(tz) + timedelta(hours=1)
    bar = st.progress(0)
    counter = 0
    for i in page_list:
        if i in choice:
            bar.progress(counter/len(choice))
            counter+=1
            if i not in st.session_state: 
                st.session_state[i+' status'] = False
                st.write(i + ' downloading...')
                if i == 'New Allele':
                    st.session_state[i] = page_dict[i](cursor,lw,tw,today)
                elif i == 'Repeats':
                    st.session_state[i] = page_dict[i](cursor,lw,tw)
                    st.session_state.illumina_yearly = pd.read_csv('Files/illumina_yearly.csv')
                    st.session_state.pacbio_yearly = pd.read_csv('Files/pacbio_yearly.csv')
                else:
                    st.session_state[i] = page_dict[i](cursor,lw,tw)

            elif i in st.session_state and st.session_state.lw != lw and st.session_state.tw != tw:
                st.session_state[i+' status'] = False
                st.write(i + ' downloading...')
                del st.session_state[i]
                if i == 'New Allele':
                    st.session_state[i] = page_dict[i](cursor,lw,tw,today)
                elif i == 'Repeats':
                    st.session_state[i] = page_dict[i](cursor,lw,tw)
                    st.session_state.illumina_yearly = pd.read_csv('Files/illumina_yearly.csv')
                    st.session_state.pacbio_yearly = pd.read_csv('Files/pacbio_yearly.csv')
                else:
                    st.session_state[i] = page_dict[i](cursor,lw,tw)
            else:
                st.write(i+' downloaded.')

        else:
            if i in st.session_state:
                del st.session_state[i]
            st.session_state[i+' status'] = True
    #disconnect(cursor)

def load_meeting(lw,tw):
    file_path = 'Archive/' + (tw+timedelta(days=1)).strftime('%m_%d_%y')
    if not os.path.exists(file_path):
        os.makedirs(file_path)
        cursor = connect()
        cursor.execute('use HistoSDB')
        today = datetime.now(tz) + timedelta(hours=1)
        for i in page_list:
            with open(file_path+'/'+i+'.pkl','wb') as f:
                if i == 'New Allele':
                    pickle.dump(page_dict[i](cursor,lw,tw,today),f)
                elif i == 'Repeats':
                    repeats_data = page_dict[i](cursor,lw,tw)
                    pickle.dump(repeats_data,f)
                    update_yearly_statistics(repeats_data,tw)
                    
                else:
                    pickle.dump(page_dict[i](cursor,lw,tw),f)
        disconnect(cursor)

@st.dialog('Generate Meeting',width='large')
def generate_meeting(lw,tw):  
    password = st.text_input('Enter a password',type='password')         
    if st.button('Submit'):
        if password == st.secrets["KEY"]:
            st.success('Meeting is being generated')
            load_meeting(lw,tw)
            st.rerun()
        else:
            st.error('Wrong Password')

@st.dialog('Remove Meeting')
def remove_meeting(file_path):
    password = st.text_input('Enter a password',type='password')         
    if st.button('Submit'):
        if password == st.secrets["KEY"]:
            st.success('Meeting is removed.')
            shutil.rmtree('Archive/' + file_path)
            if os.path.exists('Comment/' + file_path):
                shutil.rmtree('Comment/' + file_path)
            st.rerun()
        else:
            st.error('Wrong Password')

@st.dialog('Insert Comment')
def add_comment(tw):
    file_path = 'Comment/' + (tw+timedelta(days=1)).strftime('%m_%d_%y')+'/'
    if not os.path.exists(file_path):
        os.makedirs(file_path)
    page = st.selectbox('Choose your page',options=page_list)
    if not os.path.exists(file_path+page+'.txt'):
        comment = st.text_area(label='Add your Comment')
    else:
        with open(file_path+page+'.txt','r') as file:
            temp = file.read()
            st.session_state[page+ ' comment'] = temp
            comment = st.text_area(label='Edit your Comment', value = temp)

    with st.form('Comment',border=False):  
        uploaded_files = [i.read() for i in st.file_uploader("Drop Image Files", accept_multiple_files=True)]
        if os.path.exists((file_path+page+str(1)+'.png')):
            image_list, file_list = [], []
            for name in glob.glob(file_path+page+'*'+'.png'):
                file_list.append(name.replace('\\','/'))
                with open(name,'rb') as f:
                    image_list.append(f.read())
            st.write('\n'.join(file_list))
            st.session_state[page+' image'] = image_list
            if st.checkbox(label='Remove existing images'):
                for name in glob.glob(file_path+page+'*'+'.png'):
                    os.remove(name.replace('\\','/'))
                del st.session_state[page+' image']
                st.write('')
        
        if st.form_submit_button('Submit'):
            if comment == '' and os.path.exists(file_path+page+'.txt'):
                os.remove(file_path+page+'.txt')
                del st.session_state[page+ ' comment']
            elif comment != '':
                with open(file_path+page+'.txt','w') as file:
                    file.write(comment)
                    st.session_state[page+ ' comment'] = comment

            if not os.path.exists((file_path+page+str(1)+'.png')):
                if uploaded_files != []:
                    for ind,i in enumerate(uploaded_files,1):
                        with open(file_path+page+str(ind)+'.png','wb') as w:
                            w.write(i)
                    st.session_state[page+' image'] = uploaded_files
            else:
                temp = [i[:-4] for i in glob.glob(file_path+page+'*'+'.png')]
                max_val = max([int(i[len(file_path+page):]) for i in temp])
                for ind,i in enumerate(uploaded_files,max_val+1):
                    with open(file_path+page+str(ind)+'.png','wb') as w:
                        w.write(i)

                image_list = []
                for name in glob.glob(file_path+page+'*'+'.png'):
                    with open(name,'rb') as f:
                        image_list.append(f.read())
                st.session_state[page+' image'] = image_list
            st.rerun()

def load_comment(d,i):
    if os.path.exists('Comment/' + d+'/'+i+'.txt'):
        with open('Comment/' + d+'/'+i+'.txt','r') as f:
            st.session_state[i + ' comment'] = f.read()
    images = []
    for name in glob.glob('Comment/'+d+'/'+i+'*'+'.png'):
        if os.path.exists(name):
            with open(name,'rb') as f:
                images.append(f.read())
    if len(images) != 0:
        st.session_state[i + ' image'] = images

def update_yearly_statistics(df,tw):
    pickle_path = 'Archive/' + (tw+timedelta(days=1)).strftime('%m_%d_%y')
    for data,file_path,pickle_file in zip(df,
                                          ['Files/illumina_yearly.csv','Files/pacbio_yearly.csv'],
                                          [pickle_path+'/'+'illumina_yearly'+'.pkl',pickle_path+'/'+'pacbio_yearly'+'.pkl']):
        yearly_data = pd.read_csv(file_path)
        
        if datetime.now().time() >= time(10,0,0):
            if len(data) != 0:
                yearly_data = pd.concat([yearly_data[yearly_data.Date != yearly_data.Date.min()],data],ignore_index=True)
            yearly_data.to_csv(file_path,index=False)
            with open(pickle_file,'wb') as f:
                pickle.dump(yearly_data,f)