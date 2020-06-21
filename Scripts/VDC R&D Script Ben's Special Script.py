import xml.etree.ElementTree as ET                          # Import all necessary packages. This is for the XML File
import xlwt                                                 # To create excel files
from xlwt import Workbook                                   # Portion of package needed
import os                                                   # Needed to navigate file paths
import smartsheet                                           # Needed to 
import time
from time import sleep
import PySimpleGUI as sg


def xml_to_excel(xml_path, new_path, new_name):             # Define function for exporting XML to excel
    class viewfolder(object):                               # Set up class to create object                                         
        def __init__(self, level, views, name):             # Initialization function for object
            self.level = level                              # Initialize level attribute
            self.views = views                              # Initialize views attribute
            self.name = name                                # Initialize name attribute
    
    class viewpoint(object):                                # Set up class for a viewpoint
        def __init__(self,name,comment,status,date):        # Initialization function for object
            self.name = name                                # Initialize name attribute
            self.comment = comment                          # Initialize comment attribute
            self.status = status                            # Initialize status attribute
            self.date = date                                # Initialize date attribute

    def make_viewfolder(level, views, name):                # Function to create viewfolder object given needed information
        folder = viewfolder(level, views, name)             # Store information given to object named folder. viewfolder is the class
        return folder                                       # Return the viewfolder object



    tree = ET.parse(xml_path)                               # Initialize XML file given a path to the file
    root = tree.getroot()                                   # Set up the root for XML file
    wb = Workbook()                                         # Create new excel workbook
    sheet1 = wb.add_sheet('Sheet 1')                        # Create new sheet named 'Sheet 1'

    def all_views(root, count):                             # Create function to get all views underneath a viewfolder
        for elem in list(root):                             # Iterate through every element beneath current element
            if elem.tag == 'view':                          # If that element is a viewpoint
                count += 1                                  # Increment count by 1
            else:                                           # If element is not a viewpoint
                count += all_views(elem, 0)                 # Recurse through that element and increment the counter by whatever is returned through recursion
        return count                                        # Return count variable for later use


    def comments(view):                                                                                                                 # Define function to deal with comments, argument passed into function is a viewpoint                                                                                                
        if len(view) > 3:                                                                                                               # If the length of the view object is greater than 3, than it means there is a comment attached to that view
            if view[2].tag == 'comments':                                                                                               # Only deal with the portion of the view that pertains to the comments. This if statement is a little weird since there is no for loop here. I basically am checking if it has a comment section twice
                for x in range(0,len(view[2])):                                                                                         # For loop to iterate through all the comments in the 'comments' section of file
                    viewpoint_info = []                                                                                                 # Empty array to store viewpoint information
                    date = view[2][x][2][0].get('month') + '/' + view[2][x][2][0].get('day') + '/' + view[2][x][2][0].get('year')       # Concatenate all the information stored in the CreatedDate portion 
                    comment = view[2][0][1].text                                                                                        # Get body of comment and save it in variable named comment
                    status = view[2][0].get('status')                                                                                   # Get the status of the comment                                                                                                      
                    viewpoint_info.append(viewpoint(view.get('name'),comment,status,date))                                              # Append the name, body, status, and date to the viewpoint info array
                return viewpoint_info                                                                                                   # Return that entire viewpoint info array at the end of the function
        else:                                                                                                                           # If the viewpoint does not have any comments
            return None                                                                                                                 # Return NoneType to use as a way to filter out information later on


    def views(root, all_views):                             # Create function to get all viewnames in the XML file
        if root.tag == 'view':                              # If the current element is a viewpoint
            all_views.append(root)                          # Append that viewpoint name to view_names array
        for elem in list(root):                             # Iterate through every element beneath current
            views(elem, all_views)                          # Recurse through all those elements, which would append all viewnames
        return all_views                                    # Return all viewnames for later use

    views = views(root, [])                                 # After function is set up, get all viewnames by calling function, passing it the root and an empty global array

    def folder_level(root, index, folders):                                     # Function to determine level of each folder given the root, starting index, and global array to use
        index += 1                                                              # Increment the index by 1
        if root.tag == 'viewfolder':                                            # If the current element is a viewfolder
            #print(root.get('name'))                                            # Print function for checking what the name of the current element is
            rows = all_views(root,0)                                            # Create rows variable to store the total number of views beneath current viewfolder
            #print(rows, index)                                                 # Print function to see the rows and index (column) of current element
            folders.append(make_viewfolder(index,rows,root.get('name')))        # Create viewfolder objects by using make_viewfolder function and append those to the folders array
            #print(len(folders))                                                # Print function to for checking how many viewfolder objects are in the folders array
        for elem in list(root):                                                 # Iterate through every element beneath current element
            folder_level(elem, index, folders)                                  # Recurse through and do the same thing for every following element
        return folders                                                          # Return folders variable (Using an empty array that is passed through the function call allows information to be stored, and not resetm throughout the recursion)

    folders = folder_level(root[0], 0, [])                                      # After function is defined, call it, passing in the first viewfolder, index of 0, and an empty array


    levels = []                                             # Create empty array named levels, information will be appened to this array later
    for x in range(0,len(folders)):                         # Iterate through all the objects in folders array                           
        levels.append(folders[x].level)                     # Append each folder level to the levels array
    max_lvl = max(levels)                                   # Find the maximum level in the array
    #print(max_lvl)                                         # Print function to check what that max level is
    cells = []                                              # Empty array named cells

    for x in range(0,max_lvl):                              # For loop going from 0 to the highest number of levels
        columns =[]                                         # Empty array named columns
        for y in range(0,len(folders)):                     # For loop to go through every item in folders array
            if folders[y].level == x+1:                     # If the current folder element has the same level as the current index
                for z in range(0,folders[y].views):         # For loop to go for however many times there are views under that folder
                    columns.append(folders[y].name)         # Append the name to the columns array that many times
        cells.append(columns)                               # Append columns information to the cells array

    for x in range(0,len(cells)):                           # For loop to iterate through all items in cells array
        for y in range(0,len(cells[x])):                    # For loop to iterate through every item in each array that is stored in the cells array.
            #print(cells[x][y])                             # Print that info. The cells array is an array containing arrays that correspond to the information for each column
            sheet1.write(y,x-1,cells[x][y])                 # Write the information to the excel sheet 

        view_names = []                                                 # Empty array to hold view names information
        for x in range(0,len(views)):                                   # Loop through all the views
            view_names.append(views[x].get('name'))                     # Append all the names of the views to the view_names array


    view_lengths = []
    for x in range(0,len(view_names)):                      # Iterate through all viewnames
        split_views = view_names[x].split('_')              # Split the view names using an underscore '_' as the delimiter 
        view_lengths.append(len(split_views))
        for y in range(0,len(split_views)):                 # Iterate through the new array created by splitting the viewnames
            sheet1.write(x,max_lvl + y - 1,split_views[y])  # Write that information to the sheet with the start column being the max level

    all_comments = []                                                                           # Empty array to hold all comments information
    for x in range(0,len(views)):                                                               # Loop through all views          
        all_comments.append(comments(views[x]))                                                 # Call the comments function, passing in each view 

    for x in range(0,len(all_comments)):                                                        # Loop through all objects in comments array
        if all_comments[x] != None:                                                             # If they are actual comments, not of type None
            #sheet1.write(x,(max(view_lengths) + max_lvl - 1),all_comments[x][0].date)          # Write the date in the column after viewpoints secton ends
            #sheet1.write(x,(max(view_lengths) + max_lvl),all_comments[x][0].status)            # Write the status next to that
            sheet1.write(x,(max(view_lengths) + max_lvl - 1),all_comments[x][0].comment)        # Write the body of the comment after the viewpoints section
    wb.save(new_path + '//' + new_name + '.xls')                                                # Save the workbook using the path and name given by user

