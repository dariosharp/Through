#!/usr/bin/env python                                                                                     


import argparse, logging, platform
from libs.analyzer import Analyzer
from libs.windowQT import SelectLibsIDA


logger = logging.getLogger('Logger')                
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatting = logging.Formatter('[%(levelname)s] %(message)s')
handler.setFormatter(formatting)
logger.addHandler(handler)


class Main:
        def __init__(self, pathbinary, function, pathlibraries, ida):
            self.pathbinary = pathbinary
            self.function = function
            self.pathlibraries = pathlibraries
            self.ida = ida
        def run(self):
            logger.debug("Binary: {} Function: {} Library path: {}".format(self.pathbinary, self.function, self.pathlibraries))
            logger.info("Extracting dipendencies from the binary")
            analyzer = Analyzer(self.pathbinary,self.function,self.pathlibraries,self.ida)
            libxfunction = []
            for f,l in analyzer.getFunctionPerLib():
                libxfunction.append((f,l))
                logger.info("Found \"{}\" in \"{}\"".format(f, l))
            listlibs = list(map(lambda x: x[1], libxfunction))
            if listlibs == []:
                logger.info("Among the libs available and imported by the binary do not use the function \"{}\"".format(self.function))
                exit(0)
            if self.ida != None:
                self._idaanalyis(analyzer,listlibs)

        def _idaanalyis(self, analyzer, listlibs):
            sli = SelectLibsIDA(listlibs)
            selectedLibs = sli.getList()
            for l in selectedLibs:
                logger.info("Selected Lib to analyze: \"{}\"".format(l))
            if selectedLibs == []:
                logger.info("You have no selected any library")
                exit(0)
            for l in selectedLibs:
                rv = analyzer.genIDB(l)
                logger.info("IDB createtion for {}, Return Values: {}".format(l, hex(rv)))
            for l in selectedLibs:
                rv = analyzer.execplugin("{}.idb".format(l), "getexportedbyfunction.py", self.function)
                logger.info("IDB analysis for {} Rerturn Value: {}".format(l, rv))
            for l in selectedLibs:
                rowdata = analyzer.getResults("{}.idb".format(l))
                if rowdata != None:
                    reached_exp = reached_exp + [(l, eval(rowdata))]
                logger.info("{} {}".format(reached_exp[-1][0], str(reached_exp[-1][1])))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Through, finding vulnearbilities through libraries')
    parser.add_argument('-b', '--binary', type=str, help='Binary to analyze', required=True)
    parser.add_argument('-f', '--function', type=str, help='Function you are looking for', required=True)
    parser.add_argument('-l', '--libraries', type=str, help='Libraries path', required=True)
    parser.add_argument('-v','--verbosity', action='store_true', help='Debugging verbosity')
    args = parser.parse_args()
    if args.verbosity:
        logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    m = Main(args.binary,args.function, args.libraries, None)
    m.run()


