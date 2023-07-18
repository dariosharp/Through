import re,lief


class Looking4Function:
    def __init__(self, function, plib):
        self.function = function
        lib = lief.parse(plib)
        self.listFunctions = [f.name for f in lib.imported_functions]
    def __iter__(self):
        return self
    def __next__(self):
        for index, f in enumerate(self.listFunctions):
            if re.search(self.function,f):
                self.listFunctions = self.listFunctions[index+1:]
                return f
        raise StopIteration

class FindFunctionInLibs:
    def __init__(self, libList, function):
        self.libList = libList
        self.function = function
    def __iter__(self):
        return self
    def __next__(self):
        if self.libList == []:
            raise StopIteration
        lib = self.libList[0]
        self.libList = self.libList[1:]
        return [(f, lib) for f in Looking4Function(self.function, lib)]