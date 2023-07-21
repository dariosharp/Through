import idaapi


class PluginThough(idaapi.plugin_t):
    flags = 0
    comment = "Library analyzer"
    help = "Looking for specific functions, you can discover how to reach sensitive functionalities in the libraries imported"
    wanted_name = "Through"
    wanted_hotkey = "Ctrl-Alt-T"

    def init(self):
        idaapi.msg("Through plugin initialized\n")
        return idaapi.PLUGIN_KEEP

    def run(self, arg):
        import os
        from through.libs.main import Main
        from through.libs.windowQT import PathIDA
        wIDA = PathIDA()
        
        binary = os.path.basename((idaapi.get_input_file_path()))
        function, libraries = wIDA.getValues()
        m = Main(binary, function, libraries, True)
        m.run()

    def term(self):
        idaapi.msg("Through plugin terminated\n")

def PLUGIN_ENTRY():
    return PluginThough()