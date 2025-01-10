from datetime import timedelta, datetime
import pandas as pd
import plotly.express as px 
import plotly.graph_objects as go
from Functions.Visualization.utility import st_write, generate_markdown
from Files.common_list import delay_status_color_code, comment_color_code

pd.options.mode.chained_assignment = None

def generate_sample_statistics(df,col,loc):
    col1,col2,graph = loc.columns([3.5,3.5,6],border=True)
    due = 'ReportWithinTATCount' if col == 'TAT' else 'ReportWithinFinalCount'
    total = df.Total.sum()
    delay = df[(df['Delay Status'] == 'Delayed') & (df['Comment Category'] != 'Hold Report')].Total.sum() - df[(df['Delay Status'] == 'Delayed') & (df['Comment Category'] != 'Hold Report')][due].sum()
    completed = df[(df['Delay Status'] == 'Completed')&(df['Comment Category'] != 'Hold Report')].Total.sum() + df[(df['Delay Status'] == 'Delayed') & (df['Comment Category'] != 'Hold Report')][due].sum()
    hold = df[df['Comment Category'] == 'Hold Report'].Total.sum()

    modified_df = pd.DataFrame([[completed,'Completed'],[delay,'Delayed'],[hold,'Hold Report']],columns=['Count','Delay Status'])
    modified_df = modified_df[modified_df.Count != 0]

    pie = go.Figure(data=[go.Pie(labels=modified_df['Delay Status'].unique(),
                                 values=modified_df['Count'],
                                 textinfo='label+percent',
                                 insidetextorientation='horizontal',
                                 textposition='auto',
                                 domain=dict(x=[0.3,0.99]))])
    
    pie.update_layout(hovermode=False,
                      width=600,
                      height=600,
                      showlegend=False)
    
    pie.update_traces(textfont_size=28,
                      marker=dict(colors=[delay_status_color_code[label] for label in modified_df['Delay Status'].unique()],
                                  line=dict(color='#000000', width=4)))

    st_write(col1,7)
    col1.write(generate_markdown(text='Total',font_size=25,font_color='#f9423a'), unsafe_allow_html=True)
    col1.write(generate_markdown(text=total,font_size=100,font_color='black'), unsafe_allow_html=True)
    col1.write(generate_markdown(text='Delayed',font_size=25,font_color='#f9423a'), unsafe_allow_html=True)
    col1.write(generate_markdown(text=delay,font_size=100,font_color='black'), unsafe_allow_html=True)

    st_write(col2,7)
    col2.write(generate_markdown(text='Completed',font_size=25,font_color='#f9423a'), unsafe_allow_html=True)
    col2.write(generate_markdown(text=completed,font_size=100,font_color='black'), unsafe_allow_html=True)
    col2.write(generate_markdown(text='Ext/Hold',font_size=25,font_color='#f9423a'), unsafe_allow_html=True)
    col2.write(generate_markdown(text=hold,font_size=100,font_color='black'), unsafe_allow_html=True)

    graph.plotly_chart(pie,use_container_width=True,key=col+str(loc))

