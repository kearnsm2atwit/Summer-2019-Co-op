import smartsheet                                                       # Import all needed packages
import os
import time
from time import sleep
import PySimpleGUI as sg

form1 = sg.FlexForm('Smart Sheet Attachments API Token')                # Create separate forms depending on what the window needs to display
form2 = sg.FlexForm('Sheet Information')                                # Form for second window
layout01 = [                                                            # Create layout for first window
          [sg.Text('Please enter your API Token')],                     # API Token Window Header
          [sg.Text('API Token', size=(15, 1)), sg.InputText('')],       # Input for API Token as text
          [sg.Submit(), sg.Cancel()]                                    # Buttons for Submit and Cancel
         ] 


button, values = form1.Layout(layout01).Read()                          # Present form 1 and get read information
form1.Close()                                                           # Once form is submitted, close window
API_Token = values[0]                                                   # Store value taken from window to API_Token variable
smart = smartsheet.Smartsheet(API_Token)                                # Initialize smartsheet API using token

response = smart.Sheets.list_sheets(API_Token)                          # Get a list of all sheets
sheets = response.data                                                  # Store list of sheet data in variable sheets


sheetNames = []                                                         # Create empty array to store sheet names
for x in range(0,len(sheets)):                                          # Iterate through all sheets
  print(sheets[x].name)                                                 # Print function to determine funtionality
  sheetNames.append(sheets[x].name)                                     # Append all sheet names to sheetNames array

layout02 = [                                                                              # Create layout for second window
          [sg.Text('Please select your Sheet, Image Folder, and Starting Row.')],         # Header for window
          [sg.InputCombo(sheetNames)],                                                    # Drop down list containing options for every sheet name
          [sg.Text('Image Folder', size=(15, 1)), sg.InputText(''), sg.FolderBrowse()],   # Browse to image folder destination
          [sg.Text('Start Row', size=(15, 1)), sg.InputText('')],                         # Input for start row as string
          [sg.Submit(), sg.Cancel()]                                                      # Buttons for Submit and Cancel
         ]




button, values = form2.Layout(layout02).Read()                            # Present second window and read information
form2.Close()                                                             # When information is submitted, close window
sheetName = values[0]                                                     # Store selected sheet name to variable sheetName
print(sheetName)                                                          # Print to check value of sheetName variable
index = 0                                                                 # Create new index to save value of index to match name to ID
for x in range(0,len(sheets)):                                            # For loop for every sheet name
  if sheetName == sheets[x].name:                                         # Iterate through names to match up and then save index
    index = x                                                             # Store index needed to index variable for later use
print(sheets[index].id_)                                                  # Print to check if that the ID matches the sheet name
sheet_id = sheets[index].id_                                              # Store sheet ID fpr later use
sheet = smart.Sheets.get_sheet(sheet_id)                                  # Initialize sheet using sheet ID
basepath = values[1]                                                      # Store path from GUI window to basepath variable
startRow = int(values[2])                                                 # Store start row value, convert from string to integer


                                                      
files = []                                                      # Create array to store file names from directory
                                                     
for entry in os.listdir(basepath):                              # Loop through every file in the folder and append each one to the new files array
  print(entry)                                                  # Print function used to check entries in directory, and then commented out
  files.append(entry)                                           # Add entries to files array
  print(files)                                                  # Print function used to check contents of new array being built from directory files, then commented out

                                                      
for x in range(0,len(files)):                                   # Loop through and attach each file to its specific row (Sequential after starting row)
  #print(sheet.rows[x].id_)                                     # Print function used to verify that the loop iterates through each row ID in order, then commented out
  #sleep(5)                                                     # Sleep function is used to force the program to wait to upload a new attachment. This avoids hitting the upload rate limit
  sg.OneLineProgressMeter('Progress',x+1,len(files),'key')
  smart.Attachments.attach_file_to_row(                         # Function to attach a file to a row. Need to give the Sheet ID, Row ID, File Name, and FULL File Path
  sheet_id,                                                     # Sheet ID passed from GUI
  sheet.rows[startRow + x - 1].id_,                             # Loops through the row IDs for the sheet
  (str(files[x]),                                               # Loops through and names the file properly
    open(str(basepath)+'//'+ str(files[x]), 'rb'),              # add base path and file name together to get the file's full path and to get the right file
    'application/msword')                                       # application/msword does not seem to do anything because this is uploading JPG images and nothing bad happens
)