from pytz import timezone
import pandas as pd
import streamlit as st
import plotly.graph_objects as go 
from datetime import timedelta, datetime
from dateutil.relativedelta import relativedelta

tz = timezone('EST')
stop_codon = ['TAA','TAG','TGA']
gene_order = ['A','B','C','DRB1','DRB3','DRB4','DRB5','DQB1','DQA1','DPB1','DPA1']

def load_data(lw,tw,today):
    cursor = connect()
    data_0 = get_gene_index(cursor)
    gene_location,gene_codon = gene_info(data_0)
    data = get_new_allele(cursor,lw,tw,today)
    border = load_stop_codon(cursor,lw,tw,'Border')
    non_border = load_stop_codon(cursor,lw,tw,'Non-Border')
    table = load_table(cursor,lw,tw)
    disconnect(cursor)

    return gene_location,gene_codon,data,border,non_border,table

def get_date(x):
    today = datetime.now(tz) - timedelta(days=x) + timedelta(hours=1)
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

    return last_week, this_week,today

def get_query(lw,tw,today):
    last_week = "'"+lw.strftime('%m/%d/%Y')+"'"
    this_week = "'"+datetime.combine(tw, datetime.max.time()).strftime('%m/%d/%Y %H:%M:%S.%f')[:-3]+"'"
    query = "Exec Pacbio_analysis.dbo.GetNewAllelePatternMutationdetails_Period_PositionWise 20230101, "+ last_week + ',' + this_week + ',' + "'" + (tw- relativedelta(days=90)).strftime('%m/%d/%Y') + "'" + ',' + this_week + ',' + "'" + today.strftime('%m/%d/%Y %H:%M:%S.%f')[:-3] + "'"
    return query

def get_gene_index(cursor):
    cursor.execute("select GenomeSegmentName, d.ClassID, c.Name, a.NucleotideStart, NucleotideEnd, a.AminoAcidStart, a.AminoAcidEnd, a.CodonStart from ProbemapallelesHistos.dbo.genometrics a,ProbemapallelesHistos.dbo.genomesegments b,ProbemapallelesHistos.dbo.genes c, Histosdb.dbo.genes d where a.GenomeSegmentID = b.GenomeSegmentID and a.GeneID = C.GeneID and c.MethodTypeID = 2 and c.name = d.genename and d.GeneGroupID = 1 and d.Status = 'A' and NucleotideStart <> 0 and AnalysisGeneOrder is not null order by c.Name, NucleotideStart")
    temp = cursor.fetchall()
    return temp

def get_new_allele(cursor,lw,tw,today):
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

def load_stop_codon(cursor,lw,tw,type):
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

def load_table(cursor,lw,tw):
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

def name_lengthen(name):
    if name[0] == 'E':
        return 'Exon ' + name[-1]
    elif name[0] == 'I':
        return 'Intron ' + name[-1]
    else:
        return name
    
def name_shorten(name):
    if name[0] == 'E':
        return 'E' + name[-1]
    elif name[0] == 'I':
        return 'I' + name[-1]
    else:
        return name
    
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

def gene_statistics(data):
    output = {}
    for i in data:
        if i not in output:
            output[i] = [i,0,0,0]
        for j in data[i]:
            if i in ['A','B','C'] and ('E2' in data[i][j] or 'E3' in data[i][j]):
                output[i][1] += 1
            elif i not in ['A','B','C'] and 'E2' in data[i][j]:
                output[i][1] += 1
            else:
                if 'E' in set([x[0] for x in data[i][j].keys()]):
                    output[i][2] += 1
                else:
                    output[i][3] += 1
    
    def custom_sort_gene(gene):
            try:
                return gene_order.index(gene[0])
            except ValueError:
                return len(gene_order)
        
    output = sorted(list(output.values()),key=custom_sort_gene)
    return pd.DataFrame(output, columns=['Gene','ARS','Non-ARS','Intron'])

