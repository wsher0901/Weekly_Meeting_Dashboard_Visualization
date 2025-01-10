from pytz import timezone
import streamlit as st 
from Functions.Visualization.Repeats_Visualization import generate_weekly_data, style_detail_chart
from Functions.Visualization.utility import generate_markdown, st_write, generate_header
st.set_page_config(page_title="Repeat Visualization", layout="wide",initial_sidebar_state='collapsed')
st.markdown("""
        <style>
               .block-container {
                    padding-top: 2rem;
                }
        </style>
        """, unsafe_allow_html=True)

gene_list = ['A','B','C','DRB1','DRB345','DQB1','DQA1','DPB1','DPA1']
tz = timezone('EST')
st.logo('Histogenetics_Logo.png')
ngs,pac, ngs_by_client, pac_by_client = st.session_state['Repeats']
generate_header(title='Repeats',
                prev="pages/7_Pacbio.py",
                next="pages/9_Reagents.py",
                status_prev='Pacbio status',
                status_next='Reagents status')

with st.container():
    for i,j in zip(['NGS','Pacbio'],[[ngs,ngs_by_client],[pac,pac_by_client]]):
        st.markdown(generate_markdown(i,font_size=60,font_color='black'),unsafe_allow_html=True)
        if len(j[0]) != 0:
                st.plotly_chart(generate_weekly_data(j[0],i),use_container_width=True)

        for tab,l in zip(st.tabs(['By Experiment','By Client']),[0,1]):
            data = j[l]
            if len(data) != 0:
                tab.table(style_detail_chart(data,i))
            else:
                tab.markdown(generate_markdown(text='No Data from '+i,font_size=60,font_color='#f9423a'),unsafe_allow_html=True)
            st_write(st,4)


with st.container(border=True): # Comment
    font_size = 20
    if 'Repeats' + ' image' in st.session_state and 'Repeats' + ' comment' in st.session_state:
        comment_image, comment_text = st.columns(2)
    elif 'Repeats' + ' image' in st.session_state and 'Repeats' + ' comment' not in st.session_state:
        comment_image = st.container()
    elif 'Repeats' + ' image' not in st.session_state and 'Repeats' + ' comment' in st.session_state:
        comment_text = st.container()
        font_size=60
    if 'Repeats' + ' image' in st.session_state:
        image_tab = ['Comment '+str(i) for i in range(1,len(st.session_state['Repeats image'])+1,1)]
        tab_list = ['Comment '+str(i) for i in range(1,len(st.session_state['Repeats image'])+1,1)]
        tab_list = comment_image.tabs(image_tab)
        for ind,i in enumerate(tab_list):
            i.image(st.session_state['Repeats' + ' image'][ind],width=800)

    if 'Repeats' + ' comment' in st.session_state:
        if font_size == 20:
            st_write(comment_text,14)
        comment_text.markdown(f"<h1 style='text-align: center;font-size: {font_size}px;font-family: Arial;'>{st.session_state['Repeats' + ' comment']}</h1>", unsafe_allow_html=True)

st.write('')
buttons2 = st.columns([5,0.5,0.5,5])
buttons2[1].page_link("pages/7_Pacbio.py", label='Prev', icon='⏮️', disabled = st.session_state['Pacbio status'])
buttons2[2].page_link("pages/9_Reagents.py", label="Next", icon="⏭️", disabled = st.session_state['Reagents status'])