import pandas as pd
import plotly.express as px
from Files.common_list import pacbio_color_map

def generate_sequencer_bar_chart(df):
    modified_df = df.copy()
    modified_df['Pacbio Type'] = pd.Categorical(modified_df['Pacbio Type'], categories=['Pacbio Sequel-I','Pacbio Sequel-II','Pacbio Sequel-IIe'],ordered=True)
    modified_df = modified_df.sort_values(by='Pacbio Type',ascending=True).reset_index(drop=True)
    modified_df.index += 1

    fig = px.bar(df, x='Pacbio Type', y='Run Count', color='Pacbio Type',color_discrete_map=pacbio_color_map,text='Run Count')
    fig.update_layout(width=1600,
                      height=600,
                      font=dict(size=60,color='black'),
                      showlegend=False,
                      yaxis=dict(tickfont=dict(size=20,color='black'),range=[0, df['Run Count'].max() * 1.2]),
                      xaxis=dict(tickfont=dict(size=20,color='black')),
                      hovermode=False,
                      bargap=0.7,
                      xaxis_title=None,
                      yaxis_title = None)
    

    fig.update_traces(marker_line_color='black', 
                      marker_line_width=2.5,
                      textposition='outside')
    return fig

def generate_jobs_bar_chart(df):
    modified_df = df.copy()
    modified_df['Machine Type'] = pd.Categorical(modified_df['Machine Type'], categories=['Pacbio Sequel-I','Pacbio Sequel-II','Pacbio Sequel-IIe'],ordered=True)
    modified_df = modified_df.sort_values(by=['Machine Type'],ascending=True).reset_index(drop=True)
    modified_df.index += 1

    fig = px.bar(df, x='Job Name', y='Total Cells', color='Machine Type',color_discrete_map=pacbio_color_map,text='Total Cells',)
    fig.update_layout(width=1600,
                      height=600,
                      font=dict(size=60,color='black'),
                      yaxis=dict(tickfont=dict(size=20,color='black'),range=[0, df['Total Cells'].max() * 1.2]),
                      xaxis=dict(tickfont=dict(size=12,color='black')),
                      hovermode=False,
                      bargap=0.4,
                      xaxis_title=None,
                      yaxis_title = None,
                      showlegend=False)
    

    fig.update_traces(marker_line_color='black', 
                      marker_line_width=2.5,
                      textposition='outside')
    return fig

def style_total_cell_table(df):
    modified_df = df.reset_index(drop=True).copy()
    modified_df['Machine Type'] = pd.Categorical(modified_df['Machine Type'], categories=['Pacbio Sequel-I','Pacbio Sequel-II','Pacbio Sequel-IIe'],ordered=True)
    modified_df = modified_df.sort_values(by=['Machine Type'],ascending=True).reset_index(drop=True)
    modified_df = modified_df[['Machine Type','Job Name','Run Name','Job Type','Total Cells']]
    modified_df.index += 1

    def add_color_by_gene(row):
        return ['background-color: ' + pacbio_color_map.get(row['Machine Type'], 'white')] + ['']*(len(row)-1)

    return modified_df.style.apply(add_color_by_gene,axis=1).set_table_styles(
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
