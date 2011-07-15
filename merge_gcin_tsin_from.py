import os
import sys
from gcintsinlib import are_tools_existed
from gcintsinlib import get_list_from_current_tsin32
from gcintsinlib import get_list_from_remote
from gcintsinlib import write_back_merged_tsin
from gcintsinlib import USER_TSIN32

def pull_and_merge( remote_filename ):
    """
    Merge the tsin32.txt in ~/.Dropbox/linux/common back to 
    ~/.gcin/tsin32
    """
    if not are_tools_existed():
        return -1

    current = get_list_from_current_tsin32()
    cloud = get_list_from_remote( remote_filename )
    if current and cloud:
        current_set = set(current)
        cloud_set = set(cloud)
        if current_set | cloud_set:
            merged = current_set | cloud_set
            write_back_merged_tsin( merged )
        else:
            print( "Same, skip to merge." )
    else:
        print( '%s or %s is empty.' % (
                    USER_TSIN32, remote_filename ) )
    return 0

def main(arg):
    return pull_and_merge(arg[0])

if __name__ == "__main__":
    main(sys.argv[1:])
