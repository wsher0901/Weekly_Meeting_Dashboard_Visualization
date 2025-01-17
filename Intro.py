import streamlit as st 
st.set_page_config(page_title="HistoDash", layout="wide",initial_sidebar_state='collapsed')
st.markdown("""
        <style>
               .block-container {
                    padding-top: 2rem;
                }
        </style>
        """, unsafe_allow_html=True)




one,two,three = st.container().columns([1,2,1])
two.image('MyLogo.png',width=1200)
col1,col2,col3 = st.container().columns(3)
col1.markdown(f"<h1 style='text-align: center;font-size: 60px;font-family: Calibri;color: #f9423a;padding-bottom: 0;'>Purpose</h1>", unsafe_allow_html=True)
col1.markdown(f"<h1 style='text-align: center;font-size: 20px;font-family: Calibri;color: black;padding-bottom: 0;'>This is a comprehensive dashboard I have created during my tenure at Histogenetics LLC.</h1>", unsafe_allow_html=True)
col1.markdown(f"<h1 style='text-align: center;font-size: 16px;font-family: Calibri;color: black;padding-bottom: 0;'>*For security, data has been replaced by randomly generated data.</h1>", unsafe_allow_html=True)
col2.write()
col2.write()
col2.markdown(f"<h1 style='text-align: center;font-size: 60px;font-family: Calibri;color: #f9423a;padding-bottom: 0;'>Objective</h1>", unsafe_allow_html=True)
col2.markdown(f"<h1 style='text-align: center;font-size: 20px;font-family: Calibri;color: black;padding-bottom: 0;'>The objective was to reduce weekly meeting duration and improve our data-driven decision making process by switching from spreadsheets to data visualization.</h1>", unsafe_allow_html=True)
col2.write()
col2.write()
col3.markdown(f"<h1 style='text-align: center;font-size: 60px;font-family: Calibri;color: #f9423a;padding-bottom: 0;'>Usage</h1>", unsafe_allow_html=True)
col3.markdown(f"<h1 style='text-align: center;font-size: 20px;font-family: Calibri;color: black;padding-bottom: 0;'>1. Navigate to homepage using the sidebar.</h1>", unsafe_allow_html=True)
col3.markdown(f"<h1 style='text-align: center;font-size: 20px;font-family: Calibri;color: black;padding-bottom: 0;'>2. Click desired department using the widget.</h1>", unsafe_allow_html=True)
col3.markdown(f"<h1 style='text-align: center;font-size: 20px;font-family: Calibri;color: black;padding-bottom: 0;'>3. Press Enter and wait for the data to load.</h1>", unsafe_allow_html=True)
col3.markdown(f"<h1 style='text-align: center;font-size: 20px;font-family: Calibri;color: black;padding-bottom: 0;'>4. When data is loaded, navigate to view the visualization.</h1>", unsafe_allow_html=True)
