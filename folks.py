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

    # search (and limit output to certain properties if you want to)
    ./folks.py --footballers=1 tele
        # output:
        sven:tele:0703453455
        martin:tele:070143151

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
import difflib
import re

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
    return config.sections()

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

def search(filters, properties=None):
    hits = []
    for nick in config.sections():
        for prop in filters:
            if config.has_option(nick, prop) and filters[prop].lower() in config.get(nick, prop).lower():
                if properties and prop in properties:
                    hits.append({nick: (prop, config.get(nick, prop))})
                elif not properties and nick not in hits:
                    for propset in config.items(nick):
                        hits.append({nick: propset})
    return hits

def main():
    if len(sys.argv) == 1:
        print "\n".join(list())
        sys.exit()
    if any([i in sys.argv for i in ("help", "-h", "--help")]):
        usage(0)
    nick = sys.argv[1]
    if not config.has_section(nick) and "=" not in ''.join(sys.argv):
        print "%s doesn't exist yet, add with %s luke name=\"Luke S. Walker\"" % (nick, sys.argv[0])
        close = difflib.get_close_matches(nick, list(), 3)
        if close:
            print "\nAlmost what you searched for:\n%s" % "\n".join(close)
        sys.exit(1)
    args = sys.argv[1:]
    if len(args) == 1 and "=" not in ''.join(args):
        get(nick)
        sys.exit()
    filters = {}
    properties = []
    for arg in args:
        matches = re.search("--([^=]+)=(.*)", arg)
        if matches:
            filters[matches.group(1)] = matches.group(2)
        elif "=" in arg:
            set(nick, arg.split("=")[0], arg.split("=")[1])
        else:
            # ok, you're too lazy to use grep. let me help you
            properties.append(arg)
    if filters:
        matches = search(filters, properties)
        if not matches:
            print "No entries contained given filters"
            sys.exit()
        for m in matches:
            for b in m:
                print "%s:%s:%s" % (b, m[b][0], m[b][1])

if __name__ == "__main__":
    main()

# @todo make sure it makes sense to import this into another python module
# @todo tests
