import xml.etree.ElementTree as ET                          # Import all necessary packages
import xlwt
from xlwt import Workbook
import os
import smartsheet
import time
from time import sleep
import PySimpleGUI as sg


def xml_to_excel(xml_path, new_path, new_name):             # Define function for exporting XML to excel
    class viewfolder(object):                               # Set up class to create object
        level = 0                                           # This will show what level the viewfolder is on
        views = 0                                           # This will show the total number of viewpoints underneath a folder
        name = ''                                           # Name of viewfolder

        def __init__(self, level, views, name):             # Initialization function for object
            self.level = level                              # Initialize level attribute
            self.views = views                              # Initialize views attribute
            self.name = name                                # Initialize name attribute


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

    def views(root, view_names):                            # Create function to get all viewnames in the XML file
        if root.tag == 'view':                              # If the current element is a viewpoint
            view_names.append(root.get('name'))             # Append that viewpoint name to view_names array
        for elem in list(root):                             # Iterate through every element beneath current
            views(elem, view_names)                         # Recurse through all those elements, which would append all viewnames
        return view_names                                   # Return all viewnames for later use

    view_names = views(root, [])                            # After function is set up, get all viewnames by calling function, passing it the root and an empty global array

    def folder_level(root, index, folders):                                     # Function to determine level of each folder given the root, starting index, and global array to use
        index += 1                                                              # Increment the index by 1
        if root.tag == 'viewfolder':                                            # If the current element is a viewfolder
            print(root.get('name'))                                             # Print function for checking what the name of the current element is
            rows = all_views(root,0)                                            # Create rows variable to store the total number of views beneath current viewfolder
            print(rows, index)                                                  # Print function to see the rows and index (column) of current element
            folders.append(make_viewfolder(index,rows,root.get('name')))        # Create viewfolder objects by using make_viewfolder function and append those to the folders array
            #print(len(folders))                                                # Print function to for checking how many viewfolder objects are in the folders array
        for elem in list(root):                                                 # Iterate through every element beneath current element
            folder_level(elem, index, folders)                                  # Recurse through and do the same thing for every following element
        return folders                                                          # Return folders variable (Using an empty array that is passed through the function call allows information to be stored, and not resetm throughout the recursion)

    folders = folder_level(root[0], 0, [])                                      # After function is defined, call it, passing in the root, index of 0, and an empty array

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

    for x in range(0,len(view_names)):                      # Iterate through all viewnames
        split_views = view_names[x].split('_')              # Split the view names using an underscore '_' as the delimiter 
        for y in range(0,len(split_views)):                 # Iterate through the new array created by splitting the viewnames
            sheet1.write(x,max_lvl + y - 1,split_views[y])  # Write that information to the sheet with the start column being the max level

    wb.save(new_path + '//' + new_name + '.xls')            # Save the workbook using the path and name given by user



name = 'Test01'
dest_path = r'C:\Users\kearnsm2\Desktop'
xml_path = r'C:\Users\kearnsm2\Desktop\BCAHS_SC_Gilbane_Central 26-July-2019.xml'

xml_to_excel(xml_path,dest_path,name)