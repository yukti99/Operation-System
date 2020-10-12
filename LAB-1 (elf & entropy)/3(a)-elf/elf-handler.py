from elftools.elf.elffile import ELFFile
import sys

Fptr = open('section.txt','w+')
filename = sys.argv[1]
with open(filename, 'rb') as f:
	e = ELFFile(f)
	for section in e.iter_sections():
		print(hex(section['sh_addr']),section.name)
		s = str(hex(section['sh_addr'])) + '\t' + str(section.name)
		Fptr.write(s)
		Fptr.write('\n')
		
# shows all sections and where it is loaded
# .text -> opcodes
# .data -> strings and constants initialized at compile time
# .plt  -> Procedure Linkage Table
# .got  -> Global Offset Table

