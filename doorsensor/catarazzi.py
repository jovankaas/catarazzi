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
import time
import configparser

def click(closed_or_open, directory=".", db='cats.db', picture_db_table='pics', testing=False, camera=None):
    """
    Take a snapshot.
    Save to date time of now into database.
    """
    date = datetime.datetime.today().isoformat()
    filename = date[:date.index('.')] # no fractions of seconds
    filename = filename.replace('-', '') # no dashes
    filename = filename.replace(':', '') # no colons
    picturename = filename + '.jpg'
    picturepath = os.path.join(directory, picturename)
    # also possible: --rotation 270 but this makes image dark
    # or: --exposure sports
    # both night and sports take only 0.7 seconds for me
    # the trick is timeout 1 to make it faster (otherwise 5 seconds)
    if camera != None:
        localtime = time.asctime( time.localtime(time.time()) )
        camera.annotate_text=localtime
        print("Capturing image to " + picturepath)
        camera.capture(picturepath)
    else:
        picture_command = ['raspistill','--timeout', '1', '--exposure', 'night', '-o', picturepath]
        test_command = ['touch', picturepath]
        if testing:
            print("will test command", test_command)
            subprocess.Popen(test_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, preexec_fn=os.setsid)
        else:
            print("will execute command", picture_command)
            subprocess.Popen(picture_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, preexec_fn=os.setsid)
    values = {}
    # door open: 0 = false, 1 = true ==> 1 door open, 0 door closed
    if 'motion' in closed_or_open:
        door_open = 2
    else:
        door_open = 0 if 'close' in closed_or_open else 1
    values["muis"] = 2 # undetermined until analyzed
    values["sent_email"] = 0 # will do after
    values['door_open'] = door_open
    values['picture'] = picturepath
    values['date'] = date
    # textname = filename + '.txt'
    # textpath = os.path.join(directory, textname)
    # with open(textpath, 'w') as textfile:
    #     textfile.write("Cat entered or left:" + "door " + closed_or_open + "\nDate and time: " + date + "\n" + picturepath + '\n')
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

