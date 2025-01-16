from pytz import timezone
import pandas as pd
import streamlit as st 
import plotly.express as px 
import plotly.graph_objects as go 
from Functions.Visualization.New_Allele_Visualization import gene_statistics, name_lengthen, name_shorten, ars_statistics, \
get_gene_count, new_allele_pattern, edit_new_allele_pattern, static_comment_generator, no_data
from Functions.Visualization.New_Allele_Visualization2 import get_offset, generate_new_index, first_viz, second_viz, third_viz, \
info_writer, get_codon_dict, reference_writer, style_tabular_data, style_tabular_data2
from Functions.Visualization.utility import st_write, generate_markdown, generate_header

tz = timezone('EST')
color = {'3':'red','5':'red','I':'royalblue','E':'orange'}
facecolor = {'P':'lime','D':'orangered','I':'skyblue'}
gene_order = ['A','B','C','DRB1','DRB3','DRB4','DRB5','DQB1','DQA1','DPB1','DPA1']
st.set_page_config(page_title="New Allele Visualization", layout="wide",initial_sidebar_state='collapsed')
st.markdown("""
        <style>
               .block-container {
                    padding-top: 2rem;
                }
        </style>
        """, unsafe_allow_html=True)
st.logo('MyLogo.png')
gene_location, gene_codon, data, border,non_border,table = st.session_state['New Allele']
st.session_state.data, st.session_state.gl, st.session_state.gc = data, gene_location, gene_codon
if 'data' not in st.session_state:
    st.stop()
if len(st.session_state.data[2]) == 0:
    no_data()
gene_count = get_gene_count(st.session_state.data[0])
df_gene = gene_statistics(st.session_state.data[2])
df_ars = ars_statistics(st.session_state.data[2])
nap,m_d = new_allele_pattern(st.session_state.data[1], st.session_state.gl)
codon_dict = get_codon_dict()
protein_dict = {}
for i in [[v,k] for k, v in codon_dict.items()]:
    if i[0] not in protein_dict:
        protein_dict[i[0]] = [i[1]]
    else:
        protein_dict[i[0]].append(i[1])

sidebar = st.sidebar
show_all_button,on_button = sidebar.columns(2)
show_all = show_all_button.toggle('Show All')
on = on_button.toggle('Visualize')

