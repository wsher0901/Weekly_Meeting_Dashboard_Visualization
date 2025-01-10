import pandas as pd 
import plotly.express as px
from Files.common_list import illumina_color_map

def generate_sequence_run_bar_chart(df):
    modified_df = df.copy()
    modified_df['NGS Type'] = pd.Categorical(modified_df['NGS Type'], categories=['Illumina MiSeq','Illumina NovaSeq'],ordered=True)
    modified_df = modified_df.sort_values(by='NGS Type',ascending=True).reset_index(drop=True)
    modified_df.index += 1

    fig = px.bar(df, x='NGS Type', y='Run Count', color='NGS Type',color_discrete_map=illumina_color_map,text='Run Count',)
    fig.update_layout(width=1600,
                      height=600,
                      font=dict(size=70,color='black'),
                      showlegend=False,
                      yaxis=dict(tickfont=dict(size=20,color='black'),range=[0, df['Run Count'].max() * 1.2]),
                      xaxis=dict(tickfont=dict(size=20,color='black')),
                      hovermode=False,
                      bargap=0.6,
                      xaxis_title=None,
                      yaxis_title = None)
    

    fig.update_traces(marker_line_color='black', 
                      marker_line_width=2.5,
                      textposition='outside')
    return fig

def generate_pool_count_bar_chart(df):
    modified_df = df.copy()
    modified_df['NGS Type'] = pd.Categorical(modified_df['NGS Type'], categories=['Illumina MiSeq','Illumina NovaSeq'],ordered=True)
    modified_df = modified_df.sort_values(by=['NGS Type','Date'],ascending=True).reset_index(drop=True)
    modified_df.index += 1

    fig = px.bar(df, x='Experiment', y='Total Cells', color='NGS Type',color_discrete_map=illumina_color_map,text='Total Cells',)
    fig.update_layout(width=1600,
                      height=600,
                      font=dict(size=60,color='black'),
                      yaxis=dict(tickfont=dict(size=20,color='black'),range=[0, df['Total Cells'].max() * 1.2]),
                      xaxis=dict(tickfont=dict(size=16,color='black')),
                      hovermode=False,
                      bargap=0.2,
                      xaxis_title=None,
                      yaxis_title = None,
                      showlegend=False)
    

    fig.update_traces(marker_line_color='black', 
                      marker_line_width=2.5,
                      textposition='outside')
    return fig

def style_pool_count_table(df):
    modified_df = df.reset_index(drop=True).copy()
    modified_df['NGS Type'] = pd.Categorical(modified_df['NGS Type'], categories=['Illumina MiSeq','Illumina NovaSeq'],ordered=True)
    modified_df = modified_df.sort_values(by=['NGS Type','Date'],ascending=True).reset_index(drop=True)
    modified_df.index += 1

    def add_color_by_gene(row):
        return ['background-color: ' + illumina_color_map.get(row['NGS Type'], 'white')] + ['']*(len(row)-1)

    return modified_df.style.apply(add_color_by_gene,axis=1).set_table_styles(
        [
            {'selector': 'th.col_heading', 'props': 'background-color: gray; color: white;'},
            {'selector': 'th.row_heading', 'props': 'background-color: #FCF5E5; color: black;'},
            {'selector': 'td', 'props': [('border', '2px solid black')]},
            {'selector': 'th', 'props': [('border', '2px solid black')]},
            {'selector': 'td:nth-child(5)','props':[('font-weight','bold')]},
            {'selector': 'td:nth-child(3)', 'props': [('background-color', '#FCF5E5'), ('color', 'black')]},
            {'selector': 'td:nth-child(4)', 'props': [('background-color', '#FCF5E5'), ('color', 'black')]},
            {'selector': 'td:nth-child(5)', 'props': [('background-color', '#FCF5E5'), ('color', 'black')]},
            {'selector': 'td:nth-child(6)', 'props': [('background-color', '#FCF5E5'), ('color', 'black')]},
            {'selector': 'td:nth-child(7)', 'props': [('background-color', '#FCF5E5'), ('color', 'black')]},
            {'selector': 'td:nth-child(8)', 'props': [('background-color', '#FCF5E5'), ('color', 'black')]}

        ])


