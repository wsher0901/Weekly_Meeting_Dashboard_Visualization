import streamlit as st 
from Functions.Summary.Function import st_write, pre_pcr_high_chart, pre_pcr_low_chart, pcr_chart, illumina_chart, pacbio_chart, reagent_chart, repeat_chart, new_allele_chart
first = st.container()
f1,f2,f3 = first.columns(3)
f_1 = f1.container(border=True,height=400)
f_2 = f2.container(border=True,height=400)
f_3 = f3.container(border=True,height=400)
if 'Pre PCR (High Vol)' in st.session_state:
    try:
        f_1.plotly_chart(pre_pcr_high_chart(st.session_state['Pre PCR (High Vol)'][0],
                                            st.session_state['Pre PCR (High Vol)'][2],
                                            st.session_state['Pre PCR (High Vol)'][3]),use_container_width=True)
    except:
        f_1.markdown(f"<h1 style='text-align: center;font-size: 25px;font-family: Arial;color: white;padding-bottom: 0;padding-top:1px;'>Pre PCR High Volume</h1>", unsafe_allow_html=True)
        st_write(f_1,5)
        f_1.markdown(f"<h1 style='text-align: center;font-size: 100px;font-family: Arial;color: #e9ff32;padding-bottom: 0;'>No Data.</h1>", unsafe_allow_html=True)
else:
    f_1.markdown(f"<h1 style='text-align: center;font-size: 25px;font-family: Arial;color: white;padding-bottom: 0;padding-top:1px;'>Pre PCR High Volume</h1>", unsafe_allow_html=True)
    st_write(f_1,5)
    f_1.markdown(f"<h1 style='text-align: center;font-size: 100px;font-family: Arial;color: #e9ff32;padding-bottom: 0;'>No Data</h1>", unsafe_allow_html=True)

if 'Pre PCR (Low Vol)' in st.session_state:
    try:
        f_2.plotly_chart(pre_pcr_low_chart(st.session_state['Pre PCR (Low Vol)'][1]),use_container_width=True)
    except:
        f_2.markdown(f"<h1 style='text-align: center;font-size: 25px;font-family: Arial;color: white;padding-bottom: 0;padding-top:1px;'>Pre PCR Low Volume</h1>", unsafe_allow_html=True)
        st_write(f_2,5)
        f_2.markdown(f"<h1 style='text-align: center;font-size: 100px;font-family: Arial;color: #e9ff32;padding-bottom: 0;'>No Data.</h1>", unsafe_allow_html=True)

else:
    f_2.markdown(f"<h1 style='text-align: center;font-size: 25px;font-family: Arial;color: white;padding-bottom: 0;padding-top:1px;'>Pre PCR Low Volume</h1>", unsafe_allow_html=True)
    st_write(f_2,5)
    f_2.markdown(f"<h1 style='text-align: center;font-size: 100px;font-family: Arial;color: #e9ff32;padding-bottom: 0;'>No Data</h1>", unsafe_allow_html=True)

if 'PCR' in st.session_state:
    try:
        f_3.plotly_chart(pcr_chart(st.session_state['PCR'],st.session_state.color,0.3),use_container_width=True)
    except:
        f_3.markdown(f"<h1 style='text-align: center;font-size: 25px;font-family: Arial;color: white;padding-bottom: 0;padding-top:1px;'>PCR</h1>", unsafe_allow_html=True)
        st_write(f_3,5)
        f_3.markdown(f"<h1 style='text-align: center;font-size: 100px;font-family: Arial;color: #e9ff32;padding-bottom: 0;'>No Data.</h1>", unsafe_allow_html=True)
else:
    f_3.markdown(f"<h1 style='text-align: center;font-size: 25px;font-family: Arial;color: white;padding-bottom: 0;padding-top:1px;'>PCR</h1>", unsafe_allow_html=True)
    st_write(f_3,5)
    f_3.markdown(f"<h1 style='text-align: center;font-size: 100px;font-family: Arial;color: #e9ff32;padding-bottom: 0;'>No Data</h1>", unsafe_allow_html=True)

second = st.container()
s1,s2,s3 = second.columns(3)
s_1 = s1.container(border=True,height=400)
s_2 = s2.container(border=True,height=400)
s_3 = s3.container(border=True,height=400)
if 'Illumina' in st.session_state:  
    try:
        s_1.plotly_chart(illumina_chart(st.session_state['Illumina'][1], st.session_state.color[6:], 0.7),use_container_width=True)
    except:
        s_1.markdown(f"<h1 style='text-align: center;font-size: 25px;font-family: Arial;color: white;padding-bottom: 0;padding-top:1px;'>Illumina</h1>", unsafe_allow_html=True)
        st_write(s_1,5)
        s_1.markdown(f"<h1 style='text-align: center;font-size: 100px;font-family: Arial;color: #e9ff32;padding-bottom: 0;'>No Data.</h1>", unsafe_allow_html=True)
else:
    s_1.markdown(f"<h1 style='text-align: center;font-size: 25px;font-family: Arial;color: white;padding-bottom: 0;padding-top:1px;'>Illumina</h1>", unsafe_allow_html=True)
    st_write(s_1,5)
    s_1.markdown(f"<h1 style='text-align: center;font-size: 100px;font-family: Arial;color: #e9ff32;padding-bottom: 0;'>No Data</h1>", unsafe_allow_html=True)