if not on: 
    generate_header(title='New Allele',
                    prev="pages/11_Non_HLA_TAT.py",
                    status_prev='Non-HLA TAT status')

    details = st.expander('Details..')
    d1,d2,d3 = details.columns(3)
    nap_gene = d1.selectbox('Gene',['All']+list(nap.Gene.unique()))
    nap_type = d2.selectbox('Type',['All']+list(nap.Type.unique()))
    d31,d32,d33,d34 = d3.columns(4)
    d31.markdown(f"<h1 style='text-align: left;font-size: 20px;font-family: Arial;color: yellow;margin-top:0.7em'>Mixed</h1>", unsafe_allow_html=True)
    d32.markdown(f"<h1 style='text-align: left;font-size: 20px;font-family: Arial;color: #ff2727;margin-top:0.7em'>Deletion</h1>", unsafe_allow_html=True)
    d33.markdown(f"<h1 style='text-align: left;font-size: 20px;font-family: Arial;color: #0096FF;margin-top:0.7em'>Insertion</h1>", unsafe_allow_html=True)
    d34.markdown(f"<h1 style='text-align: left;font-size: 20px;font-family: Arial;color: #5bde1d;margin-top:0.7em'>Substitution</h1>", unsafe_allow_html=True)
    nap, nap_count = edit_new_allele_pattern(nap,nap_gene,nap_type,m_d)
    details.dataframe(nap,use_container_width=True,height=(nap_count+1)*36,hide_index=True)

    with st.container():
        st.write(generate_markdown('Mutation Count', font_size=80,font_color='black'), unsafe_allow_html=True)
        pie_chart,statistics, = st.columns(2)
        pie = go.Figure(go.Pie(labels=list(gene_count.keys()), values= list(gene_count.values()), textfont_size=60, hole=.3,textinfo='label+value',
                                    textposition='inside',insidetextorientation='horizontal',hovertemplate = 'Gene: %{label}'+'<br>Count: %{value}',name='',
                                    marker_colors=px.colors.qualitative.Prism))
        pie.update_layout(width=700,height=700,uniformtext_minsize=400,showlegend=False,hoverlabel=dict(font_size=24))
        pie.update_traces(sort=False,direction="counterclockwise",textfont_size=60,marker=dict(colors=px.colors.qualitative.Prism, line=dict(color='#000000', width=2)))
        pie_chart.plotly_chart(pie,use_container_width=True)
        st_write(statistics,8)
        statistics.write(generate_markdown('New Patterns', font_size=50,font_color='#f9423a'), unsafe_allow_html=True)
        statistics.write(generate_markdown(sum(list(gene_count.values())), font_size=260,font_color='black'), unsafe_allow_html=True)
        st.divider()
    
    with st.container():
        st.write(generate_markdown('ARS / Non-ARS', font_size=80,font_color='black'), unsafe_allow_html=True)
        bar_chart, statistics_2 = st.columns(2)
        bar = px.bar(df_gene.set_index('Gene')[['ARS','Non-ARS','Intron']],
                     text= 'value',
                     color_discrete_map={'ARS':'#17B169','Non-ARS':'#1B4D3E','Intron':'#7f5200'})
        
        bar.update_layout(barmode='stack', 
                          xaxis={'categoryorder':'array','categoryarray':sorted(df_gene['Gene'],key=lambda x: gene_order.index(x))})
        
        bar.update_layout(xaxis = dict(tickfont = dict(size=26)),
                          height=600,
                          width=1000,
                          font=dict(size=50),
                          legend=dict(yanchor="bottom",y=1,xanchor="left",x=0.7,orientation='h'),
                        hovermode= False,
                        yaxis_title=None, 
                        xaxis_title=None)
        
        bar.update_traces(textposition='inside',
                          textangle=0,
                          marker_line_color='black',
                          marker_line_width=2.5,)
        
        bar_chart.plotly_chart(bar,use_container_width=True)
        st_write(statistics_2,8)
        s1,s2,s3 = statistics_2.columns(3)
        s1.write(generate_markdown('ARS', font_size=40,font_color='#f9423a'), unsafe_allow_html=True)
        s1.write(generate_markdown(df_gene.ARS.sum(), font_size=160,font_color='black'), unsafe_allow_html=True)
        s1.markdown(f"<h1 style='text-align: center;font-size: 4px;font-family: Arial;color: black'>{'-'*150}</h1>", unsafe_allow_html=True)
        s2.write(generate_markdown('Non-ARS', font_size=40,font_color='#f9423a'), unsafe_allow_html=True)
        s2.write(generate_markdown(df_gene['Non-ARS'].sum(), font_size=160,font_color='black'), unsafe_allow_html=True)
        s2.markdown(f"<h1 style='text-align: center;font-size: 4px;font-family: Arial;color: black'>{'-'*150}</h1>", unsafe_allow_html=True)
        s3.write(generate_markdown('Intron', font_size=40,font_color='#f9423a'), unsafe_allow_html=True)
        s3.write(generate_markdown(df_gene['Intron'].sum(), font_size=160,font_color='black'), unsafe_allow_html=True)
        s3.markdown(f"<h1 style='text-align: center;font-size: 4px;font-family: Arial;color: black'>{'-'*150}</h1>", unsafe_allow_html=True)

    specific = st.expander(label='Tabular Data',expanded=True)
    spec1,spec2 = specific.columns(2)
    p1 = spec1.popover('Border Stop Codon',use_container_width=True)
    p2 = spec2.popover('Non-Border Stop Codon',use_container_width=True)
    specific.table(style_tabular_data(pd.DataFrame(table[3],columns=['Gene','New Pattern','ARS Syn','ARS Non-Syn','ARS Insertion','ARS Deletion','ARS Junction',
                               'ARS Mixed','Non-ARS Syn','Non-ARS Non-Syn','Non-ARS Insertion','Non-ARS Deletion',
                               'Non-ARS Junction','Non-ARS Mixed','Intron']).set_index('Gene')))
    
    if border[1] != []:
        p1.table(style_tabular_data2(pd.DataFrame(border[1],columns=['Gene','Total Pattern','ARS Insertion','ARS Deletion','ARS Substitution','ARS Mixed',
                              'Non-ARS Insertion','Non-ARS Deletion','Non-ARS Substitution','Non-ARS Mixed']).set_index('Gene')))
    else:
        p1.write('No Border Stop Codon')
        
    if non_border[1] != []:
        p2.table(style_tabular_data2(pd.DataFrame(non_border[1],columns=['Gene','Total Pattern','ARS Insertion','ARS Deletion','ARS Substitution','ARS Mixed',
                                'Non-ARS Insertion','Non-ARS Deletion','Non-ARS Substitution','Non-ARS Mixed']).set_index('Gene')))
    else:
        p2.write('No Non-Border Stop Codon')

    my_comment = st.expander('Key Take-aways',expanded=True)
    comment1,comment2,comment3,comment4,comment5 = my_comment.columns(5)
    c1 = comment1.popover('Point Mutation',use_container_width=True)
    c2 = comment2.popover('Deletion',use_container_width=True)
    c3 = comment3.popover('Insertion',use_container_width=True)
    c4 = comment4.popover('Junction/Border',use_container_width=True)
    c5 = comment5.popover('Non-Border',use_container_width=True)
    # from Functions.New_Allele.Data_Function import test
    # test([c1,c2,c3,c4,c5],data[2])
    static_comment_generator(my_comment,st.session_state.data[2])

    # reference = st.expander('Reference')
    # reference_writer(reference)

    with st.container(border=True): # Comment
        font_size = 20
        if 'New Allele' + ' image' in st.session_state and 'New Allele' + ' comment' in st.session_state:
            comment_image, comment_text = st.columns(2)
        elif 'New Allele' + ' image' in st.session_state and 'New Allele' + ' comment' not in st.session_state:
            comment_image = st.container()
        elif 'New Allele' + ' image' not in st.session_state and 'New Allele' + ' comment' in st.session_state:
            comment_text = st.container()
            font_size=60
        if 'New Allele' + ' image' in st.session_state:
            image_tab = ['Comment '+str(i) for i in range(1,len(st.session_state['New Allele image'])+1,1)]
            tab_list = ['Comment '+str(i) for i in range(1,len(st.session_state['New Allele image'])+1,1)]
            tab_list = comment_image.tabs(image_tab)
            for ind,i in enumerate(tab_list):
                i.image(st.session_state['New Allele' + ' image'][ind],width=800)

        if 'New Allele' + ' comment' in st.session_state:
            if font_size == 20:
                st_write(comment_text,14)
            comment_text.markdown(f"<h1 style='text-align: center;font-size: {font_size}px;font-family: Arial;'>{st.session_state['New Allele' + ' comment']}</h1>", unsafe_allow_html=True)

    st.write('')
    buttons2 = st.columns([5,0.5,0.5,5])
    buttons2[1].page_link("pages/11_Non_HLA_TAT.py", label="Prev", icon="⏮️", disabled = st.session_state['Non-HLA TAT status'])

