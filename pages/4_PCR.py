from pytz import timezone
import streamlit as st 
from Functions.Visualization.PCR_Visualization import generate_bar_chart_by_gene, style_table
from Functions.Visualization.utility import st_write, generate_markdown,generate_header
st.set_page_config(page_title="PCR", layout="wide",initial_sidebar_state='collapsed')
st.markdown("""
        <style>
               .block-container {
                    padding-top: 2rem;
                }
        </style>
        """, unsafe_allow_html=True)

tz = timezone('EST')
st.logo('Histogenetics_Logo.png')
data = st.session_state['PCR']
st.write(data)

generate_header(title='PCR',
                prev="pages/3_Pre_PCR_Low_Volume.py",
                next="pages/5_Gel.py",
                status_prev='Pre PCR (Low Vol) status',
                status_next='Gel status')


for i in ['Illumina','Pacbio']:
    with st.container():
        st.write(generate_markdown(i, font_size=60,font_color='black'), unsafe_allow_html=True)
        st_write(st,2)
        f1,f2 = st.columns([6,2],border=True)
        f1.plotly_chart(generate_bar_chart_by_gene(data,i),use_container_width=True)
        st_write(f2,6)
        f2.write(generate_markdown(i+' Sample', font_size=30,font_color='#f9423a'),unsafe_allow_html=True)
        f2.write(generate_markdown(data[data.Type == i]['Sample Count'].sum(), font_size=100,font_color='black'),unsafe_allow_html=True)
        st_write(f2,3)
        f2.write(generate_markdown(i+' Plate', font_size=30,font_color='#f9423a'),unsafe_allow_html=True)
        f2.write(generate_markdown(data[data.Type == i]['Plate Count'].sum(), font_size=100,font_color='black'),unsafe_allow_html=True)
        st.expander('Details').table(style_table(data,i))    
        st_write(st,6)


with st.container(border=True): # Comment
    font_size = 20
    if 'PCR' + ' image' in st.session_state and 'PCR' + ' comment' in st.session_state:
        comment_image, comment_text = st.columns(2)
    elif 'PCR' + ' image' in st.session_state and 'PCR' + ' comment' not in st.session_state:
        comment_image = st.container()
    elif 'PCR' + ' image' not in st.session_state and 'PCR' + ' comment' in st.session_state:
        comment_text = st.container()
        font_size=60
    if 'PCR' + ' image' in st.session_state:
        image_tab = ['Comment '+str(i) for i in range(1,len(st.session_state['PCR image'])+1,1)]
        tab_list = ['Comment '+str(i) for i in range(1,len(st.session_state['PCR image'])+1,1)]
        tab_list = comment_image.tabs(image_tab)
        for ind,i in enumerate(tab_list):
            i.image(st.session_state['PCR' + ' image'][ind],width=800)

    if 'PCR' + ' comment' in st.session_state:
        if font_size == 20:
            st_write(comment_text,14)
        comment_text.markdown(f"<h1 style='text-align: center;font-size: {font_size}px;font-family: Arial;'>{st.session_state['PCR' + ' comment']}</h1>", unsafe_allow_html=True)

st.write('')
buttons2 = st.columns([5,0.5,0.5,5])
buttons2[1].page_link("pages/3_Pre_PCR_Low_Volume.py", label='Prev', icon='⏮️',disabled = st.session_state['Pre PCR (Low Vol) status'])
buttons2[2].page_link("pages/5_Gel.py", label='Next', icon="⏭️",disabled = st.session_state['Gel status'])