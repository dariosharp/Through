import lief
import platform
from fingfunctioninlib import FindFunctionInLibs


class Through:
    def __init__(self, pathbinary, function, pathlibraries, pathida):
        self.binary = lief.parse(pathbinary)
        self.function = function
        parsedpathlibraries = self.parsepath(pathlibraries)
        self.libraries = ["{}{}".format(parsedpathlibraries,l) for l in self.binary.libraries]
        self.pathida = pathida
    def getLibs(self):
        return [l for list_per_lib in FindFunctionInLibs(self.libraries,self.function) for f,l in list_per_lib]
    def getFunctions(self):
        return [f for list_per_lib in FindFunctionInLibs(self.libraries,self.function) for f,l in list_per_lib] 
    def getFunctionPerLib(self):
        return [(f,l) for list_per_lib in FindFunctionInLibs(self.libraries,self.function) for f,l in list_per_lib]
    def parsepath(self,pathlibraries):
        if platform.system() == "windows" and pathlibraries[-1] != "\\":
            return "{}\\".format(pathlibraries)
        if platform.system() == "Linux" and pathlibraries[-1] != "/":
            return "{}/".format(pathlibraries)
        return pathlibraries

