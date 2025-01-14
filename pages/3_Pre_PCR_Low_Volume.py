from pytz import timezone
import streamlit as st 
from Functions.Visualization.Low_Volume_Visualization import generate_pie_chart_for_client_type, generate_bar_chart_for_client, style_client_table, \
generate_bar_chart_for_locus, style_locuswise_table, generate_map, generate_pie_chart_by_country, generate_bar_chart_for_nonhla, style_nonhla_table
from Functions.Visualization.utility import st_write, generate_markdown, generate_header
st.set_page_config(page_title="Low Volume Pre-PCR", layout="wide",initial_sidebar_state='collapsed')
st.markdown("""
        <style>
               .block-container {
                    padding-top: 2rem;
                }
        </style>
        """, unsafe_allow_html=True)

tz = timezone('EST')
st.logo('Histogenetics_Logo.png')
data = st.session_state['Pre PCR (Low Vol)']
generate_header(title='Pre-PCR (Low Volume)',
                prev="pages/2_Pre_PCR_CMV.py",
                next="pages/4_PCR.py",
                status_prev='Pre PCR (CMV) status',
                status_next='PCR status')


with st.container(): # first section
    st.write(generate_markdown('HLA Sample-wise Statistics', font_size=60,font_color='black'), unsafe_allow_html=True)
    st_write(st,2)
    f1,f2 = st.columns([4,4],border=True)
    f1.plotly_chart(generate_pie_chart_for_client_type(data[2]))
    st_write(f2,3)
    f2.plotly_chart(generate_bar_chart_for_client(data[3]))
    st.expander('Sample-wise Statistics (by client)').table(style_client_table(data[3]))    
    st_write(st,8)


with st.container(): # second section
    st.write(generate_markdown('HLA Locus- wise Statistics', font_size=60,font_color='black'), unsafe_allow_html=True)
    st.plotly_chart(generate_bar_chart_for_locus(data[0]),use_container_width=True)
    st.expander('Locus-wise Statistics').table(style_locuswise_table(data[1]))


with st.container(): # third section
    st.write(generate_markdown('By Country', font_size=60,font_color='black'),unsafe_allow_html=True)
    f1,f2 = st.columns([6,4])
    f1.plotly_chart(generate_map(data[4]))
    f2.plotly_chart(generate_pie_chart_by_country(data[4]))


with st.container(): # fourth section
    st.write(generate_markdown(text='Non-HLA Test Statistics',font_size=60,font_color='black'),unsafe_allow_html=True)
    st.plotly_chart(generate_bar_chart_for_nonhla(data[5]))
    st.expander('Non-HLA Statistics').table(style_nonhla_table(data[6]))


with st.container(border=True): # Comment
    font_size = 20
    if 'Pre PCR (Low Vol)' + ' image' in st.session_state and 'Pre PCR (Low Vol)' + ' comment' in st.session_state:
        comment_image, comment_text = st.columns(2)
    elif 'Pre PCR (Low Vol)' + ' image' in st.session_state and 'Pre PCR (Low Vol)' + ' comment' not in st.session_state:
        comment_image = st.container()
    elif 'Pre PCR (Low Vol)' + ' image' not in st.session_state and 'Pre PCR (Low Vol)' + ' comment' in st.session_state:
        comment_text = st.container()
        font_size=60
    if 'Pre PCR (Low Vol)' + ' image' in st.session_state:
        image_tab = ['Comment '+str(i) for i in range(1,len(st.session_state['Pre PCR (Low Vol) image'])+1,1)]
        tab_list = ['Comment '+str(i) for i in range(1,len(st.session_state['Pre PCR (Low Vol) image'])+1,1)]
        tab_list = comment_image.tabs(image_tab)
        for ind,i in enumerate(tab_list):
            i.image(st.session_state['Pre PCR (Low Vol)' + ' image'][ind],width=800)

    if 'Pre PCR (Low Vol)' + ' comment' in st.session_state:
        if font_size == 20:
            st_write(comment_text,14)
        comment_text.markdown(f"<h1 style='text-align: center;font-size: {font_size}px;font-family: Arial;'>{st.session_state['Pre PCR (Low Vol)' + ' comment']}</h1>", unsafe_allow_html=True)

st.write('')
buttons2 = st.columns([5,0.5,0.5,5])
buttons2[1].page_link("pages/2_Pre_PCR_CMV.py", label="Prev", icon="⏭️", disabled = st.session_state['Pre PCR (CMV) status'])
buttons2[2].page_link("pages/4_PCR.py", label='Next', icon="⏭️",disabled = st.session_state['PCR status'])