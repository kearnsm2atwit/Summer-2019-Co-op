import xml.etree.ElementTree as ET
import xlwt
from xlwt import Workbook
import PySimpleGUI as sg
import os

def CreateGUI():
    form = sg.FlexForm('Navisworks Exports')
    layout = [                                                                             
            [sg.Text('Please enter your XML file')],
            [sg.Text('XML File', size=(16, 1)), sg.InputText(''), sg.FileBrowse()],               
            [sg.Text('New File Location', size=(16,1)), sg.InputText(''), sg.FolderBrowse()],
            [sg.Text('New Excel File Name', size=(16, 1)), sg.InputText('')],
            [sg.Text('Image Folder', size=(16, 1)), sg.InputText(''), sg.FolderBrowse()],
            [sg.Submit(), sg.Cancel()]
            ]
    button, values = form.Layout(layout).Read()
    form.Close()

    return values


#values = CreateGUI()


# path = values[0]
path = r'C:\Users\kearnsm2\Desktop\Summer 2019 Co-op\Python Scripts\Resources\XML_Testing\Comments.xml'
# save_path = values[1]
# file_name = values[2]
# image_path = values[3]

tree = ET.parse(path)
root = tree.getroot()

# def XML_Parse(root):
#     viewfolders = []
#     for x in range(0,len(root[0])):
#         viewfolders.append(root[0][x])
#         print(viewfolders[x])

# XML_Parse(root)

wb = Workbook()
sheet1 = wb.add_sheet('Sheet 1')

def find_views_in_folder(folder, count):
        for elem in list(folder):
                if elem.tag == 'view':
                        count += 1
                else:
                        count += find_views_in_folder(elem, 0)
        return count

def recursion(root, column):
        if root.tag == 'viewfolder':
                count = find_views_in_folder(root, 0)
                print(root.get('name'))
                for x in range(0,len(count)):
                        sheet1.write(x,column,root.get('name'))
                print(count)
        for elem in list(root):
                recursion(elem,0)

recursion(root, 0)
#wb.save('test.xls')


def find_comments(root):
        comments = root.findall('view')
        for x in range(0,len(comments)):
                #print(x)
                real_comments = comments[x].findall('commments') 
                for x in range(0,len(real_comments)):
                        print(x)
                        print(real_comments[x].get('body'))
        for elem in list(root):
                find_comments(elem)

find_comments(root)