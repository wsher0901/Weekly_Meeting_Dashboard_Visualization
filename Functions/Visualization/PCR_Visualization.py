import pandas as pd
import plotly.express as px
from Files.common_list import test_list, colors

color_map = {i:j for i,j in zip(test_list,colors)}

def generate_bar_chart_by_gene(df,machine_type):
    modified_df = df[df.Type == machine_type].copy()
    modified_df = modified_df.groupby('Gene')['Sample Count'].sum().reset_index()
    fig = px.bar(modified_df,
                 x='Gene',
                 y='Sample Count',
                 color='Gene',
                 text='Sample Count',
                 color_discrete_map= color_map)
    
    fig.update_layout(width=1600,
                      height=600,
                      bargap=0.7,
                      font=dict(size=60,
                                color='black'),
                      xaxis=dict(tickfont=dict(size=32,
                                               color='black')),
                      yaxis=dict(tickfont=dict(size=16,
                                               color='black'),
                                 range=[0, modified_df['Sample Count'].max()*1.2]),
                      hovermode=False,
                      yaxis_title=None,
                      xaxis_title=None,
                      showlegend=False)
    
    fig.update_traces(marker_line_color='black', 
                      marker_line_width=2.5,
                      textposition='outside')
    
    fig.update_xaxes(categoryorder='array',
                     categoryarray = sorted(modified_df.Gene,key=lambda x:test_list.index(x)))
    
    return fig

def style_table(df,machine_type):
    modified_df = df[df.Type == machine_type].copy()
    modified_df['Gene'] = pd.Categorical(modified_df.Gene, categories=test_list,ordered=True)
    modified_df = modified_df.sort_values(by=['Gene'],ascending=True).reset_index(drop=True)
    modified_df = modified_df[['Gene','Blot Count','Plate Count','Sample Count']]
    modified_df.index += 1

    def add_color_by_gene(row):
        return ['background-color: ' + color_map.get(row['Gene'], 'white')] + ['']*(len(row)-1)

    return modified_df.style.apply(add_color_by_gene,axis=1).set_table_styles(
        [
            {'selector': 'th.col_heading', 'props': 'background-color: gray; color: white;'},
            {'selector': 'th.row_heading', 'props': 'background-color: #FCF5E5; color: black;'},
            {'selector': 'td', 'props': [('border', '2px solid black')]},
            {'selector': 'th', 'props': [('border', '2px solid black')]},
            {'selector': 'td:nth-child(5)','props':[('font-weight','bold')]},
            {'selector': 'td:nth-child(3)', 'props': [('background-color', '#FCF5E5'), ('color', 'black')]},
            {'selector': 'td:nth-child(4)', 'props': [('background-color', '#FCF5E5'), ('color', 'black')]},
            {'selector': 'td:nth-child(5)', 'props': [('background-color', '#FCF5E5'), ('color', 'black')]}
        ])