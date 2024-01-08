#!/usr/bin/env python

from elftools.elf.elffile import ELFFile

def get_imported_funcs(file_path):
	imported_funcs = []
	with open(file_path, 'rb') as file:
		elf_file = ELFFile(file)
		for section in elf_file.iter_sections():
			if section.name == '.dynsym':
				for symbol in section.iter_symbols():
					if symbol.entry.st_info.type == 'STT_FUNC' and symbol.entry.st_value == 0:
						func_name = symbol.name
						imported_funcs.append(symbol.name)
	return imported_funcs