def generate_shipment_statistics(df,loc):
    col1,col2,graph = loc.columns([3.5,3.5,6],border=True)

    modified_df = pd.DataFrame([[len(df[df['Delay Status'] == 'Completed']),'Completed'],
                                [len(df[(df['Delay Status'] == 'Delayed') & (df['Comment Category'] != 'Extended') & (df['Comment Category'] != 'Hold Report')]),'Delayed'],
                                [len(df[(df['Delay Status'] == 'Delayed') & (df['Comment Category'] == 'Extended') | (df['Comment Category'] == 'Hold Report')]),'Hold Report']]
                                ,columns=['Count','Delay Status'])
    modified_df = modified_df[modified_df['Count'] != 0]

    pie = go.Figure(data=[go.Pie(labels=modified_df['Delay Status'],
                                 values=modified_df['Count'],
                                 textinfo='label+percent',
                                 insidetextorientation='horizontal',
                                 domain=dict(x=[0.3,0.99]))])
    
    pie.update_layout(hovermode=False,
                      width=600,
                      height=600,
                      showlegend=False)
    
    pie.update_traces(textfont_size=30,
                      marker=dict(colors=[delay_status_color_code[label] for label in modified_df['Delay Status'].unique()],
                                  line=dict(color='#000000', width=4)))
    
    st_write(col1,6)
    col1.write(generate_markdown(text='Shipment',font_size=25,font_color='#f9423a'), unsafe_allow_html=True)
    col1.write(generate_markdown(text=len(df),font_size=120,font_color='black'), unsafe_allow_html=True)
    col1.write(generate_markdown(text='Delayed',font_size=25,font_color='#f9423a'), unsafe_allow_html=True)
    if len(df[(df['Delay Status'] == 'Delayed') & (df['Comment Category'] != 'Extended') & (df['Comment Category'] != 'Hold Report')]) != 0:
        col1.write(generate_markdown(text=len(df[(df['Delay Status'] == 'Delayed') & (df['Comment Category'] != 'Extended') & (df['Comment Category'] != 'Hold Report')]),font_size=120,font_color='black'), unsafe_allow_html=True)
    else:
        col1.write(generate_markdown(text=0,font_size=120,font_color='black'), unsafe_allow_html=True)
    
    st_write(col2,6)
    col2.write(generate_markdown(text='Completed',font_size=25,font_color='#f9423a'), unsafe_allow_html=True)
    if len(df[df['Delay Status'] == 'Completed']) != 0:
        col2.write(generate_markdown(text=len(df[df['Delay Status'] == 'Completed']),font_size=120,font_color='black'), unsafe_allow_html=True)
    else:
        col2.write(generate_markdown(text=0,font_size=120,font_color='black'), unsafe_allow_html=True)

    col2.write(generate_markdown(text='Ext / Hold',font_size=25,font_color='#f9423a'), unsafe_allow_html=True)
    if len(df[(df['Delay Status'] == 'Delayed') & (df['Comment Category'] == 'Extended') | (df['Comment Category'] == 'Hold Report')]) != 0:
        col2.write(generate_markdown(text=len(df[(df['Delay Status'] == 'Delayed') & (df['Comment Category'] == 'Extended') | (df['Comment Category'] == 'Hold Report')]),font_size=120,font_color='black'), unsafe_allow_html=True)
    else:
        col2.write(generate_markdown(text=0,font_size=120,font_color='black'), unsafe_allow_html=True)

    graph.plotly_chart(pie,use_container_width=True,key=str(col1)+str(loc))

def set_height(df):
    length = len(df['Project Name'].unique())
    # height / yaxis / textsize / legend font size
    return 150 + 45 * length, 25 - (length*0.4), 10.5, -0.2 if length > 5 else -1

def make_timeline(df,lw,tw,switch,col):

    def add_time(df,col):
        columns_to_check = ['Project Name', col,'Gene']
        temp = df[df.duplicated(subset=columns_to_check, keep=False)]
        temp = temp.groupby(['Project Name',col])['Gene'].count()
        temp = temp.reset_index().values.tolist()
        duplicates = {}
        for i in temp:
            if i[0] not in duplicates:
                duplicates[i[0]] = {i[1]:[i[2], datetime.combine(i[1],datetime.min.time()) - timedelta(hours=11)]}
            else:
                duplicates[i[0]][i[1]] = [i[2], datetime.combine(i[1],datetime.min.time()) - timedelta(hours=11)]

        start = []
        end = []
        for index,row in df.iterrows():
            if row['Project Name'] not in duplicates:
                start.append(datetime.combine(row[col], datetime.min.time()) - timedelta(hours=11))
                end.append(datetime.combine(row[col], datetime.min.time()) + timedelta(hours=11))
            else:
                if row[col] not in duplicates[row['Project Name']]:
                    start.append(datetime.combine(row[col], datetime.min.time()) - timedelta(hours=11))
                    end.append(datetime.combine(row[col], datetime.min.time()) + timedelta(hours=11))
                else:
                    divide = duplicates[row['Project Name']][row[col]][0]
                    individual_hour = (22 - (divide-1)*0.5)/ divide
                    begin_time = duplicates[row['Project Name']][row[col]][1]
                    start.append(begin_time)
                    end.append(begin_time+timedelta(hours=individual_hour))
                    duplicates[row['Project Name']][row[col]][1] = begin_time + timedelta(hours=individual_hour) + timedelta(hours=0.5)

        df['Start'] = start
        df['Finish'] = end
        return df
    
    def add_filler(df,lw,tw,col):
        def days_between(start_date, end_date):
            days = []
            current_date = start_date
            while current_date <= end_date:
                days.append(current_date)
                current_date += timedelta(days=1)
            return set(days)

        day_set = days_between(lw, tw)
        for i in day_set.difference(set(df[col].unique())):
            df = pd.concat([df, pd.DataFrame([{col:i,'Delay Status':'','Comment Category':'','Client Name':df['Client Name'].iloc[0],
                                                'Project Name':df['Project Name'].iloc[0],'Gene':df.Gene.iloc[0]}])], ignore_index=True)

        return df

    #df = add_filler(df,lw,tw,col)
    df = add_time(df,col)
    height, yaxis_size, textsize,legend_font_size = set_height(df)
    color = 'Comment Category' if switch else 'Delay Status'
    color_map = comment_color_code if switch else {'Completed':'#313695','Delayed':'#a50026','':'#0e1117'}
    textcolor= 'white'
    if switch == True:
        df['Comment Category'] = df.apply(lambda row: '' if row['Comment Category'] == 'Completed' else row['Comment Category'],axis=1)

    timeline = px.timeline(df, x_start="Start", x_end="Finish", y='Project Name',text = 'Display Text', 
                           height=height,color=color,color_discrete_map = color_map,
                           category_orders={'Project Name': sorted(df['Project Name'].unique(),reverse=True,key=lambda x: x.lower())},)
    timeline.update_xaxes(tickformat="%m/%d")
    timeline.update_yaxes(autorange="reversed")
    timeline.update_layout(font=dict(size=textsize),
                           xaxis=dict(tickfont=dict(size=30,color='black')),
                           yaxis=dict(tickfont=dict(size=yaxis_size,color='black')),
                           legend=dict(font=dict(size=14),orientation='h',x=0,y=legend_font_size,title=''),
                           showlegend=True,
                           hoverlabel=dict(font_size=16))
    
    timeline.update_traces(textfont_color=textcolor)
    if not switch:
        timeline.update_traces(marker_line_color='black',
                           marker_line_width=1.5)

    return timeline

