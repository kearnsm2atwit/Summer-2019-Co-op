import xml.etree.ElementTree as ET                          # Import all necessary packages
import xlwt
from xlwt import Workbook


def views(root, view_names):                            # Create function to get all viewnames in the XML file
    if root.tag == 'view':                              # If the current element is a viewpoint
        view_names.append(root)                         # Append that viewpoint name to view_names array
    for elem in list(root):                             # Iterate through every element beneath current
        views(elem, view_names)                         # Recurse through all those elements, which would append all viewnames
    return view_names  

def view_names(view):
    return view.get('name')

def comments(view):
    body_names = ''
    if len(view) > 3:
        if view[2].tag == 'comments':
            for x in range(0,len(view[2])):
                date = view[2][x][2][0].get('month') + '/' + view[2][x][2][0].get('day') + '/' + view[2][x][2][0].get('year')
                body_names += '\n' + str(x + 1) + ') ' + 'Date Created: ' + date + '\n' + '   Body: ' + (view[2][x][1].text) + '\n' +  '  Status: ' + view[2][x].get('status')
            return(body_names)
    else:
        return('No Comment')

tree = ET.parse(r'C:\Users\kearnsm2\Desktop\BCAHS_SC_Gilbane_Central 26-July-2019.xml')
root = tree.getroot()
views = views(root,[])
viewNames = []

for x in range(0,len(views)):
    viewNames.append(view_names(views[x]))

all_comments = []
for x in range(0,len(views)):
    all_comments.append(comments(views[x]))
print(len(all_comments))

view_lengths = []
for x in range(0,len(viewNames)):
    split_views = viewNames[x].split('_')
    view_lengths.append(len(split_views))
    print(split_views)