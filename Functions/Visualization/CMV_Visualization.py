import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from Files.common_list import cmv_test_type_list

color_map = {i:j for i,j in zip(cmv_test_type_list,px.colors.qualitative.G10)}

def generate_bar_chart_for_cmv_statistics(df):
    modified_df = pd.DataFrame([[i,df[df.Type == i]['Sample Count'].sum()] if i in df.Type.unique() else [i,0] for i in cmv_test_type_list],columns=['Type','Count'])
    fig = px.bar(modified_df,
                       x='Type',
                       y='Count',
                       color='Type',
                       text='Count',
                       color_discrete_map= color_map)
    
    fig.update_layout(width=1600,
                      height=600,
                      bargap=0.7,
                      font=dict(size=60,
                                color='black'),
                      legend=dict(orientation='h',yanchor='bottom',xanchor='right',y=-0.25,x=0.65),
                      xaxis=dict(tickfont=dict(size=28,
                                               color='black')),
                      yaxis=dict(tickfont=dict(size=16),
                                 range=[0, modified_df['Count'].max()*1.2]),
                      hovermode=False,
                      yaxis_title=None,
                      xaxis_title=None,
                      showlegend=False)
    
    fig.update_traces(marker_line_color='black', 
                      marker_line_width=2.5,
                      textposition='outside')

    return fig

def style_cmv_statistics_table(df):
    modified_df = df.copy()
    modified_df.Type = pd.Categorical(modified_df.Type, categories=cmv_test_type_list,ordered=True)
    modified_df = modified_df.sort_values(by=['Type','Experiment Date'],ascending=True).rename(columns={'Sample ID':'Sample Count'}).reset_index(drop=True)
    modified_df.index += 1

    def add_color_by_gene(row):
        return ['background-color: ' + color_map.get(row['Type'], 'white')] + ['']*(len(row)-1)

    return df.style.apply(add_color_by_gene,axis=1).set_table_styles(
        [
            {'selector': 'th.col_heading', 'props': 'background-color: gray; color: white;'},
            {'selector': 'th.row_heading', 'props': 'background-color: #FCF5E5; color: black;'},
            {'selector': 'td', 'props': [('border', '2px solid black')]},
            {'selector': 'th', 'props': [('border', '2px solid black')]},
            {'selector': 'td:nth-child(8)','props':[('font-weight','bold')]},
            {'selector': 'td:nth-child(3)', 'props': [('background-color', '#FCF5E5'), ('color', 'black')]},
            {'selector': 'td:nth-child(4)', 'props': [('background-color', '#FCF5E5'), ('color', 'black')]},
            {'selector': 'td:nth-child(5)', 'props': [('background-color', '#FCF5E5'), ('color', 'black')]},
            {'selector': 'td:nth-child(6)', 'props': [('background-color', '#FCF5E5'), ('color', 'black')]},
            {'selector': 'td:nth-child(7)', 'props': [('background-color', '#FCF5E5'), ('color', 'black')]},
            {'selector': 'td:nth-child(8)', 'props': [('background-color', '#FCF5E5'), ('color', 'black')]}
        ])

def generate_pie_chart_for_cmv_analytics(df):
    labels=['Negative','Positive','Equivocal']
    values = [df['Number of Negative'].sum(),df['Number of Positive'].sum(),df['Number of Equivocal'].sum()]
    custom_text = [
    f"{label}: <br><b>({value/sum(values)*100:.2f}%)</b>"
    for label, value in zip(labels, values)]

    fig = go.Figure(data=[go.Pie(labels=['Negative','Positive','Equivocal'],
                                 values=[df['Number of Negative'].sum(),df['Number of Positive'].sum(),df['Number of Equivocal'].sum()],
                                 text=custom_text,
                                 textinfo = 'text',
                                 insidetextorientation='horizontal',
                                 hole=0.3,
                                 domain=dict(x=[0.3,0.99]),
                                 textfont=dict(color='black'))])
    
    fig.update_layout(hovermode=False,
                      width=650,
                      height=650,
                      legend=dict(yanchor='top',
                                  xanchor='right',
                                  font=dict(size=15),
                                  orientation='h',
                                  x=0.9,
                                  y=-0.1,
                                  title=''))
    
    fig.update_traces(textfont_size=26,
                      marker=dict(colors=['#2f75b5','#a9d08e','#ff9793'], 
                                  line=dict(color='#000000', width=4)))
    return fig

