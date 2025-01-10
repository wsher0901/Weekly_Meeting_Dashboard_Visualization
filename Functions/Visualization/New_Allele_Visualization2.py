import json
from pygenomeviz import GenomeViz
from matplotlib.patches import Patch
color = {'3':'red','5':'red','I':'royalblue','E':'orange'}
facecolor = {'P':'lime','D':'orangered','I':'skyblue'}
stop_codon = ['TAA','TAG','TGA']
codon_deletion_translation = {1:0,2:2,3:1}

def get_codon_dict():
    with open('Files/codon_dict.txt') as f: 
        return json.loads(f.read()) 

codon_dict = get_codon_dict()

def name_lengthen(name):
    if name[0] == 'E':
        return 'Exon ' + name[-1]
    elif name[0] == 'I':
        return 'Intron ' + name[-1]
    else:
        return name
    
def name_shorten(name):
    if name[0] == 'E':
        return 'E' + name[-1]
    elif name[0] == 'I':
        return 'I' + name[-1]
    else:
        return name
    
def align_sequence(data):
    mut, og, ng = data[0], data[2], data[3]
    mut_ind = [int(m[2:])-1 for m in mut]
    new_og = new_ng = ''
    count = 0
    while og and ng:
        if count not in mut_ind:
            new_og += og[0]
            og = og[1:]
            new_ng += ng[0]
            ng = ng[1:]     
        else:
            mut_type = [m[0] for m in mut if int(m[2:])-1 == count][0]
            if mut_type == 'D':
                new_og += og[0]
                og = og[1:]
                new_ng += ' '
            elif mut_type == 'I':
                new_og += ' '
                new_ng += ng[0]
                ng = ng[1:]
            else:
                new_og += og[0]
                og = og[1:]
                new_ng += ng[0]
                ng = ng[1:]
            
        count+=1
           
    return new_og, new_ng

def get_offset(data,gene,frei,gene_location):
    offset = 0
    offset_dict = {}
    for i in gene_location[gene]:
        if i not in data[gene][frei]:       
            offset_dict[i] = [0,offset]
        else:
            d = data[gene][frei][i]
            seq_length = len(d[2]) if len(d[2]) > len(d[3]) else len(d[3])
            gap = seq_length - (gene_location[gene][i][1] - gene_location[gene][i][0] + 1)
            offset_dict[i] = [gap,offset]
            offset+= gap

    return offset_dict

def generate_new_index(data1,gene,frei,gene_location,offset_dict):
    new_index = {}
    prev = gene_location[gene]['5UTR'][0]
    for i in gene_location[gene]:
        start = end = 0
        if i not in data1[gene][frei]:
            start = gene_location[gene][i][0]+offset_dict[i][1]
            end = gene_location[gene][i][1]+offset_dict[i][1]       
        else:
            d = data1[gene][frei][i]
            og, ng = align_sequence(d)
            start = prev
            end = prev+len(og)-1
        if end < 0:
            new_index[i] = [start,end]
            prev = end+1
        else:
            if end == 0:
                new_index[i] = [start,end+1]
                prev = end+2
            elif end == -1:
                new_index[i] = [start,end]
                prev = end+2
            else:
                if start < 0:
                    new_index[i] = [start,end+1]
                    prev = end+2
                else:
                    new_index[i] = [start,end]
                    prev = end+1

    return new_index

