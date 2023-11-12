import lief
import platform
import subprocess
from through.libs.findfunctioninlib import FindFunctionInLibs


class LibFilter:
    def __init__(self, pathbinary, function, pathlibraries):
        self.binary = lief.parse(pathbinary)
        self.function = function
        parsedpathlibraries = self.parsepath(pathlibraries)
        self.libraries = ["{}{}".format(parsedpathlibraries,l) for l in self.binary.libraries]
    def getLibs(self):
        return [l for list_per_lib in FindFunctionInLibs(self.libraries,self.function) for f,l in list_per_lib]
    def getFunctions(self):
        return [f for list_per_lib in FindFunctionInLibs(self.libraries,self.function) for f,l in list_per_lib] 
    def getFunctionPerLib(self):
        return [(f,l) for list_per_lib in FindFunctionInLibs(self.libraries,self.function) for f,l in list_per_lib]
    def parsepath(self,pathlibraries):
        if pathlibraries[-1] != "/":
            return "{}/".format(pathlibraries)
        return pathlibraries
    def getArch(self):
        if self.binary.header.machine_type == lief.ELF.ARCH.x86_64:
            return 64
        return 32


class ExecSubPlugin:
    def __init__(self, arch):
        self.arch = arch
    def genIDB(self, lib):
        command = [
            "{}".format("idat.exe"),
            "-B",
            "-A",
            lib]
        if self.arch == 64:
            command = [
                "{}".format("idat64.exe"),
                "-B",
                "-TELF64",
                "-A",
                lib]
        process = subprocess.Popen(command)
        process.wait()
        return process.returncode
    def execplugin(self, idb, plugin, *args):
        command = [
            "{}.exe".format("idat64" if self.arch == 64 else "idat" ),
            "-S\"{}\\{} {}\"".format("plugins\\through\\subplugin", plugin, " ".join(args)),
            "-L\"{}.{}.logs\"".format(idb, "i64" if self.arch == 64 else "idb"),
            "-A",
            idb]
        command = ' '.join(command)
        subprocess.call(command)
    def getResults(self, idb):
        with open("{}.{}.logs".format(idb, "i64" if self.arch == 64 else "idb"), "r") as file:
            data = file.read()
        plugininfo = False
        prow = []
        for row in data.split("\n"):
            if plugininfo == True:
                if row == "*****PLUGIN-END*****":
                    return prow
                prow = prow + [row]
            if row == "*****PLUGIN-START*****":
                plugininfo = True
        return None





