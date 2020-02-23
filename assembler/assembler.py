import argparse
from parser import Parser
from writer import CodeWriter 

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
