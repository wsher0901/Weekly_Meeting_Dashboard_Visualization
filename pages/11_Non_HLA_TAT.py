from pytz import timezone
import streamlit as st 
from Functions.Visualization.Non_HLA_TAT_Visualization import generate_sample_statistics, generate_shipment_statistics, make_timeline, make_comment
from Functions.Visualization.utility import generate_markdown, st_write, generate_header
from Files.common_list import nonhla_gene_list
st.set_page_config(page_title="Non-HLA TAT Visualization", layout="wide",initial_sidebar_state='collapsed')
st.markdown("""
        <style>
               .block-container {
                    padding-top: 2rem;
                }
        </style>
        """, unsafe_allow_html=True)

tz = timezone('EST')
st.logo('Histogenetics_Logo.png')
df = st.session_state['Non-HLA TAT']

generate_header(title='Non-HLA TAT Status',
                prev="pages/10_HLA_TAT.py",
                next="pages/12_New_Allele.py",
                status_prev='HLA TAT status',
                status_next='New Allele status')


for i in df:
    st.write(generate_markdown(text=i, font_size=60,font_color='black'), unsafe_allow_html=True)
    tab1,tab2,tab3,tab4 = st.tabs(['By Sample','By Shipment','Timeline','Comments'])
    generate_sample_statistics(df[i],'TAT',tab1)
    generate_shipment_statistics(df[i],tab2)
    g1,g2,g3,g4 = tab3.columns(4)
    switch = g3.toggle('Show Only Delay',key=i,value=True)
    tab3.plotly_chart(make_timeline(df[i],st.session_state.lw,st.session_state.tw,switch,'TAT' if i != 'Final Due' else 'Final Due'),use_container_width=True)
    st_write(tab4,6)
    if i != 'Final Due':
        tab4.table(make_comment(df[i],'TAT'))
        st_write(tab4,4)
    else:
        tab4.table(make_comment(df[i],'Final Due'))
        st_write(tab4,4)
    st_write(st,4)

st.divider()
gene_with_no_deadline = ', '.join(sorted(list(set(nonhla_gene_list+['Final Due']).difference(set(df))), key=lambda x: (nonhla_gene_list+['Final Due']).index(x)))
st.markdown(f"<h1 style='text-align: center;font-size: 20px;font-family: Arial;color: #f9423a;padding-bottom: 0;'>*{gene_with_no_deadline} are genes for which there was no deadline during this period.</h1>", unsafe_allow_html=True)
st.divider()
st.write('')
buttons2 = st.columns([5,0.5,0.5,5])
buttons2[1].page_link("pages/10_HLA_TAT.py", label="Prev", icon="⏮️", disabled = st.session_state['HLA TAT status'])
buttons2[2].page_link("pages/12_New_Allele.py", label="Next", icon="⏭️", disabled = st.session_state['New Allele status'])