def ars_statistics(data):
    def mutation_assigner(gene,rows):
        # Syn(0) Non-Syn(1) Insertion(2) Deletion(3) Mixed(4) Junction(5) Border(6) Non-Border(7) Intron(8)
        output = []
        for area in rows:
            for row in rows[area]:
                mut_type = ''
                if gene in ['A','B','C'] and (area == 'E2' or area == 'E3'):
                    mut_type = 'ARS'
                elif gene not in ['A','B','C'] and area == 'E2':
                    mut_type = 'ARS'
                else:
                    if area[0] == 'I':
                        mut_type = 'Intron'
                    else:
                        mut_type = 'Non-ARS'
                        
                temp = [0] * 9
                if mut_type != 'Intron':
                    if row[2] == True:
                        if row[0] == 'P':
                            if row[3] == True:
                                temp[6] = 1 
                            else:
                                temp[5] = 1 
                        else:
                            if row[0] == 'I':
                                temp[2] = 1
                            elif row[0] == 'D':
                                temp[3] = 1
                    else:
                        if row[3] == True:
                            if row[0] == 'P':
                                temp[7] == 1
                            else:
                                if row[0] == 'I':
                                    temp[2] = 1
                                elif row[0] == 'D':
                                    temp[3] = 1
                        else:
                            if row[0] == 'P':
                                if row[5] == 'Syn':
                                    temp[0] = 1
                                else:
                                    temp[1] = 1
                            elif row[0] == 'I':
                                temp[2] = 1
                            else:
                                temp[3] = 1 
                else:
                    temp[-1] = 1
                output.append([gene,mut_type] + temp)
        return output
    
    def mutation_classifier(rows):
        if len(rows) == 1:
            return rows[0]
        else:
            if 'ARS' in [x[1] for x in rows]:
                ars = [x for x in rows if x[1] == 'ARS']
                if len(ars) == 1:
                    return ars[0]
                else:
                    if [sum(x) for x in zip(*[y[2:] for y in ars])].count(0) == 8:
                        return ars[0]
                    else:
                        return ars[0][0:2]+[0,0,0,0,1,0,0,0,0]
            else:
                if 'Non-ARS' in [x[1] for x in rows]:
                    non_ars = [x for x in rows if x[1] == 'Non-ARS']
                    if len(non_ars) == 1:
                        return non_ars[0]
                    else:
                        if [sum(x) for x in zip(*[y[2:] for y in non_ars])].count(0) == 8:
                            return non_ars[0]
                        else:
                            return non_ars[0][0:2]+[0,0,0,0,1,0,0,0,0]
                else:
                    intron = [x for x in rows if x[1] == 'Intron']
                    return intron[0]

    def custom_sort_gene(gene):
        return gene_order.index(gene)

    output = []
    for i in data:
        for j in data[i]:
            output.append(mutation_classifier(mutation_assigner(i,data[i][j])))
        
    df = pd.DataFrame(output,columns=['Gene','Type','Synonymous','Non-Synonymous','Insertion','Deletion','Mixed','Junction','Border Stop','Non-Border Stop','Intron']).groupby(['Gene','Type']).sum().reset_index()
    df.sort_values(by=['Gene','Type'],  key=lambda x: x if x.name!='Gene' else x.map(custom_sort_gene),inplace=True)
    return df

def ars_sunburst(data):
    # Gene Type Syn Non-Syn Deletion Insertion Mixed Junction Border Non-Broder
    # 0     1   2   3       4        5         6     7        8      9
    # isBorderMutation / IsStopCodon / BorderMutationType / Substitution Type   
    output = []
    for i in data:
        for j in data[i]:
            for k in data[i][j]:
                if k[0] == 'E':
                    d = data[i][j][k]
                    ars = ''
                    if i in ['A','B','C'] and k in ['E2','E3']:
                        ars = 'ARS'
                    elif i not in ['A','B','C'] and k == 'E2':
                        ars = 'ARS'
                    else:
                        ars = 'Non ARS'
                    for l in d:
                        temp = [i,ars]
                        if l[2] == True:
                            if l[6] in stop_codon:
                                temp.extend(['Border',1])
                            else:
                                temp.extend(['Junc',1])
                        else:
                            if l[6] in stop_codon:
                                temp.extend(['Non-Border',1])
                            else:
                                if l[0] == 'P':
                                    if l[5] == 'Syn':
                                        temp.extend(['Syn',1]) 
                                    else:
                                        temp.extend(['Non-Syn',1])
                                elif l[0] == 'D':
                                    temp.extend(['Deletion',1])
                                else:
                                    temp.extend(['Insertion',1])

                        output.append(temp)
                                            
    df = pd.DataFrame(output,columns=['Gene','Region','Type','Count'])
    return df

def no_data(): 
    st.write('')
    st.markdown("""
<style>
.big-font {
    font-size:200px !important;
}
</style>
""", unsafe_allow_html=True)

    st.markdown('<p class="big-font">No New Allele</p>', unsafe_allow_html=True)
    st.markdown('<p class="big-font">No New Allele</p>', unsafe_allow_html=True)
    st.markdown('<p class="big-font">No New Allele</p>', unsafe_allow_html=True)
    st.stop()

def get_gene_count(data):
    gene_count = {}
    for i in data:
        for j in data[i]:
            if i not in gene_count:
                gene_count[i] = 1
            else:
                gene_count[i]+=1

    return {k: gene_count[k] for k in gene_order if k in gene_count}