def make_comment(df,col):

    def combine_comment(row):
        if row['ReportSubComments'] != None and row['ReportSubComments'] != '' and row['Comment'] != None and row['Comment'] != '':
            return str(row['ReportSubComments']) + '/' + str(row['Comment'])
        else:
            if row['ReportSubComments'] != None and row['ReportSubComments'] != '' and (row['Comment'] == None or row['Comment'] == ''):
                return row['ReportSubComments']
            elif (row['ReportSubComments'] == None or row['ReportSubComments'] == '') and row['Comment'] != None and row['Comment'] != '':
                return row.Comment
            else:
                return None
 
    due = 'ReportWithinTATCount' if col == 'TAT' else 'ReportWithinFinalCount'
    report_percentage = 'TAT Report %' if col == 'TAT' else 'Final Report %'
    modified_df = df[(df['Delay Status'] != 'Completed') & (df['Comment Category'] != 'Extended')]
    modified_df['Comment'] = modified_df.apply(lambda row: combine_comment(row),axis=1)
    modified_df = modified_df[['Comment Category','Project Name','Shipment Date',col,'Comment','TotalinShipment','Total',due,report_percentage,'Reported','Today Report %']]
    modified_df = modified_df.rename(columns={'TotalinShipment':'Shipment','ReportWithinTATCount':'Reported by Due','TAT Report %':'% by Due','Reported':'Reported by Today','Today Report %':'% by Today'})
    modified_df = modified_df.sort_values(by=['Comment Category','Shipment Date']).reset_index(drop=True)
    modified_df.index += 1 

    def add_color_by_type(row):
        if row['Comment Category'] in ['Hold Report','Others','Not Commented']:
            return ['background-color: ' + comment_color_code.get(row['Comment Category'], 'black')+';color: white'] + ['']*(len(row)-1)
        else:
            return ['background-color: ' + comment_color_code.get(row['Comment Category'], 'white')] + ['']*(len(row)-1)

    return modified_df.style.apply(add_color_by_type,axis=1).set_table_styles(
    [
        {'selector': 'th.col_heading', 'props': 'background-color: gray; color: white;'},
        {'selector': 'th.row_heading', 'props': 'background-color: #FCF5E5; color: black;'},
        {'selector': 'td', 'props': [('border', '2px solid black'),('font-size','20px')]},
        {'selector': 'th', 'props': [('border', '2px solid black')]},
        {'selector': 'td:nth-child(8)','props':[('font-weight','bold')]},
        {'selector': 'td:nth-child(9)','props':[('font-weight','bold')]},
        {'selector': 'td:nth-child(10)','props':[('font-weight','bold')]},
        {'selector': 'td:nth-child(11)','props':[('font-weight','bold')]},
        {'selector': 'td:nth-child(12)','props':[('font-weight','bold')]},
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
        {'selector': 'td:nth-child(13)', 'props': [('background-color', '#FCF5E5'), ('color', 'black')]},
        {'selector': 'td:nth-child(14)', 'props': [('background-color', '#FCF5E5'), ('color', 'black')]},

    ])
 