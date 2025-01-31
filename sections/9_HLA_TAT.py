from pytz import timezone
import streamlit as st 
from Functions.Visualization.HLA_TAT_Visualization import generate_sample_statistics, generate_shipment_statistics, make_timeline, make_comment, traffic_light
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
df = st.session_state['HLA TAT']
df_nc = df[df.Type == 'Non-Clinical']
df_c = df[df.Type == 'Clinical']

generate_header(title='HLA TAT Status',
                prev="sections/8_Repeats.py",
                next="sections/10_New_Allele.py",
                status_prev='Repeats status',
                status_next='New Allele status')

# Non-Clinical
st.write(generate_markdown('Non-Clinical', font_size=60,font_color='black'), unsafe_allow_html=True)
traffic_light(df_nc,'Non-Clinical',st)
tab1, tab2, tab3, tab4, tab5 = st.tabs(['C1 Sample','C2 Sample','Shipment','Timeline','Comments'])
generate_sample_statistics(tab1,df_nc,True,True)
generate_sample_statistics(tab2,df_nc,True,False)
generate_shipment_statistics(tab3,df_nc)
g1,g2,g3,g4 = tab4.columns(4)
nc_switch = g3.toggle('Show Only Delay',key=1,value=True)
tab4.plotly_chart(make_timeline(df_nc,nc_switch, True),use_container_width=True)
st_write(tab5,5)
tab5.table(make_comment(df_nc,True))
st_write(tab5,10)


# Clinical
st.write(generate_markdown('Clinical', font_size=60,font_color='black'), unsafe_allow_html=True)
traffic_light(df_c,'Clinical',st)
tab6, tab7, tab8, tab9, tab10 = st.tabs(['C1 Sample','C2 Sample','Shipment','Timeline','Comments'])
generate_sample_statistics(tab6,df_c,True,True)
generate_sample_statistics(tab7,df_c,True,False)
generate_shipment_statistics(tab8,df_c)
g5,g6,g7,g8 = tab9.columns(4)
c_switch = g7.toggle('Show Only Delay',key=2,value=True)
tab9.plotly_chart(make_timeline(df_c,c_switch, True),use_container_width=True)
st_write(tab10,5)
tab10.table(make_comment(df_c,True))
st_write(tab10,10)

st.divider()
st.write('')
buttons2 = st.columns([5,0.5,0.5,5])
buttons2[1].page_link("sections/8_Repeats.py", label='Prev', icon='⏮️', disabled = st.session_state['Repeats status'])
buttons2[2].page_link("sections/10_New_Allele.py", label="Next", icon="⏭️", disabled = st.session_state['New Allele status'])