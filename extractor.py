#!/usr/bin/env python                                                                                     


import argparse, logging
import lief
import re


logger = logging.getLogger('Logger')                
logger.setLevel(logging.INFO)

def parsepath(pathlibraries):
    if pathlibraries[-1] == "/":
        return pathlibraries
    return "{}/".format(pathlibraries)

def findfunction(lieflibraries, function, pathlibraries):
    logger.info("Looking for the function \"{}\" in {}".format(function, pathlibraries))
    for l in lieflibraries:
        try:
            logger.debug("Opening: {}{}".format(pathlibraries, l))
            lieflib = lief.parse("{}{}".format(pathlibraries, l))
            lfunctions = [f.name for f in lieflib.imported_functions]
            logger.debug("Functions: {}".format(','.join(lfunctions)))
        except:
            logger.warning("{}{} is not a valid library".format(pathlibraries, l))
        for f in lfunctions:
            if re.search(function,f):
                print("Found \"{}\" in \"{}\"".format(f, l))       

def main(pathbinary, function, pathlibraries):
    logger.debug("Binary: {} Function: {} Library path: {}".format(pathbinary, function, pathlibraries))
    logger.info("Extracting dipendencies from the binary")
    try:
        liefbinary = lief.parse(pathbinary)
        lieflibraries = liefbinary.libraries
    except:
        logger.error("The Binary {} is not a valid file".format(pathbinary))
        exit(0)
    logger.debug("libraries list: {}".format(','.join([l for l in lieflibraries])))
    findfunction(lieflibraries,function, parsepath(pathlibraries))

if __name__ == "__main__":
    handler = logging.StreamHandler()
    formatting = logging.Formatter('[%(levelname)s] %(message)s')
    handler.setFormatter(formatting)
    parser = argparse.ArgumentParser(description='Through, sourth among libraries')
    parser.add_argument('-b', '--binary', type=str, help='Binary to analyze', required=True)
    parser.add_argument('-f', '--function', type=str, help='Function you are looking for', required=True)
    parser.add_argument('-l', '--libraries', type=str, help='Libraries path', required=True)
    parser.add_argument('-v','--verbosity', action='store_true', help='Debugging verbosity')
    args = parser.parse_args()
    if args.verbosity:
        logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    main(args.binary,args.function, args.libraries)

