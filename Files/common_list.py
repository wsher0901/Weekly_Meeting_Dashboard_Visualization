# Communal
colors = [
    "#66B3FF",  # Soft Electric Blue
    "#D75B6D",  # Muted Crimson Red
    "#FFCC00",  # Soft Yellow
    "#48C9B0",  # Muted Turquoise
    "#2E8B57",  # Olive Green
    "#DA70D6",  # Light Magenta
    "#B8860B",  # Dark Goldenrod
    "#1E90FF",  # Dodger Blue
    "#3CB371",  # Medium Sea Green
    "#7B68EE",  # Medium Slate Blue
    "#FF6347",  # Tomato Red
    "#FF7F50",  # Coral
    "#8A2BE2",  # Blue Violet
    "#D8BFD8",  # Thistle
    "#5D3FD3",  # Medium Purple
    "#20B2AA"   # Light Sea Green
]
page_list = ['Pre PCR (High Vol)','Pre PCR (CMV)','Pre PCR (Low Vol)','PCR','Gel','Illumina','Pacbio','Repeats','Reagents','HLA TAT','Non-HLA TAT','New Allele']
test_list = ['HLA','ABO-RH','CCR','CMV','DNA Extraction','ENGRAFTMENT','Illumina','KIR','Micro array','Nanopore','Non-Classical','Optical','PacBio','PGX','Whole Genome']
gene_list = ['A','B','C','DRB1','DRB345','DQB1','DQA1','DPB1','DPA1']
test_list_concise_map = {'Illumina Sequencing':'Illumina','Nanopore Sequencing':'Nanopore','Non-Classical Genes':'Non-Classical',
                'Optical Mapping':'Optical','PacBio Sequencing':'PacBio','Whole Genome Sequencing':'Whole Genome'}

comment_category = {1:'Test Delay',2:'Test Failed',3:'Test Quality issues',
                   4:'Waiting for Repeat',5:'Hold Report',6:'Others'}
comment_color_code = {'Test Delay':'#ff7400','Test Failed':'#ff0000','Test Quality issues': '#ff4d00','':'white',
              'Waiting for Repeat':'#ffc100','Hold Report':'black','Others':'#2a4d69','Not Commented':'gray','Extended':'rgb(180,151,231)','Completed':'#0e1117'}
delay_status_color_code = {'Completed':'#313695','Delayed':'#a50026','Hold Report':'white'}
# CMV
cmv_test_type_list = ['Antibody Extraction','CMV-ELISA','Plasma / Serum Dilution']
# Low-volume
low_volume_test_list = ['Clinical','Registry','Research']
# Gel
gel_color_map = {'Illumina':'#EE3233','Pacbio':'#66A7C5'}
# Illumina
illumina_color_map = {'Illumina MiSeq':'#FF5733','Illumina NovaSeq':'#FF8C42'}
# Pacbio
pacbio_color_map = {'Pacbio Sequel-I':'#008080','Pacbio Sequel-II':'#6A5ACD','Pacbio Sequel-IIe':'#B0C4DE'}
# Repeats
client_removal_list = ['Histogenetics']
repeats_color_map = {'Weekly':'indianred','Yearly':'#0096FF'}
# HLA TAT
hla_removal_list = ['Anthony Nolan-Cord DNA HLA ABO','CBS-New Event Allele HR (2020)','Anthony Nolan-HLA ABO CMV']
hla_extension_list = ['NatKidneyRegistry STAT HLA ABORH']
# Non-HLA TAT
nonhla_removal_list = ['HISTO QC']
nonhla_gene_list = ['ABO-RH','CCR','CMV','KIR','DRA','E','G','FCGR3A','MICA','MICB','HPA','Final Due']
exception_list = ['NatKidneyRegistry STAT HLA ABORH']