import streamlit as st

pages = {
    'Main':[
        st.Page('Intro.py',title='Introduction'),
        st.Page('Homepage.py',title='Homepage')
    ],
    "Pre PCR": [
        st.Page("pages/1_Pre_PCR_High_Volume.py", title="High Volume"),
        st.Page("pages/2_Pre_PCR_CMV.py", title="CMV"),
        st.Page("pages/3_Pre_PCR_Low_Volume.py",title='Low Volume')
    ],
    "Intermediate": [
        st.Page("pages/4_PCR.py", title="PCR"),
        st.Page("pages/5_Gel.py", title="Gel"),
        st.Page("pages/6_Illumina.py",title='Illumina'),
        st.Page("pages/7_Pacbio.py",title='Pacbio')
    ],
    "Repeats":[
        st.Page("pages/8_Repeats.py",title='Repeats')
    ],
    'Turn Around Time':[
        st.Page("pages/10_HLA_TAT.py",title='HLA'),
        st.Page("pages/11_Non_HLA_TAT.py",title='Non-HLA')
    ],
    'New Allele':[
        st.Page("pages/12_New_Allele.py", title='New Allele')
    ]
}

pg = st.navigation(pages)
pg.run()

