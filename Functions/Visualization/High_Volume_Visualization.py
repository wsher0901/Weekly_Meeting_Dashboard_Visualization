import pandas as pd
import pycountry
import plotly.express as px
import plotly.graph_objects as go
from Files.common_list import test_list, colors

color_map = {i:j for i,j in zip(test_list,colors)}

def generate_bar_chart_by_test(df,ind):
    bargap = 0.4 if ind == 0 else 0.6
    df = df[df['Request Type'] == 'New'] if ind == 0 else df[df['Request Type'] != 'New']
    total = ['Total','',len(df[df['Request Type'] == 'New']['Sample ID'].unique())] if ind == 0 else ['Total','',len(df[df['Request Type'] != 'New']['Sample ID'].unique())]
    modified_df = df.groupby(['Gene','Request Type'])['Sample ID'].count().reset_index().rename(columns={'Sample ID':'Sample Count'})
    modified_df.loc[len(modified_df)] = total
    fig = px.bar(modified_df, 
                 x='Gene', 
                 y='Sample Count', 
                 color='Gene', 
                 text='Sample Count', 
                 color_discrete_map = color_map)
    
    fig.update_layout(width=1600, 
                      height=600,
                      bargap=bargap,
                      font=dict(color='black',
                                    size=44),
                      xaxis=dict(tickfont=dict(size=20,
                                               color='black')), 
                      yaxis=dict(tickfont=dict(size=18),
                                 range=[0, modified_df['Sample Count'].max()*1.2],
                                 showticklabels=False),
                      hovermode=False, 
                      yaxis_title=None, 
                      xaxis_title=None, 
                      showlegend=False)
    
    fig.update_traces(marker_line_color='black', 
                      marker_line_width=2.5,
                      textposition='outside')
    
    fig.update_xaxes(categoryorder='array',
                     categoryarray = sorted(modified_df.Gene,key=lambda x: [i+j for i in ['Total']+test_list for j in ['',' (Rerequest)']].index(x)))
    return fig

def generate_bar_chart_by_client(df,ind):
    bargap = 0.1 if ind == 0 else 0.2
    df = df[df['Request Type'] == 'New'] if ind == 0 else df[df['Request Type'] != 'New']
    modified_df = df.drop_duplicates(subset=['Client','Project','Date','Country','Sample ID','Request Type'])\
        .groupby('Client').Gene.count().reset_index().rename(columns={'Gene':'Sample Count'}).sort_values('Sample Count',ascending=False)
    fig = px.bar(modified_df,
                 x='Sample Count',
                 y='Client',
                 color='Client',
                 text='Sample Count',
                 orientation='h',
                 color_discrete_sequence= px.colors.qualitative.G10)
    
    fig.update_layout(width=1600, 
                      height=600,
                      bargap=bargap,
                      font=dict(size=50,
                                color='black'),
                      xaxis=dict(showticklabels=False,
                                 range=[0,modified_df['Sample Count'].max() * 1.3]), 
                      yaxis=dict(tickfont=dict(size=16,color='black')),
                      hovermode=False, 
                      yaxis_title=None, 
                      xaxis_title=None, 
                      showlegend=False)
    
    fig.update_traces(marker_line_color='black ', 
                      marker_line_width=1.5,
                      textposition='outside')
    
    return fig

def style_samplewise_table(df):
    modified_df = df.copy()
    modified_df['Project'] = modified_df.apply(lambda row: row['Project'] + ' (Rerequest)' if row['Request Type'] != 'New' else row['Project'],axis=1)
    modified_df = modified_df.groupby(['Gene','Client','Project'])['Sample ID'].count().reset_index()
    modified_df.Gene = pd.Categorical(modified_df.Gene, categories=test_list,ordered=True)
    modified_df = modified_df.sort_values(by=['Gene'],ascending=True).rename(columns={'Sample ID':'Sample Count'}).reset_index(drop=True)
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

def generate_map(df):
    modified_df = df.drop_duplicates(subset=['Client','Project','Date','Country','Sample ID','Request Type'])\
        .groupby('Country').Gene.count().reset_index().rename(columns={'Gene':'Sample Count'})
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
    modified_df = df.drop_duplicates(subset=['Client','Project','Date','Country','Sample ID','Request Type'])\
        .groupby('Country').Gene.count().reset_index().rename(columns={'Gene':'Sample Count'})
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
                      font=dict(size=40),
                      hovermode=False,  
                      showlegend=False)
    
    fig.update_traces(marker=dict(colors=px.colors.qualitative.T10, line=dict(color='#000000', width=3)))
    
    return fig

def generate_bar_chart_for_extraction(df,client_type):
    modified_df = df[df.Type == client_type].groupby('Gene')[['Sample Count']].sum().reset_index()
    fig = px.bar(modified_df, 
                 x="Gene", 
                 y="Sample Count",
                 color='Gene',
                 height=400,
                 text_auto=True,
                 color_discrete_map = color_map)
    
    fig.update_layout(font=dict(size=50,
                                color='black'),
                      bargap=0.66,
                      xaxis_title=None,
                      yaxis_title = None,
                      xaxis=dict(tickfont=dict(size=24)),
                      yaxis=dict(tickfont=dict(size=20),
                                 range=[0, modified_df['Sample Count'].max()*1.3]),
                      showlegend=False)
    
    fig.update_xaxes(categoryorder='array',categoryarray = sorted(list(modified_df.Gene),key=lambda x: test_list.index(x)))
    fig.update_traces(marker_line_color='black', 
                      marker_line_width=2.5,
                      textposition='outside')
    return fig

def style_extraction_table(df):
    modified_df = df.copy()
    modified_df.Gene = pd.Categorical(modified_df.Gene, categories=test_list,ordered=True)
    modified_df = modified_df.sort_values(by=['Gene','Type','Date'],ascending=[True,False,True]).reset_index(drop=True)
    modified_df.index += 1
    modified_df = modified_df[['Gene','Type','Date','Day','Sample Count']]

    def add_color_by_gene(row):
        return ['background-color: ' + color_map.get(row['Gene'], 'white')] + ['']*(len(row)-1)

    return modified_df.style.apply(add_color_by_gene,axis=1).set_table_styles(
        [
            {'selector': 'th.col_heading', 'props': 'background-color: gray; color: white;'},
            {'selector': 'th.row_heading', 'props': 'background-color: #FCF5E5; color: black;'},
            {'selector': 'td', 'props': [('border', '2px solid black')]},
            {'selector': 'th', 'props': [('border', '2px solid black')]},
            {'selector': 'td:nth-child(6)','props':[('font-weight','bold')]},
            {'selector': 'td:nth-child(3)', 'props': [('background-color', '#FCF5E5'), ('color', 'black')]},
            {'selector': 'td:nth-child(4)', 'props': [('background-color', '#FCF5E5'), ('color', 'black')]},
            {'selector': 'td:nth-child(5)', 'props': [('background-color', '#FCF5E5'), ('color', 'black')]},
            {'selector': 'td:nth-child(6)', 'props': [('background-color', '#FCF5E5'), ('color', 'black')]}
        ])