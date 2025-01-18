from pytz import timezone
import streamlit as st 
from Functions.Visualization.utility import st_write, generate_markdown, generate_header
st.set_page_config(page_title="HLA TAT Visualization", layout="wide",initial_sidebar_state='collapsed')
st.markdown("""
        <style>
               .block-container {
                    padding-top: 2rem;
                }
        </style>
        """, unsafe_allow_html=True)

# Data 
tz = timezone('EST')
st.logo('MyLogo.png')

generate_header(title='New Allele',
                prev="sections/9_HLA_TAT.py",
                status_prev='HLA TAT status')

st.write(generate_markdown('Due to the intricacy of gene sequence data, I have decided to show demo instead of actual functionalities.', font_size=20,font_color='black'), unsafe_allow_html=True)
st.write(generate_markdown('Demo will done using a video and several screenshots.', font_size=20,font_color='black'), unsafe_allow_html=True)
st.divider()
demo1 = open('New_Allele_Demo/Demo_1.mp4','rb')
demo1_bytes = demo1.read()
demo2 = open('New_Allele_Demo/Demo_2.mp4','rb')
demo2_bytes = demo2.read()

st.write(generate_markdown('Demo Video', font_size=60,font_color='black'), unsafe_allow_html=True)
tab1,tab2 = st.tabs(['Part 1','Part 2'])
with tab1:
    tab1.write()
    tab1.video(demo1_bytes)

with tab2:
    tab2.write()
    tab2.video(demo2_bytes)

st.write(generate_markdown('Screenshots', font_size=60,font_color='black'), unsafe_allow_html=True)
with st.container():
    col1,col2 = st.columns([2,5])
    col1.write(generate_markdown('This interactive graph displays A gene from HLA gene. Within A gene, there are several locus. The visualization depicts genetic mutations on specific nucleotides on specific locus.', font_size=20,font_color='black'), unsafe_allow_html=True)
    col2.image('New_Allele_Demo/Gene_Wise.png',use_container_width=True)

with st.container():
    col1,col2 = st.columns([2,5])
    col1.write(generate_markdown('This is a zoomed in version. From A gene, it focuses on Intron 5 locus. In locus 5, each bar represents a nucleotide, and the color represents the type of mutations.', font_size=20,font_color='black'), unsafe_allow_html=True)
    col2.image('New_Allele_Demo/Locus_Wise.png',use_container_width=True)

with st.container():
    col1,col2 = st.columns([2,5])
    col1.write(generate_markdown('This visualization zooms in further, enabling analysis on nucleotide-level. You can see how each nucleotide changed according to their mutations.', font_size=20,font_color='black'), unsafe_allow_html=True)
    col2.image('New_Allele_Demo/Amino_Acid_Wise.png',use_container_width=True)

with st.container():
    col1,col2 = st.columns([2,3])
    st_write(col2,14)
    col2.write(generate_markdown("Using this sidebar, you can navigate through multiple samples and their genes and specific locus.", font_size=30,font_color='black'), unsafe_allow_html=True)
    col1.image('New_Allele_Demo/Sidebar.png',width=300)

with st.container():
    col1,col2 = st.columns([2,5])
    st_write(col1,14)
    col1.write(generate_markdown('*Wholistic View', font_size=40,font_color='black'), unsafe_allow_html=True)
    col2.image('New_Allele_Demo/Big_Picture.png',use_container_width=True)