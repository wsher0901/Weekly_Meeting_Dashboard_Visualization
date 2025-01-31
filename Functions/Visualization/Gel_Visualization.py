import pandas as pd 
import plotly.express as px
import plotly.graph_objects as go
from Files.common_list import gel_color_map

def generate_comprehensive_bar_chart(df):
    max_val = df.iloc[:,1:].max().max()
    fig = go.Figure(data=[
        go.Bar(name='Illumina',
               x=df.columns[1:],
               y=df[df['Type'] == 'Illumina'].iloc[0,1:],
               text=df[df['Type'] == 'Illumina'].iloc[0,1:],
               width=[0.2]*6,
               marker_color='#EE3233'),
        go.Bar(name='Pacbio',
               x=df.columns[1:],
               y=df[df['Type'] == 'Pacbio'].iloc[0,1:],
               text=df[df['Type'] == 'Pacbio'].iloc[0,1:],
               width=[0.2]*6,
               marker_color='#66A7C5')])
    
    fig.update_layout(barmode='group',
                      height=650,
                      legend=dict(orientation='h',yanchor='top',y=-0.25,xanchor='left',x=0.43,font=dict(size=15)),
                      font=dict(size=44,color='black'),
                      xaxis=dict(tickfont=dict(size=28,color='black')),
                      yaxis=dict(tickfont=dict(size=18,color='black'),
                                 range=[0, max_val * 1.15]))
    
    fig.update_traces(marker_line_color='black', 
                      marker_line_width=2.5,
                      textposition='outside')

    return fig

def style_gel_details(df):
    modified_df = df.copy()
    modified_df['Type'] = pd.Categorical(modified_df.Type, categories=['Illumina','Pacbio'],ordered=True)
    modified_df = modified_df.sort_values(by=['Type'],ascending=True).reset_index(drop=True)
    modified_df.index += 1

    def add_color_by_gene(row):
        return ['background-color: ' + gel_color_map.get(row['Type'], 'white')] + ['']*(len(row)-1)

    return modified_df.style.apply(add_color_by_gene,axis=1).set_table_styles(
        [
            {'selector': 'th.col_heading', 'props': 'background-color: gray; color: white;'},
            {'selector': 'th.row_heading', 'props': 'background-color: #FCF5E5; color: black;'},
            {'selector': 'td', 'props': [('border', '2px solid black')]},
            {'selector': 'th', 'props': [('border', '2px solid black')]},
            {'selector': 'td:nth-child(3)', 'props': [('background-color', '#FCF5E5'), ('color', 'black')]},
            {'selector': 'td:nth-child(4)', 'props': [('background-color', '#FCF5E5'), ('color', 'black')]},
            {'selector': 'td:nth-child(5)', 'props': [('background-color', '#FCF5E5'), ('color', 'black')]},
            {'selector': 'td:nth-child(6)', 'props': [('background-color', '#FCF5E5'), ('color', 'black')]},
            {'selector': 'td:nth-child(7)', 'props': [('background-color', '#FCF5E5'), ('color', 'black')]},
            {'selector': 'td:nth-child(8)', 'props': [('background-color', '#FCF5E5'), ('color', 'black')]},
            {'selector': 'td:nth-child(9)', 'props': [('background-color', '#FCF5E5'), ('color', 'black')]}
        ])

def generate_bar_chart_for_blot(df):
    modified_df = df.copy()
    modified_df['Type'] = pd.Categorical(modified_df.Type, categories=['Illumina','Pacbio'],ordered=True)
    modified_df = modified_df.sort_values(by=['Type','Blot Count'],ascending=True).reset_index(drop=True)
    modified_df.index += 1

    fig = px.bar(df, x='Category', y='Blot Count', color='Type',color_discrete_map=gel_color_map,text='Blot Count',)
    fig.update_layout(width=1600,
                      height=600,
                      font=dict(size=70,color='black'),
                      showlegend=False,
                      yaxis=dict(tickfont=dict(size=20,color='black'),range=[0, df['Blot Count'].max() * 1.2]),
                      xaxis=dict(tickfont=dict(size=18,color='black')),
                      hovermode=False,
                      bargap=0.7,
                      xaxis_title=None,
                      yaxis_title = '# of Runs')
    

    fig.update_traces(marker_line_color='black', 
                      marker_line_width=2.5,
                      textposition='outside')
    return fig

def style_blot_details(df):
    modified_df = df.copy()
    modified_df['Type'] = pd.Categorical(modified_df.Type, categories=['Illumina','Pacbio'],ordered=True)
    modified_df = modified_df.sort_values(by=['Type','Blot Count'],ascending=[True,False]).reset_index(drop=True)
    modified_df.index += 1

    def add_color_by_gene(row):
        return ['background-color: ' + gel_color_map.get(row['Type'], 'white')] + ['']*(len(row)-1)

    return modified_df.style.apply(add_color_by_gene,axis=1).set_table_styles(
        [
            {'selector': 'th.col_heading', 'props': 'background-color: gray; color: white;'},
            {'selector': 'th.row_heading', 'props': 'background-color: #FCF5E5; color: black;'},
            {'selector': 'td', 'props': [('border', '2px solid black')]},
            {'selector': 'th', 'props': [('border', '2px solid black')]},
            {'selector': 'td:nth-child(4)','props':[('font-weight','bold')]},
            {'selector': 'td:nth-child(3)', 'props': [('background-color', '#FCF5E5'), ('color', 'black')]},
            {'selector': 'td:nth-child(4)', 'props': [('background-color', '#FCF5E5'), ('color', 'black')]},

        ])

def style_rejection_details(df):
    modified_df = df.reset_index(drop=True)
    modified_df.index += 1 
    return modified_df.style.set_table_styles(
        [
            {'selector': 'th.col_heading', 'props': 'background-color: gray; color: white;'},
            {'selector': 'th.row_heading', 'props': 'background-color: #FCF5E5; color: black;'},
            {'selector': 'td', 'props': [('border', '2px solid black')]},
            {'selector': 'th', 'props': [('border', '2px solid black')]},
            {'selector': 'td:nth-child(2)', 'props': [('background-color', '#FCF5E5'), ('color', 'black')]},
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
            {'selector': 'td:nth-child(13)', 'props': [('background-color', '#FCF5E5'), ('color', 'black')]}
        ])
