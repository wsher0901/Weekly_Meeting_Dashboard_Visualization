from pytz import timezone
import streamlit as st 
from Functions.Visualization.Reagents_Visualization import generate_buffer_bar_chart, style_buffer_table, generate_primer_bar_chart, style_primer_table, \
generate_dispense_bar_chart, style_dispense_table, generate_master_bar_chart, style_master_table
from Functions.Visualization.utility import generate_markdown, st_write, generate_header
st.set_page_config(page_title="Reagent", layout="wide",initial_sidebar_state='collapsed')
st.markdown("""
        <style>
               .block-container {
                    padding-top: 2rem;
                }
        </style>
        """, unsafe_allow_html=True)

tz = timezone('EST')
st.logo('Histogenetics_Logo.png')
data = st.session_state['Reagents']

generate_header(title='Reagents',
                prev="pages/8_Repeats.py",
                next="pages/10_HLA_TAT.py",
                status_prev='Repeats status',
                status_next='HLA TAT status')

buffer, primer, dispense, master = st.container(), st.container(), st.container(), st.container()
for i,j,k,function,styling in zip([buffer,primer,dispense,master], ['Buffer','Primer','Dispense','Master Mix'], [0,1,2,3],
                          [generate_buffer_bar_chart,generate_primer_bar_chart,generate_dispense_bar_chart,generate_master_bar_chart],
                          [style_buffer_table,style_primer_table,style_dispense_table,style_master_table]): 
    with i:
        st.markdown(generate_markdown(j,font_size=60,font_color='black'),unsafe_allow_html=True)
        try:
            st.plotly_chart(function(data[k]),use_container_width=True)
            st.expander(j).table(styling(data[k]))
        except: 
            st_write(st,8)
            st.markdown(generate_markdown('No Data Available',font_size=30,font_color='black'),unsafe_allow_html=True)
        st_write(st,8)  

if len(data[3]) != 0:
    with st.container():
        st.markdown(generate_markdown('Master Mix',font_size=60,font_color='black'),unsafe_allow_html=True)
        st.plotly_chart(generate_master_bar_chart(data[3]),use_container_width=True)
        st.expander('Master').table(style_master_table(data[3]))

with st.container(border=True): # Comment
    font_size = 20
    if 'Reagents' + ' image' in st.session_state and 'Reagents' + ' comment' in st.session_state:
        comment_image, comment_text = st.columns(2)
    elif 'Reagents' + ' image' in st.session_state and 'Reagents' + ' comment' not in st.session_state:
        comment_image = st.container()
    elif 'Reagents' + ' image' not in st.session_state and 'Reagents' + ' comment' in st.session_state:
        comment_text = st.container()
        font_size=60
    if 'Reagents' + ' image' in st.session_state:
        image_tab = ['Comment '+str(i) for i in range(1,len(st.session_state['Reagents image'])+1,1)]
        tab_list = ['Comment '+str(i) for i in range(1,len(st.session_state['Reagents image'])+1,1)]
        tab_list = comment_image.tabs(image_tab)
        for ind,i in enumerate(tab_list):
            i.image(st.session_state['Reagents' + ' image'][ind],width=800)

    if 'Reagents' + ' comment' in st.session_state:
        if font_size == 20:
            st_write(comment_text,14)
        comment_text.markdown(f"<h1 style='text-align: center;font-size: {font_size}px;font-family: Arial;'>{st.session_state['Reagents' + ' comment']}</h1>", unsafe_allow_html=True)

st.write('')
buttons2 = st.columns([5,0.5,0.5,5])
buttons2[1].page_link("pages/8_Repeats.py", label='Prev', icon='⏮️', disabled = st.session_state['Repeats status'])
buttons2[2].page_link("pages/10_HLA_TAT.py", label="Next", icon="⏭️", disabled = st.session_state['HLA TAT status'])