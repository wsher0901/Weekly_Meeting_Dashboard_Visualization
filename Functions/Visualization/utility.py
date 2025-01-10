import streamlit as st 

def st_write(loc,x):
    for _ in range(x):
        loc.write('')

def generate_markdown(text,text_align='center', font_size=100, font='Arial', font_color='#f9423a'):
    return f"<h1 style='text-align: {text_align};font-size: {font_size}px;font-family: {font};color: {font_color};padding-bottom: 0;'>{text}</h1>"

def remove_columns(df,args):
    return df.drop(args,axis=1)

def generate_header(**kwargs):
    with st.container():
        st.container().markdown(generate_markdown(text=kwargs['title']), unsafe_allow_html=True)
        st.container().markdown(generate_markdown(font_size=40,text=st.session_state.lw.strftime('%m/%d/%y')+' ~ '+st.session_state.tw.strftime('%m/%d/%y')), unsafe_allow_html=True)
        st_write(st.container(),2)
        buttons = st.container().columns([4.5,0.6,0.5,5])

        if 'prev' in kwargs:
            buttons[1].page_link(kwargs['prev'], label='Prev', icon="⏮️",disabled = st.session_state[kwargs['status_prev']])

        if 'next' in kwargs:
            buttons[2].page_link(kwargs['next'], label='Next', icon='⏭️', disabled = st.session_state[kwargs['status_next']])
        st.container().divider()