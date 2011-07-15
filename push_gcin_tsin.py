import os
import sys
from gcintsinlib import are_tools_existed
from gcintsinlib import write_tsin
from gcintsinlib import get_list_from_current_tsin32
from gcintsinlib import DROPBOX_TSIN32_TXT 

def push():
    """
    Write ~/.gcin/tsin32 to ~/.Dropbox/linux/common 
    """
    if not are_tools_existed():
        return -1

    os.system( "mkdir -p \"%s\"" % (
                os.path.dirname( DROPBOX_TSIN32_TXT ) ) )
    write_tsin( open( 
                DROPBOX_TSIN32_TXT, "w" 
                ), get_list_from_current_tsin32() )
    print( "Done." )
    return 0

def main(arg):
    return push()

if __name__ == "__main__":
    main(sys.argv[1:])

