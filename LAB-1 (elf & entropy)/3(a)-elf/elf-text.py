from elftools.elf.elffile import ELFFile
from capstone import *
import sys


F = open('textSection.txt','w+')
fname = sys.argv[1]

with open(fname, 'rb') as f:
	elf = ELFFile(f)
	code = elf.get_section_by_name('.text')
	ops = code.data()
	addr = code['sh_addr']
	md = Cs(CS_ARCH_X86, CS_MODE_64)
	for i in md.disasm(ops, addr):
		print('0x',i.address,'\t',i.mnemonic,'\t',i.op_str)
		s = '0x'+str(i.address)+'\t'+str(i.mnemonic)+'\t'+str(i.op_str)
		F.write(s)
		F.write('\n')

