import smartsheet
import os
import time
from time import sleep
import PySimpleGUI as sg

form = sg.FlexForm('Smart Sheet Attachments')
layout = [
          [sg.Text('Please enter your API Token, Sheet ID, Directory Path (no quotation marks), and Starting Row.')],
          [sg.Text('API Token', size=(15, 1)), sg.InputText('')],
          [sg.Text('Sheet ID', size=(15, 1)), sg.InputText('')],
          [sg.Text('Image Folder Path', size=(15, 1)), sg.InputText(''), sg.FolderBrowse()],
           [sg.Text('Start Row', size=(15, 1)), sg.InputText('')],
          [sg.Submit(), sg.Cancel()]
         ]

button, values = form.Layout(layout).Read()
form.Close()
#print(button, values[0], values[1], values[2], values[3])


# API_Token = input("Enter API Token: ")             # Input functions used prior to GUI
API_Token = values[0]
# sheet_id = input("Enter Sheet ID: ")      
sheet_id = int(values[1])
# basepath = input("Enter Directory Path: ")
basepath = values[2]
# start = input("Enter Start Row: ")                  
start = int(values[3])


                                                      # Get the sheet
smart = smartsheet.Smartsheet(API_Token) 
sheet = smart.Sheets.get_sheet(sheet_id)

                                                      # Get array of all files in directory
files = []
                                                      # Loop through every file in the folder and append each one to the new files array
for entry in os.listdir(basepath):
  #print(entry)                                       # Print function used to check entries in directory, and then commented out
  files.append(entry)
  #print(files)                                       # Print function used to check contents of new array being built from directory files, then commented out

                                                      # Loop through and attach each file to its specific row (Sequential after starting row)
startRow = int(start)
for x in range(0,len(files)):
  #print(sheet.rows[x].id_)                           # Print function used to verify that the loop iterates through each row ID in order, then commented out
  sleep(5)                                            # Sleep function is used to force the program to wait to upload a new attachment. This avoids hitting the upload rate limit
  sg.OneLineProgressMeter('Progress',x+1,len(files),'key')
  smart.Attachments.attach_file_to_row(               # Function to attach a file to a row. Need to give the Sheet ID, Row ID, File Name, and FULL File Path
  sheet_id,                                           # Sheet ID passed from GUI
  sheet.rows[startRow + x - 1].id_,                   # Loops through the row IDs for the sheet
  (str(files[x]),                                     # Loops through and names the file properly
    open(str(basepath)+'//'+ str(files[x]), 'rb'),    # add base path and file name together to get the file's full path and to get the right file
    'application/msword')                             # application/msword does not seem to do anything because this is uploading JPG images and nothing bad happens
)
