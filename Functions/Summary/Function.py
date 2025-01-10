import math
import copy
import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

def st_write(loc,x):
    for _ in range(x):
        loc.write('')

def pre_pcr_high_chart(total,gene,gene_detailed):
    temp = []
    for i in gene_detailed:
        for j in gene_detailed[i]:
            temp.append([i,j,gene_detailed[i][j]])
    df_gene = pd.DataFrame(temp,columns=['Gene','Client','Count'])
    df_gene = df_gene.groupby('Gene')['Count'].sum().reset_index().sort_values('Count',ascending=False)

    fig = px.bar(df_gene, 
                 x='Gene', 
                 y='Count', 
                 color='Gene', 
                 text='Count',
                 color_discrete_sequence=st.session_state.color,
                 title='Pre PCR High Volume')
    
    fig.add_annotation(
        x=0.47,
        y=1.25,
        xref="paper",
        yref="paper",
        text=f"Total: {total}",
        showarrow=False,
        font=dict(
            family="Courier New, monospace",
            size=30,
            color="#e9ff32"
            ),
        align="center",
        ax=20,
        ay=-30,
        bordercolor="#c7c7c7",
        borderwidth=1,
        borderpad=4,
        bgcolor="#0E1117",
        opacity=1
        )

    fig.update_layout(width=400,
                      height=400,
                      font=dict(size=26),
                      legend=dict(orientation='h',yanchor='bottom',xanchor='right',y=-0.25,x=1),
                      yaxis=dict(range=[0, math.ceil(df_gene.Count.max())*1.2],tickfont=dict(size=12)),
                      xaxis=dict(tickfont=dict(size=15)),
                      hovermode=False,
                      yaxis_title=None,
                      xaxis_title=None,
                      showlegend=False,
                      title=dict(font=dict(size=25), automargin=True, x=0.3,y=1))
    fig.update_yaxes(categoryorder='array',categoryarray = sorted(list(gene.keys()),key=lambda x: ['HLA','ABO-RH','CCR','CMV','DNA Extraction','ENGRAFTMENT','Illumina','KIR','Micro array','Nanopore','Non-Classical','Optical','PacBio','PGX','Whole Genome'].index(x))[::-1])
    fig.update_traces(textposition='outside')
    return fig

def pre_pcr_low_chart(raw):
    data = raw.groupby('Type')['Total'].sum().reset_index()
    data = data.rename(columns={'Total':'Sample Count'})
    pie = go.Figure(data=[go.Pie(labels=data['Type'],values=data['Sample Count'],textinfo='label+value',insidetextorientation='horizontal',hole=0.3)])
    pie.update_layout(legend=dict(yanchor='top',xanchor='right',font=dict(size=20),orientation='h',x=0.6,y=-0.1,title=''),hovermode=False,width=400,height=400,showlegend=False,
                      title=dict(text='Pre PCR Low Volume',font=dict(size=25), automargin=True, x=0.3,y=1))
    pie.update_traces(textfont_size=30,marker=dict(colors=st.session_state.color[6:], line=dict(color='#000000', width=2)))

    for i in data['Type'].unique():
        y_coordinate = 5
        pie.add_annotation(
            x=5,
            y=y_coordinate,
            text=f"{i}: {data[data['Type'] == i]['Sample Count'].iloc[0]}",
            showarrow=False,
            font=dict(
                family="Courier New, monospace",
                size=24,
                color="#e9ff32"
                ),
            align="center",
            ax=20,
            ay=-30,
            borderwidth=0,
            borderpad=4,
            opacity=1
            )
        y_coordinate+=1

    pie.add_annotation(
        x=0.5,
        y=1.25,
        xref="paper",
        yref="paper",
        text=f"Sample Count: {data['Sample Count'].sum()}",
        showarrow=False,
        font=dict(
            family="Courier New, monospace",
            size=20,
            color="#e9ff32"
            ),
        align="center",
        ax=20,
        ay=-30,
        bordercolor="#c7c7c7",
        borderwidth=1,
        borderpad=4,
        bgcolor="#0E1117",
        opacity=1
        )
    pie.add_annotation(
        x=0.95,
        y=0.85,
        xref="paper",
        yref="paper",
        text=f"Client Count",
        showarrow=False,
        font=dict(
            family="Courier New, monospace",
            size=12,
            color="#e9ff32"
            ),
        align="right",
        ax=20,
        ay=-30,
        bordercolor="#c7c7c7",
        borderwidth=1,
        borderpad=4,
        bgcolor="#0E1117",
        opacity=1
        )
    y_val = 0.75
    for i in data.Type.unique():
        pie.add_annotation(
        x=0.95,
        y=y_val,
        xref="paper",
        yref="paper",
        text=f"{i}: {raw[raw.Type == i]['Project'].count()}",
        showarrow=False,
        font=dict(
            family="Courier New, monospace",
            size=12,
            color="#e9ff32"
            ),
        align="right",
        ax=20,
        ay=-30,
        bordercolor="#c7c7c7",
        borderwidth=1,
        borderpad=4,
        bgcolor="#0E1117",
        opacity=1
        )
        if i == 'Registry':
            y_val -= 0.1114
        else:
            y_val -= 0.15

    return pie

