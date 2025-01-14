import pandas as pd
import pycountry
import plotly.express as px
import plotly.graph_objects as go
from Files.common_list import test_list, low_volume_test_list, gene_list, colors

low_volume_test_type_color_map = {i:j for i,j in zip(low_volume_test_list,px.colors.qualitative.G10)}
test_type_color_map = {i:j for i,j in zip(test_list,colors)}
gene_color_map = {i:j for i,j in zip(test_list,colors)}

def generate_pie_chart_for_client_type(df):
    fig = go.Figure(data=[go.Pie(labels=df['Type'],
                                 values=df['Sample Count'],
                                 textinfo='label+value+percent',
                                 insidetextorientation='horizontal',
                                 textposition='auto',
                                 hole=0.3,
                                 domain=dict(x=[0.2,1]),
                                 textfont=dict(color='black'))])
    
    fig.update_layout(hovermode=False,
                      width=700,
                      height=700,
                      showlegend=False,
                      legend=dict(yanchor='top',
                                  xanchor='right',
                                  font=dict(size=15),
                                  orientation='h',
                                  x=0.78,
                                  y=-0.1,
                                  title=''))
    
    fig.update_traces(textfont_size=32,
                      marker=dict(colors=px.colors.qualitative.G10, 
                                  line=dict(color='#000000', width=4)))
    return fig

def generate_bar_chart_for_client(df):
    modified_df = df.sort_values('Sample Count',ascending=False).iloc[0:10]
    fig = px.bar(modified_df,
                 x='Sample Count',
                 y='Client',
                 color='Client',
                 text='Sample Count',
                 orientation='h',
                 color_discrete_sequence= px.colors.qualitative.G10)
    
    fig.update_layout(width=1600, 
                      height=600, 
                      bargap=0.1,
                      font=dict(size=40,
                                color='black'),
                      xaxis=dict(tickfont=dict(size=12),
                                 showticklabels=False,
                                  range=[0, modified_df['Sample Count'].max()*1.2]), 
                      yaxis=dict(tickfont=dict(size=18,
                                               color='black')),
                      hovermode=False, 
                      yaxis_title=None, 
                      xaxis_title=None, 
                      showlegend=False)
    
    fig.update_traces(marker_line_color='black', 
                      marker_line_width=2.5,
                      textangle = 0,
                      textposition='outside')
    
    return fig

def style_client_table(df):
    modified_df = df.copy()
    modified_df.Type = pd.Categorical(modified_df.Type, categories=low_volume_test_list,ordered=True)
    modified_df = modified_df.sort_values(by=['Type','Sample Count'],ascending=[True,False]).reset_index(drop=True)
    modified_df.index += 1

    def add_color_by_type(row):
        return ['background-color: ' + low_volume_test_type_color_map.get(row['Type'], 'white')] + ['']*(len(row)-1)

    return modified_df.style.apply(add_color_by_type,axis=1).set_table_styles(
        [
            {'selector': 'th.col_heading', 'props': 'background-color: gray; color: white;'},
            {'selector': 'th.row_heading', 'props': 'background-color: #FCF5E5; color: black;'},
            {'selector': 'td', 'props': [('border', '2px solid black')]},
            {'selector': 'th', 'props': [('border', '2px solid black')]},
            {'selector': 'td:nth-child(4)','props':[('font-weight','bold')]},
            {'selector': 'td:nth-child(3)', 'props': [('background-color', '#FCF5E5'), ('color', 'black')]},
            {'selector': 'td:nth-child(4)', 'props': [('background-color', '#FCF5E5'), ('color', 'black')]}
        ])

def generate_bar_chart_for_locus(df):
    bar_list = []
    for i in df.Type.unique():
        bar_list.append(go.Bar(name=i,
                               x=gene_list,
                               y=df[df.Type==i].iloc[0,1:],
                               text=df[df.Type==i].iloc[0,1:],
                               width=0.25,
                               marker=dict(color=low_volume_test_type_color_map[i])))

    fig = go.Figure(data=bar_list)
    fig.update_layout(barmode='group',
                      width=1600,
                      height=600,
                      font=dict(size=40,
                                color='black'),
                      legend=dict(orientation='h',yanchor='bottom',xanchor='right',y=-0.25,x=0.65),
                      xaxis=dict(tickfont=dict(size=28,
                                               color='black')),
                      yaxis=dict(tickfont=dict(size=16,
                                               color='black'),
                                 range=[0, df[gene_list].max().max()*1.2]),
                      hovermode=False,
                      yaxis_title=None,
                      xaxis_title=None,
                      showlegend=False)
    
    fig.update_traces(marker_line_color='black', 
                      marker_line_width=2.5,
                      textposition='outside')
    
    return fig