def check_ars(gene,mut_list):
    area_set = set([x for x in mut_list if x[0] == 'E'])
    temp = [0,0]
    if gene in ['A','B','C']:
        if len(area_set) != 0:
            if 'E2' in area_set or 'E3' in area_set:
                temp[0] = 1

            if len(area_set.difference(set(['E2','E3']))) > 0:
                temp[1] = 1
    else:
        if len(area_set) != 0:
            if 'E2' in area_set:
                temp[0] = 1

            if len(area_set.difference(set(['E2']))) > 0:
                temp[1] = 1
            
    if temp == [1,1]:
        return 'Both'
    elif temp == [1,0]:
        return 'ARS'
    else:
        return 'Non-ARS'

def check_mut_type(data):
    mut_type = set()
    for i in data:
        mut_type.add(i[0])
    if len(mut_type) == 1:
        mut = list(mut_type)[0]
        if mut == 'P':
            return 'Substitution'
        elif mut == 'D':
            return 'Deletion'
        else:
            return 'Insertion'
    else:
        return 'Mixed'

def new_allele_pattern(data1,gene_location):
    test_list = []
    mut_type_dict = {}
    for i in data1:
        for j in data1[i]:
            temp = [i,j]
            temp.append(check_ars(i,list(data1[i][j].keys())))
            for k in gene_location['A'].keys():
                if k not in gene_location[i]:
                    temp.append(-1)
                else:
                    if k not in data1[i][j]:
                        temp.append(0)
                    else:
                        mut_type_dict[(i,j,check_ars(i,list(data1[i][j].keys())),name_lengthen(k))] = check_mut_type(data1[i][j][k][0])
                        temp.append(len(data1[i][j][k][0]))

            test_list.append(temp)

    df = pd.DataFrame(test_list,columns=['Gene','Pattern ID','Type']+[name_lengthen(i) for i in gene_location['A'].keys()])
    df.sort_values(by=['Gene'],inplace=True)
    df.index +=1
    return df, mut_type_dict

def edit_new_allele_pattern(df,gene,typ,mutation_dict):
    if gene != 'All' and typ != 'All':
        df = df[(df['Gene'] == gene) & (df['Type'] == typ)]
    elif gene != 'All' and typ == 'All':
        df = df[df['Gene'] == gene]
    elif gene == 'All' and typ != 'All':
        df = df[df['Type'] == typ]

    def color_cell(value,m_d):
        color_table = [None] * 20
        for ind,i in enumerate(value.index,0):
            temp = (value['Gene'],value['Pattern ID'],value['Type'],i)
            text_color = ''
            background_color = ''
            if temp in m_d:
                if m_d[temp] == 'Substitution':
                    text_color='red'
                    background_color='#5bde1d'
                elif m_d[temp] == 'Deletion':
                    text_color= '#D3D3D3'
                    background_color='#ff2727'
                elif m_d[temp] == 'Insertion':
                    text_color='#D3D3D3'
                    background_color='#0096FF'
                else:
                    text_color='purple'
                    background_color = 'yellow'
            else:
                if i not in ['Gene','Type','Pattern ID']:
                    text_color = '#0e1117'
                    if value[i] == -1:
                        background_color='black'

            color_table[ind] = f'color: {text_color}; background-color: {background_color};'
         
        return color_table

    styled_df = df.style.apply(lambda x: color_cell(x,mutation_dict), axis=1)
    return styled_df, len(df)

def load_past_mutation_count():
    cursor = connect()
    total_set = set()
    for i in range(0,85,7):
        data = get_past_mutation_count(cursor,i)
        total_set.update(data)

    disconnect(cursor)
    df = pd.DataFrame(list(total_set),columns=['Date','Pattern ID']).groupby('Date').count()
    df.reset_index(inplace=True)
    return df

def get_past_mutation_count(cursor,x):
    lw,tw,today = get_date(x)
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

    pattern_set = set()
    for i in data[1]:
        pattern_set.add((tw,i[3]))

    return pattern_set

def make_trend_chart(loc):
    over_time = load_past_mutation_count()
    min_date,max_date = over_time.Date.min().date(), over_time.Date.max().date()
    loc.markdown(f"<h1 style='text-align: center;font-size: 60px;font-family: Arial;color: #F96167;padding-bottom: 0;'>{min_date} ~ {max_date}</h1>", unsafe_allow_html=True)
    count_plot = go.Figure()
    count_plot.add_trace(go.Scatter(x=over_time.Date, y=over_time['Pattern ID'], mode="lines+markers+text", 
                                    name="Lines, Markers and Text",text=over_time['Pattern ID'], textposition="top center"))
    count_plot.update_layout(showlegend=False,font=dict(size=20),height=600)
    count_plot.update_traces(line_color='#61F9F3',hoverinfo='skip')
    count_plot.add_bar(x=over_time.Date,y=over_time['Pattern ID'],name='',hoverinfo='skip',marker_color='#F96167')
    return count_plot

