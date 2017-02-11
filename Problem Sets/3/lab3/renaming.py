
import os
import csv

nameToId = dict()

with open('C:\Users\Cojocaru\Desktop\Oppla_img\imgs_Names_users.csv', 'rb') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',')
    for row in spamreader:
        nameToId[row[4]] = "user_" + row[0] + ".jpg";

print nameToId

path = "C:\Users\Cojocaru\Desktop\Oppla_img"
for filename in os.listdir(path):
    if nameToId.get(filename):
        #print nameToId[filename]
        whole_path = path + "\\" + filename
        #print whole_path
        os.rename(whole_path,path + "\\" + nameToId[filename])