import os
from constants import *

class CodeWriter:

    def __init__(self, parser):
        filename, ext = os.path.splitext(parser.filename)
        self.filename = filename + '.hack'
        self.commands = parser.commands

        if os.path.exists(self.filename):
            os.remove(self.filename)

        self.f = open(self.filename, 'a')
        self.st = parser.symbol_table

    def convert_instruction(self, c):
        command = C_TYPE_MAP[c['type']]

        if c['type'] == 'compute':
            command += COMP_MAP[c['comp']]
            command += DEST_MAP[c['dest']]
            command += JUMP_MAP[None]
        elif c['type'] == 'jump':
            command += COMP_MAP[c['comp']]
            command += DEST_MAP[None]
            command += JUMP_MAP[c['jump']]
        elif c['type'] == 'load':
            binary = None
            symbol = c['symbol'] if c['symbol'].isdigit() else \
                self.st.entries[c['symbol']]

            binary = bin(int(symbol))[2:]

            padding = 15 - len(binary)
            command += padding * '0' + binary

        if command is not None:
            print(command, file=self.f)

    def write(self):
        for c in self.commands:
            self.convert_instruction(c)

        self.f.close()

        print('Finished assembling file %s' % self.filename)

