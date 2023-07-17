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
        for index, l in enumerate(self.libList):
            self.libList = self.libList[index+1:]
            return [(f, l) for f in Looking4Function(self.function, l)]
        raise StopIteration
