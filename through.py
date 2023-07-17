#!/usr/bin/env python                                                                                     


import argparse, logging
import lief
import platform
from fingfunctioninlib import FindFunctionInLibs

logger = logging.getLogger('Logger')                
logger.setLevel(logging.INFO)

class Through:
    def __init__(self, pathbinary, function, pathlibraries, pathida):
        self.binary = lief.parse(pathbinary)
        self.function = function
        parsedpathlibraries = parsepath(pathlibraries)
        self.libraries = ["{}{}".format(parsedpathlibraries,l) for l in self.binary.libraries]
        self.pathida = pathida
    def getLibs(self):
        return [l for list_per_lib in FindFunctionInLibs(self.libraries,self.function) for f,l in list_per_lib]
    def getFunctions(self):
        return [f for list_per_lib in FindFunctionInLibs(self.libraries,self.function) for f,l in list_per_lib] 
    def getFunctionPerLib(self):
        return [(f,l) for list_per_lib in FindFunctionInLibs(self.libraries,self.function) for f,l in list_per_lib]


def parsepath(pathlibraries):
    if platform.system() == "windows" and pathlibraries[-1] != "\\":
        return "{}\\".format(pathlibraries)
    if platform.system() == "Linux" and pathlibraries[-1] != "/":
        return "{}/".format(pathlibraries)
    return pathlibraries

def main(pathbinary, function, pathlibraries, ida):
    logger.debug("Binary: {} Function: {} Library path: {}".format(pathbinary, function, pathlibraries))
    logger.info("Extracting dipendencies from the binary")
    through = Through(pathbinary,function,pathlibraries,ida)
    for f,l in through.getFunctionPerLib():
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


