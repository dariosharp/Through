#!/usr/bin/env python                                                                                     


import argparse, logging, platform
from through.libs.analyzer import LibFilter, ExecSubPlugin
from through.libs.windowQT import SelectLibsIDA
from through.libs.results import ResultClass


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
            self.analyzer = LibFilter(self.pathbinary,self.function,self.pathlibraries)
            libxfunction = []
            for f,l in self.analyzer.getFunctionPerLib():
                libxfunction.append((f,l))
                logger.info("Found \"{}\" in \"{}\"".format(f, l))
            listlibs = list(set(map(lambda x: x[1], libxfunction)))
            if listlibs == []:
                logger.info("Among the libs available and imported by the binary do not use the function \"{}\"".format(self.function))
                exit(0)
            if self.ida == True:
                sli = SelectLibsIDA(listlibs)
                selectedLibs = sli.getList()
                for l in selectedLibs:
                    logger.info("Selected Lib to analyze: \"{}\"".format(l))
                if selectedLibs == []:
                    logger.info("You have't selected any library")
                    exit(0)
                self._idaanalyis(selectedLibs)

        def _idaanalyis(self, selectedLibs):
            execsubplg = ExecSubPlugin(self.analyzer.getArch())
            for l in selectedLibs:
                rv = execsubplg.genIDB(l)
                logger.info("IDB createtion for {}, Return Values: {}".format(l, hex(rv)))
            for l in selectedLibs:
                rv = execsubplg.execplugin("{}".format(l), "getexportedbyfunction.py", self.function)
                logger.info("IDB analysis for {} Rerturn Value: {}".format(l, rv))
            reached_exp = []
            for l in selectedLibs:
                rowdata = execsubplg.getResults("{}".format(l))
                if rowdata != None:
                    data = eval(rowdata[0])
                    logger.debug("{}: {}".format(l, data))
                    reached_exp = reached_exp + [(l, data)]
            plg = ResultClass()
            plg.Show("Lib Analysis Results")
            for l,functions in reached_exp:
                for name, args, addr, faddr in functions:
                    import idaapi
                    if idaapi.get_name_ea(0, name) != 0xffffffff and args.split(":")[1] != "0":
                        plg.add_row([l, name, faddr])
                        logger.debug("[!!] Potential Match! {}: {}, exploitable at {}".format(l, name, faddr))
                logger.info("Done")


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


