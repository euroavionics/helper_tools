'''
REV 002: initial setup

AIM: Summarize in a table the maps contained by a Euronav-disk (using a python script in a windows computer)

PRE-REQUISITES:

Some python packages (matplotlib and pandas) are required, so follow this instructions if you do not have them

1. Install pip

 Download get-pip.py (https://bootstrap.pypa.io/get-pip.py) to a folder on your computer.
 Open a command prompt window and navigate to the folder containing get-pip.py.
 Then run: python get-pip.py

2. Install matplotlib  und pandas with pip (it does not matter where you open the cmd)

python -mpip install -U pip
python -mpip install -U matplotlib
python -mpip install -U pandas
python -mpip install -U numpy
python -mpip install -U kiwisolver
python -mpip install -U future

USAGE:

(A) Just make double click with the mouse on the script or

(B) Open cmd in the folder containing this script (map_def_tool.py) and write: python map_def_tool.py

DF & CC, 25.10.2018

'''
from __future__ import print_function
from __future__ import division
from builtins import input
from builtins import str
from builtins import range
from past.utils import old_div

import os, sys
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import pandas as pd

os.system('cls')
python_version = sys.version
print('\n'+'Script running on Python ' + str(python_version[0]))
#################################
#1. Input and output
#################################

input_pfad = input('\n'+'Please type path to db folder (for example D:\db): ')

if os.path.exists(input_pfad):
    pass
else:
    print('Invalid path')
    sys.exit()

print('\n'+ 'db folder: ' + input_pfad)

output_folder  = input('\n'+'Please type path where pdf files should be created: ')

if os.path.exists(output_folder):
    pass
else:
    print('Invalid path')
    sys.exit()

print('\n'+ 'pdf folder: ' + output_folder)

if os.path.exists(os.path.join(input_pfad,'vector')) or os.path.exists(os.path.join(input_pfad,'raster')) or os.path.exists(os.path.join(input_pfad,'terrain')):
    data_vector = os.path.join(input_pfad, 'vector')
    data_raster = os.path.join(input_pfad, 'raster')
    data_terrain = os.path.join(input_pfad, 'terrain')
    data_SQL = os.path.join(input_pfad, 'SQL')
else:
    data_vector = os.path.join(input_pfad, 'data', 'vector')
    data_raster = os.path.join(input_pfad, 'data', 'raster')
    data_terrain = os.path.join(input_pfad, 'data', 'terrain')
    data_SQL = os.path.join(input_pfad,'data','SQL')


#################################
# 2. Data Frame
# (collect information from map.def and
#  save it in a table-like data type)
#################################

try:
    with open(os.path.join(input_pfad,'EuroNavMedia.ini')) as f:
        content = f.readlines()
        for l in content:
            if 'EAM_Name' in l:
                eam_name = str(l[len('EAM_Name') + 1:])
                if eam_name[-1:] == '\n':
                    eam_name = eam_name[:-1]
except:
    eam_name = 'X.XX.XX'

print('\n'+ eam_name + '\n')

vector_maps, raster_maps, terrain_maps = [],[],[]
name, group, priority, publication, bbmin, bbmax, category, type, lod, xmin, xmax, ymin, ymax, sql = [],[],[],[],[],[],[],[],[],[],[],[],[],[]


def indices_space(s):
    return [pos for pos, char in enumerate(s) if char == ' ']

try:
    num_vector_maps = len(os.listdir(data_vector))
    for e in os.listdir(data_vector):
        vector_maps.append(e)
except:
    num_vector_maps = 0

try:
    num_raster_maps = len(os.listdir(data_raster))
    for e in os.listdir(data_raster):
        raster_maps.append(e)
except:
    num_raster_maps = 0


try:
    num_terrain_maps = len(os.listdir(data_terrain))
    for e in os.listdir(data_terrain):
        terrain_maps.append(e)
except:
    num_terrain_maps = 0

print('Number of datasets: ' + str(num_raster_maps) + ' raster, ' + str(num_vector_maps) + ' vector, ' + str(num_terrain_maps) + ' terrain.' + '\n')

