import lief, os
import platform
import subprocess
from libs.findfunctioninlib import FindFunctionInLibs


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
        if platform.system() == "Windows" and pathlibraries[-1] != "\\":
            return "{}\\".format(pathlibraries)
        if platform.system() == "Linux" and pathlibraries[-1] != "/":
            return "{}/".format(pathlibraries)
        return pathlibraries
    def execplugin(self, idb, plugin, *args):
        command = "{}\\{} -S\"{}\\{} {}\" -L\"{}.logs\" -A {}".format(self.pathida,"idat.exe","{}\\{}".format(os.path.dirname(os.getcwd()),"subplugin"),
                                                      plugin," ".join(args), idb, idb)
        subprocess.call(command)
    def genIDB(self, lib):
        command = [
            "{}\\{}".format(self.pathida,"idat.exe"),
            "-B",
            "-A",
            lib]
        process = subprocess.Popen(command)
        process.wait()
        return process.returncode


        
