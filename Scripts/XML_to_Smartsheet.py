import smartsheet
import xml.etree.ElementTree as ET

API_Token = 'dnzz6g1by3o0wfeo5kqylztcv1'
sheet_ID = 6212864257091460
XML_Path = r'C:\Users\kearnsm2\Desktop\Summer 2019 Co-op\Navisworks Testing\BCAHS_DB_Gilbane_Central 26-July-2019.xml'
smart = smartsheet.Smartsheet(API_Token)
sheet = smart.Sheets.get_sheet(sheet_ID)

rows = sheet.rows
sheet_columns = sheet.columns


def xml_to_excel(xml_path, sheet_ID):                       # Define function for exporting XML to excel

    class viewfolder(object):                               # Set up class to create object                                           # Name of viewfolder
        def __init__(self, level, views, name):             # Initialization function for object
            self.level = level                              # Initialize level attribute
            self.views = views                              # Initialize views attribute
            self.name = name                                # Initialize name attribute
    
    class viewpoint(object):
        def __init__(self,name,comment,status,date):
            self.name = name
            self.comment = comment
            self.status = status
            self.date = date

    def make_viewfolder(level, views, name):                # Function to create viewfolder object given needed information
        folder = viewfolder(level, views, name)             # Store information given to object named folder. viewfolder is the class
        return folder                                       # Return the viewfolder object



    tree = ET.parse(xml_path)                               # Initialize XML file given a path to the file
    root = tree.getroot()                                   # Set up the root for XML file


    def all_views(root, count):                             # Create function to get all views underneath a viewfolder
        for elem in list(root):                             # Iterate through every element beneath current element
            if elem.tag == 'view':                          # If that element is a viewpoint
                count += 1                                  # Increment count by 1
            else:                                           # If element is not a viewpoint
                count += all_views(elem, 0)                 # Recurse through that element and increment the counter by whatever is returned through recursion
        return count                                        # Return count variable for later use


    def comments(view):
        body_names = ''
        if len(view) > 3:
            if view[2].tag == 'comments':
                for x in range(0,len(view[2])):
                    viewpoint_info = []
                    date = view[2][x][2][0].get('month') + '/' + view[2][x][2][0].get('day') + '/' + view[2][x][2][0].get('year')
                    comment = view[2][0][1].text
                    status = view[2][0].get('status')
                    print(status)
                    viewpoint_info.append(viewpoint(view.get('name'),comment,status,date))
                    # body_names += str(x + 1) + ') ' + 'Date Created: ' + date + '\n' + '   Body: ' + (view[2][x][1].text) + '\n' +  '  Status: ' + view[2][x].get('status') + '\n'
                return viewpoint_info
        else:
            return None

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
    repeat_rows= []

    for x in range(0,len(rows)):
        for y in range(0,len(sheet_columns)):
            for z in range(0,len(views)):
                if views[z].get('guid') == rows[x].cells[y].display_value:
                    #print('repeat' + str(z))
                    repeat_rows.append(x)
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
            for z in range(0,len(repeat_rows)):
                if x != repeat_rows[z]:
                    write(rows[y].id,sheet_columns[x-1].id,cells[x][y])                        # Write the information to the excel sheet 

    view_lengths = []
    for x in range(0,len(views)):                      # Iterate through all viewnames
        
        split_views = views[x].get('name').split('_')              # Split the view names using an underscore '_' as the delimiter 
        view_lengths.append(len(split_views))
        for y in range(0,len(split_views)):                 # Iterate through the new array created by splitting the viewnames
            for z in range(0,len(repeat_rows)):
                if x != repeat_rows[z]:
                    write(rows[x].id,sheet_columns[max_lvl + y - 1].id,split_views[y])      # Write that information to the sheet with the start column being the max level


    all_comments = []
    for x in range(0,len(views)):
        all_comments.append(comments(views[x]))


    for x in range(0,len(all_comments)):
        for z in range(0,len(repeat_rows)):
            if x != repeat_rows[z]:
                if all_comments[x] != None:
                    write(rows[x].id,sheet_columns[max(view_lengths) + max_lvl -1].id,all_comments[x][0].comment)

    for x in range(0,len(views)):
        for z in range(0,len(repeat_rows)):
            if x != repeat_rows[z]:
                if views[x].get('guid') != None:
                    write(rows[x].id,sheet.columns[max(view_lengths)+ max_lvl].id,views[x].get('guid'))


def write(x,y,text):
    new_cell = smartsheet.models.Cell()
    new_cell.column_id = y
    new_cell.value = text
    new_cell.strict = False

    new_row = smartsheet.models.Row()
    new_row.id = x
    new_row.cells.append(new_cell)

    updated_row = smart.Sheets.update_rows(
        sheet_ID,
        [new_row]
    )



xml_to_excel(XML_Path, sheet_ID)