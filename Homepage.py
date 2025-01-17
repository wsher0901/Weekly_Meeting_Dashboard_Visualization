import os
import pickle
from datetime import timedelta, datetime
from pytz import timezone
import streamlit as st 
import pandas as pd 
import plotly.express as px
from Functions.Data.fetch_data import load_data, get_date, generate_meeting, remove_meeting, add_comment, load_comment
from Files.common_list import page_list
st.set_page_config(page_title="HistoDash", layout="wide",initial_sidebar_state='collapsed')
st.markdown("""
        <style>
               .block-container {
                    padding-top: 2rem;
                }
        </style>
        """, unsafe_allow_html=True)

tz = timezone('EST')
lw,tw = get_date()
if 'lw' not in st.session_state:
    st.session_state.lw = lw
    st.session_state.tw = tw

col1,col2,col3 = st.columns([2,3,2])
col2.image('MyLogo.png')
i1,i2,i3= st.columns([2,2,2])
form = i2.form('Customize')
input_date = form.date_input('Date Range', value=[st.session_state.lw,st.session_state.tw])

if 'choice' not in st.session_state:
    st.session_state.choice = []
    for i in page_list:
        st.session_state[i+' status'] = True

choice = form.pills(
    'Pages',
    options=page_list,
    default=st.session_state.choice,
    selection_mode='multi'
)
submitted = form.form_submit_button('Enter',use_container_width=True)

if submitted:
    with i2.status("Downloading data...", expanded=True) as status:
        choice = page_list if len(choice) == 0 else choice
        load_data(input_date[0],input_date[1],choice)
        for i in choice:
            load_comment(input_date[0].strftime('%m_%d_%y'),i)
        status.update(label="Download complete!", state="complete", expanded=False)

    st.session_state.choice = choice
    st.session_state.lw, st.session_state.tw = input_date[0], input_date[1]
    st.rerun()

st.write('')
a1,a5,a9 = st.columns([4,1,4])
a5.page_link("Homepage.py", label="Home", icon="🏠")
a5.page_link("pages/1_Pre_PCR_High_Volume.py", label="Pre PCR High Volume", icon="💉", disabled = st.session_state['Pre PCR (High Vol) status'])
a5.page_link("pages/2_Pre_PCR_CMV.py", label="Pre PCR CMV", icon="🦠", disabled = st.session_state['Pre PCR (CMV) status'])
a5.page_link("pages/3_Pre_PCR_Low_Volume.py", label='Pre PCR Low Volume', icon='🏥',disabled = st.session_state['Pre PCR (Low Vol) status'])
a5.page_link("pages/4_PCR.py", label='PCR', icon="🧪",disabled = st.session_state['PCR status'])
a5.page_link("pages/5_Gel.py", label='Gel', icon="🧫",disabled = st.session_state['Gel status'])
a5.page_link("pages/6_Illumina.py", label='Illumina', icon='🇮🇱', disabled = st.session_state['Illumina status'])
a5.page_link("pages/7_Pacbio.py",label='Pacbio',icon='🅿', disabled = st.session_state['Pacbio status'])
a5.page_link("pages/8_Repeats.py", label="Repeats", icon="♻️", disabled = st.session_state['Repeats status'])
a5.page_link("pages/10_HLA_TAT.py", label="HLA TAT", icon="📆", disabled = st.session_state['HLA TAT status'])
a5.page_link("pages/11_Non_HLA_TAT.py", label="Non HLA TAT", icon="📆", disabled = st.session_state['Non-HLA TAT status'])
a5.page_link("pages/12_New_Allele.py", label="New Allele", icon="🧬", disabled = st.session_state['New Allele status'])

if os.path.exists('Archive/'):
    entries = sorted([i for i in os.listdir('Archive/') if i[0:2] == tw.strftime('%m')],key=lambda x: int(x[3:5]),reverse=True)
    for ind,d in enumerate(entries,0):
        meetings = st.sidebar.container()
        m1,m2 = meetings.columns([10,1])
        meeting = m1.button('/'.join(d.split('_')),use_container_width=True)
        remove_button = m2.button('X',key=ind)
        if meeting:
            file_path = 'Archive/' + d
            for i in page_list:
                with open(file_path+'/'+i+'.pkl','rb') as f:
                    st.session_state[i] = pickle.load(f)
                    st.session_state[i+' status'] = False
                load_comment(d,i)
            if os.path.exists(file_path+'/'+'illumina_yearly.pkl'):
                with open(file_path+'/'+'illumina_yearly.pkl','rb') as f:
                    st.session_state.illumina_yearly = pickle.load(f)
            else:
                st.session_state.illumina_yearly = pd.read_csv('Files/illumina_yearly.csv')
            if os.path.exists(file_path+'/'+'pacbio_yearly.pkl'):
                with open(file_path+'/'+'pacbio_yearly.pkl','rb') as f:
                    st.session_state.pacbio_yearly = pickle.load(f)
            else:
                st.session_state.pacbio_yearly = pd.read_csv('Files/pacbio_yearly.csv')
            st.session_state.lw = datetime.strptime(d,'%m_%d_%y') - timedelta(days=7)
            st.session_state.tw = datetime.strptime(d,'%m_%d_%y') - timedelta(days=1)      
            st.switch_page("pages/1_Pre_PCR_High_Volume.py")

        if remove_button:
            remove_meeting(d)

generate = st.sidebar.button('Generate Meeting',use_container_width=True)
if generate:
    generate_meeting(lw,tw)

gap = st.sidebar.write('')

comment = st.sidebar.button('Add Comment',use_container_width=True)
if comment:
    add_comment(tw)