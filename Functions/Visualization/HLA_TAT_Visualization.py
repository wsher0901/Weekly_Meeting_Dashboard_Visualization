import pandas as pd
import streamlit as st
import plotly.express as px 
import plotly.graph_objects as go
from Functions.Visualization.utility import st_write, generate_markdown
from Files.common_list import delay_status_color_code, comment_color_code

def traffic_light(data,type,loc):
    shipment_threshold = 30
    sample_threshold = 35
    if type == 'Clinical':
        shipment_threshold = 10
        sample_threshold = 20
    elif type == 'Final':
        shipment_threshold = 15
        sample_threshold = 32

    shipment = len(data[~data['Comment Category'].isin(['','Extended','Hold Report'])])/len(data)*100
    c1 = 100 - (data.C1ReportWithinTATCount.sum() / data['C1 Requested'].sum() * 100)
    c2 = 100 - (data.C2ReportWithinTATCount.sum() / data['C2 Requested'].sum() * 100)
    if shipment < shipment_threshold:
        loc.success('No Issue',icon='🟢')
    else:
        if c1 < sample_threshold and c2 < sample_threshold:
            loc.success('No Issue',icon='🟢')
        else:
            if c1 < 50 and c2 < 50:
                loc.warning('Minor Issue',icon='🟠')
            else:
                loc.error('Anomaly',icon='🔴')

def generate_sample_statistics(loc,df,by_TAT,C1):
    arg1, arg2 = '', 'C1 Requested'
    if by_TAT:
        if C1:
            arg1 = 'C1ReportWithinTATCount'
        else: 
            arg1 = 'C2ReportWithinTATCount'
            arg2 = 'C2 Requested'
    else:
        if C1:
            arg1 = 'C1ReportWithinFinalCount'
        else:
            arg1 = 'C2ReportWithinFinalCount'
            arg2 = 'C2 Requested'

    total = df[arg2].sum()

    delay = df[(df['Delay Status'] == 'Delayed') & (~df['Comment Category'].isin(['Hold Report','Extended']))][arg2].sum() - df[(df['Delay Status'] == 'Delayed') & (~df['Comment Category'].isin(['Hold Report','Extended']))][arg1].sum()

    completed = df[(df['Delay Status'] == 'Completed') & (~df['Comment Category'].isin(['Hold Report','Extended']))][arg2].sum() + df[(df['Delay Status'] == 'Delayed') & (~df['Comment Category'].isin(['Hold Report','Extended']))][arg1].sum()

    hold = df[df['Comment Category'].isin(['Hold Report','Extended'])][arg2].sum()
 
    modified_df = pd.DataFrame([[completed,'Completed'],[delay,'Delayed'],[hold,'Hold Report']],columns=['Count','Delay Status'])
    modified_df = modified_df[modified_df['Count'] != 0]

    pie = go.Figure(data=[go.Pie(labels=modified_df['Delay Status'].unique(),
                                 values=modified_df['Count'],
                                 textinfo='label+percent',
                                 insidetextorientation='horizontal',
                                 textposition='auto',
                                 domain=dict(x=[0.3,0.99]))])
    
    pie.update_layout(hovermode=False,
                      width=600,
                      height=600,
                      showlegend=False,
                      legend=dict(yanchor='top',
                                  xanchor='right',
                                  font=dict(size=20),
                                  orientation='h',
                                  x=0.8,
                                  y=-0.1,
                                  title=''))
    
    pie.update_traces(textfont_size=28,
                      marker=dict(colors=[delay_status_color_code[label] for label in modified_df['Delay Status'].unique()],
                                  line=dict(color='#000000', width=4)))
    
    col1,col2,graph = loc.columns([3.5,3.5,6],border=True)

    st_write(col1,7)
    col1.write(generate_markdown(text='C1 Request',font_size=25,font_color='#f9423a'), unsafe_allow_html=True)
    col1.write(generate_markdown(text=total,font_size=100,font_color='black'), unsafe_allow_html=True)
    col1.write(generate_markdown(text='C1 Delayed',font_size=25,font_color='#f9423a'), unsafe_allow_html=True)
    col1.write(generate_markdown(text=delay,font_size=100,font_color='black'), unsafe_allow_html=True)

    st_write(col2,7)
    col2.write(generate_markdown(text='C1 Completed',font_size=25,font_color='#f9423a'), unsafe_allow_html=True)
    col2.write(generate_markdown(text=completed,font_size=100,font_color='black'), unsafe_allow_html=True)
    col2.write(generate_markdown(text='C1 Ext/Hold',font_size=25,font_color='#f9423a'), unsafe_allow_html=True)
    col2.write(generate_markdown(text=hold,font_size=100,font_color='black'), unsafe_allow_html=True)

    graph.plotly_chart(pie,use_container_width=True,key=arg1+arg2+str(loc))

