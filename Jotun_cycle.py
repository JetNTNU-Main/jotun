from cycle_calc import CONSTANTS_PATH, CONFIG_PATH
from cycle_output import print_txt_table, print_json
import sys

if __name__ == "__main__":
    args = sys.argv[1:]
    cst = False
    cfg = False
    txt_output = False
    txt_file = None
    json_output = False
    json_file = None

    for arg in args:
        if cst:
            CONSTANTS_PATH = arg
            cst = False
        elif cfg:
            CONFIG_PATH = arg
            cfg = False
        elif txt_output:
            txt_file = arg
            txt_output = False
        elif json_output:
            json_file = arg
            json_output = False

        if arg == "-cst":
            cst = True
        elif arg == "-cfg":
            cfg = True
        elif arg == "-t":
            txt_output = True
        elif arg == "-j":
            json_output = True

    if txt_file:
        print_txt_table(txt_file)
    if json_file:
        print_json(json_file)
    if txt_file is None and json_file is None:
        print_txt_table()


