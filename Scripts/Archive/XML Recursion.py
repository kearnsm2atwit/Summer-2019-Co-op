import xml.etree.ElementTree as ET
import xlwt
from xlwt import Workbook

path = r'C:\Users\kearnsm2\Desktop\Summer 2019 Co-op\Python Scripts\Resources\XML_Testing\Alnylam_MASTER.xml'


class viewfolder(object):
    level = 0
    views = 0
    name = ''

    def __init__(self, level, views, name):
        self.level = level
        self.views = views
        self.name = name


def make_viewfolder(level, views, name):
    folder = viewfolder(level, views, name)
    return folder



tree = ET.parse(path)
root = tree.getroot()
wb = Workbook()
sheet1 = wb.add_sheet('Sheet 1')

def all_views(root, count):
    for elem in list(root):
        if elem.tag == 'view':
            count += 1
        else:
            count += all_views(elem, 0)
    return count

def views(root, view_names):
    if root.tag == 'view':
        view_names.append(root.get('name'))
    for elem in list(root):
        views(elem, view_names)
    return view_names

view_names = views(root, [])
for x in range(0,len(view_names)):
    print(view_names[x])

def folder_level(root, index, folders):
    index += 1
    if root.tag == 'viewfolder':
        #print(root.get('name'))
        rows = all_views(root,0)
        #print(rows, index)
        folders.append(make_viewfolder(index,rows,root.get('name')))
        #print(len(folders))
    for elem in list(root):
        folder_level(elem, index, folders)
    return folders

folders = folder_level(root[0][0], 0, [])


levels = []
for x in range(0,len(folders)):
    levels = []
    levels.append(folders[x].level)
max_lvl = max(levels)
print(max_lvl)
cells = []

for x in range(0,max_lvl):
    columns =[]
    for y in range(0,len(folders)):
        if folders[y].level == x+1:
            for z in range(0,folders[y].views):
                columns.append(folders[y].name)
    cells.append(columns)

for x in range(0,len(cells)):
    for y in range(0,len(cells[x])):
        print(cells[x][y])
        sheet1.write(y,x,cells[x][y])

for x in range(0,len(view_names)):
    split_views = view_names[x].split('_')
    for y in range(0,len(split_views)):
        sheet1.write(x,max_lvl + y,split_views[y])

wb.save('Test.xls')