def generate_shipment_statistics(loc,df):
    col1,col2,graph = loc.columns([3.5,3.5,6],border=True)

    modified_df = pd.DataFrame([[len(df[df['Delay Status'] == 'Completed']),'Completed'],
                                [len(df[(df['Delay Status'] == 'Delayed') & (df['Comment Category'] != 'Extended') & (df['Comment Category'] != 'Hold Report')]),'Delayed'],
                                [len(df[(df['Delay Status'] == 'Delayed') & (df['Comment Category'] == 'Extended') | (df['Comment Category'] == 'Hold Report')]),'Hold Report']]
                                ,columns=['Count','Delay Status'])
    modified_df = modified_df[modified_df['Count'] != 0]

    pie = go.Figure(data=[go.Pie(labels=modified_df['Delay Status'],
                                 values=modified_df['Count'],
                                 textinfo='label+percent',
                                 insidetextorientation='horizontal',
                                 domain=dict(x=[0.3,0.99]))])
    
    pie.update_layout(hovermode=False,
                      width=600,
                      height=600,
                      showlegend=False,
                      legend=dict(yanchor='top',
                                  xanchor='right',
                                  font=dict(size=20),
                                  orientation='h',
                                  x=0.9,
                                  y=-0.1,
                                  title=''))
    
    pie.update_traces(textfont_size=28,
                      marker=dict(colors=[delay_status_color_code[label] for label in modified_df['Delay Status'].unique()],
                                  line=dict(color='#000000', width=4)))
    
    st_write(col1,6)
    col1.write(generate_markdown(text='Shipment',font_size=25,font_color='#f9423a'), unsafe_allow_html=True)
    col1.write(generate_markdown(text=len(df),font_size=120,font_color='black'), unsafe_allow_html=True)
    col1.write(generate_markdown(text='Delayed',font_size=25,font_color='#f9423a'), unsafe_allow_html=True)
    if len(df[(df['Delay Status'] == 'Delayed') & (df['Comment Category'] != 'Extended') & (df['Comment Category'] != 'Hold Report')]) != 0:
        col1.write(generate_markdown(text=len(df[(df['Delay Status'] == 'Delayed') & (df['Comment Category'] != 'Extended') & (df['Comment Category'] != 'Hold Report')]),font_size=120,font_color='black'), unsafe_allow_html=True)
    else:
        col1.write(generate_markdown(text=0,font_size=120,font_color='black'), unsafe_allow_html=True)
    
    st_write(col2,6)
    col2.write(generate_markdown(text='Completed',font_size=25,font_color='#f9423a'), unsafe_allow_html=True)
    if len(df[df['Delay Status'] == 'Completed']) != 0:
        col2.write(generate_markdown(text=len(df[df['Delay Status'] == 'Completed']),font_size=120,font_color='black'), unsafe_allow_html=True)
    else:
        col2.write(generate_markdown(text=0,font_size=120,font_color='black'), unsafe_allow_html=True)

    col2.write(generate_markdown(text='Ext / Hold',font_size=25,font_color='#f9423a'), unsafe_allow_html=True)
    if len(df[(df['Delay Status'] == 'Delayed') & (df['Comment Category'] == 'Extended') | (df['Comment Category'] == 'Hold Report')]) != 0:
        col2.write(generate_markdown(text=len(df[(df['Delay Status'] == 'Delayed') & (df['Comment Category'] == 'Extended') | (df['Comment Category'] == 'Hold Report')]),font_size=120,font_color='black'), unsafe_allow_html=True)
    else:
        col2.write(generate_markdown(text=0,font_size=120,font_color='black'), unsafe_allow_html=True)

    graph.plotly_chart(pie,use_container_width=True)

def make_timeline(df,switch, by_TAT):

    def set_height(df):
        length = len(df['Project Name'].unique())
        if length < 5:
            return 200, 24, 15
        elif length >= 5 and length < 10:
            return 400, 21, 9
        elif length >= 10 and length < 20:
            return 600, 18, 9
        elif length >= 20 and length < 30:
            return 900, 15, 8
        elif length >= 30 and length < 40:
            return 900, 12, 8
        else:
            return 1000, 12, 8

    text = 'By TAT' if by_TAT else 'By Final'
    due = 'Class I TAT' if by_TAT else 'Final Due'
    color = 'Comment Category' if switch else 'Delay Status'
    color_map = comment_color_code if switch else {'Completed':'#313695','Delayed':'#a50026','':'#0e1117'}
    textcolor= 'white'
    height, yaxis_size, textsize = set_height(df)

    timeline = px.timeline(df, x_start="Start", x_end="Finish", y='Project Name',height=height,color=color,color_discrete_map = color_map, text =text,
                           category_orders={'Project Name': sorted(df['Project Name'].unique(),reverse=True,key=lambda x: x.lower())},
                           custom_data=['Shipment Date',due,text,'By Today'],
                           hover_data={'Project Name':True,due:True,text:True,'By Today':True,'Start':False,'Finish':False,color:False,})
    
    timeline.update_xaxes(tickformat="%m/%d")
    timeline.update_yaxes(autorange="reversed")
    timeline.update_layout(font=dict(size=textsize,color='black'),
                           xaxis=dict(tickfont=dict(size=30,color='black')),
                           yaxis=dict(tickfont=dict(size=yaxis_size,color='black')),
                           legend=dict(font=dict(size=14),orientation='h',x=0,y=-0.25,title=''),
                           hoverlabel=dict(font_size=16))
    
    timeline.update_traces(textfont_color=textcolor,
                           hovertemplate="<br>".join(['%{y}','Shipment: %{customdata[0]}',
                                                      'Due: %{customdata[1]}',
                                                      'By TAT: %{customdata[2]}',
                                                      'By Today: %{customdata[3]}']))
    if not switch:
        timeline.update_traces(marker_line_color='black',
                                marker_line_width=1.5,)

    return timeline
 