def first_viz(data,gene,frei,area,new_index,show_all):
    gene_length = new_index['3UTR'][1] - new_index['5UTR'][0] + 1 
    gene_end = new_index['3UTR'][1]
    gv = GenomeViz(tick_style='axis',fig_track_height=0.4)
    track = gv.add_feature_track(name=gene,size=gene_length,start_pos=new_index['5UTR'][0],labelsize = 30,linecolor='black')
    for i in new_index:
        track.add_feature(new_index[i][0],new_index[i][1],facecolor=color[i[0]],plotstyle='box',linewidth=0.8)
    
    if show_all:
        for i in data[gene][frei]:
            area_start = new_index[i][0]
            for j in data[gene][frei][i]:
                position = area_start + j[1] - 1
                end = position+gene_length/250
                if end > gene_end:
                    end = gene_end
                track.add_feature(position, end, facecolor=facecolor[j[0]],
                                    edgecolor = 'black', plotstyle='box', labelvpos = 'top',
                                    labelhpos = 'center', labelsize = 17, strand = -1, linewidth = 0.8)
    else:
        area_start = new_index[area][0]
        for i in data[gene][frei][area]:
            position = area_start + i[1] - 1 
            end = position + gene_length/250
            if end > gene_end:
                end = gene_end

            track.add_feature(position, end, facecolor=facecolor[i[0]],
                                edgecolor = 'black', plotstyle='box', labelvpos = 'top',
                                labelhpos = 'center', labelsize = 17, strand = -1, linewidth = 0.8)
            
    fig = gv.plotfig()
    for i in new_index:
        if gene in ['A','B','DPA1','DQA1']:
            gv.top_track.ax.text((new_index[i][0]+new_index[i][1])/2- new_index['5UTR'][0], 1.5, i, fontsize=16, ha="center", va="bottom")
        else:
            if gene == 'DPB1':
                if i == '5UTR':
                    gv.top_track.ax.text((new_index[i][0]+new_index[i][1])/2- new_index['5UTR'][0]-100, 1.5, i, fontsize=16, ha="center", va="bottom")
                elif i == 'E1':
                    gv.top_track.ax.text((new_index[i][0]+new_index[i][1])/2- new_index['5UTR'][0]+100, 1.5, i, fontsize=16, ha="center", va="bottom")
                else:
                    gv.top_track.ax.text((new_index[i][0]+new_index[i][1])/2- new_index['5UTR'][0], 1.5, i, fontsize=16, ha="center", va="bottom")

            elif gene == 'C':
                if i == 'E8':
                     gv.top_track.ax.text((new_index[i][0]+new_index[i][1])/2- new_index['5UTR'][0]-10, 1.5, i, fontsize=16, ha="center", va="bottom")
                elif i == '3UTR':
                     gv.top_track.ax.text((new_index[i][0]+new_index[i][1])/2- new_index['5UTR'][0]+50, 1.5, i, fontsize=16, ha="center", va="bottom")
                else:
                     gv.top_track.ax.text((new_index[i][0]+new_index[i][1])/2- new_index['5UTR'][0], 1.5, i, fontsize=16, ha="center", va="bottom")

            elif gene == 'DQB1':
                if i == 'E6':
                     gv.top_track.ax.text((new_index[i][0]+new_index[i][1])/2- new_index['5UTR'][0]-30, 1.5, i, fontsize=16, ha="center", va="bottom")
                elif i == '3UTR':
                     gv.top_track.ax.text((new_index[i][0]+new_index[i][1])/2- new_index['5UTR'][0]+80, 1.5, i, fontsize=16, ha="center", va="bottom")
                else:
                     gv.top_track.ax.text((new_index[i][0]+new_index[i][1])/2- new_index['5UTR'][0], 1.5, i, fontsize=16, ha="center", va="bottom")

            elif gene == 'DRB1':
                if i == 'E6':
                     gv.top_track.ax.text((new_index[i][0]+new_index[i][1])/2- new_index['5UTR'][0]-50, 1.5, i, fontsize=16, ha="center", va="bottom")
                elif i == '3UTR':
                     gv.top_track.ax.text((new_index[i][0]+new_index[i][1])/2- new_index['5UTR'][0]+140, 1.5, i, fontsize=16, ha="center", va="bottom")
                else:
                     gv.top_track.ax.text((new_index[i][0]+new_index[i][1])/2- new_index['5UTR'][0], 1.5, i, fontsize=16, ha="center", va="bottom")

            elif gene == 'DRB3':
                if i == '5UTR':
                    gv.top_track.ax.text((new_index[i][0]+new_index[i][1])/2- new_index['5UTR'][0]-150, 1.5, i, fontsize=16, ha="center", va="bottom")
                elif i == 'E1':
                    gv.top_track.ax.text((new_index[i][0]+new_index[i][1])/2- new_index['5UTR'][0]+60, 1.5, i, fontsize=16, ha="center", va="bottom")
                elif i == 'E6':
                     gv.top_track.ax.text((new_index[i][0]+new_index[i][1])/2- new_index['5UTR'][0]-50, 1.5, i, fontsize=16, ha="center", va="bottom")
                elif i == '3UTR':
                     gv.top_track.ax.text((new_index[i][0]+new_index[i][1])/2- new_index['5UTR'][0]+140, 1.5, i, fontsize=16, ha="center", va="bottom")
                else:
                     gv.top_track.ax.text((new_index[i][0]+new_index[i][1])/2- new_index['5UTR'][0], 1.5, i, fontsize=16, ha="center", va="bottom")

            elif gene == 'DRB4':
                if i == '5UTR':
                    gv.top_track.ax.text((new_index[i][0]+new_index[i][1])/2- new_index['5UTR'][0]-170, 1.5, i, fontsize=16, ha="center", va="bottom")
                elif i == 'E1':
                    gv.top_track.ax.text((new_index[i][0]+new_index[i][1])/2- new_index['5UTR'][0]+90, 1.5, i, fontsize=16, ha="center", va="bottom")
                elif i == 'E5':
                    gv.top_track.ax.text((new_index[i][0]+new_index[i][1])/2- new_index['5UTR'][0]-10, 2.5, i, fontsize=16, ha="center", va="bottom")
                elif i == 'E6':
                     gv.top_track.ax.text((new_index[i][0]+new_index[i][1])/2- new_index['5UTR'][0]+10, 2.5, i, fontsize=16, ha="center", va="bottom")
                elif i == '3UTR':
                     gv.top_track.ax.text((new_index[i][0]+new_index[i][1])/2- new_index['5UTR'][0]+180, 1.5, i, fontsize=16, ha="center", va="bottom")
                else:
                     gv.top_track.ax.text((new_index[i][0]+new_index[i][1])/2- new_index['5UTR'][0], 1.5, i, fontsize=16, ha="center", va="bottom")

            elif gene == 'DRB5':
                if i == '5UTR':
                    gv.top_track.ax.text((new_index[i][0]+new_index[i][1])/2- new_index['5UTR'][0]-170, 1.5, i, fontsize=16, ha="center", va="bottom")
                elif i == 'E1':
                    gv.top_track.ax.text((new_index[i][0]+new_index[i][1])/2- new_index['5UTR'][0]+90, 1.5, i, fontsize=16, ha="center", va="bottom")
                elif i == 'E5':
                    gv.top_track.ax.text((new_index[i][0]+new_index[i][1])/2- new_index['5UTR'][0]-10, 2.5, i, fontsize=16, ha="center", va="bottom")
                elif i == 'E6':
                     gv.top_track.ax.text((new_index[i][0]+new_index[i][1])/2- new_index['5UTR'][0]+10, 2.5, i, fontsize=16, ha="center", va="bottom")
                elif i == '3UTR':
                     gv.top_track.ax.text((new_index[i][0]+new_index[i][1])/2- new_index['5UTR'][0]+180, 1.5, i, fontsize=16, ha="center", va="bottom")
                else:
                     gv.top_track.ax.text((new_index[i][0]+new_index[i][1])/2- new_index['5UTR'][0], 1.5, i, fontsize=16, ha="center", va="bottom")

            else:
                gv.top_track.ax.text((new_index[i][0]+new_index[i][1])/2- new_index['5UTR'][0], 1.5, i, fontsize=16, ha="center", va="bottom")

    if gene in ['A','B','C']:
        ars_list = ['E2','E3']
        for i in ars_list:
            label = 'ARS'
            start = new_index[i][0] - new_index['5UTR'][0]
            end = new_index[i][1] - new_index['5UTR'][0]
            gv.top_track.ax.hlines(3, start, end, colors="black", linewidth=2, linestyles="dashed", clip_on=False)
            gv.top_track.ax.text((start+end)/2, 3.4, label, fontsize=15, ha="center", va="bottom")

    else:
        start = new_index['E2'][0] - new_index['5UTR'][0] 
        end = new_index['E2'][1] - new_index['5UTR'][0] 
        label = 'ARS'
        gv.top_track.ax.hlines(3, start, end, colors="black", linewidth=2, linestyles="dashed", clip_on=False)
        gv.top_track.ax.text((start+end)/2, 3.4, label, fontsize=15, ha="center", va="bottom")

    return fig

