import xml.etree.ElementTree as ET                                                              # Import all necessary modules
import xlwt                                                                                     
from xlwt import Workbook
import PySimpleGUI as sg
import os

form = sg.FlexForm('Smart Sheet Attachments')                                                   # Create form for GUI from PySimpleGUI
layout = [                                                                                      # Create Layout for window
          [sg.Text('Please enter your XML file')],
          [sg.Text('XML File', size=(16, 1)), sg.InputText(''), sg.FileBrowse()],               # File browser to locate XML file
          [sg.Text('New File Location', size=(16,1)), sg.InputText(''), sg.FolderBrowse()],
          [sg.Text('New Excel File Name', size=(16, 1)), sg.InputText('')],
          [sg.Text('Image Folder', size=(16, 1)), sg.InputText(''), sg.FolderBrowse()],
          [sg.Submit(), sg.Cancel()]
         ]

button, values = form.Layout(layout).Read()                                                     # Read buttons from GUI
form.Close()                                                                                    # Close GUI window

path = values[0]                                                                                # Set file location equal to variable for later use
file_name = values[2]
save_path = values[1]
image_path = values[3]
tree = ET.parse(path)                                                                           # Create tree from XML file
root = tree.getroot()                                                                           # Get root of XML file


viewfolders = []                                                                                # Empty array for storing all viewfolder elements
for x in range(0,len(root)):                                                                    # Iterate one step down from root to get all viewfolders
    for y in range(0,len(root[x])):                                                             # Nested for loop to get "down" one level         
        viewfolders.append(root[x][y])                                                          # Append all viewfolders to array created earlier


viewpoints = []                                                                                 # Create empty array to store elements that are two steps down in the tree

#THIS WORKS FOR A RIGID FOLDER AND VIEWPOINT STRUCTURE (2 FOLDERS)

for x in range(0,len(viewfolders)):                                                             # For loop to iterate through all the viewfolders
    #print(viewfolders[x].get('name'))                                                          # Print function to help see what the names of the folders are
    folder_name = viewfolders[x].get('name')                                                    # Save the folder name to a variable for later use
    for y in range(0,len(viewfolders[x])):                                                      # For loop to iterate through each folder
        #print(viewfolders[x][y].get('name'))                                                   # Print function to see the name of elements inside of each folder
        viewpoint_or_folder_name = viewfolders[x][y].get('name')                                # Save the name of the elements inside the folder to a variable
        for view in viewfolders[x][y].findall('view'):                                          # For loop to get all the names of anything inside folders found previously
            views = view.get('name')                                                            # Save name to a variable
            #print(view.get('name'))                                                            # Print to see what name is being stored
            string = folder_name + '_' + viewpoint_or_folder_name + '_' + views                 # Create a string to concatenate all information taken from XML file. The double underscores are added so they can be pulled apart later on
            #string = views + '_' + viewpoint_or_folder_name + '_' + folder_name                # Better (After testing it may be worse) way of formatting string to be able to have a variety of folder and viewpoint structure
            viewpoints.append(string)                                                           # Append that single string line to an array

files = []                                                                                                                                      # Empty array to store image file names
for entry in os.listdir(image_path):                                                                                                            # Iterate through every file in the directory (folder)
        files.append(entry)                                                                                                                     # Append every file in directory to the files array created previously

for x in range(0,len(viewpoints)):                                                                                                              # Iterate through every viewpoint
        if x < 10:                                                                                                                              # Want images less than 10 (0-9) to have an extra 0 in front of them to maintain order
                os.rename(str(image_path + '//' + files[x]), str(image_path + '//' + '0' + str(x) + '_' + viewpoints[x] + '.jpg'))              # Renaming the images with the viewpoint name and then extra information like index in front
        else:                                                                                                                                   # For all the images that have a index greater than or equal to 10
                os.rename(str(image_path + '//' + files[x]), str(image_path + '//' + str(x) + '_' + viewpoints[x] + '.jpg'))                    # Rename them based on corresponding viewpoint, add index out front (doesnt need extra 0)

#Creating brand new excel file based on XML information
wb = Workbook()                                                                                 # Set up new excel workbook
sheet1 = wb.add_sheet('Sheet 1')                                                                # Create new sheet for workbook


for x in range(0,len(viewpoints)):                                                              # For loop to go through each string that was created
    print(viewpoints[x])                                                                        # Print to check what the strings are
    split_views = viewpoints[x].split('_')                                                      # Split the strings based on how they were created earlier. This is a lot easier than having multiple nested for loops to get the information to go into the right cells in excel
    for y in range(0,len(split_views)):                                                         # The strings were split and saved in a temp array, so this nested for loop goes through that temp array and puts each entry into its own column
            sheet1.write(x,y,split_views[y])                                                    # Write to each cell. The index in the viewpoints array determines the row and the index in the temporary split string array determines the column. The name comes from the split string array as well

wb.save(save_path + '\\' + file_name + '.xls')                                                  # Save the sheet, can give it any name. The sheet is saved in an excel file in the same location as this python script.