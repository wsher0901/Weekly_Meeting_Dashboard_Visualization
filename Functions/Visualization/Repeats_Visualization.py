import streamlit as st 
import pandas as pd
import plotly.express as px 
import plotly.graph_objects as go 
from plotly.graph_objs import Figure
from Files.common_list import gene_list, repeats_color_map

gene_list = gene_list + ['Overall']
column_list = [f"{cat} {stat}" for cat in gene_list for stat in ['Total','Repeat','%']]

def generate_weekly_data(df,machine_type):
    file_path = 'Functions/Repeats/illumina_yearly.csv' if machine_type == 'NGS' else 'Functions/Repeats/pacbio_yearly.csv'
    #yearly_data = pd.read_csv(file_path)
    yearly_data = st.session_state.illumina_yearly if machine_type == 'NGS' else st.session_state.pacbio_yearly
    yearly_avg = (yearly_data[[i+' Repeat' for i in gene_list]].sum().reset_index(drop=True) \
                  / yearly_data[[i+' Total' for i in gene_list]].sum().reset_index(drop=True) * 100).round(2).to_frame().T
    weekly_avg = (df[[i+' Repeat' for i in gene_list]].sum().reset_index(drop=True) / df[[i+' Total' for i in gene_list]].sum().reset_index(drop=True) * 100).round(2).to_frame().T
    weekly_avg.columns = gene_list

    bar_list = []
    for i,j in zip(['Weekly','Yearly'],[weekly_avg,yearly_avg]):
        bar_list.append(go.Bar(name=i,
                               x=gene_list,
                               y=j.iloc[0],
                               text=j.iloc[0],
                               width=0.3,
                               marker=dict(color=repeats_color_map[i])))

    fig = go.Figure(data=bar_list)
    fig.update_layout(font=dict(size=40,color='black'),
                     xaxis=dict(tickfont=dict(size=35,color='black')),
                      yaxis=dict(range=[0, max([weekly_avg.max().max(),yearly_avg.max().max()])+2],tickfont=dict(size=20,color='black')), 
                      legend=dict(font=dict(size=20),x=0.7,y=1.0,bgcolor='rgba(0,0,0,0)',orientation='h')
                      ,height=500,
                      hovermode=False,
                      bargap=0.35)
    
    fig.update_traces(marker_line_color='black', 
                      marker_line_width=2.5,
                      textposition='outside')
    return fig