def pcr_chart(data,color,width):
    def change_naming(gene):
        if gene in ['Illumina Sequencing','Nanopore Sequencing','Non-Classical Genes','Optical Mapping','PacBio Sequencing','Whole Genome Sequencing']:
            if gene == 'Illumina Sequencing':
                return 'Illumina'
            elif gene == 'Nanopore Sequencing':
                return 'Nanopore'
            elif gene == 'Non-Classical Genes':
                return 'Non-Classical'
            elif gene == 'Optical Mapping':
                return 'Optical'
            elif gene == 'PacBio Sequencing':
                return 'PacBio'
            elif gene == 'Whole Genome Sequencing':
                return 'Whole Genome'
        else:
            return gene
    data = data.groupby(['Type','Gene'])[['Sample Count']].sum().reset_index()
    data['Gene'] = data.apply(lambda row: change_naming(row['Gene']),axis=1)
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=data.Gene,
        y=data[data.Type=='Illumina']['Sample Count'],
        name='Illumina',
        text=data[data.Type=='Illumina']['Sample Count']
    ))

    fig.add_trace(go.Bar(
        x=data.Gene,
        y=data[data.Type=='Pacbio']['Sample Count'],
        name='Pacbio',
        text=data[data.Type=='Pacbio']['Sample Count']
    ))
    fig.update_layout(width=400,
                      height=400,
                      font=dict(size=28),
                      yaxis=dict(tickfont=dict(size=12),range=[0, data['Sample Count'].max() * 1.3]),
                      xaxis=dict(tickfont=dict(size=20)),
                      hovermode=False,
                      bargap=0.3,
                      xaxis_title=None,
                      legend=dict(orientation='h',yanchor='bottom',xanchor='right',xref='paper',yref='paper',y=-0.3,x=0.6,font=dict(size=10)),
                      title=dict(text='PCR',font=dict(size=25), automargin=True, x=0.45,y=1))
    fig.update_traces(textposition='outside',width=width)

    fig.add_annotation(
        x=0.1,
        y=1.2,
        xref="paper",
        yref="paper",
        text=f"Illumina: {data[data.Type=='Illumina']['Sample Count'].sum()}",
        showarrow=False,
        font=dict(
            family="Courier New, monospace",
            size=20,
            color="#e9ff32"
            ),
        align="center",
        ax=20,
        ay=-30,
        bordercolor="#c7c7c7",
        borderwidth=1,
        borderpad=4,
        bgcolor="#0E1117",
        opacity=1
        )
    
    fig.add_annotation(
        x=0.8,
        y=1.2,
        xref="paper",
        yref="paper",
        text=f"Pacbio: {data[data.Type=='Pacbio']['Sample Count'].sum()}",
        showarrow=False,
        font=dict(
            family="Courier New, monospace",
            size=20,
            color="#e9ff32"
            ),
        align="center",
        ax=20,
        ay=-30,
        bordercolor="#c7c7c7",
        borderwidth=1,
        borderpad=4,
        bgcolor="#0E1117",
        opacity=1
        )
    return fig

def illumina_chart(data,color,width):
    fig = px.bar(data.sort_values(['NGS Type','Total Cell']), x='Experiment', y='Total Cell', color='NGS Type',color_discrete_sequence=color,text='Total Cell',)
    fig.update_layout(width=400,
                      height=400,
                      font=dict(size=30),
                      legend=dict(orientation='h',yanchor='bottom',xanchor='right',xref='paper',yref='paper',y=-0.2,x=0.65,font=dict(size=8),title=''),
                      yaxis=dict(tickfont=dict(size=12),range=[0, data['Total Cell'].max() * 1.2]),
                      xaxis=dict(tickfont=dict(size=7)),
                      hovermode=False,
                      bargap=0.3,
                      xaxis_title=None,
                      title=dict(text='Illumina',font=dict(size=25), automargin=True, x=0.4,y=1))
    fig.update_traces(textposition='outside',width=width)

    fig.add_annotation(
        x=0.1,
        y=1.1,
        xref="paper",
        yref="paper",
        text=f"MiSeq: {data[data['NGS Type'] == 'Illumina MiSeq']['Total Cell'].sum()}",
        showarrow=False,
        font=dict(
            family="Courier New, monospace",
            size=18,
            color="#e9ff32"
            ),
        align="center",
        ax=20,
        ay=-30,
        bordercolor="#c7c7c7",
        borderwidth=1,
        borderpad=4,
        bgcolor="#0E1117",
        opacity=1
        )
    
    fig.add_annotation(
        x=0.6,
        y=1.1,
        xref="paper",
        yref="paper",
        text=f"NovaSeq: {data[data['NGS Type'] == 'Illumina NovaSeq']['Total Cell'].sum()}",
        showarrow=False,
        font=dict(
            family="Courier New, monospace",
            size=18,
            color="#e9ff32"
            ),
        align="center",
        ax=20,
        ay=-30,
        bordercolor="#c7c7c7",
        borderwidth=1,
        borderpad=4,
        bgcolor="#0E1117",
        opacity=1
        )
    return fig

