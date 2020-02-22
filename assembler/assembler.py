import os
import argparse

A_PREFIX = '0'
C_PREFIX = '111'


COMP_MAP = {
    "0":    "0101010",
    "1":    "0111111",
    "-1":   "0111010",
    "D":    "0001100",
    "A":    "0110000",
    "!D":   "0001101",
    "!A":   "0110001",
    "-D":   "0001111",
    "-A":   "0110011",
    "D+1":  "0011111",
    "A+1":  "0110111",
    "D-1":  "0001110",
    "A-1":  "0110010",
    "D+A":  "0000010",
    "D-A":  "0010011",
    "A-D":  "0000111",
    "D&A":  "0000000",
    "D|A":  "0010101",
    "M":    "1110000",
    "!M":   "1110001",
    "-M":   "1110011",
    "M+1":  "1110111",
    "M-1":  "1110010",
    "D+M":  "1000010",
    "D-M":  "1010011",
    "M-D":  "1000111",
    "D&M":  "1000000",
    "D|M":  "1010101",
}

DEST_MAP = {
    None:   "000",
    "M":   "001",
    "D":   "010",
    "MD":  "011",
    "A":   "100",
    "AM":  "101",
    "AD":  "110",
    "AMD": "111"
}

JUMP_MAP = {
    None:   "000",
    "JGT": "001",
    "JEQ": "010",
    "JGE": "011",
    "JLT": "100",
    "JNE": "101",
    "JLE": "110",
    "JMP": "111"
}


c_type_map = {
    "load": A_PREFIX,
    "compute": C_PREFIX,
    "jump": C_PREFIX
}

max_posve = 2**15 - 1
max_negve = -2**15

class Parser:

    def __init__(self, filename):
        self.current_line = None
        self.filename = filename
        self.commands = []

        self.open_file()
        self.strip()

        while self.has_more_commands():
            self.advance()
            self.commands.append(self.get_command_params())

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
        if self.c_type == "compute":
            command_params['dest'] = self.get_destination()
            command_params['comp'] = self.get_computation()
        if self.c_type == "jump":
            command_params['comp'] = self.get_jump_comp()
            command_params['jump'] = self.get_jump()

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


class CodeWriter:

    def __init__(self, parser):
        filename, ext = os.path.splitext(parser.filename)
        self.filename = filename + '.hack'
        self.commands = parser.commands
        self.f = open(self.filename, 'a')

    def convert_instruction(self, c):
        command = c_type_map[c['type']]

        if c['type'] == 'compute':
            command += COMP_MAP[c['comp']]
            command += DEST_MAP[c['dest']]
            command += JUMP_MAP[None]
        elif c['type'] == 'jump':
            command += COMP_MAP[c['comp']]
            command += DEST_MAP[None]
            command += JUMP_MAP[c['jump']]
        else:
            binary = bin(int(c['symbol']))[2:]
            padding = 15 - len(binary)
            command += padding * '0' + binary

        print(command, file=self.f)

    def write(self):
        for c in self.commands:
            self.convert_instruction(c)

        self.f.close()

        print('Finished assembling file %s' % self.filename)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Assembler for the 'Hack' \
    platform, specs detailed in The Elements of Computing Systems: Building \
    a Modern Computer from First Principles")

    parser.add_argument('filename')

    args = parser.parse_args()

    print('Assembling %s' % args.filename)

    p = Parser(args.filename)
    c = CodeWriter(p)
    c.write()