else: 
    gene = sidebar.radio('Select Gene: ',sorted(st.session_state.data[1].keys(),key=lambda x: gene_order.index(x))) if len(st.session_state.data[1].keys()) == 1 else sidebar.selectbox("Select Gene",options=sorted(st.session_state.data[1].keys(),key=lambda x: gene_order.index(x)))
    frei_col,area_sample_col = sidebar.columns(2)
    frei = frei_col.radio('Select FREI Pattern',sorted(st.session_state.data[1][gene].keys()))
    area_list = []
    for i in st.session_state.gl[gene]:
        if i in st.session_state.data[1][gene][frei]:
            area_list.append(i)
    area_list = [name_lengthen(i) for i in area_list]
    area = area_sample_col.radio('Select the region',area_list) if len(area_list) == 1 else area_sample_col.select_slider('Select the region',options=area_list)
    sample = area_sample_col.radio('Select Sample ID',[i for i in st.session_state.data[0][gene][frei]])
    codon_info = sidebar.container(border=True)
    codon_col,protein_col = codon_info.columns(2)
    final_codon = codon_info.empty()
    codon = codon_col.text_input('Codon 1', 'AAA').upper()
    codon2 = codon_col.text_input('Codon 2', 'AAA',key='').upper()
    if codon in codon_dict and codon2 in codon_dict:
        codon_col.write(codon_dict[codon]+' / '+codon_dict[codon2])
        if codon_dict[codon] == codon_dict[codon2]:
            final_codon.markdown(f"<h1 style='text-align: center;font-size: 30px;'>Synonymous</h1>", unsafe_allow_html=True)
        else:
            final_codon.markdown(f"<h1 style='text-align: center;font-size: 30px;'>Non-Synonymous</h1>", unsafe_allow_html=True)
    else:
        codon_col.write('Enter a codon.') if codon == '' or codon2 == '' else codon_col.write('There is no such a codon.')
            
    protein = protein_col.text_input('Silent Mutation','AAA').upper()
    if protein not in codon_dict:
        protein_col.write('Enter a codon.') if protein == '' else protein_col.write('There is no such a codon.')
    else:
        candidate = protein_dict[codon_dict[protein]]
        candidate.remove(protein)
        protein_col.write(candidate)