if num_raster_maps == 0 and num_vector_maps == 0 and num_terrain_maps == 0:
    exit_statement = input('There are no raster, vector or terrain data in the db folder.' + '\n' + 'Press ENTER to exit.')
    if input_pfad == "":
        sys.exit()
    else:
        sys.exit()
else:

    maps = [vector_maps,raster_maps,terrain_maps]
    data = [data_vector,data_raster,data_terrain]

    for i in range(0,3):
        for e in maps[i]:
            count_lod = 0

            if i == 0:
                count_label = 0
                if 'jepp' in str(e).lower():
                    for label in os.listdir(data_SQL):
                        if 'JEPP' in label:
                            count_label += 1
                elif 'reppts' in str(e).lower():
                    for label in os.listdir(data_SQL):
                        if 'REPORTINGPOINTS' in label:
                            count_label += 1
                else:
                #elif 'nwork' in str(e) or 'street' in str(e) or 'ne_mid' in str(e) or 'ne_low' in str(e):
                    count_label = 0
                    label_name = str(e).upper()
                    for label in os.listdir(data_SQL):
                        if label_name in label:
                            count_label += 1
                #else:
                #   count_label = -1

            try:

                for e2 in os.listdir(os.path.join(data[i],e)):
                    if os.path.isdir(os.path.join(data[i],e,e2)):
                        count_lod += 1
                    if e2 == 'map.def':

                        # Count to determinate if any parameter is missing

                        count_type = 0
                        count_name = 0
                        count_group = 0
                        count_priority = 0
                        count_category = 0
                        count_publication = 0
                        count_bbmin = 0
                        count_bbmax = 0

                        # Fill the empty lists with data form map.def

                        with open(os.path.join(data[i],e,e2)) as f:
                            content = f.readlines()
                            for l in content:
                                if 'type' in l:
                                    if l[-1:] == '\n':
                                        type.append(str(l[len('type') + 1:-1]))
                                        count_type += 1
                                    elif l[-1:] != '\n':
                                        type.append(str(l[len('type') + 1:]))
                                        count_type += 1
                                elif 'name' in l:
                                    name.append(str(l[len('name') + 1:-1]))
                                    count_name += 1
                                elif 'group' in l:
                                    group.append(str(l[len('group') + 1:-1]))
                                    count_group += 1
                                elif 'priority' in l:
                                    priority.append(int(l[len('priority') + 1:]))
                                    count_priority += 1
                                elif 'category' in l and i == 0:
                                    category.append(str(l[len('category') + 1:]))
                                    count_category += 1
                                elif 'category' in l and i > 0:
                                    category.append(str(l[len('category') + 1:-1]))
                                    count_category += 1
                                elif 'publication' in l:
                                    publication.append(str(l[len('publication') + 1:-1]))
                                    count_publication += 1
                                elif 'bbmin' in l:
                                    xmin.append(round(float(l[indices_space(l)[0]:indices_space(l)[1]]),2))
                                    ymin.append(round(float(l[indices_space(l)[1]:]),2))
                                    count_bbmin += 1
                                elif 'bbmax' in l:
                                    xmax.append(round(float(l[indices_space(l)[0]:indices_space(l)[1]]),2))
                                    ymax.append(round(float(l[indices_space(l)[1]:]),2))
                                    count_bbmax += 1

                            # If there is no data for a parameter in the map.def, add '--'

                            if count_type == 0:
                                type.append('--')
                            if count_name == 0:
                                name.append('--')
                            if count_group == 0:
                                group.append('--')
                            if count_priority == 0:
                                priority.append('--')
                            if count_category == 0:
                                category.append('--')
                            if count_publication == 0:
                                publication.append('--')
                            if count_bbmin == 0:
                                xmin.append('--')
                                ymin.append('--')
                            if count_bbmax == 0:
                                xmax.append('--')
                                ymax.append('--')

                        lod.append(count_lod)

                        if count_label > 0:
                            sql.append('yes')
                        elif count_label == 0:
                            sql.append('no')
                        elif count_label < 0:
                            sql.append('?')

                       # count_label zuruecksetzen
                        count_label = 0

            except:
                pass

    #################################
    # 3. Plot df_ext (Extended)
    #################################

    # Create data frame and order columns as desired

    d_ext = {'TYPE':type, 'NAME':name, 'GROUP':group, 'PRIO.': priority, 'CATEG.':category, 'PUBLIC.':publication, 'LOD':lod, 'XMIN':xmin, 'XMAX':xmax,'YMIN':ymin,'YMAX':ymax, 'SQL':sql}
    df_ext = pd.DataFrame(data=d_ext)
    cols_ext = df_ext.columns.tolist()

    if python_version[0] == '2':
        cols_ext_new = [cols_ext[7], cols_ext[3], cols_ext[1], cols_ext[4], cols_ext[0], cols_ext[5], cols_ext[2],cols_ext[6],cols_ext[9],cols_ext[8],cols_ext[11],cols_ext[10]]
    elif python_version[0] == '3':
        cols_ext_new = [cols_ext[0], cols_ext[1], cols_ext[2], cols_ext[3], cols_ext[4], cols_ext[5], cols_ext[6],cols_ext[11],cols_ext[7],cols_ext[8],cols_ext[9],cols_ext[10]]

    df_ext = df_ext[cols_ext_new]

    # Divide the table each 20 rows

    if df_ext.shape[0] <= 20:
        divided = 'no'
    else:
        divided = 'yes'
        df_list = []
        fig_list = []

        for i in range(0, (old_div(df_ext.shape[0], 20)) + 1):
            if i <= (old_div(df_ext.shape[0], 20)) - 1:
                df_list.append(df_ext[(20*i):(20*(i+1))])
            elif i == (old_div(df_ext.shape[0], 20)):
                df_list.append(df_ext[(20*i):])

    if divided == 'no':

        # Create variables needed to properly show oolors in the table

        colors_vector = [["#FFFFDA","w","w","w","w","w","w","w","w","w","w","w"]] * num_vector_maps
        colors_raster = [["#C8E3C8","w","w","w","w","w","w","w","w","w","w","w"]] * num_raster_maps
        colors_terrain = [["#FFC8C8","w","w","w","w","w","w","w","w","w","w","w"]] * num_terrain_maps
        colors = []
        for c in colors_vector:
            colors.append(c)
        for c in colors_raster:
            colors.append(c)
        for c in colors_terrain:
            colors.append(c)

        # Call the figure (which will be made up of two tables)

        fig, ax = plt.subplots()
        ax.axis('off')

        ax.set_title(eam_name + ' - ' + 'Table 1 of 1' + '\n', fontsize=10)
        #ax.set_title('\n' + eam_name + '\n' + 'Table 1 of 1' + '\n', fontsize=10)

        # Table with all the information

        tabelle = ax.table(cellText=df_ext.values, colLabels=df_ext.columns, colColours = ('#C8C8C8',)*12, cellColours=colors, loc='center', rowLoc = 'center', colLoc='center')
        tabelle.auto_set_font_size(False)
        tabelle.set_fontsize(6)
        tabelle.scale(1.5, 1.5)
        for key, cell in list(tabelle.get_celld().items()):
           cell.set_linewidth(0.5)

        cell_dict = tabelle.get_celld()
        for i in range(0,len(name)+1):
            cell_dict[(i, 1)].set_width(0.25)
        for r in range(0, len(name) + 1):
            for c in range(0, 12):
                cell_dict[(r, c)].set_height(0.05)

        try:
            plt.savefig(output_folder + "\Extended_" + eam_name + ".pdf", bbox_inches = 'tight', format='pdf')
        except:
            exit_statement = input('It was not possible to write the PDF file because a file with the same name is already open.'+ '\n'+'Please close older versions of the PDF file you want to overwrite and run the tool again!!'+ '\n'+'Press ENTER to exit.')
            if input_pfad == "":
                sys.exit()
            else:
                sys.exit()


    if divided == 'yes':

        plots = []

        for i in range(0,len(df_list)):

            # Create variables needed to properly show oolors in the table

            num_vector_maps,num_raster_maps,num_terrain_maps = 0,0,0
            for e in df_list[i]['TYPE']:
                if e[0:5] == 'vecto':
                    num_vector_maps += 1
                elif e == 'raster':
                    num_raster_maps += 1
                elif e == 'terrain':
                    num_terrain_maps += 1

            # Create variables needed to properly show oolors in the table

            colors_vector = [["#FFFFDA","w","w","w","w","w","w","w","w","w","w","w"]] * num_vector_maps
            colors_raster = [["#C8E3C8","w","w","w","w","w","w","w","w","w","w","w"]] * num_raster_maps
            colors_terrain = [["#FFC8C8","w","w","w","w","w","w","w","w","w","w","w"]] * num_terrain_maps
            colors = []
            for c in colors_vector:
                colors.append(c)
            for c in colors_raster:
                colors.append(c)
            for c in colors_terrain:
                colors.append(c)


            # Call the figure (which will be made up of one table with title)

            fig,ax = plt.subplots()
            ax.axis('off')

            ax.set_title(eam_name + ' - Table ' + str(i+ 1) + ' of ' + str(len(df_list)) + '\n', fontsize=10)

            # Table with all the information

            tabelle = ax.table(cellText=df_list[i].values, colLabels=df_list[i].columns, colColours=('#C8C8C8',) * 12,
                                cellColours=colors, loc='center', rowLoc='center', colLoc='center')
            tabelle.auto_set_font_size(False)
            tabelle.set_fontsize(6)
            tabelle.scale(1.5, 1.5)
            for key, cell in list(tabelle.get_celld().items()):
                cell.set_linewidth(0.5)

            cell_dict = tabelle.get_celld()
            for r in range(0, len(df_list[i]['NAME']) + 1):
                cell_dict[(r, 0)].set_width(0.07)
                cell_dict[(r, 1)].set_width(0.19)
                cell_dict[(r, 2)].set_width(0.10)
                cell_dict[(r, 3)].set_width(0.05)
                cell_dict[(r, 4)].set_width(0.08)
                cell_dict[(r, 5)].set_width(0.10)
                cell_dict[(r, 6)].set_width(0.05)
                cell_dict[(r, 7)].set_width(0.05)
                cell_dict[(r, 8)].set_width(0.085)
                cell_dict[(r, 9)].set_width(0.085)
                cell_dict[(r, 10)].set_width(0.075)
                cell_dict[(r, 11)].set_width(0.075)
                for c in range(0,df_list[i].shape[1]):
                    cell_dict[(r, c)].set_height(0.05)

            fig.tight_layout()

            fig_list.append(fig)


        with PdfPages(output_folder +'\Extended_' + eam_name + '.pdf') as pdf:
            for fig in fig_list:
                plt.figure(fig.number)
                pdf.savefig()

    #################################
    # 3. Plot df (Overview)
    #################################

    # Remove 'repeated' maps (z.B. rus_100k_nat_2,rus_100k_nat_3,...)

    rows_to_remove = []
    for i in range(1,len(name)):
        letzte_unterstrich_A = name[i].rfind('_')
        letzte_unterstrich_B = name[i-1].rfind('_')
        if (name[i][:letzte_unterstrich_A] == name[i-1][:letzte_unterstrich_B]) and (name[i].split('_')[len(name[i].split('_'))-1]).isdigit():
            rows_to_remove.append(i)
            name[i-1] = name[i-1][:letzte_unterstrich_B]

    removed_vector, removed_raster, removed_terrain = 0,0,0
    for i in rows_to_remove:
        if type[i]== 'vector':
            removed_vector += 1
        elif type[i]== 'raster':
            removed_raster += 1
        elif type[i]== 'terrain':
            removed_terrain += 1

    for i in sorted(rows_to_remove, reverse=True):
        del name[i]
        del group[i]
        del priority[i]
        del category[i]
        del publication[i]
        del type[i]


    # Create data frame and order columns as desired

    d = {'TYPE':type, 'NAME':name, 'GROUP':group, 'PRIORITY': priority, 'CATEGORY':category, 'PUBLICATION':publication}
    df = pd.DataFrame(data=d)
    cols = df.columns.tolist()

    if python_version[0] == '2':
        cols_new = [cols[5], cols[2], cols[1], cols[3], cols[0], cols[4]]
    if python_version[0] == '3':
        cols_new = [cols[0], cols[1], cols[2], cols[3], cols[4], cols[5]]

    df = df[cols_new]


    # Divide the table each 20 rows

    if df.shape[0] <= 20:
        divided = 'no'
    else:
        divided = 'yes'
        df_list = []
        fig_list = []

        for i in range(0, (old_div(df.shape[0], 20)) + 1):
            if i <= (old_div(df.shape[0], 20)) - 1:
                df_list.append(df[(20*i):(20*(i+1))])
            elif i == (old_div(df.shape[0], 20)):
                df_list.append(df[(20*i):])

    if divided == 'no':

        # Create variables needed to properly show oolors in the table

        colors_vector = [["#FFFFDA","w","w","w","w","w"]] * (num_vector_maps - removed_vector)
        colors_raster = [["#C8E3C8","w","w","w","w","w"]] * (num_raster_maps - removed_raster)
        colors_terrain = [["#FFC8C8","w","w","w","w","w"]] * (num_terrain_maps - removed_terrain)
        colors = []
        for c in colors_vector:
            colors.append(c)
        for c in colors_raster:
            colors.append(c)
        for c in colors_terrain:
            colors.append(c)

        # Call the figure (which will be made up of one table with title)

        fig, ax = plt.subplots()
        ax.axis('off')

        ax.set_title('\n' + eam_name + '\n' + ' - Table 1 of 1' + '\n', fontsize=10)
        ax.table(cellText=df.values, colLabels=df.columns, colColours = ('#C8C8C8',)*6, cellColours=colors, loc='center', rowLoc = 'center left', colLoc='center left')

        try:
            plt.savefig(output_folder + "\Overview_" + eam_name + ".pdf", bbox_inches = 'tight', format='pdf')
        except:
            exit_statement = input('It was not possible to write the PDF file because a file with the same name is already open.'+ '\n'+'Please close older versions of the PDF file you want to overwrite and run the tool again!!'+ '\n'+'Press ENTER to exit.')
            if input_pfad == "":
                sys.exit()
            else:
                sys.exit()

    elif divided == 'yes':

        plots = []

        for i in range(0,len(df_list)):

            # Create variables needed to properly show oolors in the table

            num_vector_maps,num_raster_maps,num_terrain_maps = 0,0,0
            for e in df_list[i]['TYPE']:
                if e == 'vector':
                    num_vector_maps += 1
                elif e == 'raster':
                    num_raster_maps += 1
                elif e == 'terrain':
                    num_terrain_maps += 1

            # Create variables needed to properly show oolors in the table

            colors_vector = [["#FFFFDA","w","w","w","w","w"]] * num_vector_maps
            colors_raster = [["#C8E3C8","w","w","w","w","w"]] * num_raster_maps
            colors_terrain = [["#FFC8C8","w","w","w","w","w"]] * num_terrain_maps
            colors = []
            for c in colors_vector:
                colors.append(c)
            for c in colors_raster:
                colors.append(c)
            for c in colors_terrain:
                colors.append(c)


            # Call the figure (which will be made up of one table with title)

            fig,ax = plt.subplots()
            ax.axis('off')

            ax.set_title(eam_name + ' - Table ' + str(i+ 1) + ' of ' + str(len(df_list)))
            tabelle = ax.table(cellText=df_list[i].values, colLabels=df_list[i].columns, colColours = ('#C8C8C8',)*6, cellColours=colors, loc='center', rowLoc = 'center left', colLoc='center left')
            for key, cell in list(tabelle.get_celld().items()):
                cell.set_linewidth(0.5)
            fig.tight_layout()

            fig_list.append(fig)

        with PdfPages(output_folder +'\Overview_' + eam_name + '.pdf') as pdf:
            for fig in fig_list:
                plt.figure(fig.number)
                pdf.savefig()

    #################################
    # 4. Write csv (Overview)
    #################################

    df.to_csv(output_folder +'\Overview_' + eam_name + '.csv', sep=';')



    print('Two PDF files were created under ' + output_folder + '\n' + '\n' +'Do not forget to remove the EN7 Drive with safely remove!!!'+ '\n')

    exit_statement = input('Press ENTER to exit.')

    if input_pfad == "":
        sys.exit()
    else:
        sys.exit()