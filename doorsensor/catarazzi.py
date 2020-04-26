#!/usr/bin/env python3
# cc0 copyleft -- public domain
"""
take a snapshot using raspistill
save to datetimeformat
"""
import subprocess
import datetime
import sql3 as sql
import os
import configparser

def click(closed_or_open, directory=".", db='cats.db', picture_db_table='pics', testing=False):
    """
    Take a snapshot.
    Save to date time of now into database.
    """
    date = datetime.datetime.today().isoformat()
    filename = date[:date.index('.')] # no fractions of seconds
    filename = filename.replace('-', '') # no dashes
    filename = filename.replace(':', '') # no colons
    picturename = filename + '.jpg'
    print(directory)
    picturepath = os.path.join(directory, picturename)
    picture_command = ['raspistill', '-o', picturepath]
    test_command = ['touch', picturepath]
    if testing:
        print("will test command", test_command)
        subprocess.Popen(test_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, preexec_fn=os.setsid)
    else:
        print("will execute command", picture_command)
        subprocess.Popen(picture_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, preexec_fn=os.setsid)
    values = {}
    # door open: 0 = false, 1 = true ==> 1 door open, 0 door closed
    door_open = 0 if 'close' in closed_or_open else 1
    values["muis"] = 2 # undetermined until analyzed
    values["sent_email"] = 0 # will do after
    values['door_open'] = door_open
    values['picture'] = picturepath
    values['date'] = date
    textname = filename + '.txt'
    textpath = os.path.join(directory, textname)
    with open(textpath, 'w') as textfile:
        textfile.write("Cat entered or left:" + "door " + closed_or_open + "\nDate and time: " + date + "\n" + picturepath + '\n')
    sql.dict_to_db(values, os.path.join(directory, db), picture_db_table)

    return picturepath

if __name__ == "__main__":
    # read directory from config file
    config = configparser.ConfigParser()
    config.read('catarazzi_settings.ini')
    directory = config['catpics']['picture_dir']
    db = config['catpics']['picture_db']
    table = config['catpics']['picture_db_table']
    print(directory)
    click('closed', directory, db)

