import plotly.express as px

def generate_buffer_bar_chart(df):
    modified_df = df.copy()
    modified_df['Qty Made'] = modified_df.apply(lambda row: float(row['Qty Made'].strip('L ')),axis=1)
    modified_df = modified_df.groupby('Buffer Name')[['Qty Made']].sum().reset_index()

    fig = px.bar(modified_df.sort_values('Qty Made',ascending=False), x='Buffer Name', y='Qty Made',text='Qty Made',)

    fig.update_layout(width=1600,
                      height=500,
                      bargap=0.8,
                      font=dict(size=40,color='black'),
                      legend=dict(orientation='h',yanchor='bottom',xanchor='right',y=-0.25,x=0.7,font=dict(size=16)),
                      yaxis=dict(tickfont=dict(size=20,color='black'),range=[0, modified_df['Qty Made'].max() * 1.3]),
                      xaxis=dict(tickfont=dict(size=24,color='black')),
                      hovermode=False,
                      xaxis_title=None,
                      yaxis_title = 'Quantity (L)',
                      showlegend=False)
    
    fig.update_traces(marker_line_color='black', 
                      marker_line_width=2.5,
                      textposition='outside')
    
    return fig

def style_buffer_table(df):
    modified_df = df.sort_values(by='Make Date').reset_index(drop=True)
    modified_df.index += 1
    return modified_df.style.set_table_styles(
        [
            {'selector': 'th.col_heading', 'props': 'background-color: gray; color: white;'},
            {'selector': 'th.row_heading', 'props': 'background-color: #FCF5E5; color: black;'},
            {'selector': 'td', 'props': [('border', '2px solid black')]},
            {'selector': 'th', 'props': [('border', '2px solid black')]},
            {'selector': 'td:nth-child(7)','props':[('font-weight','bold')]},
            {'selector': 'td:nth-child(2)', 'props': [('background-color', '#FCF5E5'), ('color', 'black')]},
            {'selector': 'td:nth-child(3)', 'props': [('background-color', '#FCF5E5'), ('color', 'black')]},
            {'selector': 'td:nth-child(4)', 'props': [('background-color', '#FCF5E5'), ('color', 'black')]},
            {'selector': 'td:nth-child(5)', 'props': [('background-color', '#FCF5E5'), ('color', 'black')]},
            {'selector': 'td:nth-child(6)', 'props': [('background-color', '#FCF5E5'), ('color', 'black')]},
            {'selector': 'td:nth-child(7)', 'props': [('background-color', '#FCF5E5'), ('color', 'black')]},
            {'selector': 'td:nth-child(8)', 'props': [('background-color', '#FCF5E5'), ('color', 'black')]},
            {'selector': 'td:nth-child(9)', 'props': [('background-color', '#FCF5E5'), ('color', 'black')]}
        ])

def generate_primer_bar_chart(df):

    def assign_color(row):
        if 'ILU' in row or 'Illumina' in row:
            return '#E63946'
        else:
            if 'Index' in row:
                if 'PAC' in row or 'PacBio' in row:
                    return '#91B8D5'
                else:
                    return '#F4A261'
            else:
                if 'PAC' in row or 'PacBio' in row:
                    return '#457B9D'
                else:
                    return 'gray'
        
    modified_df = df.copy()
    modified_df['Qty Made'] = modified_df.apply(lambda row: float(row['Qty Made'].strip('ml ')),axis=1)
    modified_df = modified_df.groupby('Primer Name')[['Qty Made']].sum().reset_index()
    modified_df['Color'] = modified_df.apply(lambda row: assign_color(row['Primer Name']),axis=1)
    modified_df = modified_df.sort_values(['Color','Qty Made'],ascending=False)
    color_map = {i:assign_color(i) for i in modified_df['Primer Name']}

    fig = px.bar(modified_df, 
                 x='Primer Name', 
                 y='Qty Made', 
                 text='Qty Made',
                 color='Primer Name',
                 color_discrete_map=color_map)
    
    fig.update_layout(width=1600,
                      height=500,
                      bargap = 0.8,
                      font=dict(size=60,color='black'),
                      legend=dict(orientation='h',yanchor='bottom',xanchor='right',y=-0.25,x=0.7,font=dict(size=16)),
                      yaxis=dict(tickfont=dict(size=20,color='black'),range=[0, modified_df['Qty Made'].max() * 1.3]),
                      xaxis=dict(tickfont=dict(size=20,color='black')),
                      hovermode=False,
                      xaxis_title=None,
                      yaxis_title = 'Quantity (ml)',
                      showlegend=False)
    
    fig.update_traces(marker_line_color='black', 
                      marker_line_width=2.5,
                      textposition='outside')
    
    return fig

