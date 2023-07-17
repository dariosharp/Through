#!/usr/bin/env python                                                                                     


import argparse, logging
import lief
import re
import platform


logger = logging.getLogger('Logger')                
logger.setLevel(logging.INFO)


class Looking4Function:
    def __init__(self, function, plib):
        self.function = function
        lib = lief.parse(plib)
        self.listFunctions = [f.name for f in lib.imported_functions]
    def __iter__(self):
        return self
    def __next__(self):
        for index, f in enumerate(self.listFunctions):
            if re.search(self.function,f):
                self.listFunctions = self.listFunctions[index+1:]
                return f
        raise StopIteration

class FindFunctionInLibs:
    def __init__(self, libList, function):
        self.libList = libList
        self.function = function
    def __iter__(self):
        return self
    def __next__(self):
        for index, l in enumerate(self.libList):
            self.libList = self.libList[index+1:]
            return [(f, l) for f in Looking4Function(self.function, l)]
        raise StopIteration

def parsepath(pathlibraries):
    if platform.system() == "windows" and pathlibraries[-1] != "\\":
        return "{}\\".format(pathlibraries)
    if platform.system() == "Linux" and pathlibraries[-1] != "/":
        return "{}/".format(pathlibraries)
    return pathlibraries

def main(pathbinary, function, pathlibraries, ida):
    logger.debug("Binary: {} Function: {} Library path: {}".format(pathbinary, function, pathlibraries))
    logger.info("Extracting dipendencies from the binary")
    try:
        liefbinary = lief.parse(pathbinary)
        lieflibraries = ["{}/{}".format(pathlibraries,l) for l in liefbinary.libraries]
    except:
        logger.error("The Binary {} is not a valid file".format(pathbinary))
        exit(0)
    logger.debug("libraries list: {}".format(','.join([l for l in lieflibraries])))
    for data in FindFunctionInLibs(lieflibraries,function):
        for f,l in data:
            print("Found \"{}\" in \"{}\"".format(f, l))       

if __name__ == "__main__":
    handler = logging.StreamHandler()
    formatting = logging.Formatter('[%(levelname)s] %(message)s')
    handler.setFormatter(formatting)
    parser = argparse.ArgumentParser(description='Through, finding vulnearbilities through libraries')
    parser.add_argument('-b', '--binary', type=str, help='Binary to analyze', required=True)
    parser.add_argument('-f', '--function', type=str, help='Function you are looking for', required=True)
    parser.add_argument('-l', '--libraries', type=str, help='Libraries path', required=True)
    parser.add_argument('-i', '--ida', type=str, help='Perform ida analysis, in order to discover how to trigger the function u looking for. Set here the path to ida folder. Moreover, exec the script in ida ex: ida.exe -t -S"through.py ..." -L"results.txt"')
    parser.add_argument('-v','--verbosity', action='store_true', help='Debugging verbosity')
    args = parser.parse_args()
    if args.verbosity:
        logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    main(args.binary,args.function, args.libraries, args.ida or None)

