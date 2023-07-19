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
        from libs.main import Main
        from libs.windowQT import PathIDA
        wIDA = PathIDA()
        binary, function, libraries, pathida = wIDA.getValues()
        m = Main(binary, function, libraries, pathida)
        m.run()

    def term(self):
        idaapi.msg("Through plugin terminated\n")

def PLUGIN_ENTRY():
    return PluginThough()