def make_comment(df,by_TAT):
    
    def combine_comment(row):
        if row['ReportSubComments'] != None and row['ReportSubComments'] != '' and row['Comment'] != None and row['Comment'] != '':
            return str(row['ReportSubComments']) + '/' + str(row['Comment'])
        else:
            if row['ReportSubComments'] != None and row['ReportSubComments'] != '' and (row['Comment'] == None or row['Comment'] == ''):
                return row['ReportSubComments']
            elif (row['ReportSubComments'] == None or row['ReportSubComments'] == '') and row['Comment'] != None and row['Comment'] != '':
                return row.Comment
            else:
                return None

    due = 'Class I TAT' if by_TAT else 'Final Due'
    modified_df = df[(df['Delay Status'] != 'Completed') & (df['Comment Category'] != 'Extended')]
    modified_df['Comment'] = modified_df.apply(lambda row: combine_comment(row),axis=1)

    if by_TAT:
        modified_df = modified_df[['Comment Category','Project Name','Shipment Date',due,'Comment','C1 by TAT','C1% by TAT','C2 by TAT','C2% by TAT','C1 by Today','C1% by Today','C2 by Today','C2% by Today']]
    else:
        modified_df = modified_df[['Comment Category','Project Name','Shipment Date',due,'Comment','C1 by Final','C1% by Final','C2 by Final','C2% by Final','C1 by Today','C1% by Today','C2 by Today','C2% by Today']]

    modified_df = modified_df.sort_values(by=['Comment Category','Shipment Date']).reset_index(drop=True)
    modified_df.index += 1
    def add_color_by_type(row):
        if row['Comment Category'] in ['Hold Report','Others','Not Commented']:
            return ['background-color: ' + comment_color_code.get(row['Comment Category'], 'black')+';color: white'] + ['']*(len(row)-1)
        else:
            return ['background-color: ' + comment_color_code.get(row['Comment Category'], 'white')] + ['']*(len(row)-1)

    return modified_df.style.apply(add_color_by_type,axis=1).set_table_styles(
    [
        {'selector': 'th.col_heading', 'props': 'background-color: gray; color: white;'},
        {'selector': 'th.row_heading', 'props': 'background-color: #FCF5E5; color: black;'},
        {'selector': 'td', 'props': [('border', '2px solid black'),('font-size','20px')]},
        {'selector': 'th', 'props': [('border', '2px solid black')]},
        {'selector': 'td:nth-child(7)','props':[('font-weight','bold')]},
        {'selector': 'td:nth-child(8)','props':[('font-weight','bold')]},
        {'selector': 'td:nth-child(9)','props':[('font-weight','bold')]},
        {'selector': 'td:nth-child(10)','props':[('font-weight','bold')]},
        {'selector': 'td:nth-child(3)', 'props': [('background-color', '#FCF5E5'), ('color', 'black')]},
        {'selector': 'td:nth-child(4)', 'props': [('background-color', '#FCF5E5'), ('color', 'black')]},
        {'selector': 'td:nth-child(5)', 'props': [('background-color', '#FCF5E5'), ('color', 'black')]},
        {'selector': 'td:nth-child(6)', 'props': [('background-color', '#FCF5E5'), ('color', 'black')]},
        {'selector': 'td:nth-child(7)', 'props': [('background-color', '#FCF5E5'), ('color', 'black')]},
        {'selector': 'td:nth-child(8)', 'props': [('background-color', '#FCF5E5'), ('color', 'black')]},
        {'selector': 'td:nth-child(9)', 'props': [('background-color', '#FCF5E5'), ('color', 'black')]},
        {'selector': 'td:nth-child(10)', 'props': [('background-color', '#FCF5E5'), ('color', 'black')]},
        {'selector': 'td:nth-child(11)', 'props': [('background-color', '#FCF5E5'), ('color', 'black')]},
        {'selector': 'td:nth-child(12)', 'props': [('background-color', '#FCF5E5'), ('color', 'black')]},
        {'selector': 'td:nth-child(13)', 'props': [('background-color', '#FCF5E5'), ('color', 'black')]},
        {'selector': 'td:nth-child(14)', 'props': [('background-color', '#FCF5E5'), ('color', 'black')]},

    ])