def second_viz(data,gene,frei,area,new_index,boundary):
    gv = GenomeViz(tick_style='axis',fig_track_height=0.4)
    first_pos, last_pos = new_index[area][0], new_index[area][1]
    region_length = last_pos - first_pos + 1 
    track = gv.add_feature_track(area,region_length,start_pos = new_index[area][0],labelsize=30,linecolor='black')
    
    for i in data[gene][frei][area]:
        position = i[1] + first_pos - 1
        end = last_pos+1 if position+region_length/250 > last_pos else position + region_length/250
        if position == last_pos:
            track.add_feature(start = position,end = end, strand = -1, plotstyle='bigbox', labelsize = 10,
                              facecolor = 'black', edgecolor = 'black', linewidth = 1)
        elif position == first_pos:
            track.add_feature(start = position,end = end, strand = -1, plotstyle='bigbox', labelsize = 10,
                              facecolor = 'black', edgecolor = 'black', linewidth = 1)
        else:
            track.add_feature(start = position,end = end, strand = -1, plotstyle='bigbox', labelsize = 10,
                              facecolor = facecolor[i[0]], edgecolor = 'black', linewidth = 1)
        
    fig = gv.plotfig()
    new_label = label_maker(data,gene,frei,area)
    for i in new_label:
        if i[2] == 0:
            gv.top_track.ax.text(i[0]-1, -1.5, str(i[0]+new_index[area][0]-1), fontsize=10, ha="center",
                                 va="center_baseline",rotation=-45)
        else:
            gv.top_track.ax.text((i[0]+i[1])/2-1, -1.5, 
                                 str(i[0]+new_index[area][0]-1)+'~', 

                                 fontsize=10, ha="center", va="center_baseline",rotation=-45)
            
    handles = [Patch(facecolor="lime", label="Point Mutation",edgecolor='black',linewidth=0.8,linestyle='-'), 
           Patch(facecolor="orangered", label="Deletion",edgecolor='black',linewidth=0.8,linestyle='-'),
           Patch(facecolor="royalblue", label="Insertion",edgecolor='black',linewidth=0.8,linestyle='-'),
           Patch(facecolor='black',label='Border Mutation',edgecolor='gray',linewidth=0.8,linestyle='-')]
    fig.legend(handles=handles, bbox_to_anchor=(0.3,-0.30),ncol=4)
    start_pos = boundary - first_pos
    end_pos = region_length if boundary + 21 - first_pos > region_length else boundary + 21 - first_pos
    gv.top_track.ax.fill((start_pos,start_pos,end_pos,end_pos),(1.2,-1.2,-1.2,1.2),fc='gray',linewidth=0, alpha=0.9, zorder=-10)
    return fig       

