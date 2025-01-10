from pytz import timezone
import streamlit as st 
from Functions.Visualization.Gel_Visualization import generate_comprehensive_bar_chart, style_gel_details, generate_bar_chart_for_blot, style_blot_details, style_rejection_details
from Functions.Visualization.utility import st_write, generate_markdown, generate_header
st.set_page_config(page_title="Gel", layout="wide",initial_sidebar_state='collapsed')
st.markdown("""
        <style>
               .block-container {
                    padding-top: 2rem;
                }
        </style>
        """, unsafe_allow_html=True)

tz = timezone('EST')
st.logo('Histogenetics_Logo.png')
gel_summary,gel_specific,blot_summary,blot_specific,rejection = st.session_state['Gel']

generate_header(title='Gel',
                prev="pages/4_PCR.py",
                next="pages/6_Illumina.py",
                status_prev='PCR status',
                status_next='Illumina status')


with st.container(): # first section
    st.write(generate_markdown('Gel', font_size=60,font_color='black'), unsafe_allow_html=True)
    st.plotly_chart(generate_comprehensive_bar_chart(gel_summary),use_container_width=True)
    st.expander('Gel Details').table(style_gel_details(gel_specific))
    st_write(st,8)


with st.container(): # second section
    st.write(generate_markdown('Blot', font_size=60,font_color='black'), unsafe_allow_html=True)
    st_write(st,2)
    s1,s2 = st.columns([4,1],border=True)
    st_write(s2,4)
    s1.plotly_chart(generate_bar_chart_for_blot(blot_specific),use_container_width=True)
    s2.write(generate_markdown('Illumina', font_size=30,font_color='#EE3233'), unsafe_allow_html=True)
    s2.write(generate_markdown(blot_summary[blot_summary.Type == 'Illumina']['Blot Count'].iloc[0], font_size=120,font_color='black'), unsafe_allow_html=True)
    s2.write(generate_markdown('Pacbio', font_size=30,font_color='#66A7C5'), unsafe_allow_html=True)
    s2.write(generate_markdown(blot_summary[blot_summary.Type == 'Pacbio']['Blot Count'].iloc[0], font_size=120,font_color='black'), unsafe_allow_html=True)
    st.expander('Blot Details').table(style_blot_details(blot_specific))


with st.container(): # third section
    if len(rejection) != 0:
        st_write(st,8)
        st.write(generate_markdown('Rejection', font_size=60,font_color='black'), unsafe_allow_html=True)
        st_write(st,4)
        st.table(style_rejection_details(rejection))

with st.container(border=True): # Comment
    font_size = 20
    if 'Gel' + ' image' in st.session_state and 'Gel' + ' comment' in st.session_state:
        comment_image, comment_text = st.columns(2)
    elif 'Gel' + ' image' in st.session_state and 'Gel' + ' comment' not in st.session_state:
        comment_image = st.container()
    elif 'Gel' + ' image' not in st.session_state and 'Gel' + ' comment' in st.session_state:
        comment_text = st.container()
        font_size=60
    if 'Gel' + ' image' in st.session_state:
        image_tab = ['Comment '+str(i) for i in range(1,len(st.session_state['Gel image'])+1,1)]
        tab_list = ['Comment '+str(i) for i in range(1,len(st.session_state['Gel image'])+1,1)]
        tab_list = comment_image.tabs(image_tab)
        for ind,i in enumerate(tab_list):
            i.image(st.session_state['Gel' + ' image'][ind],width=800)

    if 'Gel' + ' comment' in st.session_state:
        if font_size == 20:
            st_write(comment_text,14)
        comment_text.markdown(f"<h1 style='text-align: center;font-size: {font_size}px;font-family: Arial;'>{st.session_state['Gel' + ' comment']}</h1>", unsafe_allow_html=True)

st.write('')
buttons2 = st.columns([5,0.5,0.5,5])
buttons2[1].page_link("pages/4_PCR.py", label='Prev', icon="⏮️",disabled = st.session_state['PCR status'])
buttons2[2].page_link("pages/6_Illumina.py", label='Next', icon='⏭️', disabled = st.session_state['Illumina status'])