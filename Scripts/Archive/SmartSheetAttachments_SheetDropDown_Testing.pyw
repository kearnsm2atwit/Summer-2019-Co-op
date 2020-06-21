import smartsheet
import os
import time
from time import sleep
import PySimpleGUI as sg

form1 = sg.FlexForm('Smart Sheet Attachments API Token')
form2 = sg.FlexForm('Sheet Information')
layout01 = [
          [sg.Text('Please enter your API Token')],
          [sg.Text('API Token', size=(15, 1)), sg.InputText('')],
          [sg.Submit(), sg.Cancel()]
         ]


button, values = form1.Layout(layout01).Read()
form1.Close()
API_Token = values[0]
smart = smartsheet.Smartsheet(API_Token)

response = smart.Sheets.list_sheets(API_Token)
sheets = response.data



sheetNames = []
for x in range(0,len(sheets)):
  #print(sheets[x].name)
  sheetNames.append(sheets[x].name)

layout02 = [
          [sg.Text('Please select your Sheet, Image Folder, and Starting Row.')],
          [sg.InputCombo(sheetNames)],
          [sg.Text('Image Folder', size=(15, 1)), sg.InputText(''), sg.FolderBrowse()],
          [sg.Text('Start Row', size=(15, 1)), sg.InputText('')],
          [sg.Submit(), sg.Cancel()]
         ]




button, values = form2.Layout(layout02).Read()
form2.Close()
sheetName = values[0]
#print(sheetName)
index = 0
for x in range(0,len(sheets)):
  if sheetName == sheets[x].name:
    index = x
#print(sheets[index].id_)
sheet_id = sheets[index].id_
sheet = smart.Sheets.get_sheet(sheet_id)
basepath = values[1]
startRow = int(values[2])


                                                      
files = []                                                      # Create array to store file names from directory
                                                     
for entry in os.listdir(basepath):                              # Loop through every file in the folder and append each one to the new files array
  #print(entry)                                                 # Print function used to check entries in directory, and then commented out
  files.append(entry)                                           # Add entries to files array
  #print(files)                                                 # Print function used to check contents of new array being built from directory files, then commented out

                                                      
for x in range(0,len(files)):                                   # Loop through and attach each file to its specific row (Sequential after starting row)
  #print(sheet.rows[x].id_)                                     # Print function used to verify that the loop iterates through each row ID in order, then commented out
  sleep(5)                                                      # Sleep function is used to force the program to wait to upload a new attachment. This avoids hitting the upload rate limit
  #sg.OneLineProgressMeter('Progress',x+1,len(files),'key')
  smart.Attachments.attach_file_to_row(                         # Function to attach a file to a row. Need to give the Sheet ID, Row ID, File Name, and FULL File Path
  sheet_id,                                                     # Sheet ID passed from GUI
  sheet.rows[startRow + x - 1].id_,                             # Loops through the row IDs for the sheet
  (str(files[x]),                                               # Loops through and names the file properly
    open(str(basepath)+'//'+ str(files[x]), 'rb'),              # add base path and file name together to get the file's full path and to get the right file
    'application/msword')                                       # application/msword does not seem to do anything because this is uploading JPG images and nothing bad happens
)