def style_primer_table(df):
    modified_df = df.sort_values(by='Make Date').reset_index(drop=True)
    modified_df.index += 1
    return modified_df.style.set_table_styles(
        [
            {'selector': 'th.col_heading', 'props': 'background-color: gray; color: white;'},
            {'selector': 'th.row_heading', 'props': 'background-color: #FCF5E5; color: black;'},
            {'selector': 'td', 'props': [('border', '2px solid black')]},
            {'selector': 'th', 'props': [('border', '2px solid black')]},
            {'selector': 'td:nth-child(7)','props':[('font-weight','bold')]},
            {'selector': 'td:nth-child(2)', 'props': [('background-color', '#FCF5E5'), ('color', 'black')]},
            {'selector': 'td:nth-child(3)', 'props': [('background-color', '#FCF5E5'), ('color', 'black')]},
            {'selector': 'td:nth-child(4)', 'props': [('background-color', '#FCF5E5'), ('color', 'black')]},
            {'selector': 'td:nth-child(5)', 'props': [('background-color', '#FCF5E5'), ('color', 'black')]},
            {'selector': 'td:nth-child(6)', 'props': [('background-color', '#FCF5E5'), ('color', 'black')]},
            {'selector': 'td:nth-child(7)', 'props': [('background-color', '#FCF5E5'), ('color', 'black')]},
            {'selector': 'td:nth-child(8)', 'props': [('background-color', '#FCF5E5'), ('color', 'black')]},
            {'selector': 'td:nth-child(9)', 'props': [('background-color', '#FCF5E5'), ('color', 'black')]},
            {'selector': 'td:nth-child(10)', 'props': [('background-color', '#FCF5E5'), ('color', 'black')]}
        ])

def generate_dispense_bar_chart(df):
    
    def assign_color(row):
        if 'ILU' in row or 'Illumina' in row:
            return '#E63946'
        else:
            if 'Index' in row:
                if 'PAC' in row or 'PacBio' in row:
                    return '#91B8D5'
                else:
                    return '#F4A261'
            else:
                if 'PAC' in row or 'PacBio' in row:
                    return '#457B9D'
                else:
                    return 'gray'
    
    modified_df = df.groupby('Primer Name')[['# of Plates']].sum().reset_index()
    modified_df['Color'] = modified_df.apply(lambda row: assign_color(row['Primer Name']),axis=1)
    modified_df = modified_df.sort_values(by=['Color','# of Plates'],ascending=[True,False])
    color_map = {i:assign_color(i) for i in modified_df['Primer Name']}

    fig = px.bar(modified_df, 
                 x='Primer Name', y='# of Plates',
                 color='Primer Name',
                 text='# of Plates',
                 color_discrete_map=color_map)
    
    fig.update_layout(width=1600,
                      height=500,
                      bargap=0.25,
                      font=dict(size=40,color='black'),
                      legend=dict(orientation='h',yanchor='bottom',xanchor='right',y=-0.25,x=0.7,font=dict(size=16)),
                      yaxis=dict(tickfont=dict(size=20,color='black'),range=[0, modified_df['# of Plates'].max() * 1.3]),
                      xaxis=dict(tickfont=dict(size=12,color='black')),
                      hovermode=False,
                      xaxis_title=None,
                      showlegend=False)
    
    fig.update_traces(marker_line_color='black', 
                      marker_line_width=2.5,
                      textposition='outside')
    
    return fig