def label_maker(data,gene,frei,area):
    if len(data[gene][frei][area]) == 1:
        return [[data[gene][frei][area][0][1],
                data[gene][frei][area][0][1],
                0]]
    else:
        temp = []
        prev = data[gene][frei][area][0][1] 
        start = prev
        count = 0
        for ind,i in enumerate(data[gene][frei][area][1:],1):
            pos = i[1]
            if pos - prev <= 4:
                prev = pos
                count+=1
                if ind == len(data[gene][frei][area])-1:
                    temp.append([start,prev,count])

            else:
                temp.append([start,prev,count])
                prev = pos
                start = prev
                count = 0
                if ind == len(data[gene][frei][area])-1:
                    temp.append([start,prev,count])
                
        return temp

def info_writer(loc,data1,gene,frei,area,sample):
    l1,l2,l3 = loc.columns(3)
    allele = data1[gene][frei][area][1]

    l1.markdown(f"<h1 style='text-align: center;font-size: 15px;font-family: Arial;color: #FF4B4B;padding: 0em'>Gene</h1>", unsafe_allow_html=True)
    l1.markdown(f"<h1 style='text-align: center;font-size: 30px;font-family: Arial;color: #FF4B4B;border-style: double'>{gene}</h1>", unsafe_allow_html=True)
    l2.markdown(f"<h1 style='text-align: center;font-size: 15px;font-family: Arial;color: #FF4B4B;padding: 0em'>Area</h1>", unsafe_allow_html=True)
    l2.markdown(f"<h1 style='text-align: center;font-size: 30px;font-family: Arial;color: #FF4B4B;border-style: double'>{name_lengthen(area)}</h1>", unsafe_allow_html=True)
    l3.markdown(f"<h1 style='text-align: center;font-size: 15px;font-family: Arial;color: #FF4B4B;padding: 0em'>Closest Allele</h1>", unsafe_allow_html=True)
    l3.markdown(f"<h1 style='text-align: center;font-size: 25px;font-family: Arial;color: #FF4B4B;border-style: double'>{allele}</h1>", unsafe_allow_html=True)

