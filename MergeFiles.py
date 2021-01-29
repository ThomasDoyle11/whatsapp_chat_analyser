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

print("Total of " + str(len(files)) + " files to be merged:")
for i in range(len(files)) :
    print(str(i+1) + ": " + files[i])

earliest_start_date = 0
latest_end_date = 0

def getDate(text, line) :
    date = text[line].split(", ", 1)[0]
    if(dateFormat.match(date)) :
        date = date.split("/")
        date = 10000 * int(date[2]) + 100 * int(date[1]) + int(date[0])
    else :
        date = -1
    # print(date)
    return date

def getStartDate(text) :
    return getDate(text, 0)

def getEndDate(text) :
    return(getDate(text,-1))

if len(files) > 0 :
    # Find earliest file

    # Decide the new_order the files will be merged in
    print("\nDeciding order to merge in.")
    new_order = []
    start_dates = []
    end_dates = []
    for i in range(len(files)) :
        new_file = open(root_dir + "/data/" + folder_to_merge + "/" + files[i], encoding = 'utf-8-sig')
        all_lines = new_file.readlines()
        start_dates.append(getStartDate(all_lines))
        end_dates.append(getEndDate(all_lines))
        new_file.close()

    # Choose the earliest start date for the first file, and if two files have equal start date, choose the one with the latest end date
    new_index = 0
    for i in range(len(start_dates) - 1) :
        if start_dates[i+1] < start_dates[new_index] or (start_dates[i+1] == start_dates[new_index] and end_dates[i+1] > end_dates[new_index]) :
            new_index = i + 1
    new_order.append(files[new_index])
    previous_end_date = end_dates[new_index]

    print("\nFile order:")
    print("1: " + files[new_index] + " (" + str(start_dates[new_index]) + " - " + str(end_dates[new_index]) + ").")
    earliest_start_date = start_dates[new_index]

    files.pop(new_index)
    start_dates.pop(new_index)
    end_dates.pop(new_index)

    # Maximise the difference in end dates for subsequent files, ensuring that the next file's start date is before or equal to the previous files endate
    for i in range(len(start_dates)) :
        new_index = 0
        new_length = 0
        for j in range(len(start_dates)) :
            if previous_end_date >= start_dates[j] and end_dates[j] - previous_end_date > new_length :
                new_index = j
                new_length = end_dates[j] - previous_end_date
        if new_length > 0 :
            new_order.append(files[new_index])
            previous_end_date = end_dates[new_index]

            print(str(i+2) + ": " + files[new_index] + " (" + str(start_dates[new_index]) + " - " + str(end_dates[new_index]) + ").")

            files.pop(new_index)
            start_dates.pop(new_index)
            end_dates.pop(new_index)
    latest_end_date = previous_end_date

    files = new_order

    print("Using " + str(len(files)) + " of the original files.")

    # Merge files in order given

    # Load the first file
    x1 = open(root_dir + "/data/" + folder_to_merge + "/" + files[0], encoding = 'utf-8-sig')
    x1_lines = x1.readlines()
    x1.close()

    print("\n" + files[0] + " loaded.")

    # Load and empty the merged file and add the first file
    merged_files = open(root_dir + "/data/input/" + folder_to_merge + "_" + str(earliest_start_date) + "-" + str(latest_end_date) + ".txt", "w+", encoding = 'utf-8-sig')
    merged_files.writelines(x1_lines)
    merged_files_lines = x1_lines
    merged_files_end = getEndDate(x1_lines)
    
    print(files[0] + " merged.")

    files.pop(0)

    # Add subsequent files at the correct point
    for i in range(len(files)) :
        x2 = open(root_dir + "/data/" + folder_to_merge + "/" + files[i], encoding = 'utf-8-sig')
        x2_lines = x2.readlines()
        x2_end = getEndDate(x2_lines)
        
        print(files[i] + " loaded.")

        passed_date = False
        for j in range(len(x2_lines)) :
            x2_date = getDate(x2_lines,j)
            if (not passed_date and x2_date > merged_files_end) :
                passed_date = True
            if passed_date :
                merged_files.write(x2_lines[j])
            if (not passed_date and x2_date == merged_files_end) :
                if (x2_lines[j] == merged_files_lines[-1]) :
                    passed_date = True
                    
        print(files[i] + " merged.")

        merged_files_end = x2_date
        
print("\n******************************")
print(" MERGE FILES PROCESS COMPLETE")
print("******************************\n")