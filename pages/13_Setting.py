import os, glob
from pytz import timezone
import streamlit as st 
from Functions.Visualization.High_Volume_Visualization import st_write
st.set_page_config(page_title="Setting", layout="wide",initial_sidebar_state='collapsed')
st.markdown("""
        <style>
               .block-container {
                    padding-top: 2rem;
                }
        </style>
        """, unsafe_allow_html=True)

tz = timezone('EST')
st.logo('Histogenetics_Logo.png')

with st.container():
    st.markdown(f"<h1 style='text-align: center;font-size: 100px;font-family: Arial;color: #f9423a;padding-bottom: 0;'>Setting</h1>", unsafe_allow_html=True)
    st.write('')

with st.container(border=False,height=700):
    o1,o2,o3 = st.columns([5,1,5])
    col1,col2,col3 = st.columns(3)
    if os.path.exists('Data/'):
        order_by = o2.radio('Order',['Page','Date'])
        if order_by == 'Date':
            meeting = col1.selectbox('Date',sorted(['/'.join(i.split('_')) for i in os.listdir('Data/')]))
            col1.write(['/'.join(i.split('_')) for i in os.listdir('Data/')])
            if meeting:
                st_write(col2,4)
                page= col2.selectbox('Page',sorted(['/'.join(i[:-4].split('_')) for i in os.listdir('Data/'+'_'.join(meeting.split('/')))],
                                                key=lambda x: ['Pre PCR (High Vol)','Pre PCR (CMV)','Pre PCR (Low Vol)','PCR','Gel','Illumina','Pacbio','Repeats','Reagents','New Allele','HLA TAT','Non-HLA TAT'].index(x)))
                col2.write(sorted(['/'.join(i[:-4].split('_')) for i in os.listdir('Data/'+'_'.join(meeting.split('/')))],
                                                key=lambda x: ['Pre PCR (High Vol)','Pre PCR (CMV)','Pre PCR (Low Vol)','PCR','Gel','Illumina','Pacbio','Repeats','Reagents','New Allele','HLA TAT','Non-HLA TAT'].index(x)))
                if page:
                    st_write(col3,8)
                    if os.path.exists('Comment/'+'_'.join(meeting.split('/'))+'/'+page+'.txt'):
                        with open('Comment/'+'_'.join(meeting.split('/'))+'/'+page+'.txt','r') as f:
                            col3.markdown(f"<h1 style='text-align: center;font-size: 50px;font-family: Arial;color: white;padding-bottom: 0;'>Comment:</h1>", unsafe_allow_html=True)
                            col3.write('')
                            col3.markdown(f"<h1 style='text-align: center;font-size: 20px;font-family: Arial;color: #f9423a;padding-bottom: 0;'>{f.read()}</h1>", unsafe_allow_html=True)
                            col3.write('')

                    col3.markdown(f"<h1 style='text-align: center;font-size: 50px;font-family: Arial;color: white;padding-bottom: 0;'>Images:</h1>", unsafe_allow_html=True)
                    for name in glob.glob('Comment/'+'_'.join(meeting.split('/'))+'/'+page+'*'+'.png'):
                        if os.path.exists(name):
                            col3.markdown(f"<h1 style='text-align: center;font-size: 15px;font-family: Arial;color: #f9423a;padding-bottom: 0;'>{name}</h1>", unsafe_allow_html=True)
    
        else:
            page = col1.selectbox('Page',['Pre PCR (High Vol)','Pre PCR (CMV)','Pre PCR (Low Vol)','PCR','Gel','Illumina','Pacbio','Repeats','Reagents','New Allele','HLA TAT','Non-HLA TAT'])
            col1.write(['Pre PCR (High Vol)','Pre PCR (CMV)','Pre PCR (Low Vol)','PCR','Gel','Illumina','Pacbio','Repeats','Reagents','New Allele','HLA TAT','Non-HLA TAT'])
            if page:
                st_write(col2,4)
                meeting = col2.selectbox('Date',(['/'.join(i.split('_')) for i in os.listdir('Data/') if os.path.exists('Data/'+i+'/'+page+'.pkl')]))
                col2.write((['/'.join(i.split('_')) for i in os.listdir('Data/') if os.path.exists('Data/'+i+'/'+page+'.pkl')]))
                if meeting:
                    st_write(col3,8)
                    if os.path.exists('Comment/'+'_'.join(meeting.split('/'))+'/'+page+'.txt'):
                        with open('Comment/'+'_'.join(meeting.split('/'))+'/'+page+'.txt','r') as f:
                            col3.markdown(f"<h1 style='text-align: center;font-size: 50px;font-family: Arial;color: white;padding-bottom: 0;'>Comment:</h1>", unsafe_allow_html=True)
                            col3.write('')
                            col3.markdown(f"<h1 style='text-align: center;font-size: 20px;font-family: Arial;color: #f9423a;padding-bottom: 0;'>{f.read()}</h1>", unsafe_allow_html=True)
                            col3.write('')

                    col3.markdown(f"<h1 style='text-align: center;font-size: 50px;font-family: Arial;color: white;padding-bottom: 0;'>Images:</h1>", unsafe_allow_html=True)
                    for name in glob.glob('Comment/'+'_'.join(meeting.split('/'))+'/'+page+'*'+'.png'):
                        if os.path.exists(name):
                            col3.markdown(f"<h1 style='text-align: center;font-size: 15px;font-family: Arial;color: #f9423a;padding-bottom: 0;'>{name}</h1>", unsafe_allow_html=True)
