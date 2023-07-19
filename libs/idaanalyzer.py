import idautils
import idaapi

class GetXref:
    def __init__(self, address):
        if type(address) == str:
            address = idaapi.get_name_ea(0, address)
        sf =  self._getStartFunction(address)[1]
        self.xref = []
        if sf != None:
            self.xref = list(idautils.XrefsTo(self._getStartFunction(address)[1]))
    def _getStartFunction(self, address):
        function = idaapi.get_func(address)
        if function is None:
            return None, None
        return idaapi.get_func_name(function.start_ea), function.start_ea
    def __iter__(self):
        return self
    def __next__(self):
        if self.xref == []:
            raise StopIteration
        x = self.xref[0]
        self.xref = self.xref[1:]
        xstartname, xstartaddr = self._getStartFunction(x.frm)
        if xstartaddr == None:
            self.__next__()
        return x.frm, xstartaddr, xstartname
    
class GetExport:
    def __init__(self, fname):
        self.fname = fname
        exported_function_count = idaapi.get_entry_qty()
        self.addressExported = [ idaapi.get_entry_ordinal(exported) for exported in range(exported_function_count)]
    def reachAnExport(self):
        return self._reachAnExport(self.fname, [])
    def _reachAnExport(self, aefunction, crossed_functions):
        reachableExported = []
        for address,xstartaddr,xstartname in GetXref(aefunction):
                if xstartaddr not in crossed_functions:
                    if xstartaddr not in self.addressExported:
                        return reachableExported + self._reachAnExport(xstartaddr, crossed_functions + [xstartname])
                    reachableExported =  reachableExported + [(xstartname, xstartaddr, address)]
                    crossed_functions = crossed_functions + [xstartname]
        return reachableExported

if __name__ == '__main__':
    e = GetExport("system")
    print(str(e.reachAnExport()))
