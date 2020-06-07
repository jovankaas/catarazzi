#!/usr/bin/env zsh
# cc0 -- copyleft public domain

args=$(ps aux  | grep woosh | grep python)
nargs=$(ps aux  | grep woosh | grep python | wc -l)
echo $nargs programs running:
for arg in $args
do
    echo $arg
done
echo ''
if [[ $nargs -lt 1 ]]
then
    echo no programs running. starting program
    echo python /home/pi/catarazzi/door_and_motion/sesam_woosh_cheese.py
    python /home/pi/catarazzi/door_and_motion/sesam_woosh_cheese.py&
else
    echo programs running, will do nothing
fi