if 'Pacbio' in st.session_state:
    try:
        s_2.plotly_chart(pacbio_chart(st.session_state['Pacbio'][1],st.session_state.color,0.4),use_container_width=True)
    except:
        s_2.markdown(f"<h1 style='text-align: center;font-size: 25px;font-family: Arial;color: white;padding-bottom: 0;padding-top:1px;'>Pacbio</h1>", unsafe_allow_html=True)
        st_write(s_2,5)
        s_2.markdown(f"<h1 style='text-align: center;font-size: 100px;font-family: Arial;color: #e9ff32;padding-bottom: 0;'>No Data.</h1>", unsafe_allow_html=True)
else:
    s_2.markdown(f"<h1 style='text-align: center;font-size: 25px;font-family: Arial;color: white;padding-bottom: 0;padding-top:1px;'>Pacbio</h1>", unsafe_allow_html=True)
    st_write(s_2,5)
    s_2.markdown(f"<h1 style='text-align: center;font-size: 100px;font-family: Arial;color: #e9ff32;padding-bottom: 0;'>No Data</h1>", unsafe_allow_html=True)

if 'Reagents' in st.session_state:
    try:
        s_3.plotly_chart(reagent_chart(st.session_state['Reagents'][0],st.session_state.color[3:],0.40),use_container_width=True)
    except:
        s_3.markdown(f"<h1 style='text-align: center;font-size: 25px;font-family: Arial;color: white;padding-bottom: 0;padding-top:1px;'>Reagents</h1>", unsafe_allow_html=True)
        st_write(s_3,5)
        s_3.markdown(f"<h1 style='text-align: center;font-size: 100px;font-family: Arial;color: #e9ff32;padding-bottom: 0;'>No Data.</h1>", unsafe_allow_html=True)
else:
    s_3.markdown(f"<h1 style='text-align: center;font-size: 25px;font-family: Arial;color: white;padding-bottom: 0;padding-top:1px;'>Reagents</h1>", unsafe_allow_html=True)
    st_write(s_3,5)
    s_3.markdown(f"<h1 style='text-align: center;font-size: 100px;font-family: Arial;color: #e9ff32;padding-bottom: 0;'>No Data</h1>", unsafe_allow_html=True)

third = st.container()
t1,t2,t3 = third.columns(3)
t_1 = t1.container(border=True,height=400)
t_2 = t2.container(border=True,height=400)
t_3 = t3.container(border=True,height=400)
if 'Repeats' in st.session_state:   
    try:
        t_1.plotly_chart(repeat_chart(st.session_state['Repeats'],'NGS'),use_container_width=True)
    except:
        t_1.markdown(f"<h1 style='text-align: center;font-size: 25px;font-family: Arial;color: white;padding-bottom: 0;padding-top:1px;'>Repeats</h1>", unsafe_allow_html=True)
        st_write(t_1,5)
        t_1.markdown(f"<h1 style='text-align: center;font-size: 100px;font-family: Arial;color: #e9ff32;padding-bottom: 0;'>No Data.</h1>", unsafe_allow_html=True)
    try:
        t_2.plotly_chart(repeat_chart(st.session_state['Repeats'],'Pacbio'),use_container_width=True)
    except:
        t_2.markdown(f"<h1 style='text-align: center;font-size: 25px;font-family: Arial;color: white;padding-bottom: 0;padding-top:1px;'>Repeats</h1>", unsafe_allow_html=True)
        st_write(t_2,5)
        t_2.markdown(f"<h1 style='text-align: center;font-size: 100px;font-family: Arial;color: #e9ff32;padding-bottom: 0;'>No Data.</h1>", unsafe_allow_html=True)
else:
    t_1.markdown(f"<h1 style='text-align: center;font-size: 25px;font-family: Arial;color: white;padding-bottom: 0;padding-top:1px;'>Repeats</h1>", unsafe_allow_html=True)
    st_write(t_1,5)
    t_1.markdown(f"<h1 style='text-align: center;font-size: 100px;font-family: Arial;color: #e9ff32;padding-bottom: 0;'>No Data</h1>", unsafe_allow_html=True)
    t_2.markdown(f"<h1 style='text-align: center;font-size: 25px;font-family: Arial;color: white;padding-bottom: 0;padding-top:1px;'>Repeats</h1>", unsafe_allow_html=True)
    st_write(t_2,5)
    t_2.markdown(f"<h1 style='text-align: center;font-size: 100px;font-family: Arial;color: #e9ff32;padding-bottom: 0;'>No Data</h1>", unsafe_allow_html=True)

if 'New Allele' in st.session_state:
    try:
        t_3.plotly_chart(new_allele_chart(st.session_state['New Allele'][2][0]),use_container_width=True)
    except:
        t_3.markdown(f"<h1 style='text-align: center;font-size: 25px;font-family: Arial;color: white;padding-bottom: 0;padding-top:1px;'>New Allele</h1>", unsafe_allow_html=True)
        st_write(t_3,5)
        t_3.markdown(f"<h1 style='text-align: center;font-size: 100px;font-family: Arial;color: #e9ff32;padding-bottom: 0;'>No Data.</h1>", unsafe_allow_html=True)
else:
    t_3.markdown(f"<h1 style='text-align: center;font-size: 25px;font-family: Arial;color: white;padding-bottom: 0;padding-top:1px;'>New Allele</h1>", unsafe_allow_html=True)
    st_write(t_3,5)
    t_3.markdown(f"<h1 style='text-align: center;font-size: 100px;font-family: Arial;color: #e9ff32;padding-bottom: 0;'>No Data</h1>", unsafe_allow_html=True)