import smartsheet                                                                               # Import all necessary packages
import os
import time
from time import sleep
import PySimpleGUI as sg
import xml.etree.ElementTree as ET
import xlwt as Workbook

form = sg.FlexForm('Smartsheet')                                                                # Create form for GUI from PySimpleGUI
layout = [                                                                                      # Create Layout for window
          [sg.Text('Please Enter Information')],
          [sg.Text('XML File', size=(16, 1)), sg.InputText(''), sg.FileBrowse()],               # File browser to locate XML file
          [sg.Text('Image Folder', size=(16,1)), sg.InputText(''), sg.FolderBrowse()],          # Folder browser for image folder
          [sg.Text('API Token', size=(16, 1)), sg.InputText('')],
          [sg.Text('New Sheet Name', size = (16,1)), sg.InputText('')],
          [sg.Submit(), sg.Cancel()]
         ]

button, values = form.Layout(layout).Read()                                                     # Read buttons from GUI
form.Close()                                                                                    # Close the window

path = values[0]                                                                                # Variable named path to store location from window
image_path = values[1]                                                                          # Variable named image_path to store location to image folder from window
API_Token = values[2]                                                                           # Variable named API_Token to store the API Token given by user in window
sheet_name = values[3]                                                                          # Variable named sheet_name to store desired name of the new smartsheet

smart = smartsheet.Smartsheet(API_Token)                                                        # Initialize smartsheet client using API Token. Can be thought of as 'logging in'


tree = ET.parse(path)                                                                           # Set up tree element based on the XML file. This gives the raw XML file a structure 
root = tree.getroot()                                                                           # Get root, or base on XML file

new_sheet = smartsheet.models.Sheet({                                                           # Set up new sheet, give it a name and a bunch of columns because it doesnt start off with any columns
    'name': sheet_name,
    'columns': [{
        'title': 'Primary',                                                                     # One of the columns must be the primary column
        'primary': True,
        'type': 'TEXT_NUMBER'
    }, {
        'title': 'Column 1',
        'type': 'TEXT_NUMBER'
    }, {
        'title': 'Column 2',
        'type': 'TEXT_NUMBER'
    }, {
        'title': 'Column 3',
        'type': 'TEXT_NUMBER'
    }, {
        'title': 'Column 4',
        'type': 'TEXT_NUMBER'
    }, {
        'title': 'Column 5',
        'type': 'TEXT_NUMBER'
    }, {
        'title': 'Column 6',
        'type': 'TEXT_NUMBER'
    }, {
        'title': 'Column 7',
        'type': 'TEXT_NUMBER'
    }, {
        'title': 'Column 8',
        'type': 'TEXT_NUMBER'
    }, {
        'title': 'Column 9',
        'type': 'TEXT_NUMBER'
    }, {
        'title': 'Column 10',
        'type': 'TEXT_NUMBER'
    }, {
        'title': 'Column 11',
        'type': 'TEXT_NUMBER'
    }, {
        'title': 'Column 12',
        'type': 'TEXT_NUMBER'
    }, {
        'title': 'Column 13',
        'type': 'TEXT_NUMBER'
    }, {
        'title': 'Column 14',
        'type': 'TEXT_NUMBER'
    }, {
        'title': 'Column 15',
        'type': 'TEXT_NUMBER'
    }]
})
response = smart.Home.create_sheet(new_sheet)           # Save the response to the creation of the new sheet
new_sheet = response.result                             # Save the response results, which is the sheet object

#print(new_sheet.id)                                    # Print function to check what the new sheet's ID is 
sheet_id = new_sheet.id                                 # Save the new sheet's ID for later use

def add_new_row(columnID, sheet_ID, cellInfo):          # New function to add rows to a sheet. Need to pass array of columns to use, and sheet ID. Also need to pass what information is going to filll each new cell
  row_a = smartsheet.models.Row()                       # Create new row object outside of for loop so it doesnt re-create over the old object each iteration
  row_a.to_bottom = True                                # Append new row to the bottom of the sheet
  for x in range(0,len(cellInfo)):                      # For loop to append information for each cell for as long as there is information to append
    row_a.cells.append({                                # Append cells
      'column_id': columnID[x],                         # To append cells, need the column ID      
      'value': cellInfo[x]                              # Can put values or information into new cells
    })
  response = smart.Sheets.add_rows(                     # Update the sheet with the new rows        
    sheet_ID,                                           # Need to give sheet ID
    [row_a])                                            # Need to give array of row objects, will add rows in order of array


viewfolders = []                                                                                # Empty array for storing all viewfolder elements
for x in range(0,len(root)):                                                                    # Iterate one step down from root to get all viewfolders
    for y in range(0,len(root[x])):                                                             # Nested for loop to get "down" one level         
        viewfolders.append(root[x][y])                                                          # Append all viewfolders to the array for later use


viewpoints = []                                                                                 # Empty array to store all thre viewpoint names
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
            viewpoints.append(string)
              

columnIDs = []                                                      # Create empty array to store all the column IDs
for x in range(0,len(new_sheet.columns)):                           # Iterate through all the column objects in the new sheet
    columnIDs.append(new_sheet.columns[x].id)                       # Append each column ID to column ID array
    #print(new_sheet.columns[x].id)                                 # Test print function to check if its storing the right things 
for x in range(0,len(viewpoints)):                                  # Iterate through all the viewpoints 
    split_views = viewpoints[x].split('_')                          # Split all the viewpoint names to parse information 
    add_new_row(columnIDs, sheet_id, split_views)                   # Add new rows to the smartsheet with the information from the split views


sheet = smart.Sheets.get_sheet(sheet_id)                            # Get an updated sheet after the new rows are added to make sure all IDs are there

files = []                                                          # Empty array to hold all file names 

for entry in os.listdir(image_path):                                # Iterate through all files in folder path
        files.append(entry)                                         # Append all files in folder to files array

for x in range(0,len(viewpoints)):                                  # Iterate through all viewpoints to rename images
    if x < 10:                                                      # If the index, x, is less than 10
        files[x] = '0' + str(x) + '_' + viewpoints[x]               # Add an extra '0' in front to avoid '10' being sorted before '2'. So '2' becomes '02'
    else:                                                           # Else, so if the index, x, is greater than or equal to 10
        files[x] = str(x) + '_' + viewpoints[x]                     # Rename files with number in front and rename it using the viewpoint name


for x in range(0,len(files)):                                       # For loop to loop the same amount of times as there are files to upload
    if len(files >= 30):                                            # If we are uploading 30 files or more, the rate limit will be exceeded
        sleep(5)                                                    # To account for this, wait 5 seconds per upload. This is very slow but hitting the rate limit makes it even slower
    smart.Attachments.attach_file_to_row(                           # Smartsheet API function to attach a file to a row
        sheet_id,                                                   # Need to give sheet ID
        sheet.rows[x].id_,                                          # Pass through the row ID in accordance to the for loop, so it'll go down sequentially
        (str(files[x]),                                             # Specifify the attachments name
        open(str(image_path) + '//' + str(files[x]), 'rb'),         # Specify the location of the attachment so it can be uploaded
        'application/msword')                                       # I'm 99% sure this part does not do anything but I am afraid to take it out
    )                                                               