def  image_rename(image_path, xml_path, start_number):      # Function for renaming all images. needs to be passed an image path and an XML path
    def get_views(root, viewpoints):                        # Function to get all view names in XML file
        for elem in list(root):                             # Iterate through all elements under current element/root
            if elem.tag == 'view':                          # If the element is a viewpoint
                viewpoints.append(elem.get('name'))         # Append that element to the viewpoints array
            get_views(elem, viewpoints)                     # Recursion for all subsequent viewfolders
        return viewpoints                                   # Return viewpoints array
    
    tree = ET.parse(xml_path)                               # Initialize XML tree
    root = tree.getroot()                                   # Get root of XML
    views = get_views(root, [])                             # Call get_views function and store it in variable named viewpoints
    files = []                                              # Empty array named files



    view_names = []                                                     # Empty array for view names
    for x in range(0,len(views)):                                       # Loop through all viewpoints
        view_names.append(views[x])                                     # Append the name of the viewpoint to the empty array
    illegal_chars = ['?','"','\'','%','*',':']                          # List of illegal characters (chars = characters)
    for x in range(0,len(illegal_chars)):                               # Loop through all viewpoints again

            view_names[x] = view_names[x].replace('?', '.')             # Replace '?' with a '.'
            view_names[x] = view_names[x].replace('"', 'inch')          # Replace '"' with 'inch'
            view_names[x] = view_names[x].replace('\'', 'foot')         # Replace ''' with 'foot'
            view_names[x] = view_names[x].replace('%', 'percent')       # Replace '%' with 'percent'
            view_names[x] = view_names[x].replace('*', '')              # Replace '*' with nothing
            view_names[x] = view_names[x].replace(':', '-')             # Replace ':' with '-'
            view_names[x] = view_names[x].replace('/', '')              # Replace '/' with nothing
            view_names[x] = view_names[x].replace('|', '')              # Replace '|' with nothing
            view_names[x] = view_names[x].replace('\\', '')             # Replace '\' with nothing 


    for entry in os.listdir(image_path):                    # Iterate throughthe image directory given by user
        files.append(entry)                                 # Append all files in directory to files array
    start_number = int(start_number)
    final_name = []
    for x in range(0,len(views)):                                                                   # Iterate through all viewpoints
        if (start_number + x) < 100:                                                                 # If the index 'x' is less than 10
            temp_name = '00' + str(start_number + x)                                                 # Append the index (with an extra 0 in front) to the front of the viewpoint name
            final_name.append(temp_name)                                                            # Append that new temp name to the viewnames array
        else:                                                                                       # Else, so if the index 'x' is greater than or equal to 10
            temp_name = str(start_number + x)                                                       # Append the index to the front of the viewpoint name
            final_name.append(temp_name)                                                            # Append that temp name to the viewnames array
    for x in range(0,len(view_names)):                                                              # Loop through all viewnames in array
        os.rename(image_path + '//' + files[x], image_path + '//' + final_name[x] + '.jpg')         # Use os.rename() to rename all the files in directory