def viz_assist(i,start,end,first_pos,offset):
    start_slide, end_slide = 0, 1 
    if (i-first_pos+offset)%3 == 2:
        if i == start:
            start_slide, end_slide = 0, 0.85
        else:
            start_slide, end_slide = -0.05, 0.85
    elif (i-first_pos+offset)%3 == 0:
        if i == end-1:
            start_slide, end_slide = 0.15, 1
        else:
            start_slide, end_slide = 0.15, 1.05
    else:
        start_slide, end_slide = 0.05, 0.95
                
    return start_slide, end_slide

def stop_codon_check(data1,gene,frei,area,i,first_pos,offset,ng):
    candidate = ''
    if i-first_pos >= 1:
        candidate = ng[i-first_pos-1:i-first_pos+2]
    else:
        if (i-first_pos+offset)%3 == 1:
            if data1[gene][frei][area][6]:
                candidate = data1[gene][frei][area][6][-1] + ng[0:2]
            else:
                return False
        elif (i-first_pos+offset)%3 == 2:
            if data1[gene][frei][area][6]:
                candidate = data1[gene][frei][area][6][-2:] + ng[0]
            else:
                return False

    if candidate in stop_codon:
        return True
    else:
        return False

def get_mutation_type(a,b):
    if a in codon_dict and b in codon_dict:
        return 'Syn' if codon_dict[a] == codon_dict[b] else 'Non-Syn'
    else:
        return None

def viz_mutation(data1,gene,frei,area,og,ng,i,first_pos,start,positions,gv):
    if i-first_pos == 0:
        if i in positions or i+1 in positions:
            if data1[gene][frei][area][4] and data1[gene][frei][area][6]:
                syn = get_mutation_type(data1[gene][frei][area][4][-1] + og[0:2],
                                       data1[gene][frei][area][6][-1] + ng[0:2])
                gv.top_track.ax.text(i-start+0.5, -2, syn, fontsize=16 , ha="center",va="center_baseline")
    elif i-first_pos == 2:
        if i-2 in positions:
            if data1[gene][frei][area][4] and data1[gene][frei][area][6]:
                syn = get_mutation_type(data1[gene][frei][area][4][-2:] + og[0],
                                       data1[gene][frei][area][6][-2:] + ng[0])
                gv.top_track.ax.text(i-start-2+0.5, -2, syn, fontsize=16 , ha="center",va="center_baseline")

            
        if i-1 in positions or i in positions or i+1 in positions:
            syn = get_mutation_type(og[i-first_pos-1:i-first_pos+2],
                                       ng[i-first_pos-1:i-first_pos+2])
            gv.top_track.ax.text(i-start+0.5, -2, syn, fontsize=16 , ha="center",va="center_baseline")
                
    else:
        if i-1 in positions or i in positions or i+1 in positions:
            syn = get_mutation_type(og[i-first_pos-1:i-first_pos+2],
                                       ng[i-first_pos-1:i-first_pos+2])
            gv.top_track.ax.text(i-start+0.5, -2, syn, fontsize=16 , ha="center",va="center_baseline")

