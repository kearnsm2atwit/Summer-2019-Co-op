import smartsheet                                   # Import package used to work with the smartsheet API
import xml.etree.ElementTree as ET                  # Import package used to parse XML files
import numpy as np                                  # Import numpy just to use the randn function to generate random numbers



sheetID = 8286687336916868                          # Store sheet ID in a variable for easy re-use


API_Token = 'wmo1vbwmgpmw229kkh1ygqqhcn'            # API Token to access smartsheets
sheet_id = sheetID                                  # Sheet ID to identify what sheet I want to work with


smart = smartsheet.Smartsheet(API_Token)            # Initialize smartsheet client
sheet = smart.Sheets.get_sheet(sheet_id)            # Get sheet


column_ids = []                                     # Create empty array to store column IDs                                      
for x in range(0,len(sheet.columns)):               # For loop to go through each column in the sheet
  #print(sheet.columns[x].id_)                      # Print function to test that it is getting each column ID
  column_ids.append(sheet.columns[x].id_)           # While iterating through each column, get its ID and append (add) it to the column_ids array






def add_new_row(columnID, sheet_ID, cellInfo):        # New function to add rows to a sheet. Need to pass array of columns to use, and sheet ID. Also need to pass what information is going to filll each new cell
  row_a = smartsheet.models.Row()                     # Create new row object outside of for loop so it doesnt re-create over the old object each iteration
  row_a.to_bottom = True                              # Append new row to the bottom of the sheet
  for x in range(0,len(cellInfo)):                    # For loop to append information for each cell for as long as there is information to append
    row_a.cells.append({                              # Append cells
      'column_id': columnID[x],                       # To append cells, need the column ID      
      'value': cellInfo[x]                            # Can put values or information into new cells
    })
  response = smart.Sheets.add_rows(                   # Update the sheet with the new rows        
    sheet_ID,                                         # Need to give sheet ID
    [row_a])                                          # Need to give array of row objects, will add rows in order of array




# For example, could create new array and append new entries of the array cell_info based on information provided from XML

CellArray = []
for x in range(0,3):
  cell_info = [np.random.randn(),np.random.randn(),np.random.randn(),np.random.randn()]
  CellArray.append(cell_info)
  add_new_row(column_ids, sheetID, CellArray[x])

# This for loop shows that multiple arrays of information can be sent to the new row function to create multiple rows of unique information


import xml.etree.ElementTree as ET
tree = ET.parse(r'C:\Users\kearnsm2\Desktop\SmartSheets API\Haemonetics_Gilbane Master NWF_example.xml')
root = tree.getroot()
#print(dir(root))
viewpoints = list(root)
print(viewpoints[0].getchildren)
