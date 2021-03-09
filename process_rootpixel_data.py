import csv
import math
import numpy as np

data_files = ["1259-1265.csv",
              "1266-1276.csv",
              "1277-1280_1282.csv",
              "1283-1285.csv",
              "1286_1342.csv",
              "1287-1291_1317-1323.csv",
              "1292-1294.csv",
              "1295-1299.csv",
              "1300-1304.csv",
              "1305-1308.csv",
              "1309-1316.csv",
              "1324-1328.csv",
              "1329-1334.csv",
              #"1330.csv",
              "1331-1332.csv",
              "1333-1336.csv",
              "1337-1341.csv",
              #"1342.csv", MISSING?
              "1343-1345.csv",
              "1346-1347.csv",
              "1348-1350.csv",
              "1351-1354.csv",
              "1355-1358.csv",
              "1359-1364.csv",
              "1365-1369.csv",
              "1370-1373.csv",
              "1373-1377.csv",
              "1379-1384.csv",
              "1385-1394.csv",
              "1395-1404.csv",
              "1405-1409.csv",
              "1410-1417.csv",
              "1415-1417_1431_1434.csv",
              "1418_1429-1431_1433.csv",
              "1419-1421.csv",
              "1422-1424.csv",
              "1425-1428.csv",
              "1435-1444.csv",
              #"1436.csv",
              #"1437-1438.csv",
              #"1439.csv",
             ]

#data_files = ["1277-1280_1282.csv",
#             ]

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
