import time
import re
from nltk.corpus import stopwords

print("\n******************************")
print(" STARTING TEXT TO CSV PROCESS")
print("******************************\n")

################# USER DEFINED ##################

file_name = "ganrer_20140723-20140807"

root_dir = r"C:\Users\thoma\Documents\Python_Projects\ChatToCSV\ChatToCSV"

#################################################

start_time = time.time()

english_stopwords = stopwords.words('english_edited_2')

date_format = re.compile(r"\d{2}/\d{2}/\d{4}")
time_format = re.compile(r"\d{2}:\d{2}")

input_file = open(root_dir + "/data/input/" + file_name + ".txt", encoding="utf-8-sig")

output = open(root_dir + "/data/output/" + file_name + "_CSV.csv", "w+", errors = "ignore")
output.write("Word,Sender,Hour,Minute,Day,Month,Year,Message,Location,AbsoluteLocation\n")

output_no_stopwords = open(root_dir + "/data/output/" + file_name + "_CSV_no_stopwords.csv", "w+", errors = "ignore")
output_no_stopwords.write("Word,Sender,Hour,Minute,Day,Month,Year,Message,Location,AbsoluteLocation\n")

# Convert the data to csv
message = 1
total_words = 1

for line in input_file :

    # Check for \ufeff at the start

    line = line.split(", ",1)

    if (date_format.match(line[0])) :
        date = line[0]
        day, month, year = date.split("/")
        line = line[1]

        line = line.split(" - ",1)

        msg_time = line[0]
        hour, minute =  msg_time.split(":")
        line = line[1]

        line = line.split(": ",1)

        if (len(line) > 1) :
            sender = line[0].replace(" ","")
            line = line[1] 
        else :
            sender = ""
            line = line[0]
    else :
        line = line[0]

    line = line.replace("<Media omitted>", "")


    line = re.sub("[^a-zA-z0-9'\\s]+", "", line)

    line = line.lower()

    words = line.split()
    location = 1
    if len(words) > 0 :
        for word in words :
            output.write(word + "," + sender + "," + hour + "," + minute + "," + day + "," + month + "," + year + "," + str(message) + "," + str(location) + "," + str(total_words) + "\n")
            if word not in english_stopwords :
                output_no_stopwords.write(word + "," + sender + "," + hour + "," + minute + "," + day + "," + month + "," + year + "," + str(message) + "," + str(location) + "," + str(total_words) + "\n")
            location += 1
            total_words += 1
        message += 1

    if (message % 100000 == 0) :
        current_time = time.time() - start_time
        print(str(message) + " messages encoded so far in " + str(current_time) + " seconds.")

output.close()
output_no_stopwords.close()

current_time = time.time() - start_time
print(str(message) + " messages and " + str(total_words) + " words encoded in total in " + str(current_time) + " seconds.")



print("\n******************************")
print(" TEXT TO CSV PROCESS COMPLETE")
print("******************************\n")