def pacbio_chart(data,color,width):
    data = data[data['Total Cell'] != 0]
    data['Job Name'] = data.apply(lambda row: row['Job Name'][4:],axis=1)
    fig = px.bar(data.sort_values(['Machine Type','Total Cell']), 
                 x='Job Name', y='Total Cell', 
                 color='Machine Type',
                 color_discrete_sequence=color,
                 text='Total Cell',
                 barmode = 'group')
    legend_x_pos = 0.75 if len(data['Machine Type'].unique()) == 3 else 0.63
    fig.update_layout(width=400,
                      height=400,
                      font=dict(size=40),
                      legend=dict(orientation='h',yanchor='bottom',xanchor='right',yref='paper',xref='paper',y=-0.2,x=legend_x_pos,font=dict(size=8),title=''),
                      yaxis=dict(tickfont=dict(size=12),range=[0, data['Total Cell'].max() * 1.2]),
                      xaxis=dict(tickfont=dict(size=8)),
                      hovermode=False,
                      xaxis_title=None,
                      title=dict(text='Pacbio',font=dict(size=25), automargin=True, x=0.4,y=1))
    fig.update_traces(textposition='outside',width=width)

    x = []
    if len(data['Machine Type'].unique()) == 1:
        x = [0.45]
    elif len(data['Machine Type'].unique()) == 2:
        x=[0.25,0.65]
    else:
        x=[0.05,0.45,0.9]
    x_ind = 0
    for i in data['Machine Type'].unique():
        fig.add_annotation(
            x=x[x_ind],
            y=1.1,
            xref="paper",
            yref="paper",
            text=f"{i[7:]}: {data[data['Machine Type'] == i]['Total Cell'].sum()}",
            showarrow=False,
            font=dict(
                family="Courier New, monospace",
                size=13,
                color="#e9ff32"
                ),
            align="center",
            ax=20,
            ay=-30,
            bordercolor="#c7c7c7",
            borderwidth=1,
            borderpad=4,
            bgcolor="#0E1117",
            opacity=1
            )
        x_ind += 1

    return fig

def reagent_chart(data,color,width):
    data['Quantity'] = data.apply(lambda row: float(row['Qty Made'].strip('L ')),axis=1)
    data = data.groupby('Buffer Name')[['Quantity']].sum().reset_index()
    fig = px.bar(data, x='Buffer Name', y='Quantity', color='Buffer Name',color_discrete_sequence=color,text='Quantity',)
    fig.update_layout(width=400,
                      height=400,
                      font=dict(size=32),
                      legend=dict(orientation='h',yanchor='bottom',xanchor='right',y=-0.25,x=0.7,font=dict(size=16)),
                      yaxis=dict(tickfont=dict(size=15),range=[0, data['Quantity'].max() * 1.3]),
                      xaxis=dict(tickfont=dict(size=8)),
                      hovermode=False,
                      xaxis_title=None,
                      yaxis_title = 'Quantity (L)',
                      showlegend=False,
                      title=dict(text='Reagent',font=dict(size=25), automargin=True, x=0.4,y=1))
    fig.update_traces(textposition='outside',width=width)
    return fig

