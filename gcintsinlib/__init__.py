import os
import subprocess
import platform

python_version = platform.python_version_tuple()[0]
if python_version == "3":
    from urllib.request import Request, urlopen
    from urllib.parse import urlparse
else:
    from urllib2 import Request, urlopen
    from urlparse import urlparse

def get_application_data_folder():
    """
    Get User's "Application Data" folder in Windows.
    Reference:
     * http://stackoverflow.com/questions/626796/how-do-i-find-the-windows-common-application-data-folder-using-python
    """
    import ctypes
    from ctypes import wintypes, windll
    CSIDL_APPDATA = 26
    _SHGetFolderPath = windll.shell32.SHGetFolderPathW
    _SHGetFolderPath.argtypes = [wintypes.HWND,
                                ctypes.c_int,
                                wintypes.HANDLE,
                                wintypes.DWORD, wintypes.LPCWSTR]

    path_buf = ctypes.create_unicode_buffer(wintypes.MAX_PATH)
    result = _SHGetFolderPath(0, CSIDL_APPDATA, 0, 0, path_buf)
    return path_buf.value

system_name = platform.system()

if system_name == "Windows":
    TSD2A32 = r"C:\Program Files\gcin\bin\tsd2a32.exe"
    TSA2D32 = r"C:\Program Files\gcin\bin\tsa2d32.exe"
    home = os.path.expanduser( "~" )
    app_data_dir = get_application_data_folder()
    USER_GCIN_DIR = os.path.join( home, app_data_dir, "gcin" )
else:
    TSD2A32 = "/usr/bin/tsd2a32"
    TSA2D32 = "/usr/bin/tsa2d32"
    USER_GCIN_DIR = os.path.expanduser( "~/.gcin" )

USER_TSIN32 = os.path.join( USER_GCIN_DIR, "tsin32" )

def print_exception( e ):
    print( e )

def are_tools_existed():
    """
    Check whether the necessary tools are existed.
    """
    if not os.path.exists( TSD2A32
            ) or not os.path.exists( TSA2D32 ):
        print("You need to install gcin")
        return False
    if not os.path.exists( USER_GCIN_DIR
            ) and not os.path.exists( USER_TSIN32 ):
        print("You don't run gcin yet.")
        return False
    return True

def parse_file_and_get_list( f ):
    """
    Parse lines in file to a tuple.
    """
    r = []
    if f:
        try:
            for line in f:
                t = line.split()
                r.append( tuple(t) )
            f.close()
        except Exception as e:
            print_exception( e )
    return r

def get_list_from_current_tsin32():
    """
    Use TSDA2A32 to convert tsin32 to text file.
    Then parse the text file and get a list.
    """
    args = [ TSD2A32, USER_TSIN32, "-nousecount" ]
    f = subprocess.Popen( args, stdout=subprocess.PIPE ).stdout
    return parse_file_and_get_list( f )

def get_list_from_remote( remote_filename ):
    """
    Parse the text file in Dropbox and get a list.
    """
    r = urlparse( remote_filename )
    f = None
    if r.scheme=="":
        filename = os.path.expanduser( r.path )
        if os.path.exists( filename ):
            f = open( filename, "rb" )
        else:
            print( "%s is not found." % remote_filename )
    elif r.scheme in ["http", "ftp", "https"]:
        req = Request( r.geturl() )
        try:
            f = urlopen(req)
        except Exception as e:
            print_exception( e )
    tsin = []
    if f:
        tsin = parse_file_and_get_list( f )
    return tsin

def convert_tuple_to_string( t ):
    if python_version=="3":
        s = b''
        try:
            s = (b' '.join( t )).decode('utf-8') + '\n'
        except Exception as e:
            print_exception( e )
    else:
        s = ' '.join(t) + '\n'
    return s

def write_tsin( f, s ):
    """
    The element in s is tuple.
    Write the tuple to file.
    """
    import sys
    for t in s:
        if len(t)>=2:
            f.write( convert_tuple_to_string( t ) )
    f.close()

def write_back_merged_tsin( s ):
    """
    Write the set to a temporary file.
    Then use TSA2D32 to convert text file to tsin32
    """
    import tempfile
    f = tempfile.NamedTemporaryFile( delete=False )
    write_tsin( f, s )
    args = [ TSA2D32, f.name ]
    subprocess.call( args, cwd=USER_GCIN_DIR )
    os.unlink( f.name )

