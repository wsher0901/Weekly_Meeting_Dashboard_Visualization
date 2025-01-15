from datetime import timedelta, datetime, date, time
import random
import math
from faker import Faker
import pandas as pd

fake = Faker()

countries = ["United States","Canada","United Kingdom","Germany","France","Italy","Spain","Australia","New Zealand",
             "China","Japan","India","Brazil","Mexico","Russia","South Africa","Argentina","Egypt""Turkey","Switzerland",
             "Netherlands","Sweden","Norway","Denmark","Greece","Thailand","South Korea","Indonesia","Vietnam","Saudi Arabia"]

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
last_week, this_week = get_date()

def get_prob(n):
    sum = 1.0
    counter = n
    prob_list = []
    while sum != 0:
        if counter != 1:
            condition = True
            while condition:
                val = round(random.uniform(0,sum),2)
                if val != sum:
                    condition = False
                    prob_list.append(val)
                    sum -= val
                    counter-= 1
        else:
            prob_list.append(round(sum,2))
            sum -= sum
            
    return prob_list

def generate_high_volume():
    client_count = random.randint(5,10)
    client_name = [fake.name() for _ in range(client_count)]
    country_name = random.sample(countries,client_count)
    country_dict = {i:j for i,j in zip(client_name,country_name)}
    sample_count = random.randint(12000,15000)
    date_list = [(last_week + timedelta(days=i)) for i in range(0,7,1)]

    data = []
    for _ in range(sample_count):
        client = random.choices(client_name,weights=get_prob(client_count),k=1)[0]
        rand_date = random.choice(date_list)
        data.append([client,
                     client,
                     rand_date,
                     rand_date.strftime('%A'),
                     country_dict[client],
                     random.choices(['HLA','ABO-RH','CMV','CCR','KIR'],weights=[0.4,0.4,0.1,0.05,0.05],k=1)[0],
                     client[0:3].upper()+str(random.randint(100000,999999)),
                     random.choices(['New','Rerequest'],weights=[0.95,0.05],k=1)[0],
                     random.choices(['Genomic DNA','Client DNA'],weights=[0.95,0.05],k=1)[0]
                     ])
    first_table = pd.DataFrame(data,columns=['Client','Project','Date','Day','Country','Gene','Sample ID','Request Type','Type'])

    second_table = first_table.groupby(['Type','Gene','Date','Day'])['Sample ID'].count().reset_index()
    second_table.rename(columns={'Sample ID':'Sample Count'},inplace=True)

    third_table = second_table.groupby('Type')['Sample Count'].sum().reset_index()

    return first_table, second_table, third_table  

def generate_cmv():
    sample_count = random.randint(7000,8000)
    client_count = random.randint(5,10)
    client_name = [fake.name() for _ in range(client_count)]

    data = []
    for _ in range(sample_count):
        client = random.choice(client_name)
        data.append([random.choices(['Antibody Extraction','CMV-ELISA','Plasma / Serum Dilution'],weights=[0.47,0.06,0.47],k=1)[0],
                     client[0:3].upper(),
                     client[0:3].upper()+str(random.randint(100000,999999)),
                     client
                     ])
    
    first_table = pd.DataFrame(data,columns=['Elisa Type','Experiment Names','Sample ID','Client'])
    first_table = first_table.groupby(['Elisa Type','Experiment Names','Client'])['Sample ID'].count().reset_index()
    first_table.rename(columns={'Sample ID':'Sample Count'},inplace=True)

    experiment_count = random.randint(3,5)
    client_name = [fake.name() for _ in range(experiment_count)]
    data = []
    for i in range(0,experiment_count):
        client = client_name[i]
        sample_count = random.randint(300,700)
        for _ in range(sample_count):
            data.append([client,
                         client[0:3].upper(),
                         random.choices(['Positive','Negative','Equivocal'],weights=[0.22,0.74,0.04],k=1)[0],
                         1
                         ])

    second_table = pd.DataFrame(data,columns=['Client','Experiment Names','Result','Sample Count'])
    second_table = second_table.groupby(['Client','Experiment Names','Result'])['Sample Count'].count().reset_index()\
    .pivot(index=['Client','Experiment Names'],columns='Result',values='Sample Count').reset_index()
    second_table['Total'] = second_table.apply(lambda row: row['Equivocal']+row['Negative']+row['Positive'],axis=1)
    second_table['Negative Rate'] = second_table.apply(lambda row: round(row['Negative']/row['Total']*100,2),axis=1)
    second_table['Positive Rate'] = second_table.apply(lambda row: round(row['Positive']/row['Total']*100,2),axis=1)
    second_table['Equivocal Rate'] = second_table.apply(lambda row: round(row['Equivocal']/row['Total']*100,2),axis=1)
    second_table = second_table[['Client','Experiment Names','Total','Negative','Positive','Equivocal','Negative Rate','Positive Rate','Equivocal Rate']]

    data = []
    for i in ['Positive','Negative','Blank','Blank Swab']:
        temp = []
        for _ in range(3):
            client = fake.name()
            for j in range(8):
                od = 0
                if i == 'Positive':
                    od = round(random.uniform(1.9, 2.2),3)
                else:
                    od = round(random.uniform(1.85,2.1),3)
                temp.append([client,
                            client[0:3].upper()+'-'+i+'Control'+str(j),
                            od])
        data.append(pd.DataFrame(temp,columns=['Client','Experiment Names','Observed OD Value']))
    for i in data:
        i.index +=1
            
    return first_table, second_table, data[0], data[1], data[2], data[3]