def style_detail_chart(df, machine_type):
    def get_summary(df,label):
        total = df[[i+' Total' for i in gene_list]].sum()
        repeat = df[[i+' Repeat' for i in gene_list]].sum()
        avg = (repeat.reset_index(drop=True) / total.reset_index(drop=True) * 100).round(2)
        avg.index = [i+' %' for i in gene_list]

        repeat.index = gene_list
        total.index = gene_list
        string = repeat.astype(str) + '/' + total.astype(str)
        summary = pd.concat([string,avg],axis=0).to_frame().T
        summary.insert(0,'Experiment', label+' Total')
        summary.insert(1,'Sample Count', int(total['Overall']))
        return summary[['Experiment','Sample Count']+[f"{gene}{label}" for gene in gene_list for label in ['',' %']]]
    
    file_path = 'Functions/Repeats/illumina_yearly.csv' if machine_type == 'NGS' else 'Functions/Repeats/pacbio_yearly.csv'
    #yearly_data = pd.read_csv(file_path)
    yearly_data = st.session_state.illumina_yearly if machine_type == 'NGS' else st.session_state.pacbio_yearly
    yearly_avg = (yearly_data[[i+' Repeat' for i in gene_list]].sum().reset_index(drop=True) \
                  / yearly_data[[i+' Total' for i in gene_list]].sum().reset_index(drop=True) * 100).round(2).to_frame().T
    

    table_data = df.copy()
    for i in gene_list:
        table_data[i] = table_data[i+' Repeat'].astype(str) + '/' + table_data[i+' Total'].astype(str)

    
    table_data.insert(2, 'Sample Count', table_data['Overall Total'])
    table_data = table_data[['Experiment','Sample Count']+[f"{gene}{label}" for gene in gene_list for label in ['',' %']]]
    table_data = pd.concat([table_data, get_summary(df,'Weekly'), get_summary(yearly_data,'Yearly')], axis=0, ignore_index=True)
    table_data.index +=1
    bgcolor,textcolor = '#f9423a','white'
    headers = {
        'selector': 'th.col_heading',
        'props': f"background-color: {bgcolor}; color: {textcolor};"
        }
    index_style = {
        'selector': 'th.index_name',
        'props': f"background-color: {bgcolor}; color: {textcolor};"
        }

    return table_data.style.set_table_styles(
        [
            {'selector': 'th.col_heading', 'props': 'background-color: gray; color: white;'},
            {'selector': 'th.row_heading', 'props': 'background-color: #FCF5E5; color: black;'},
            {'selector': 'td', 'props': [('border', '2px solid black')]},
            {'selector': 'th', 'props': [('border', '2px solid black')]},
            {'selector': 'td:nth-child(2)', 'props': [('background-color', '#FCF5E5'), ('color', 'black')]},
            {'selector': 'td:nth-child(3)', 'props': [('background-color', '#FCF5E5'), ('color', 'black')]},
            {'selector': 'td:nth-child(4)', 'props': [('background-color', '#FCF5E5'), ('color', 'black')]},
            {'selector': 'td:nth-child(5)', 'props': [('background-color', '#FCF5E5'), ('color', '')]},
            {'selector': 'td:nth-child(6)', 'props': [('background-color', '#FCF5E5'), ('color', 'black')]},
            {'selector': 'td:nth-child(7)', 'props': [('background-color', '#FCF5E5'), ('color', '')]},
            {'selector': 'td:nth-child(8)', 'props': [('background-color', '#FCF5E5'), ('color', 'black')]},
            {'selector': 'td:nth-child(9)', 'props': [('background-color', '#FCF5E5'), ('color', '')]},
            {'selector': 'td:nth-child(10)', 'props': [('background-color', '#FCF5E5'), ('color', 'black')]},
            {'selector': 'td:nth-child(11)', 'props': [('background-color', '#FCF5E5'), ('color', '')]},
            {'selector': 'td:nth-child(12)', 'props': [('background-color', '#FCF5E5'), ('color', 'black')]},
            {'selector': 'td:nth-child(13)', 'props': [('background-color', '#FCF5E5'), ('color', '')]},
            {'selector': 'td:nth-child(14)', 'props': [('background-color', '#FCF5E5'), ('color', 'black')]},
            {'selector': 'td:nth-child(15)', 'props': [('background-color', '#FCF5E5'), ('color', '')]},
            {'selector': 'td:nth-child(16)', 'props': [('background-color', '#FCF5E5'), ('color', 'black')]},
            {'selector': 'td:nth-child(17)', 'props': [('background-color', '#FCF5E5'), ('color', '')]},
            {'selector': 'td:nth-child(18)', 'props': [('background-color', '#FCF5E5'), ('color', 'black')]},
            {'selector': 'td:nth-child(19)', 'props': [('background-color', '#FCF5E5'), ('color', '')]},
            {'selector': 'td:nth-child(20)', 'props': [('background-color', '#FCF5E5'), ('color', 'black')]},
            {'selector': 'td:nth-child(21)', 'props': [('background-color', '#FCF5E5'), ('color', '')]},
            {'selector': 'td:nth-child(22)', 'props': [('background-color', '#FCF5E5'), ('color', 'black')]},
            {'selector': 'td:nth-child(23)', 'props': [('background-color', '#FCF5E5'), ('color', '')]}
        ]).format({i+' %':'{:.2f}' for i in gene_list})\
        .highlight_between(subset=[i+' %' for i in gene_list],left=[a+b for a,b in zip(yearly_avg.values.tolist()[0],[0.01]*10)],right=[100]*10,axis=1,
                                             props='font-weight:bold;color:#f9423a').set_properties(**{'text-align': 'right'})

def visualize_yearly_data(df_yearly: pd.DataFrame) -> Figure:
    '''
    Generates a figure of line graph with each line representing particulra gene's repeat rate
    
    Args:
        df_yearly (dataframe): one-year amount of repeat rate in a dataframe
        
    Return:
        fig (Figure): line chart
    '''
    fig = px.line(df_yearly,x=df_yearly.index,y=[i+'%' for i in gene_list],height=700)
    fig.update_layout(legend=dict(font=dict(size=20),y=-0.1,x=0.2,bgcolor='rgba(0,0,0,0)',orientation='h'),
                      xaxis=dict(tickfont=dict(size=30),title=''),
                      yaxis=dict(tickfont=dict(size=20),title='Repeat Rate'),height=800)
    
    return fig
