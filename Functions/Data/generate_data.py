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
    date_list = [(last_week + timedelta(days=i)) for i in range(0,7,1)]

    data = []
    for _ in range(sample_count):
        client = random.choice(client_name)
        data.append([random.choices(['Antibody Extraction','CMV-ELISA','Plasma / Serum Dilution'],weights=[0.45,0.1,0.45],k=1)[0],
                     client[0:3].upper()+str(random.randint(100000,999999)),
                     client,

        ])



