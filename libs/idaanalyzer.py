
import idautils
import idaapi

class GetXref:
    def __init__(self, address):
        if type(address) == str:
            address = idaapi.get_name_ea(0, address)
        print(hex(address))
        self.xref = list(idautils.XrefsTo(self._getStartFunction(address)[1]))
        print(self.xref)
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
    

def reachAnExport(aefunction, addressExported, crossed_functions):
    reachableExported = []
    for address,xstartaddr,xstartname in GetXref(aefunction):
            if xstartaddr in addressExported:
                reachableExported =  reachableExported + [(xstartname, xstartaddr, address)]
            return reachableExported + reachAnExport(xstartaddr, addressExported, crossed_functions + [xstartname])
    return reachableExported

def main():
    exported_function_count = idaapi.get_entry_qty()
    addressExported = [ idaapi.get_entry_ordinal(exported) for exported in range(exported_function_count)]
    return reachAnExport("system",addressExported, [])
