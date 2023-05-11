'''
This Python script processes data from multiple CSV files containing information about plants. The data includes the plant ID, the number of roots per whorl, the width of the leftmost root, the width of the stalk, the height and width of the roots on the left and right sides, and other measurements.

The script defines a function is_header that checks if a row in the CSV file is a header row. If it is, the row is skipped.

The script then iterates over each file in the data_files list and opens it using the csv module. For each row in the file, it checks if it is a header row using the is_header function. If it is not a header row, it processes the data in the row.

The script calculates various values such as the pixels per inch (ppi), the number of whorls (num_whorls), and the width of the spread (spread_width) using the data in the row. It also calculates the angle of the roots on the left and right sides in degrees (root_angledeg_left and root_angledeg_right) using the math.atan function.

The calculated values are stored in a list (data_list) and added to a dictionary (plant_dict) with the plant ID as the key.

After all rows in all files have been processed, the script sorts the keys of plant_dict and appends their corresponding values to a list (plant_data). It then writes this data to a new CSV file called processed_root_data.csv.

The script also prints some information to the console such as the number of plots processed, the number of image data saved, and other statistics.
'''

import csv
import math
import numpy as np

data_files = ["1259-1265.csv",
              "1277-1280_1282.csv"
             ]



def is_header(curr_row):
    if curr_row[0] == 'Plant ID':
        print('removing header')
        return True
    else:
        return False

plots = []
plants = []
plant_data = []
plant_dict = {}
for i in range(len(data_files)):
    print(data_files[i])
    with open(data_files[i]) as csv_file:
        csv_reader = csv.reader(csv_file, skipinitialspace=True, delimiter=',')
        line_count = 0
        for row in csv_reader:
            # ID pixheight w1 w2 w3 w4 leftrootwide stalkwide rootheightleft rootlenleft rootheighright rootlenright
            # FOR TROUBLESHOOTING -------> print(row)
            print(row)
            whorl_cnt = 0
            if is_header(row):
                pass
            else:
                plantid = row[0]
                plants.append(plantid)
                plot = plantid.split("_")[0]
                if len(plantid.split("_")[1]) == 2:
                    # Fix plant ID (1 -> 01) so plant 1 sorts before 10
                    plantid = str(plantid.split("_")[0]) + '_0' + str(plantid.split("_")[1])
                if not plot in plots:
                    plots.append(plot)
                ppi = 0.5/float(row[1])  # pixels per inch
                roots_per_whorl = np.zeros(4)
                for j in range(4):
                    if row[2+j] == '':
                        pass
                    else:
                       roots_per_whorl[j] = int(row[2+j])
                       whorl_cnt += 1
                num_whorls = whorl_cnt
                w1,w2,w3,w4 = roots_per_whorl
                leftmost_root_width = float(row[6])*ppi
                stalk_width = float(row[7])*ppi
                root_height_left = float(row[8])*ppi
                root_width_left = float(row[9])*ppi
                root_height_right = float(row[10])*ppi
                root_width_right = float(row[11])*ppi
                try:
                    root_anglerad_left = math.atan(root_width_left/root_height_left)
                    root_anglerad_right = math.atan(root_width_right/root_height_right)
                    root_angledeg_left = 180 * root_anglerad_left/math.pi
                    root_angledeg_right = 180 * root_anglerad_right/math.pi
                except:
                    # if there is a tagging error then div 0 will be overwritten by redo, this is a temp fix to pass the zero angle measurement
                    root_angledeg_left, root_angledeg_right = [0,0]
                spread_width = root_width_left + root_width_right + stalk_width
                data_list=[plantid, stalk_width, leftmost_root_width, num_whorls, w1,w2,w3,w4, \
                          root_height_left, root_width_left, root_angledeg_left, \
                          root_height_right, root_width_right, root_angledeg_right, \
                          spread_width]
                plant_dict[plantid] = data_list
            line_count += 1
for key in sorted(plant_dict.keys()):
    print(plant_dict[key])
    plant_data.append(plant_dict[key])
#print(plant_data)
#print(plant_dict)
#print(plants)
print('Plots processed: ' + str(plots))
print('Image data saved: ' + str(len(plant_data)))
print(len(plant_data), len(plant_dict))

print('Writing data to .csv')
with open('processed_root_data.csv', 'wb') as f:
    w = csv.writer(f)
    data_header = ['plantid', 'stalk_width', 'leftmost_single_root_width', 'num_whorls', 'w1','w2','w3','w4', \
          'root_heightonstalk_left', 'stalk_to_leftmost_rootgrounding', 'root_angledeg_left', \
          'root_heightonstalk_right', 'stalk_to_rightmost_rootgrounding', 'root_angledeg_right', \
          'spread_width']
    w.writerow(data_header)
    for item in plant_data:
       w.writerow(item)