def repeat_chart(data, machine_type):
    gene_list = ['A','B','C','DRB1','DRB345','DQB1','DQA1','DPB1','DPA1','Overall']
    ngs_cap = pd.read_csv('Functions/Repeats/ngs_cap.csv')
    pac_cap = pd.read_csv('Functions/Repeats/pac_cap.csv')
    ngs_avg = pd.read_csv('Functions/Repeats/ngs_avg.csv')
    pac_avg = pd.read_csv('Functions/Repeats/pac_avg.csv')
    column_list_exp = []
    for i in gene_list:
        column_list_exp.append(i+': Total')
        column_list_exp.append(i+': Repeat')
        column_list_exp.append(i+'%')
        column_list_exp.append(i)

    def get_statistics_by_experiment(data):
        df_list = []
        ngs_data = [x for x in data if x[4] == 'NGS' or x[6] == '1KB']
        pac_data = [x for x in data if x[4] == 'Pacbio' and x[6] == '4XALL']
        for data in [ngs_data,pac_data]:
            per_category = {i:{'Total':0,'Repeat':0} for i in gene_list}
            by_exp = {i:copy.deepcopy(per_category) for i in ([i[0] for i in data])}
            for i in data:
                for j in i[1]:
                    by_exp[i[0]][j]['Total'] += 1
                for j in i[2]:
                    if j != '':
                        by_exp[i[0]][j]['Repeat'] += 1
                
                if i[1] != ['']:
                    by_exp[i[0]]['Overall']['Total'] += 1
                if i[2] != ['']:
                    by_exp[i[0]]['Overall']['Repeat'] += 1
            
            exp_rows = []
            for i in by_exp:
                temp = [i]
                for j in by_exp[i]:
                    for k in by_exp[i][j]:
                        temp.append(by_exp[i][j][k])
                    if by_exp[i][j]['Total'] != 0:
                        temp.append(round(by_exp[i][j]['Repeat'] / by_exp[i][j]['Total'] * 100,2))
                    else:
                        temp.append(np.nan)
                    temp.append(str(by_exp[i][j]['Repeat'])+'/'+str(by_exp[i][j]['Total']))
                    
                exp_rows.append(temp)
            
            df_exp = pd.DataFrame(exp_rows,columns=['Experiment']+column_list_exp).sort_values(by='Experiment').set_index('Experiment')      
            df_list.append(df_exp)

        return df_list

    df_weekly = get_statistics_by_experiment(data)[0] if machine_type =='NGS' else get_statistics_by_experiment(data)[1]
    data = [x for x in data if x[4] == machine_type]

    cap = ngs_cap if machine_type == 'NGS' else pac_cap
    avg = ngs_avg if machine_type == 'NGS' else pac_avg
    weekly_avg = df_weekly[[i+'%' for i in gene_list]].mean().reset_index()
    weekly_avg.rename(columns={0:'Repeat Rate','index':'Gene'},inplace=True)
    weekly_avg['Gene'] = weekly_avg.apply(lambda row: row['Gene'].strip('% '),axis=1)
    weekly_avg['Repeat Rate'] = weekly_avg.apply(lambda row: round(row['Repeat Rate'],2),axis=1)
    max_value = weekly_avg['Repeat Rate'].max() if weekly_avg['Repeat Rate'].max() > avg.Mean.max() else avg.Mean.max()

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=weekly_avg.Gene,
        y=weekly_avg['Repeat Rate'],
        text=weekly_avg['Repeat Rate'],
        name='Repeat Rate',
        marker_color='indianred'
    ))
    fig.add_trace(go.Bar(
        x=avg.Gene,
        y=avg['Mean'],
        text=avg['Mean'],
        name='Mean',
        marker_color='#0096FF'
    ))
    
    fig.update_layout(xaxis={'categoryorder':'array','categoryarray':gene_list,'title':'','tickfont':dict(size=15)},
                      yaxis=dict(range=[0, math.ceil(max_value)],tickfont=dict(size=10)), 
                      legend=dict(orientation='h',yanchor='bottom',xanchor='right',xref='paper',yref='paper',y=-0.25,x=0.6,font=dict(size=10),title='')
                      ,width=400,height=400,hovermode=False,
                      title=dict(text=f"Repeat ({machine_type})",font=dict(size=25), x=0.35,y=1))#bargap=0.1
    fig.update_traces(width=0.27,textposition='outside',textfont_size=24)
    
    return fig

def new_allele_chart(data):
    gene_order = ['A','B','C','DRB1','DRB3','DRB4','DRB5','DQB1','DQA1','DPB1','DPA1']
    def get_gene_count(data):
        gene_count = {}
        for i in data:
            for j in data[i]:
                if i not in gene_count:
                    gene_count[i] = 1
                else:
                    gene_count[i]+=1

        return {k: gene_count[k] for k in gene_order if k in gene_count}
    gene_count = get_gene_count(data)
    pie = go.Figure(go.Pie(labels=list(gene_count.keys()), values= list(gene_count.values()), textfont_size=30, hole=.3,textinfo='label+value',
                                 textposition='inside',insidetextorientation='horizontal',hovertemplate = 'Gene: %{label}'+'<br>Count: %{value}',name='',
                                 marker_colors=st.session_state.color))
    pie.update_layout(width=400,height=400,showlegend=False,hoverlabel=dict(font_size=24),
                      title=dict(text='New Allele',font=dict(size=25), automargin=True, x=0.38,y=1))
    pie.update_traces(sort=False,direction="counterclockwise",marker=dict(colors=st.session_state.color, line=dict(color='#000000', width=2)))
    return pie