def generate_low_volume():
    client_count = random.randint(7,10)
    client_name = [fake.name() for _ in range(client_count)]
    sample_count = random.randint(300,400)
    country_name = random.sample(countries,client_count)
    country_dict = {i:j for i,j in zip(client_name,country_name)}
    data = []
    for _ in range(sample_count):
        client = random.choice(client_name)
        data.append([random.choices(['Clinical','Registry','Research'],weights=[0.7,0.28,0.02],k=1)[0],
                    client,
                     country_dict[client],
                     1
                     ])
    df = pd.DataFrame(data,columns=['Type','Client','Country','Sample Count'])
    fifth_table = df.groupby('Country')['Sample Count'].count().reset_index()
    df = df.groupby(['Type','Client'])['Sample Count'].count().reset_index()
    for i in ['A','B','C','DRB1','DRB345','DQB1','DQA1','DPB1','DPA1']:
        df[i] = df.apply(lambda row: random.randint(row['Sample Count']-10,row['Sample Count']) if row['Sample Count'] > 10 else \
                         random.randint(0,row['Sample Count']),axis=1)

    first_table = df.groupby('Type')[['A','B','C','DRB1','DRB345','DQB1','DQA1','DPB1','DPA1']].sum().reset_index()
    third_table = df.groupby('Type')['Sample Count'].sum().reset_index()
    fourth_table = df.groupby(['Type','Client'])['Sample Count'].sum().reset_index()

    data = []
    for _ in range(random.randint(100,150)):
        data.append([random.choices(['HLA','ABO-RH','CCR','CMV','DNA Extraction'],weights=[0.6,0.23,0.12,0.03,0.02],k=1)[0],
                     random.choice(client_name[0:3]),
                     1])
    df2 = pd.DataFrame(data,columns=['Gene','Client','Sample Count'])
    sixth_table = df2.groupby('Gene')['Sample Count'].sum().reset_index()
    return first_table, df, third_table, fourth_table, fifth_table, sixth_table, df2.groupby(['Gene','Client'])['Sample Count'].sum().reset_index()

def generate_pcr():
    sample_count = random.randint(18000,20000)
    client_count = random.randint(7,10)
    client_name = [fake.name() for _ in range(client_count)]
    data = []
    for _ in range(sample_count):
        client = random.choice(client_name)
        data.append([random.choices(['Illumina','Pacbio'],weights=[0.8,0.2],k=1)[0],
                     random.choices(['HLA','ABO-RH','CCR','KIR'],weights=[0.45,0.45,0.09,0.01],k=1)[0],
                     client,
                     client[0:3].upper(),
                     1])
    df = pd.DataFrame(data,columns=['Type','Gene','Client','Experiment Names','Sample Count'])
    df = df.groupby(['Type','Gene','Client','Experiment Names'])['Sample Count'].sum().reset_index()
    df['Blot Count'] = df.apply(lambda row: math.ceil(row['Sample Count']/400),axis=1)
    df['Plate Count'] = df.apply(lambda row: row['Blot Count'] * random.randint(1,30),axis=1)
    return df