#---------------------------------------------------------------------------------------------------------------------------------------
    zero_layer = st.expander('Comments')
    first_layer = st.expander('Whole Gene',expanded=True)
    middle_layer = st.container()
    fi1,fi2 = middle_layer.columns(2)
    second_layer = st.expander('Area-Specific',expanded=True)
    third_layer = st.expander('Sequence-Specific',expanded=True)
#---------------------------------------------------------------------------------------------------------------------------------------
    static_comment_generator(zero_layer,st.session_state.data[2])
#---------------------------------------------------------------------------------------------------------------------------------------
    area = name_shorten(area)
    offset_dict = get_offset(st.session_state.data[1],gene,frei,st.session_state.gl)
    new_index = generate_new_index(st.session_state.data[1],gene,frei,st.session_state.gl,offset_dict)
    fig = first_viz(st.session_state.data[2],gene,frei,area,new_index,show_all)
    first_layer.write(fig)
#---------------------------------------------------------------------------------------------------------------------------------------
    sequence_length = new_index[area][1] - new_index[area][0] + 1 
    min_mutation = sorted([i[1] for i in st.session_state.data[2][gene][frei][area]],key=lambda x: x)[0] + new_index[area][0] - 1 
    if min_mutation - 10 >= new_index[area][0]:
        min_mutation = min_mutation -10
    else:
        min_mutation = new_index[area][0]
    
    boundary = fi1.slider('Select the boundary',min_value=new_index[area][0],max_value = new_index[area][1]-20,value=min_mutation,step=1)
    info = fi2.container()
    info_writer(info,st.session_state.data[1],gene,frei,area,sample)
    fig2 = second_viz(st.session_state.data[2],gene,frei,area,new_index,boundary)
    second_layer.write(fig2)
#---------------------------------------------------------------------------------------------------------------------------------------
    fig3 = third_viz(st.session_state.data[1],st.session_state.data[2],gene,frei,area,new_index,st.session_state.gl,st.session_state.gc,boundary)
    third_layer.write(fig3)