def image_upload(API_Token, Sheet_ID, Start_Row, image_path):                   # Function for uploading images to Smartsheet
    smart = smartsheet.Smartsheet(API_Token)                                    # Initialize Smartsheet using API Token
    sheet = smart.Sheets.get_sheet(int(Sheet_ID))                               # Get the desired Smartsheet using the Sheet ID 

    files = []                                                                  # Empty array named files
    for entry in os.listdir(image_path):                                        # Loop through the directory given by user
        files.append(entry)                                                     # Append all files in directory to files array

    for x in range(0,len(files)):                                               # Loop through all files in that files array
        sg.OneLineProgressMeter('Progress',x+1,len(files),'key')                # PySimpleGUI's Progress Meter
        sleep(5)                                                                # Sleep function to avoid exceeding the rate limit
        smart.Attachments.attach_file_to_row(                                   # Function to attach files to a row in Smartsheet
            Sheet_ID,                                                           # Pass through the Sheet ID
            sheet.rows[int(Start_Row) + x - 1].id_,                             # This will iterate through and get all the row IDs in order
            (str(files[x]),                                                     # Name the attachment based on the name of the file being uploaded
                open(str(image_path)+'//'+str(files[x]), 'rb'),                 # Open the location of the file being uploaded
                'application/msword')                                           # Pretty sure this does nothing but I do not want to delete it
        )





