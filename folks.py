#!/usr/bin/env python
"""
folks.py [id] [property] [property=value]

A simple CLI address book with backend stored in an .ini-file
(default ~/folks.ini).

USAGE
    folks is intented to be grep-, sed-, columns-, cut- and awk-friendly:

    # list all id's
    ./folks.py
        # output:
        sven
        rocker
        nisse

    # list properties of given id
    ./folks.py sven
        # output:
        name:Sven Larsson
        tele:+4670677151
        email:sven@larsson.com

    # get some options of an id
    ./folks.py martin | grep phone | cut -d: -f2 # output: +46462462446
        # shortcut, if you don't like grep:
    ./folks.py sven tele
        # output:
        +4670677151

    # sets properties
    ./folks.py sven tel=325236266 email=sven@email.com

    If you need more import channels than stdin, edit the text file. I'm
    just a frontend.

PROPERTIES

    You are yourself responsible for what a "property" is, for example
    "tel" vs "tele" vs "telephone". If you want to consolidate the format:

        sed -i -e 's/^tele /tel /' your-file.ini

"""

file = "~/folks.ini"

import sys
import ConfigParser
import inspect
import os

file = os.path.expanduser(file)
config = ConfigParser.ConfigParser()
if not file or not len(config.read(file)):
    print "Could not read the file '%s', create it for me or change the path" % file
    sys.exit(1)

def get(nick, option=None):
    if option and config.has_option(nick, option):
        print config.get(nick, option).strip("\"'")
        return
    for x, y in config.items(nick):
        print "%s:%s" % (x, y.strip("\"'"))

def list():
    print "\n".join(config.sections())

def set(nick, key, value, write=True):
    try:
        config.set(nick, key, value)
    except ConfigParser.NoSectionError:
        config.add_section(nick)
        config.set(nick, key, value)

    if write:
        config.write(open(file, 'w'))

def usage(exit_code=0):
    print inspect.getdoc(sys.modules[__name__])
    sys.exit(exit_code)

if __name__ == "__main__":
    if len(sys.argv) == 1:
        list()
        sys.exit()
    if any([i in sys.argv for i in ("help", "-h", "--help")]):
        usage(0)
    nick = sys.argv[1]
    if not config.has_section(nick) and "=" not in ''.join(sys.argv):
        print "%s doesn't exist yet, add with %s luke --name=\"Luke S. Walker\"" % (nick, sys.argv[0])
        sys.exit(1)
    args = sys.argv[2:]
    if not len(args):
        get(nick)
        sys.exit()
    for arg in args:
        if "=" in arg:
            set(nick, arg.split("=")[0], arg.split("=")[1])
        else:
            # ok, you're too lazy to use grep. let me help you
            get(nick, arg)


# @todo make sure it makes sense to import this into another python module
# @todo add a filter function, like --name=sven which is a case
# insensitive reduce
    #folks --email=gmail
        ## output:
        #rocker:johnyboy@gmail.com
        #nisse:nils@gmail.com

    #./folks --beachvolley=1 tel
        ## output
        #sven:+4670677151
# @todo tests
