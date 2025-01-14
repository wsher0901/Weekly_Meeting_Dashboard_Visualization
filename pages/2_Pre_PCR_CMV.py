from pytz import timezone
import streamlit as st 
from Functions.Visualization.CMV_Visualization import generate_bar_chart_for_cmv_statistics, style_cmv_statistics_table, generate_pie_chart_for_cmv_analytics, style_cmv_analytics_table, generate_box_plot_chart_for_cmv_analytics, style_positive_control_table, style_remaining_control_table
from Functions.Visualization.utility import st_write, generate_markdown, generate_header
st.set_page_config(page_title="CMV Pre-PCR", layout="wide",initial_sidebar_state='collapsed')
st.markdown("""
        <style>
               .block-container {
                    padding-top: 2rem;
                }
        </style>
        """, unsafe_allow_html=True)

tz = timezone('EST')
st.logo('Histogenetics_Logo.png')
data = st.session_state['Pre PCR (CMV)']
generate_header(title='Pre PCR (CMV)',
                prev="pages/1_Pre_PCR_High_Volume.py",
                next="pages/3_Pre_PCR_Low_Volume.py",
                status_prev='Pre PCR (High Vol) status',
                status_next='Pre PCR (Low Vol) status')

with st.container(): # first section
    st.markdown(generate_markdown(text='CMV Statistics',font_color='black',font_size=60), unsafe_allow_html=True)
    st.markdown(generate_markdown(text='Note: Instruments used: <br>Tecan Fluent instrument (Automated Liquid Handler) <br> Biotek ELX405 Select (Plate Washer)',font_size=14), unsafe_allow_html=True)
    st_write(st,2)
    st.plotly_chart(generate_bar_chart_for_cmv_statistics(data[0]),use_container_width=True)
    st.table(style_cmv_statistics_table(data[0]))
    st_write(st,6)


with st.container(): # second section
    st.markdown(generate_markdown(text='CMV Analytics',font_color='black',font_size=60), unsafe_allow_html=True)
    f1,f2 = st.columns([6.5,3.5])
    st_write(f1,10)
    f1.table(style_cmv_analytics_table(data[1]))
    f1.write(generate_markdown(text='Note: Expected Percentage (%) of Equivocal results must be less than 5%.',font_size=15),unsafe_allow_html=True)
    st_write(f1,10)
    f2.plotly_chart(generate_pie_chart_for_cmv_analytics(data[1]))
            

    st_write(st,4)


with st.container(): # third section
    st.divider()
    st.markdown(generate_markdown(text='Controls',font_color='black',font_size=60), unsafe_allow_html=True)
    st.markdown(generate_markdown(text='Note: Optimized Observed OD value (approximately) for: <br> Positive control: 2.0 OD value<br>\
                                         Negative control: 0.18 OD value <br>      Blank control: 0.18 OD value <br>     Blank Swab control: 0.18 OD value<br>\
                                  Instrument: Spectramax ABS (Molecular Devices).',font_size=14),unsafe_allow_html=True)
    st_write(st,2)
    tab1,tab2,tab3,tab4 = st.tabs(['Positive','Negative','Blank','Blank Swab'])
    for i,j in zip([tab1,tab2,tab3,tab4],[2,3,4,5]):
        s1,s2 = i.columns(2)
        with i:
            s1.table(style_remaining_control_table(data[j]))
        
        st_write(s2,2)
        s2.markdown(generate_markdown(text='Average OD Value',font_color='black',font_size=40), unsafe_allow_html=True)
        s2.markdown(generate_markdown(text=round(data[j]['Observed OD Value'].mean(),3),font_size=110), unsafe_allow_html=True)
        s2.plotly_chart(generate_box_plot_chart_for_cmv_analytics(data[j]),use_container_width=True)

st.write('')
buttons2 = st.columns([5,0.5,0.5,5])
buttons2[1].page_link("pages/1_Pre_PCR_High_Volume.py", label="Prev", icon="⏮️", disabled = st.session_state['Pre PCR (High Vol) status'])
buttons2[2].page_link("pages/3_Pre_PCR_Low_Volume.py", label="Next", icon="⏭️", disabled = st.session_state['Pre PCR (Low Vol) status'])