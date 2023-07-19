#!/usr/bin/env python                                                                                     


import argparse, logging, platform
from libs.through import Through


logger = logging.getLogger('Logger')                
logger.setLevel(logging.INFO)

def main(pathbinary, function, pathlibraries, ida):
    logger.debug("Binary: {} Function: {} Library path: {}".format(pathbinary, function, pathlibraries))
    logger.info("Extracting dipendencies from the binary")
    through = Through(pathbinary,function,pathlibraries,ida)
    libxfunction = []
    for f,l in through.getFunctionPerLib():
        libxfunction.append((f,l))
        logger.info("Found \"{}\" in \"{}\"".format(f, l))
    listlibs = list(map(lambda x: x[1], libxfunction))
    if listlibs == []:
        logger.info("Among the libs available and imported by the binary do not use the function \"{}\"".format(function))
        exit(0)
    if ida != None:
        sli = SelectLibsIDA(listlibs)
        selectedLibs = sli.getList()
        for l in selectedLibs:
            logger.info("Selected Lib to analyze: \"{}\"".format(l))
        if selectedLibs == []:
            logger.info("You have no selected any library")
            exit(0)
        for l in selectedLibs:
            logger.info("IDB createtion for {}".format(l))
            through.genIDB(l)
        for l in selectedLibs:
            logger.info("IDB analysis for {}".format(l))
            through.execplugin("{}.idb".format(l), "getexportedbyfunction.py", function)


if __name__ == "__main__":
    handler = logging.StreamHandler()
    formatting = logging.Formatter('[%(levelname)s] %(message)s')
    handler.setFormatter(formatting)
    if platform.system() == "Windows":
        logger.addHandler(handler)
        from libs.windowQT import PathIDA, SelectLibsIDA
        wIDA = PathIDA()
        binary, function, libraries, pathida = wIDA.getValues()
        main(binary, function, libraries, pathida)
    if platform.system() == "Linux":
        parser = argparse.ArgumentParser(description='Through, finding vulnearbilities through libraries')
        parser.add_argument('-b', '--binary', type=str, help='Binary to analyze', required=True)
        parser.add_argument('-f', '--function', type=str, help='Function you are looking for', required=True)
        parser.add_argument('-l', '--libraries', type=str, help='Libraries path', required=True)
        parser.add_argument('-v','--verbosity', action='store_true', help='Debugging verbosity')
        args = parser.parse_args()
        if args.verbosity:
            logger.setLevel(logging.DEBUG)
        logger.addHandler(handler)
        main(args.binary,args.function, args.libraries, None)


