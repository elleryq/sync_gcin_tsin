import os
import sys
from gcintsinlib import are_tools_existed
from gcintsinlib import write_tsin
from gcintsinlib import get_list_from_current_tsin32

def push( remote_file ):
    """
    Write ~/.gcin/tsin32 to remote_file.
    """
    if not are_tools_existed():
        return -1

    dirname = os.path.dirname( remote_file )
    if dirname and not os.path.exists(dirname):
        os.makedirs( dirname )

    write_tsin( open( 
                remote_file, "wb"
                ), get_list_from_current_tsin32() )
    print( "Done." )
    return 0

def main(arg):
    return push(arg[0])

if __name__ == "__main__":
    main(sys.argv[1:])

