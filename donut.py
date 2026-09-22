import sys
from utils.compile import Compiler

def print_usage() -> None:
    print("USAGE: donut <script>.dt [OPTIONS]")
    print("OPTION:")
    print("    <nothing>")

def main(args: list[str]) -> None:
    if len(args) <= 1:
        print("ERROR: required a .dt file")
        print_usage()
        sys.exit(1)
    with open(args[1], 'r') as file:
        compile = Compiler(file.read())
        bytecode = compile.compile()
        final_path = args[1][:-len(".dt")] + ".class"
        with open(final_path, 'wb') as write_file:
            write_file.write(bytecode)

if __name__ == "__main__":
    main(sys.argv)
