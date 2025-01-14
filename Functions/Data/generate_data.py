from datetime import timedelta, datetime, date, time
import random
from faker import Faker
import pandas as pd

fake = Faker()

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
    country_name = [fake.country() for _ in range(client_count) if fake.country() not in ['Antarctica (the territory South of 60 deg S)','palestinian territory']]
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

