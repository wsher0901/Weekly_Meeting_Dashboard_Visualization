import streamlit as st

pages = {
    'Main':[
        st.Page('Intro.py',title='Introduction'),
        st.Page('Homepage.py',title='Homepage')
    ],
    "Pre PCR": [
        st.Page("sections/1_Pre_PCR_High_Volume.py", title="High Volume"),
        st.Page("sections/2_Pre_PCR_CMV.py", title="CMV"),
        st.Page("sections/3_Pre_PCR_Low_Volume.py",title='Low Volume')
    ],
    "Intermediate": [
        st.Page("sections/4_PCR.py", title="PCR"),
        st.Page("sections/5_Gel.py", title="Gel"),
        st.Page("sections/6_Illumina.py",title='Illumina'),
        st.Page("sections/7_Pacbio.py",title='Pacbio')
    ],
    "Repeats":[
        st.Page("sections/8_Repeats.py",title='Repeats')
    ],
    'Turn Around Time':[
        st.Page("sections/9_HLA_TAT.py",title='HLA')
    ],
    'New Allele':[
        st.Page("sections/10_New_Allele.py", title='New Allele')
    ]
}

pg = st.navigation(pages)
pg.run()

