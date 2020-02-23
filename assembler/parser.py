from constants import *

class SymbolTable:
    def __init__(self):
        self.entries = SYMBOLS

    def contains(self, symbol):
        return symbol in self.entries

    def add_entry(self, symbol, addr):
        self.entries[symbol] = addr

    def get_addr(self, symbol):
        return self.entries[symbol]

class Parser:

    def __init__(self, filename):
        self.current_line = None
        self.filename = filename
        self.commands = []
        self.symbol_table = SymbolTable()
        self.ROM_addr = 0
        self.RAM_var_start = 16

        self.open_file()
        self.strip()

        while self.has_more_commands():
            self.advance()
            self.commands.append(self.get_command_params())

            if self.c_type == 'label':
                symbol = self.commands[-1]['label']
                self.symbol_table.add_entry(symbol, self.ROM_addr)
            else:
                self.ROM_addr += 1

        for c in self.commands:
            if c['type'] == 'load':
                # If trying to load a symbol and not directly addressing a memory
                # location
                if not c['symbol'].isdigit():
                    # If the symbol table doesn't already contain this symbol
                    if not self.symbol_table.contains(c['symbol']):
                        self.symbol_table.add_entry(c['symbol'],
                                self.RAM_var_start)
                        self.RAM_var_start += 1

    def open_file(self):
        f = open(self.filename, 'r')
        self.file = f
        self.lines = self.file.readlines()
        f.close()

    def strip(self):
        # Strip out lines that are comments
        self.lines = [x for x in self.lines if x[:2] != '//']

        # Strip out blank lines
        self.lines = [x.strip() for x in self.lines if x[:2] != '\n']

        self.lines = [x.split(' ')[0] for x in self.lines]

    def has_more_commands(self):
        return len(self.lines) > 0

    def advance(self):
        if self.has_more_commands():
            self.current_line = self.lines.pop(0)
            self.c_type = self.get_command_type()

    def get_command_params(self):
        command_params = {"type": self.c_type}

        if self.c_type == "load":
            command_params['symbol'] = self.get_symbol()
        elif self.c_type == "compute":
            command_params['dest'] = self.get_destination()
            command_params['comp'] = self.get_computation()
        elif self.c_type == "jump":
            command_params['comp'] = self.get_jump_comp()
            command_params['jump'] = self.get_jump()
        else:
            command_params['label'] = self.get_label()

        return command_params

    def get_command_type(self):
        if self.current_line[0] == '@':
            return "load"
        elif self.current_line[1] == '=':
            return "compute"
        elif self.current_line[1] == ';':
            return "jump"
        elif self.current_line[0] == '(' and self.current_line[-1] == ')':
            return "label"
        else:
            raise SyntaxError('Command format invalid\n\n%s' % self.current_line)


    def get_symbol(self):
        return self.current_line[1:]

    def get_destination(self):
        return self.current_line[0]

    def get_computation(self):
        return self.current_line.split('=')[1]

    def get_jump(self):
        return self.current_line.split(';')[1]

    def get_jump_comp(self):
        return self.current_line.split(';')[0]

    def get_label(self):
        return self.current_line[1:self.current_line.rfind(')')]


