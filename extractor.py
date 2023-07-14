#!/usr/bin/env python                                                                                     


import argparse, logging

logger = logging.getLogger('Logger')                
logger.setLevel(logging.INFO)

def main(binary, function, libraries):
    logger.debug("Binary: {} Function: {} Library path: {}".format(binary, function, libraries))

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

