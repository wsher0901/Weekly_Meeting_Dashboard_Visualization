from pytz import timezone
import streamlit as st 
from Functions.Visualization.High_Volume_Visualization import generate_bar_chart_by_test, generate_bar_chart_by_client, \
    style_samplewise_table, generate_map, generate_pie_chart_by_country, generate_bar_chart_for_extraction, style_extraction_table
from Functions.Visualization.utility import st_write, generate_markdown, generate_header
st.set_page_config(page_title="High Volume Pre-PCR", layout="wide",initial_sidebar_state='collapsed')
st.markdown("""
        <style>
               .block-container {
                    padding-top: 2rem;
                }
        </style>
        """, unsafe_allow_html=True)

tz = timezone('EST')
st.logo('MyLogo.png')
gene_order = ['HLA','ABO-RH','CCR','CMV','DNA Extraction','ENGRAFTMENT','Illumina','KIR','Micro array','Nanopore','Non-Classical','Optical','PacBio','PGX','Whole Genome']
table1, table2, table3 = st.session_state['Pre PCR (High Vol)']

generate_header(title= 'Pre-PCR (High Volume)', next= 'sections/2_Pre_PCR_CMV.py', status_next='Pre PCR (CMV) status')


with st.container(): # first section
    st.write(generate_markdown('Sample-wise Statistics', font_size=60,font_color='black'), unsafe_allow_html=True)
    st_write(st,1)
    tab1,tab2 = st.tabs(['New','Rerequest'])
    for ind,tab in enumerate([tab1,tab2]):
        f1,f2 = tab.columns([6,5],border=True)
        f1.plotly_chart(generate_bar_chart_by_test(table1,ind),key='f1'+str(ind))
        f2.plotly_chart(generate_bar_chart_by_client(table1,ind),key='f2'+str(ind))
    st.expander('Sample-wise Statistics for Non-clinical').table(style_samplewise_table(table1))
    st_write(st,5)


with st.container(): # second section
    st.write(generate_markdown('By Country', font_size=60,font_color='black'), unsafe_allow_html=True)
    f1,f2 = st.columns([6,4])
    f1.plotly_chart(generate_map(table1),use_container_width=True)
    f2.plotly_chart(generate_pie_chart_by_country(table1),use_container_width=True)


with st.container(): # fourth section
    st.write(generate_markdown('DNA Extraction', font_size=60,font_color='black'), unsafe_allow_html=True)
    st_write(st,4)
    f1,f2 = st.columns([3,5],border=True)
    st_write(f1,3)
    f1.write(generate_markdown('Extracted DNA', font_size=40,font_color='#f9423a'), unsafe_allow_html=True)
    f1.write(generate_markdown(table3[table3.Type == 'Genomic DNA']['Sample Count'].iloc[0], font_size=120,font_color='black'), unsafe_allow_html=True)
    st_write(f1,13)
    f1.write(generate_markdown('Diluted DNA', font_size=40,font_color='#f9423a'), unsafe_allow_html=True)
    f1.write(generate_markdown(table3[table3.Type == 'Client DNA']['Sample Count'].iloc[0], font_size=120,font_color='black'), unsafe_allow_html=True)
    f2.plotly_chart(generate_bar_chart_for_extraction(table2,'Genomic DNA'),use_container_width=True)
    f2.plotly_chart(generate_bar_chart_for_extraction(table2,'Client DNA'),use_container_width=True)
    st.expander('DNA Extraction Statistics').table(style_extraction_table(table2))

    
with st.container(border=True): # Comment
    font_size = 20
    if 'Pre PCR (High Vol)' + ' image' in st.session_state and 'Pre PCR (High Vol)' + ' comment' in st.session_state:
        comment_image, comment_text = st.columns(2)
    elif 'Pre PCR (High Vol)' + ' image' in st.session_state and 'Pre PCR (High Vol)' + ' comment' not in st.session_state:
        comment_image = st.container()
    elif 'Pre PCR (High Vol)' + ' image' not in st.session_state and 'Pre PCR (High Vol)' + ' comment' in st.session_state:
        comment_text = st.container()
        font_size=60
    if 'Pre PCR (High Vol)' + ' image' in st.session_state:
        image_tab = ['Comment '+str(i) for i in range(1,len(st.session_state['Pre PCR (High Vol) image'])+1,1)]
        tab_list = ['Comment '+str(i) for i in range(1,len(st.session_state['Pre PCR (High Vol) image'])+1,1)]
        tab_list = comment_image.tabs(image_tab)
        for ind,i in enumerate(tab_list):
            i.image(st.session_state['Pre PCR (High Vol)' + ' image'][ind],width=800)

    if 'Pre PCR (High Vol)' + ' comment' in st.session_state:
        if font_size == 20:
            st_write(comment_text,14)
        comment_text.markdown(f"<h1 style='text-align: center;font-size: {font_size}px;font-family: Arial;'>{st.session_state['Pre PCR (High Vol)' + ' comment']}</h1>", unsafe_allow_html=True)

st.write('')
buttons2 = st.columns([5,0.5,0.5,5])
buttons2[2].page_link("sections/2_Pre_PCR_CMV.py", label="Next", icon="⏭️", disabled = st.session_state['Pre PCR (CMV) status'])