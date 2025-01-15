from pytz import timezone
import streamlit as st 
from Functions.Visualization.Illumina_Visualization import generate_sequence_run_bar_chart, generate_pool_count_bar_chart, style_pool_count_table
from Functions.Visualization.utility import st_write, generate_markdown, generate_header
st.set_page_config(page_title="Illumina", layout="wide",initial_sidebar_state='collapsed')
st.markdown("""
        <style>
               .block-container {
                    padding-top: 2rem;
                }
        </style>
        """, unsafe_allow_html=True)

tz = timezone('EST')
st.logo('Histogenetics_Logo.png')
data = st.session_state['Illumina']
generate_header(title='Illumina',
                prev="pages/5_Gel.py",
                next="pages/7_Pacbio.py",
                status_prev='Gel status',
                status_next='Pacbio status')


with st.container(): # first section
    f1,f2 = st.columns([2,4],border=True)
    f1.markdown(generate_markdown(text='# of Sequence Runs',font_size=50,font_color='black'),unsafe_allow_html=True)
    st_write(f1,4)
    f1.plotly_chart(generate_sequence_run_bar_chart(data[0]),use_container_width=True)
    f2.markdown(generate_markdown(text='Pool Count',font_size=50,font_color='black'),unsafe_allow_html=True)
    st_write(f2,4)
    f2.plotly_chart(generate_pool_count_bar_chart(data[1]),use_container_width=True)
    st.expander('Pool Count Details').table(style_pool_count_table(data[1]))

with st.container(border=True): # Comment
    font_size = 20
    if 'Illumina' + ' image' in st.session_state and 'Illumina' + ' comment' in st.session_state:
        comment_image, comment_text = st.columns(2)
    elif 'Illumina' + ' image' in st.session_state and 'Illumina' + ' comment' not in st.session_state:
        comment_image = st.container()
    elif 'Illumina' + ' image' not in st.session_state and 'Illumina' + ' comment' in st.session_state:
        comment_text = st.container()
        font_size=60
    if 'Illumina' + ' image' in st.session_state:
        image_tab = ['Comment '+str(i) for i in range(1,len(st.session_state['Illumina image'])+1,1)]
        tab_list = ['Comment '+str(i) for i in range(1,len(st.session_state['Illumina image'])+1,1)]
        tab_list = comment_image.tabs(image_tab)
        for ind,i in enumerate(tab_list):
            i.image(st.session_state['Illumina' + ' image'][ind],width=800)

    if 'Illumina' + ' comment' in st.session_state:
        if font_size == 20:
            st_write(comment_text,14)
        comment_text.markdown(f"<h1 style='text-align: center;font-size: {font_size}px;font-family: Arial;'>{st.session_state['Illumina' + ' comment']}</h1>", unsafe_allow_html=True)

st.write('')
buttons2 = st.columns([5,0.5,0.5,5])
buttons2[1].page_link("pages/5_Gel.py", label='Prev', icon="⏮️",disabled = st.session_state['Gel status'])
buttons2[2].page_link("pages/7_Pacbio.py",label='Next',icon='⏭️', disabled = st.session_state['Pacbio status'])