def style_dispense_table(df):
    modified_df = df.sort_values(by='Dispense Date').reset_index(drop=True)
    modified_df.index += 1
    return modified_df.style.set_table_styles(
        [
            {'selector': 'th.col_heading', 'props': 'background-color: gray; color: white;'},
            {'selector': 'th.row_heading', 'props': 'background-color: #FCF5E5; color: black;'},
            {'selector': 'td', 'props': [('border', '2px solid black')]},
            {'selector': 'th', 'props': [('border', '2px solid black')]},
            {'selector': 'td:nth-child(7)','props':[('font-weight','bold')]},
            {'selector': 'td:nth-child(2)', 'props': [('background-color', '#FCF5E5'), ('color', 'black')]},
            {'selector': 'td:nth-child(3)', 'props': [('background-color', '#FCF5E5'), ('color', 'black')]},
            {'selector': 'td:nth-child(4)', 'props': [('background-color', '#FCF5E5'), ('color', 'black')]},
            {'selector': 'td:nth-child(5)', 'props': [('background-color', '#FCF5E5'), ('color', 'black')]},
            {'selector': 'td:nth-child(6)', 'props': [('background-color', '#FCF5E5'), ('color', 'black')]},
            {'selector': 'td:nth-child(7)', 'props': [('background-color', '#FCF5E5'), ('color', 'black')]},
            {'selector': 'td:nth-child(8)', 'props': [('background-color', '#FCF5E5'), ('color', 'black')]},
            {'selector': 'td:nth-child(9)', 'props': [('background-color', '#FCF5E5'), ('color', 'black')]},
            {'selector': 'td:nth-child(10)', 'props': [('background-color', '#FCF5E5'), ('color', 'black')]}
        ])

def generate_master_bar_chart(df):
    modified_df = df.copy()
    modified_df['Qty Made'] = modified_df.apply(lambda row: float(row['Qty Made'].strip('L ')),axis=1)
    modified_df = modified_df.groupby('Master Mix Name')[['Qty Made']].sum().reset_index()

    fig = px.bar(modified_df.sort_values('Qty Made',ascending=False), 
                 x='Master Mix Name', 
                 y='Qty Made',
                 text='Qty Made')
    
    fig.update_layout(width=1600,
                      height=600,
                      bargap = 0.95,
                      font=dict(size=40,color='black'),
                      legend=dict(orientation='h',yanchor='bottom',xanchor='right',y=-0.25,x=0.7,font=dict(size=16)),
                      yaxis=dict(tickfont=dict(size=20,color='black'),range=[0, modified_df['Qty Made'].max() * 1.1]),
                      xaxis=dict(tickfont=dict(size=24,color='black')),
                      hovermode=False,
                      xaxis_title=None,
                      yaxis_title='Quantity (L)',
                      showlegend=False)
    
    fig.update_traces(marker_line_color='black', 
                      marker_line_width=2.5,
                      textposition='outside')
    
    return fig

def style_master_table(df):
    modified_df = df.sort_values(by='Make Date').reset_index(drop=True)
    modified_df.index += 1
    return modified_df.style.set_table_styles(
        [
            {'selector': 'th.col_heading', 'props': 'background-color: gray; color: white;'},
            {'selector': 'th.row_heading', 'props': 'background-color: #FCF5E5; color: black;'},
            {'selector': 'td', 'props': [('border', '2px solid black')]},
            {'selector': 'th', 'props': [('border', '2px solid black')]},
            {'selector': 'td:nth-child(7)','props':[('font-weight','bold')]},
            {'selector': 'td:nth-child(2)', 'props': [('background-color', '#FCF5E5'), ('color', 'black')]},
            {'selector': 'td:nth-child(3)', 'props': [('background-color', '#FCF5E5'), ('color', 'black')]},
            {'selector': 'td:nth-child(4)', 'props': [('background-color', '#FCF5E5'), ('color', 'black')]},
            {'selector': 'td:nth-child(5)', 'props': [('background-color', '#FCF5E5'), ('color', 'black')]},
            {'selector': 'td:nth-child(6)', 'props': [('background-color', '#FCF5E5'), ('color', 'black')]},
            {'selector': 'td:nth-child(7)', 'props': [('background-color', '#FCF5E5'), ('color', 'black')]},
            {'selector': 'td:nth-child(8)', 'props': [('background-color', '#FCF5E5'), ('color', 'black')]},
            {'selector': 'td:nth-child(9)', 'props': [('background-color', '#FCF5E5'), ('color', 'black')]},
            {'selector': 'td:nth-child(10)', 'props': [('background-color', '#FCF5E5'), ('color', 'black')]}
        ])