def codon_wrap(data1,gene,frei,new_index):
    exons = [i for i in list(new_index.items()) if i[0][0] == 'E']
    edited_sequence = {}
    offset = 0
    for i in exons:
        if i[0] in data1[gene][frei]:
            og = data1[gene][frei][i[0]][2]
            ng = data1[gene][frei][i[0]][3]
            og_len, ng_len = len(og),len(ng)
            if offset > 0:
                ng = '*' * offset + ng
            elif offset < 0:
                og = '*' * offset + og
                
            if len(data1[gene][frei][i[0]][2]) == len(data1[gene][frei][i[0]][3]):
                edited_sequence[i[0]] = [og,ng]
                offset = 0
            else:
                diff = ng_len - og_len
                if diff > 0:
                    edited_sequence[i[0]] = [og + ' ' * diff,ng]
                    offset = diff
                else:
                    edited_sequence[i[0]] = [og,ng + ' ' * (-1*diff)]
                    offset = -1 * diff
                
    return edited_sequence

def codon_slider(next_pos,diff):
    end_pos = next_pos
    if diff < 0:
        if next_pos == 0:
            return end_pos + (-1*diff)//3+1, next_pos+1
        elif next_pos == -1:
            return end_pos + (-1*diff)//3+1, next_pos
        elif next_pos < -1:
            if end_pos + (-1*diff)//3 >= 0:
                return end_pos + (-1*diff)//3+1, next_pos
            else:
                return end_pos + (-1*diff)//3, next_pos
        else:
            return end_pos + (-1*diff)//3, next_pos
     
    elif diff == 0:
        if next_pos == 0:
            return end_pos+1, next_pos+1
        else:
            return end_pos, next_pos
    else:
        if end_pos == 0:
            return end_pos+1, next_pos - (diff+1)//3
        elif end_pos > 0:
            if next_pos - (diff+1)//3 >= 0:
                return end_pos+1, next_pos - (diff+1)//3 + 1
            else:
                return end_pos+1, next_pos - (diff+1)//3

def get_new_codon_ind(data1,gene,frei,new_index,gene_location,gene_codon):
    new_codon = {}
    exons = [i[0] for i in list(new_index.items()) if i[0][0] == 'E']
    start_pos = gene_codon[gene]['E1'][0]
    left_over = total_offset = 0
    for i in exons:
        length = gene_location[gene][i][1] - gene_location[gene][i][0] + 1 + left_over 
        diff = 0
        if i in data1[gene][frei]:
            length = len(data1[gene][frei][i][2]) + left_over if len(data1[gene][frei][i][2]) > len(data1[gene][frei][i][3]) else len(data1[gene][frei][i][3]) + left_over
            diff = len(data1[gene][frei][i][2])-len(data1[gene][frei][i][3])

        quotient, remainder = length//3, length%3
        next_pos = start_pos + quotient - 1 
        if remainder != 0:
            next_pos +=1
        if start_pos <= 0 and next_pos >= 0:
            next_pos+=1
        
        end_pos, next_pos = codon_slider(next_pos,diff)
        new_codon[i] = [start_pos,end_pos,left_over%3,total_offset]
        start_pos = next_pos
        if remainder == 0:
            start_pos += 1
        left_over = remainder
        total_offset += diff
        
    return new_codon