def style_locuswise_table(df):
    modified_df = df.copy()
    modified_df = modified_df.rename(columns={'Sample Count':'Total'})
    modified_df['Type'] = pd.Categorical(modified_df.Type, categories=low_volume_test_list,ordered=True)
    modified_df = modified_df.sort_values(by=['Type','Total'],ascending=[True,False]).reset_index(drop=True)
    modified_df.index += 1

    def add_color_by_type(row):
        return ['background-color: ' + low_volume_test_type_color_map.get(row['Type'], 'white')] + ['']*(len(row)-1)

    return modified_df.style.apply(add_color_by_type,axis=1).set_table_styles(
        [
            {'selector': 'th.col_heading', 'props': 'background-color: gray; color: white;'},
            {'selector': 'th.row_heading', 'props': 'background-color: #FCF5E5; color: black;'},
            {'selector': 'td', 'props': [('border', '2px solid black')]},
            {'selector': 'th', 'props': [('border', '2px solid black')]},
            {'selector': 'td:nth-child(4)','props':[('font-weight','bold')]},
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

def generate_map(df):
    modified_df = df.copy()
    modified_df['iso_alpha'] = modified_df.apply(lambda row: pycountry.countries.lookup(row['Country']).alpha_3,axis=1)
    fig = px.choropleth(modified_df, locations = 'iso_alpha', color = 'Sample Count', color_continuous_scale = 'Turbo',
                        hover_name = 'Country',labels='Sample Count')
    fig.update_geos(
    projection_type="equirectangular",
    bgcolor='lightblue',
    showocean=True,
    oceancolor='lightblue',
    showland=True,
    landcolor='#e5ecf6',
    showcountries=True,
    countrycolor='black',
    )
    fig.update_layout(height=800,width=1000,dragmode=False)
    return fig

def generate_pie_chart_by_country(df):
    modified_df = df.copy()
    modified_df['Country'] = modified_df.apply(lambda row: row['Country'] if row['Country'] not in ['United Kingdom','United States of America'] else \
                                               ('UK' if row['Country'] == 'United Kingdom' else 'USA'),axis=1)
    fig = go.Figure(data=[go.Pie(labels=modified_df['Country'],
                                 values=modified_df['Sample Count'],
                                 textinfo='label+value',
                                 textposition='inside',
                                 insidetextorientation='auto',
                                 hole=0.3)])
    
    fig.update_layout(width=700, 
                      height=700, 
                      font=dict(size=12),
                      hovermode=False,  
                      showlegend=False)
    fig.update_traces(textfont_size=32,
                      marker=dict(colors=px.colors.qualitative.T10, line=dict(color='#000000', width=3)))
    return fig

def generate_bar_chart_for_nonhla(df):
    modified_df = df.copy()
    modified_df['Gene'] = pd.Categorical(modified_df.Gene, categories=['HLA','ABO-RH','CCR','CMV','DNA Extraction'],ordered=True)
    modified_df = modified_df.sort_values(by=['Gene'],ascending=True).reset_index(drop=True)
    fig = px.bar(modified_df, 
                 x="Gene", 
                 y="Sample Count",
                 color='Gene',
                 height=600,
                 text_auto=True,
                 color_discrete_map = gene_color_map)
    
    fig.update_layout(font=dict(size=60,
                                color='black'),
                      bargap=0.85,
                      xaxis_title=None,
                      yaxis_title = None,
                      xaxis=dict(tickfont=dict(size=32,
                                               color='black')),
                      yaxis=dict(tickfont=dict(size=20,
                                               color='black'),
                                 range=[0, df['Sample Count'].max()*1.2]),
                      showlegend=False)
    
    fig.update_traces(marker_line_color='black', 
                      marker_line_width=2.5,
                      textposition='outside')
    return fig

def style_nonhla_table(df):
    modified_df = df.copy()
    modified_df['Gene'] = pd.Categorical(modified_df.Gene, categories=test_list,ordered=True)
    modified_df = modified_df.sort_values(by=['Gene','Client'],ascending=True).reset_index(drop=True)
    modified_df.index += 1

    def add_color_by_gene(row):
        return ['background-color: ' + test_type_color_map.get(row['Gene'], 'white')] + ['']*(len(row)-1)

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