def generate_gel():
    sample_count = random.randint(6,12)
    data = []
    for _ in range(sample_count):
        data.append([random.choices(['Illumina','Pacbio'],weights=[0.6,0.4],k=1)[0],
                     random.randint(10,40),
                     random.randint(10,120),
                     random.randint(0,5),
                     random.randint(0,5)])

    df = pd.DataFrame(data,columns=['Type','Gel Count','Amplicon Count','Rerun Count','Repeat Count'])
    df['Total Amplicons'] = df.apply(lambda row: row['Amplicon Count'] + row['Rerun Count'] + row['Repeat Count'],axis=1)
    df['Gel Row Count'] = df.apply(lambda row: random.randint(row['Amplicon Count'],row['Amplicon Count'] + 50),axis=1)

    first_table = df.groupby('Type')[['Gel Count','Amplicon Count','Rerun Count','Repeat Count','Total Amplicons','Gel Row Count']].sum().reset_index()

    sample_count = random.randint(50,100)
    data = []
    for _ in range(sample_count):
        ilu_or_pac = random.choices(['Illumina','Pacbio'],weights=[0.6,0.4],k=1)[0]
        data.append([ilu_or_pac,
                     ilu_or_pac + ' Category-' + random.choice(['I','II','III']),
                    1])
                     
    df2 = pd.DataFrame(data,columns=['Type','Category','Blot Count'])
    third_table = df2.groupby('Type')['Blot Count'].sum().reset_index()
    
    return first_table, df, third_table, df2.groupby(['Type','Category'])['Blot Count'].sum().reset_index()
                     
def generate_illumina():
    run_count = random.randint(8,12)
    data = []
    mi = 1
    nov = 1
    for _ in range(run_count):
        machine = random.choices(['Illumina MiSeq','Illumina NovaSeq'],weights=[0.7,0.3],k=1)[0]
        cell_count = random.randint(1000,10000) if machine == 'Illumina MiSeq' else random.randint(100000,145000)
        experiment_name = mi if machine == 'Illumina MiSeq' else nov
        data.append([machine,
                     machine+str(0000)+'-'+str(experiment_name),
                     cell_count,
                     0 if machine == 'Illumina MiSeq' else 150000])
        if machine == 'Illumina MiSeq':
            mi+=1 
        else:
            nov+=1

    df = pd.DataFrame(data,columns=['NGS Type','Experiment','Total Cells','Pool Threshold'])
    first_table = df.groupby('NGS Type')['Pool Threshold'].count().reset_index()
    first_table.rename(columns={'Pool Threshold':'Run Count'},inplace=True)
    return first_table, df  

def generate_pacbio():
    run_count = random.randint(4,9)
    data = []
    experiment_name = {'Pacbio Sequel-I':1,'Pacbio Sequel-II':1,'Pacbio Sequel-IIe':1}
    for _ in range(run_count):
        machine = random.choices(['Pacbio Sequel-I','Pacbio Sequel-II','Pacbio Sequel-IIe'],weights=[0.6,0.2,0.2],k=1)[0]
        cell_count = random.randint(1000,10000)
        data.append([machine,
                     cell_count,
                     machine+'0000-'+str(experiment_name[machine]),
                     machine+'0000-'+str(experiment_name[machine])+random.choice(['A','B']),
                     random.choices(['LR','SR'],weights=[0.3,0.7],k=1)[0]])
        experiment_name[machine] += 1

    df = pd.DataFrame(data,columns=['Pacbio Type','Total Cells','Job Name','Run Name','Job Type'])
    first_table = df.groupby('Pacbio Type')['Total Cells'].count().reset_index()
    first_table.rename(columns={'Total Cells':'Run Count'},inplace=True)
    df.rename(columns={'Pacbio Type':'Machine Type'},inplace=True)
    return first_table, df  

def generate_repeats():
    experiment_count = random.randint(15,20)
    data = []
    for _ in range(experiment_count):
        machine_type = random.choices(['NGS','Pacbio'],weights=[0.7,0.3],k=1)[0]
        temp = []
        if machine_type == 'NGS':
            temp = [fake.name()[0:3]+str(random.randint(100000,999999))]
        else:
            temp = ['PAC'+str(random.randint(100000,999999))+fake.name()[0:3]]
        sample_count = random.randint(300,750)
        max_repeat = 0
        for i in ['A','B','C','DRB1','DRB345','DQB1','DQA1','DPB1','DPA1']:
            per_gene = random.randint(sample_count-200,sample_count)
            repeat = random.randint(0,int(per_gene*0.1))
            temp.append(per_gene)
            temp.append(repeat)
            if repeat > max_repeat: 
                max_repeat = repeat
            temp.append(round(repeat/per_gene*100,2))

        temp.append(sample_count)
        overall_repeat = max_repeat+random.randint(0,10)
        temp.append(overall_repeat)
        temp.append(round(overall_repeat/sample_count*100,2))

        data.append(temp)

    df = pd.DataFrame(data,columns=['Experiment'] +[f"{cat} {stat}" for cat in ['A','B','C','DRB1','DRB345','DQB1','DQA1','DPB1','DPA1','Overall'] for stat in ['Total','Repeat','%']])
    return df 