def third_viz(data1,data2,gene,frei,area,new_index,gene_location,gene_codon,boundary):
    first_pos, last_pos = new_index[area][0], new_index[area][1] 
    start = boundary
    end = last_pos + 1 if boundary + 21 > last_pos else boundary + 21
    positions = {i[1]+first_pos-1:i[0] for i in data2[gene][frei][area]}
    gv = GenomeViz(tick_style='axis',fig_track_height=0.7)
    track = gv.add_feature_track(area,21,start_pos = start,linewidth=1,labelsize=30,linecolor='black')
    new_codon = get_new_codon_ind(data1,gene,frei,new_index,gene_location,gene_codon)[area] if area[0] == 'E' else ''
    og, ng = codon_wrap(data1,gene,frei,new_index)[area] if area[0] == 'E' else align_sequence(data1[gene][frei][area])
    offset = 0
    if area[0] == 'E':
        if area != 'E1':
            offset = 1 if new_codon[3] <= 0 else codon_deletion_translation[new_codon[3]%3]
    start_slide,end_slide = 0,1
    
    for i in range(start,end,1):
        if area[0] == 'E':
            start_slide, end_slide = viz_assist(i,start,end,first_pos,offset)
        og_seq = og[i-first_pos]
        ng_seq = ng[i-first_pos]
        label_size = 12
        if i not in positions:
            track.add_feature(start=i+start_slide,end=i+end_slide,strand=1,plotstyle='box',label=og_seq,edgecolor='black',
                              labelrotation=0,facecolor='lightcoral',labelhpos='center',labelvpos='center',labelha='center',
                              linewidth=1, labelsize=12)
            track.add_feature(start=i+start_slide,end=i+end_slide,strand=-1,plotstyle='box',label=ng_seq,edgecolor='black',
                              labelrotation=0,facecolor='lightcoral',labelhpos='center',labelvpos='center',labelha='center',
                              linewidth=1, labelsize=label_size)
        else:
            mut_type = positions[i]
            og_color = 'orangered' if mut_type == 'D' else 'lightcoral'
            ng_color = 'skyblue' if mut_type == 'I' else ('lime' if mut_type == 'P' else 'lightcoral')
            track.add_feature(start=i+start_slide,end=i+end_slide,strand=1,plotstyle='box',label=og_seq,edgecolor='black',
                                labelrotation=0,facecolor=og_color,labelhpos='center',labelvpos='center',labelha='center',
                                linewidth=1, labelsize=12)
            track.add_feature(start=i+start_slide,end=i+end_slide,strand=-1,plotstyle='box',label=ng_seq,edgecolor='black',
                                labelrotation=0,facecolor=ng_color,labelhpos='center',labelvpos='center',
                                labelha='center',linewidth=1, labelsize=12)
                
    fig = gv.plotfig()
    for i in range(start,end,1):
        if area[0] == 'E':
            if (i-first_pos+offset)%3 == 1:
                if stop_codon_check(data1,gene,frei,area,i,first_pos,offset,ng):
                    gv.top_track.ax.text(i-start+0.5, 3, 'Stop Codon', fontsize=16, ha="center", va="center_baseline",color='lightcoral',fontweight='bold',fontfamily='Sans-serif')
                viz_mutation(data1,gene,frei,area,og,ng,i,first_pos,start,positions,gv)
                if new_codon[0]+(i-first_pos)//3 == 0:
                    gv.top_track.ax.text(i-start+0.5, 1.8, str(1), fontsize=16, ha="center", va="center_baseline")
                else:
                    gv.top_track.ax.text(i-start+0.5, 1.8, str(new_codon[0]+(i-first_pos)//3), fontsize=24, ha="center", va="center_baseline")

            if (i-first_pos+offset)%3 == 2:
                gv.top_track.ax.text(i-start+0.4, -1.4, str(i), fontsize=10 , ha="center", va="center_baseline")
            elif (i-first_pos+offset)%3 == 0:
                gv.top_track.ax.text(i-start+0.6, -1.4, str(i), fontsize=10 , ha="center", va="center_baseline")
            else:
                gv.top_track.ax.text(i-start+0.5, -1.4, str(i), fontsize=10 , ha="center", va="center_baseline")
        else:
                gv.top_track.ax.text(i-start+0.5, -1.4, str(i), fontsize=10 , ha="center", va="center_baseline")
    return fig

def reference_writer(loc):
    loc.markdown(f"<h1 style='text-align: left;font-size: 20px;color: #5bde1d'>Substitution: a mutation affecting only one or very few nucleotides in a gene sequence. </h1>", unsafe_allow_html=True)
    loc.markdown(f"<h1 style='text-align: left;font-size: 20px;color: #ff2727'>Deletion: Point mutations in which one or more base is removed.</h1>", unsafe_allow_html=True)
    loc.markdown(f"<h1 style='text-align: left;font-size: 20px;color: #0096FF'>Insertion: Point mutations in which one or more base is inserted.</h1>", unsafe_allow_html=True)
    loc.markdown(f"<h1 style='text-align: left;font-size: 20px;color: yellow'>Mixed: When more than one type of mutation occurs together, e.g., Syn and Non-Syn/Substitution and Deletion/Syn and Deletion.</h1>", unsafe_allow_html=True)
    loc.markdown(f"<h1 style='text-align: left;font-size: 20px;color: white'>Junction: When any of the mutation occurs at the edge.</h1>", unsafe_allow_html=True)
    loc.markdown(f"<h1 style='text-align: left;font-size: 20px;color: white'>Border Stop Codon: When any of the mutation, occurring at the edge, results in premature stop codon.</h1>", unsafe_allow_html=True)
    loc.markdown(f"<h1 style='text-align: left;font-size: 20px;color: white'>Non-Border Stop Codon: When any of the mutation, not occurring at the edge, results in premature stop codon.</h1>", unsafe_allow_html=True)

# def style_specific_columns(column):
#     if column.name in ['ARS Syn','ARS Non-Syn','ARS Insertion','ARS Deletion','ARS Junction','ARS Mixed']:
#         return ['background-color: #17B169'] * len(column)
#     elif column.name in ['Non-ARS Syn','Non-ARS Non-Syn','Non-ARS Insertion','Non-ARS Deletion','Non-ARS Junction','Non-ARS Mixed']:
#         return ['background-color: #1B4D3E'] * len(column)
#     elif column.name == 'Intron':
#         return ['background-color: #7f5200'] * len(column)
#     else:
#         return ['background-color: #0E1117'] * len(column)
        
def style_tabular_data(df):
    def style_specific_columns(column):
        if column.name in ['ARS Syn','ARS Non-Syn','ARS Insertion','ARS Deletion','ARS Junction','ARS Mixed']:
            return ['background-color: #17B169'] * len(column)
        elif column.name in ['Non-ARS Syn','Non-ARS Non-Syn','Non-ARS Insertion','Non-ARS Deletion','Non-ARS Junction','Non-ARS Mixed']:
            return ['background-color: #1B4D3E'] * len(column)
        elif column.name == 'Intron':
            return ['background-color: #7f5200'] * len(column)
        else:
            return ['background-color: #0E1117'] * len(column)
        
    return df.style.apply(style_specific_columns).set_table_styles(
    [
        {'selector': 'th.col_heading', 'props': 'background-color: gray; color: white;'},
        {'selector': 'th.row_heading', 'props': 'background-color: #FCF5E5; color: black;'},
        {'selector': 'td', 'props': [('border', '2px solid black'),('font-size','20px'),('color','white')]},
        {'selector': 'th', 'props': [('border', '2px solid black')]},
        {'selector': 'td:nth-child(2)', 'props': [('background-color', '#FCF5E5'), ('color', 'black')]}
    ])

    
def style_tabular_data2(df):
    def style_specific_columns2(column):
        if column.name in ['ARS Insertion','ARS Deletion','ARS Substitution','ARS Mixed']:
            return ['background-color: #17B169'] * len(column)
        elif column.name in ['Non-ARS Insertion','Non-ARS Deletion','Non-ARS Substitution','Non-ARS Mixed']:
            return ['background-color: #1B4D3E'] * len(column)
        elif column.name == 'Intron':
            return ['background-color: #7f5200'] * len(column)
        else:
            return ['background-color: #0E1117'] * len(column)   
        
    return df.style.apply(style_specific_columns2).set_table_styles(
    [
        {'selector': 'th.col_heading', 'props': 'background-color: gray; color: white;'},
        {'selector': 'th.row_heading', 'props': 'background-color: #FCF5E5; color: black;'},
        {'selector': 'td', 'props': [('border', '2px solid black'),('font-size','20px'),('color','white')]},
        {'selector': 'th', 'props': [('border', '2px solid black')]},
        {'selector': 'td:nth-child(2)', 'props': [('background-color', '#FCF5E5'), ('color', 'black')]}
    ])







