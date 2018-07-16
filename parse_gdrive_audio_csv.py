import csv
import re

audio_headers = ['id',                     # Required 
                 'url',                    # Required
                 'file_name',              # Required
                 'file_format',            # Required
                 'date',                   # Required
                 'meeting_type',           # Required
                 'message_type',           # Required
                 'message_series',         # Required
                 'message_theme',          # Optional
                 'message_description']    # Optional
audio_data = []

gdrive_audio_list_path = "audio_list.csv"

with open(gdrive_audio_list_path, newline='') as csvfile:
    audio_list = csv.DictReader(csvfile)
    for row in audio_list:
        # Splitting the file name into the name and format
        file = row['Name'].split(".")
        file_name = file[0]
        file_format = file[1]
        
        # Splitting the file name into the descriptor elements
        file_desc = file_name.split("_")
        
        # Required Fields
        # file_desc[0] == Date (format = YYYYMMDD)
        # file_desc[1] == Type of Meeting (e.g. Summer Conference)
        # file_desc[2] == Type of Message (e.g. Ministry)
        # file_desc[3] == Series Number (0 if singular, else 1 ... n)
        # Optional Fields
        # file_desc[4]
        #    if starts with '[' and ends with ']' is the Theme
        #    else is the Message Description
        # file_desc[5] == Message Description (if it exists)
        
        # Parsing date into YYYY-MM-DD for Jekyll
        date = file_desc[0][0:4] + '-' + file_desc[0][4:6] + '-' + file_desc[0][6:]
        
        # Creating the downloadable link for shared files
        message_url = 'https://drive.google.com/file/d/' + row['Id']
        
        meeting_type = file_desc[1]
        message_type = file_desc[2]
        message_series = file_desc[3]
        message_theme = ''
        message_desc = ''
        
        # Getting the data for the optional fields
        if len(file_desc) == 6:
            # Get rid of the '[' and ']'
            message_theme = re.sub('\[|\]', '', file_desc[4])
            message_desc = file_desc[5]
        elif len(file_desc) == 5:
            r = re.compile('^\[.*\]$')
            if r.match(file_desc[4]):
                message_theme = re.sub('\[|\]', '', file_desc[4])
            else:
                message_desc = file_desc[4]
        
        # Creating our list
        audio_data.append([row['Id'],
                          message_url,
                          file_name,
                          file_format,
                          date, 
                          meeting_type, 
                          message_type, 
                          message_series, 
                          message_theme, 
                          message_desc])

# Going to write out the processed gdrive data
path = "./jekyll_audio_list.csv"
with open(path, 'w') as csvfile:
    writer = csv.writer(csvfile, delimiter=",")
    writer.writerow(audio_headers)
    for line in audio_data:
        writer.writerow(line)