def style_cmv_analytics_table(df):
    def color_column_neg(val):
        return 'background-color: #2f75b5'
    def color_column_pos(val):
        return 'background-color: #a9d08e' 
    def color_column_equ(val):
        return 'background-color: #ff9793'

    return df.style.set_table_styles(
        [
            {'selector': 'th.col_heading', 'props': 'background-color: gray; color: white;'},
            {'selector': 'th.row_heading', 'props': 'background-color: #FCF5E5; color: black;'},
            {'selector': 'td', 'props': [('border', '2px solid black')]},
            {'selector': 'th', 'props': [('border', '2px solid black')]},
            {'selector': 'td:nth-child(6)','props':[('font-weight','bold')]},
            {'selector': 'td:nth-child(10)','props':[('font-weight','bold')]},
            {'selector': 'td:nth-child(11)','props':[('font-weight','bold')]},
            {'selector': 'td:nth-child(12)','props':[('font-weight','bold')]},
            {'selector': 'td:nth-child(2)', 'props': [('background-color', '#FCF5E5'), ('color', 'black')]},
            {'selector': 'td:nth-child(3)', 'props': [('background-color', '#FCF5E5'), ('color', 'black')]},
            {'selector': 'td:nth-child(4)', 'props': [('background-color', '#FCF5E5'), ('color', 'black')]},
            {'selector': 'td:nth-child(5)', 'props': [('background-color', '#FCF5E5'), ('color', 'black')]},
            {'selector': 'td:nth-child(6)', 'props': [('background-color', '#FCF5E5'), ('color', 'black')]},
            {'selector': 'td:nth-child(7)', 'props': [('background-color', '#FCF5E5'), ('color', 'black')]},
            {'selector': 'td:nth-child(8)', 'props': [('background-color', '#FCF5E5'), ('color', 'black')]},
            {'selector': 'td:nth-child(9)', 'props': [('background-color', '#FCF5E5'), ('color', 'black')]},
            {'selector': 'th.col8', 'props': [('background-color', '#2f75b5'),('color', 'black')]},
            {'selector': 'th.col9', 'props': [('background-color', '#a9d08e'),('color', 'black')]}, 
            {'selector': 'th.col10', 'props': [('background-color', '#ff9793'),('color', 'black')]}   
        ]
    ).map(color_column_pos, subset=['Rate of Positive']) \
    .map(color_column_neg, subset=['Rate of Negative']) \
    .map(color_column_equ, subset=['Rate of Equivocal']) \
    .map(lambda x: 'color: black', subset = ['Rate of Negative','Rate of Positive','Rate of Equivocal'])

def generate_box_plot_chart_for_cmv_analytics(df):
    fig = go.Figure()
    fig.add_trace(go.Box(
        x=df['Observed OD Value'],
        name="All Points",
        jitter=0.5,
        notched=True,
        pointpos=-1.8,
        marker_size=4,
        line_width=2.5,
        boxpoints='all', # represent all points
        marker_color='rgb(7,40,89)',
        line_color='rgb(7,40,89)'))

    return fig

def style_positive_control_table(df):
    def row_color(row_index):
        if ((row_index + 1) // 2) % 2 == 0:
            background_color = 'background-color: white'
        else:
            background_color = 'background-color: #98ec98'
        
        text_color = 'color: black'
        
        row_styles = []
        for i, col in enumerate(df.columns):
            if col == 'Observed OD Value':
                font_weight = 'font-weight: bold' if ((row_index - 1) // 2) % 2 == 0 else 'font-weight: normal'
                row_styles.append(f'background-color: #ffefd5; color: black; {font_weight}')
            elif col == 'RI (Relative Index)':
                font_weight = 'font-weight: bold' if row_index % 2 == 0 else 'font-weight: normal'
                row_styles.append(f'{background_color}; color: black; {font_weight}')
            else:
                row_styles.append(f'{background_color}; {text_color}')
        
        return row_styles
    
    return df.style.set_table_styles(
        [
            {'selector': 'th.col_heading', 'props': 'background-color: gray; color: white;'},
            {'selector': 'th.row_heading', 'props': 'background-color: #FCF5E5; color: black;'},
            {'selector': 'td', 'props': [('border', '2px solid black')]},
            {'selector': 'th', 'props': [('border', '2px solid black')]},
        ]
    ).apply(lambda x: row_color(x.name), axis=1)

def style_remaining_control_table(df):
    def row_color(row_index):
        if row_index % 2 == 0:
            background_color = 'background-color: white'
        else:
            background_color = 'background-color: #98ec98'
        
        text_color = 'color: black'
        
        row_styles = []
        for i, col in enumerate(df.columns):
            if col == 'Observed OD Value':
                font_weight = 'font-weight: bold' if row_index % 2 == 1 else 'font-weight: normal'
                row_styles.append(f'background-color: #ffefd5; color: black; {font_weight}')
            else:
                row_styles.append(f'{background_color}; {text_color}')
        
        return row_styles
    
    return df.style.set_table_styles(
        [
            {'selector': 'th.col_heading', 'props': 'background-color: gray; color: white;'},
            {'selector': 'th.row_heading', 'props': 'background-color: #FCF5E5; color: black;'},
            {'selector': 'td', 'props': [('border', '2px solid black')]},
            {'selector': 'th', 'props': [('border', '2px solid black')]},
        ]
    ).apply(lambda x: row_color(x.name), axis=1)