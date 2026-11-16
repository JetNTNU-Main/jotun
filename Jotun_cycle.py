from cycle_calc import CONSTANTS_PATH, CONFIG_PATH
from cycle_output import call_engine_cycle
import sys

if __name__ == "__main__":
    args = sys.argv[1:]
    cst = False
    cfg = False
    file = False

    for arg in args:
        if cst:
            CONSTANTS_PATH = arg
            cst = False
        elif cfg:
            CONFIG_PATH = arg
            cfg = False
        elif file:
            sys.stdout = open(arg, 'w')
            file = False

        if arg == "-cst":
            cst = True
        elif arg == "-cfg":
            cfg = True
        elif arg == "-f":
            file = True

    call_engine_cycle()
    sys.stdout.flush()
    sys.stdout.close()