options = ['XML to Excel', 'Image Rename', 'Smartsheet Image Upload']                                       # Options for the GUI 

form_option_1 = sg.FlexForm('XML to Excel')                                                                 # Set up form for XML to Excel and Image Rename
form_option_2 = sg.FlexForm('Smartsheet Image Upload')                                                      # Set up form for Smartsheet Image Upload
form_option_3 = sg.FlexForm('Image Rename')


layout_option_1 = [                                                                                         # Set up layout for option 1
          [sg.Text('XML to Excel')],                                                                        # Header for window
          [sg.Text('XML File', size=(18, 1)), sg.InputText(''), sg.FileBrowse()],                           # File browse to get the XML file
          [sg.Text('New Excel File Location', size=(18,1)), sg.InputText(''), sg.FolderBrowse()],           # Folder browse to select where the new excel file will be saved
          [sg.Text('New Excel File Name', size=(18,1)), sg.InputText('')],                                  # Input text for the new excel file name
          [sg.Submit(), sg.Cancel()]                                                                        # Submit and cancel buttons
         ]

layout_option_2 = [                                                                                         # Set up layout for option 2
          [sg.Text('Smartsheet Image Upload')],                                                             # Header for window
          [sg.Text('API Token', size=(15, 1)), sg.InputText('')],                                           # Input text to put in the API Token
          [sg.Text('Sheet ID', size=(15, 1)), sg.InputText('')],                                            # Inout text for the Sheet ID
          [sg.Text('Image Folder Path', size=(15, 1)), sg.InputText(''), sg.FolderBrowse()],                # Folder browse to select the image folder
          [sg.Text('Start Row', size=(15, 1)), sg.InputText('')],                                           # Input text for the start row
          [sg.Submit(), sg.Cancel()]                                                                        # Submit and cancel buttons
         ]

layout_option_3 = [
          [sg.Text('Image Rename')],                                                                        # Header for window
          [sg.Text('XML File', size=(18, 1)), sg.InputText(''), sg.FileBrowse()],                           # File browse to get the XML file                 
          [sg.Text('Image Folder', size=(18,1)), sg.InputText(''), sg.FolderBrowse()],                      # Folder browse to select where the new excel file will be saved
          [sg.Text('Start Number', size=(18, 1)), sg.InputText('')],                                                        
          [sg.Submit(), sg.Cancel()]                                                                        # Submit and cancel buttons
         ]

                                                              
layout_master = [                                                           # Set up the layout for the first window that will appear
        [sg.Text('Please Choose an Option')],                               # Header for window
        [sg.InputCombo(options)],                                           # Drop down list containing that options array created earlier
        [sg.Button('Enter'), sg.Exit()]                                     # Enter and exit buttons
        ]
window_master = sg.Window('Options').Layout(layout_master)                  # Create window for the first window that will appear
button, values = window_master.Read()                                       # Read window and store information in variables named button and values
window_master.Close()                                                       # Close the master window

if values[0] == 'XML to Excel' and button == 'Enter':                       # If the first option is chosen
    button_1, values_1 = form_option_1.Layout(layout_option_1).Read()       # Show the option 1 window and read the output
    xml_to_excel(values_1[0], values_1[1], values_1[2])                     # Call xml_to_excel function and pass the information given by user                           
    form_option_1.Close()                                                   # Close that window

if values[0] == 'Image Rename' and button == 'Enter':                       # If the third option is chosen (These are out of order because Image Upload used to be part of operation 1)
    button_3, values_3 = form_option_3.Layout(layout_option_3).Read()       # Show the option 3 window and read it
    form_option_3.Close()                                                   # Close window
    image_rename(values_3[1], values_3[0], values_3[2])                                  # Call the Image_rename function


if values[0] == 'Smartsheet Image Upload' and button == 'Enter':            # If the second option is chosen
    button_2, values_2 = form_option_2.Layout(layout_option_2).Read()       # Show the option 2 window and read the output
    form_option_2.Close()                                                   # Close the window
    image_upload(values_2[0],int(values_2[1]),values_2[3],values_2[2])      # Call image_upload function and pass the information by user