# def test(loc_list,data):
#     point, deletion, insertion, border, non_border = [], [], [], [], []
#     for i in data:
#         for j in data[i]:
#             for k in data[i][j]:
#                 if k[0] == 'E':
#                     d = data[i][j][k]
#                     queue = [d[0]]
#                     for l in d[1:]:
#                         if l[2] == queue[-1][2] and 
#     for i,j in zip([point,deletion,insertion,border,non_border],loc_list):
#         if i:
#             for k in i:
#                 j.write(f"{k[0]} / {k[1]} / {k[2]}")

def static_comment_generator(loc,data):
    exon_list = [0,0,0]
    del_list = []
    ins_list = []
    junc_list = []
    stop_list = []
    for i in data:
        for j in data[i]:
            for k in data[i][j]:
                if k[0] == 'E':
                    d = data[i][j][k]
                    for l in d:
                        if l[2] == True:
                            if l[6] in stop_codon:
                                junc_list.append([i,j,k,'Stop Codon'])
                            else:
                                junc_list.append([i,j,k,''])
                        else:
                            if l[6] in stop_codon:
                                stop_list.append([i,j,k])
                            else:
                                if l[0] == 'P':
                                    exon_list[0] +=1
                                elif l[0] == 'D':
                                    exon_list[1] +=1
                                    del_list.append([i,j,k,l[1]])
                                else:
                                    exon_list[2] +=1
                                    ins_list.append([i,j,k,l[1]])
                                
    
    for ind,i in enumerate([exon_list,junc_list,stop_list],0):
        if ind == 0:
            for indd, j in enumerate(i,0):
                if indd == 0:
                    loc.write(f"  \n- There are :green[{str(i[0])}] Point Mutations.")
                elif indd == 1:
                    loc.write(f"  \n- There are :green[{str(i[1])}] Deletions.")
                    if i[1] > 0:
                        del_set = set()
                        for k in del_list:
                            if frozenset([k[0],k[1],k[2]]) not in del_set:
                                lloc = loc.container()
                                lloc0,lloc1 = lloc.columns([0.2,8])
                                lloc1.write(f"  - Gene: :red[{k[0]}] / Pattern ID: :red[{str(k[1])}] / Area: :red[{name_lengthen(k[2])}]  \n")
                                del_set.add(frozenset([k[0],k[1],k[2]]))         
                else:
                    loc.write(f"  \n- There are :green[{str(i[2])}] Insertions.")
                    if i[2] > 0:
                        ins_set = set()
                        for k in ins_list:
                            if frozenset([k[0],k[1],k[2]]) not in ins_set:
                                lloc = loc.container()
                                lloc0,lloc1 = lloc.columns([0.2,8])
                                lloc1.write(f"  - Gene: :red[{k[0]}] / Pattern ID: :red[{str(k[1])}] / Area: :red[{name_lengthen(k[2])}]  \n")
                                ins_set.add(frozenset([k[0],k[1],k[2]]))

        elif ind == 1:
            loc.write(f"  \n- There are :green[{str(len([m for m in i if m[3] == '']))}] Junction Mutations and :green[{str(len([m for m in i if m[3] == 'Stop Codon']))}] Border Stop Codons.  \n")
            if len(i) > 0:
                junc_set = set()
                bsc_set = set()
                for k in i:
                    if k[3] == '':
                        if frozenset([k[0],k[1],k[2]]) not in junc_set:
                            lloc = loc.container()
                            lloc0,lloc1 = lloc.columns([0.2,8])
                            lloc1.write(f"  - (Junction) Gene: :red[{k[0]}] / Pattern ID: :red[{str(k[1])}] / Area: :red[{name_lengthen(k[2])}]  \n")
                            junc_set.add(frozenset([k[0],k[1],k[2]]))
                    else:
                        if frozenset([k[0],k[1],k[2]]) not in bsc_set:
                            lloc = loc.container()
                            lloc0,lloc1 = lloc.columns([0.2,8])
                            lloc1.write(f"  - (Border Stop Codon) Gene: :red[{k[0]}] / Pattern ID: :red[{str(k[1])}] / Area: :red[{name_lengthen(k[2])}]  \n")
                            bsc_set.add(frozenset([k[0],k[1],k[2]]))

        else:
            loc.write(f"  \n- There are :green[{str(len(i))}] Non Border Stop Codons.  \n")
            if len(i) > 0:
                nbsc_set = set()
                for k in i:
                    if frozenset([k[0],k[1],k[2]]) not in nbsc_set:
                        lloc = loc.container()
                        lloc0,lloc1 = lloc.columns([0.2,8])
                        lloc1.write(f"  - Gene: :red[{k[0]}] / Pattern ID: :red[{str(k[1])}] / Area: :red[{name_lengthen(k[2])}]  \n")
                        nbsc_set.add(frozenset([k[0],k[1],k[2]]))