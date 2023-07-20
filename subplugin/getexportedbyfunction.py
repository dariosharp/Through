import idautils
import idaapi
import idc
import ida_hexrays

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
                    args = "args:{}".format(self._getArgs(xstartaddr))
                    reachableExported =  reachableExported + [(xstartname, args, hex(xstartaddr), hex(address))]
                    crossed_functions = crossed_functions + [xstartname]
        return reachableExported
    def _getArgs(self, addr):
        ida_hexrays.decompile(addr)
        tif = ida_typeinf.tinfo_t()
        funcdata = ida_typeinf.func_type_data_t()
        ida_nalt.get_tinfo(tif, addr)
        tif.get_func_details(funcdata)
        return len([a for a in enumerate(funcdata)])

if __name__ == '__main__':
    e = GetExport(idc.ARGV[1])
    results = str(e.reachAnExport())
    print("*****PLUGIN-START*****")
    print(results)
    print("*****PLUGIN-END*****")
    ida_pro.qexit(0)
