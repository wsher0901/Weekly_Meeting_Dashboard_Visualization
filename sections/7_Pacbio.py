from pytz import timezone
import streamlit as st 
from Functions.Visualization.Pacbio_Visualization import generate_sequencer_bar_chart, generate_jobs_bar_chart, style_total_cell_table
from Functions.Visualization.utility import generate_markdown, st_write, generate_header
st.set_page_config(page_title="Pacbio", layout="wide",initial_sidebar_state='collapsed')
st.markdown("""
        <style>
               .block-container {
                    padding-top: 2rem;
                }
        </style>
        """, unsafe_allow_html=True)

tz = timezone('EST')
st.logo('MyLogo.png')
data = st.session_state['Pacbio']
generate_header(title='Pacbio',
                prev="sections/6_Illumina.py",
                next="sections/8_Repeats.py",
                status_prev='Illumina status',
                status_next='Repeats status')


with st.container(): # first section
    f1,f2 = st.columns([4,6],border=True)
    f1.markdown(generate_markdown('Pacbio Sequencer',font_size=50,font_color='black'),unsafe_allow_html=True)
    f1.plotly_chart(generate_sequencer_bar_chart(data[0]),use_container_width=True)
    f2.markdown(generate_markdown('Pacbio Jobs',font_size=50,font_color='black'),unsafe_allow_html=True)
    f2.plotly_chart(generate_jobs_bar_chart(data[1]),use_container_width=True)
    st.expander('Details').table(style_total_cell_table(data[1]))

with st.container(border=True): # Comment
    font_size = 20
    if 'Pacbio' + ' image' in st.session_state and 'Pacbio' + ' comment' in st.session_state:
        comment_image, comment_text = st.columns(2)
    elif 'Pacbio' + ' image' in st.session_state and 'Pacbio' + ' comment' not in st.session_state:
        comment_image = st.container()
    elif 'Pacbio' + ' image' not in st.session_state and 'Pacbio' + ' comment' in st.session_state:
        comment_text = st.container()
        font_size=60
    if 'Pacbio' + ' image' in st.session_state:
        image_tab = ['Comment '+str(i) for i in range(1,len(st.session_state['Pacbio image'])+1,1)]
        tab_list = ['Comment '+str(i) for i in range(1,len(st.session_state['Pacbio image'])+1,1)]
        tab_list = comment_image.tabs(image_tab)
        for ind,i in enumerate(tab_list):
            i.image(st.session_state['Pacbio' + ' image'][ind],width=800)

    if 'Pacbio' + ' comment' in st.session_state:
        if font_size == 20:
            st_write(comment_text,14)
        comment_text.markdown(f"<h1 style='text-align: center;font-size: {font_size}px;font-family: Arial;'>{st.session_state['Pacbio' + ' comment']}</h1>", unsafe_allow_html=True)

st.write('')
buttons2 = st.columns([5,0.5,0.5,5])
buttons2[1].page_link("sections/6_Illumina.py", label='Prev', icon='⏮️', disabled = st.session_state['Illumina status'])
buttons2[2].page_link("sections/8_Repeats.py", label="Next", icon="⏭️", disabled = st.session_state['Repeats status'])