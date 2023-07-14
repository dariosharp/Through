#!/usr/bin/env python                                                                                     


import argparse


def main(binary, function, libraries):
    print(binary, function, libraries)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Through, sourth among libraries')
    parser.add_argument('-b', '--binary', type=str, help='Binary to analyze', required=True)
    parser.add_argument('-f', '--function', type=str, help='Function you are looking for', required=True)
    parser.add_argument('-l', '--libraries', type=str, help='Libraries path', required=True)
    args = parser.parse_args()
    main(args.binary,args.function, args.libraries)

