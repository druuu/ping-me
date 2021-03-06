"""The engine module of ping-me"""
from __future__ import absolute_import
from __future__ import print_function
from __future__ import division
import datetime
import getpass
import os
import requests
import sys
import time

from ping_me import authenticate
from ping_me.utils import cryptex

today = datetime.date.today()
home = os.path.expanduser("~")


def engine(message, year, month, day, hour=0, minute=0, v=False):
    """Sets the reminder"""
    if not os.path.exists(home + '/.pingmeconfig'):
        authenticate.newuser()
    else:
        if not authenticate.check_saved_password():
            authenticate.olduser()

    d = datetime.datetime(year, month, day, hour, minute)
    if d < datetime.datetime.now():
        sys.stdout.write("Are you sure about being reminded in the past?\n")
        sys.exit(2)
    # Set offset according to the UTC-05:00 timezone
    _server_offset = 5
    offset = _server_offset - (time.timezone)/3600

    if v:
        print("I have got this message :", message)
        print("I have to ping you on {:%Y-%m-%d %H:%M} hours.".format(d))
        print("Your timezone offset with UTC-05:00 is {} hours.".format(offset))

    d = d - datetime.timedelta(hours=offset)  # Convert into NYC timezone

    extra = ' '*(16*(len(message)//16 + 1) - len(message))
    crypto_message = message + extra
    crypto_message = cryptex.encryptor(authenticate.extract_password(),
                                       crypto_message)
    target = "http://45.55.91.182:2012/message/"
    credentials = {'email' : authenticate.extract_email(),
                   'ping_datetime' : d.strftime("%Y-%m-%d %H:%M:00"),
                   'message' : crypto_message
                   }

    r = requests.post(target, data=credentials)
    print(r.status_code, r.reason)
