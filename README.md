# WhatsApp Chat Analyser

This is a selection of tools that allow the user to take '.txt' files that can be generated from WhatsApp chats and organise them into a '.csv' file which can be used to explore the data.

**The files showcase** my ability to clean, manipulate and play with data, and my proficiency with Python.

I took on this project when I was curious about my 'chats' with my acquaintances and what information could be extracted from them (purely for entertainment purposes), such as who sent the most messages, how the number of messages sent peaked and troughed over time and what words, topics or names were repeated most. **Specifically**, I thought it would be a great gift to a significant other to provide an analysis of our conversations for the past 8 years. Some might call it creepy, I'd say romantic.

WhatsApp allows users to export their chats as a .txt file where each line is of the format `[date], [time] - [sender]: [message]`, where `date` is of the `dd/mm/yyyy` format and `time` is of the the 24-hour `hh:mm` format. However, WhatsApp only allows the user to export the last 40,000 messages, thus if you want to export a chat with more messages, you're out of luck unless you plan ahead. And plan ahead I did, ensuring that at least once a year I'd do a backup of any chats I'd like to have an extended history of. And to ease the joining of these overlapping chat histories, one can use the **MergeFiles.py** file. Once the messages are all stored in a single .txt file, they can then be used as input into the **ChatToCSV.py** file, which converts the messages into a format more useful for analysis.

## data

This folder contains all input and output data for the scripts. Go to this folder for more information.

## MergeFiles.py

This script allows the user to select a folder containing multiple Whatsapp .txt files, and will output a single WhatsApp .txt from the earliest start date of the files to the latest end date, provided that there are no gaps in the history.

### Limitations

The input files MUST overlap by at least 1 day, otherwise the script will assume the two files do not belong to the same chat (this could be altered, but it was not neccessary for my needs). The scipt will also not detect if the files come from different chats, thus if they overlap, it will just merge two different chats.

## ChatToCSV.py

This file takes a single .txt file of the WhatsApp chat format, and encodes each word into a data point, encapsulating the following data:

The *example* column uses the word 'wowzers' from the following line of a WhatsApp .txt file, assuming it is the 34th line in the chat, and a total of 187 words are in all the prior messages.

`21/01/2021, 16:52 - Joe Swanson: I like to say the word 'wowzers'`

| Field Name | Description | Example |
| --- | --- | --- |
| Word | The word that is being recorded | wowzers |
| Sender | The name of the message sender | JoeSwanson |
| Hour | The hour that the message was sent | 16 |
| Minute | The minute that the message was sent | 52 |
| Day | The day that the message was sent | 21 |
| Month | The month that the message was sent | 01 |
| Year | The year that the message was sent | 2021 |
| Message | The location of the message from the start of the file | 34 |
| Location | The location of the word from the start of the message | 7 |
| AbsoluteLocation | The location of the word from the start of the file | 194 |

An example of a full .csv file can be found [here](https://github.com/ThomasDoyle11/whatsapp_chat_analyser/blob/master/data/output/ganrer_20140723-20140807_CSV.csv).

The script only records alphanumeric characters and acts as if any other characters are not there, such as commas, hyphens, emojis or apostrophes. There are two output files: one with all the words from the messages, and one which omits 'stopwords', where a stopword is a 'word which does not add much meaning to a sentence', such as 'the', 'is', 'and' and 'at'. The former is good for more generic analysis, such as total words sent or average words per message, and the latter is better for more specific analysis, such as most common words sent, where uninteresting words don't clog up the analysis.

### Limitiations

The script will not detect if a participant changes their name at some point in the chat, as this is not recorded in the file, thus it will assume that the two different names are two different senders.
