#!/usr/bin/env python                                                                                     


import argparse, logging, platform
from libs.through import Through


logger = logging.getLogger('Logger')                
logger.setLevel(logging.INFO)

def main(pathbinary, function, pathlibraries, ida):
    logger.debug("Binary: {} Function: {} Library path: {}".format(pathbinary, function, pathlibraries))
    logger.info("Extracting dipendencies from the binary")
    through = Through(pathbinary,function,pathlibraries,ida)
    liblist = []
    for f,l in through.getFunctionPerLib():
        liblist.append(l)
        logger.info("Found \"{}\" in \"{}\"".format(f, l))
    if ida != None:
        pass


if __name__ == "__main__":
    handler = logging.StreamHandler()
    formatting = logging.Formatter('[%(levelname)s] %(message)s')
    handler.setFormatter(formatting)
    if platform.system() == "Windows":
        logger.addHandler(handler)
        from libs.windowQT import PathIDA
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


