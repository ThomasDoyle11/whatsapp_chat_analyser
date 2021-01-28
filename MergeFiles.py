import os
import re

# Load and merge input files
print("\n******************************")
print(" STARTING MERGE FILES PROCESS")
print("******************************\n")

############# USER DEFINED ################

folder_to_merge = "my_betrothed"

root_dir = r"C:\Users\thoma\Documents\Python_Projects\ChatToCSV\ChatToCSV"

###########################################

dateFormat = re.compile("\d{2}/\d{2}/\d{4}")

files = os.listdir(root_dir + "/data/" + folder_to_merge + "/")

print("Total of " + str(len(files)) + " files to be merged.")

earliest_start_date = ""
latest_end_date = ""

def getDate(text, line) :
    date = text[line].split(", ", 1)[0]
    if(dateFormat.match(date)) :
        date = date.split("/")
        date = 10000 * int(date[2]) + 100 * int(date[1]) + int(date[0])
    else :
        date = -1
    return date

def getStart(text) :
    return getDate(text, 0)

def getEnd(text) :
    return(getDate(text,-1))

if len(files) > 0 :
    # Find earliest file

    # Decide the new_order the files will be merged in
    print("Deciding order to merge in.")
    new_order = []
    new_start = []
    new_end = []
    for i in range(len(files)) :
        new_file = open(root_dir + "/data/" + folder_to_merge + "/" + files[i], encoding = 'utf-8-sig')
        all_lines = new_file.readlines()
        new_start.append(getStart(all_lines))
        new_end.append(getEnd(all_lines))
        new_file.close()

    # Choose the earliest start date for the first file
    new_index = 0
    for i in range(len(new_start) - 1) :
        if new_start[i+1] < new_start[new_index] or (new_start[i+1] == new_start[new_index] and new_end[i+1] > new_end[new_index]) :
            new_index = i + 1
    new_order.append(files[new_index])
    old_start = new_start[new_index]
    old_end = new_end[new_index]

    print("\nFile order:")
    print("1: " + files[new_index] + " (" + str(old_start) + " - " + str(old_end) + ").")
    earliest_start_date = old_start

    files.pop(new_index)
    new_start.pop(new_index)
    new_end.pop(new_index)

    # Maximise the difference in end dates for subsequent files, ensuring that the next file's start date is before the previous files endate
    for i in range(len(new_start)) :
        new_index = 0
        new_length = 0
        for j in range(len(new_start)) :
            if old_end > new_start[j] and new_end[j] - old_end > new_length :
                new_index = j
                new_length = new_end[j] - old_end
        if new_length == 0 :
            latest_end_date = old_end
            break
        else :
            new_order.append(files[new_index])
            old_start = new_start[new_index]
            old_end = new_end[new_index]
               
            print(str(i+2) + ": " + files[new_index] + " (" + str(old_start) + " - " + str(old_end) + ").")

            files.pop(new_index)
            new_start.pop(new_index)
            new_end.pop(new_index)

    files = new_order

    print("Using " + str(len(files)) + " of the original files.")

    # Merge files in order given

    # Load the first file
    x1 = open(root_dir + "/data/" + folder_to_merge + "/" + files[0], encoding = 'utf-8-sig')
    x1_lines = x1.readlines()
    x1.close()

    print("\n" + files[0] + " loaded.")

    files.pop(0)

    # Load and empty the merged file and add the first file
    merged_files = open(root_dir + "/data/input/" + folder_to_merge + "_" + str(earliest_start_date) + "-" + str(latest_end_date) + ".txt", "w+", encoding = 'utf-8-sig')
    merged_files.writelines(x1_lines)
    merged_files_lines = x1_lines
    merged_files_end = getEnd(x1_lines)
    
    print("New file loaded and first file written.")

    # Add subsequent files at the correct point
    for i in range(len(files)) :
        x2 = open(root_dir + "/data/" + folder_to_merge + "/" + files[i], encoding = 'utf-8-sig')
        x2_lines = x2.readlines()
        x2_end = getEnd(x2_lines)
        
        print(files[i] + " loaded.")

        passed_date = False
        for j in range(len(x2_lines)) :
            x2_date = getDate(x2_lines,j)
            if (passed_date == False and x2_date > merged_files_end) :
                passed_date = True
            if passed_date :
                merged_files.write(x2_lines[j])
            if (passed_date == False and x2_date == merged_files_end) :
                if (x2_lines[j] == merged_files_lines[-1]) :
                    passed_date = True
                    
        print(files[i] + " merged.")

        merged_files_end = x2_date
        
print("\n******************************")
print(" MERGE FILES PROCESS COMPLETE")
print("******************************\n")