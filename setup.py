#!/usr/bin/env python
"""Modified from Terminator's setup.py."""

from distutils.core import setup
from distutils.cmd import Command
from distutils.log import warn, info, error
from distutils.errors import DistutilsFileError
import os
from gcintsinlib.version import APP_NAME, APP_VERSION

class Uninstall(Command):
  description = "Attempt an uninstall from an install --record file"

  user_options = [('manifest=', None, 'Installation record filename')]

  def initialize_options(self):
    self.manifest = None

  def finalize_options(self):
    pass

  def get_command_name(self):
    return 'uninstall'

  def run(self):
    f = None
    self.ensure_filename('manifest')
    try:
      try:
        if not self.manifest:
            raise DistutilsFileError("Pass manifest with --manifest=file")
        f = open(self.manifest)
        files = [file.strip() for file in f]
      except IOError, e:
        raise DistutilsFileError("unable to open install manifest: %s", str(e))
    finally:
      if f:
        f.close()

    for file in files:
      if os.path.isfile(file) or os.path.islink(file):
        info("removing %s" % repr(file))
        if not self.dry_run:
          try:
            os.unlink(file)
          except OSError, e:
            warn("could not delete: %s" % repr(file))
      elif not os.path.isdir(file):
        info("skipping %s" % repr(file))

    dirs = set()
    for file in reversed(sorted(files)):
      dir = os.path.dirname(file)
      if dir not in dirs and os.path.isdir(dir) and len(os.listdir(dir)) == 0:
        dirs.add(dir)
        # Only nuke empty Python library directories, else we could destroy
        # e.g. locale directories we're the only app with a .mo installed for.
        if dir.find("site-packages/") > 0:
          info("removing %s" % repr(dir))
          if not self.dry_run:
            try:
              os.rmdir(dir)
            except OSError, e:
              warn("could not remove directory: %s" % str(e))
        else:
          info("skipping empty directory %s" % repr(dir))

setup(name=APP_NAME.capitalize(),
      version=APP_VERSION,
      description='',
      author='Yan-ren Tsai',
      author_email='elleryq@gmail.com',
      url='https://github.com/elleryq/sync_gcin_tsin',
      license='GNU GPL v3',
      scripts=['push_gcin_tsin.py', 'merge_gcin_tsin_from.py'],
      data_files=[],
      packages=['gcintsinlib',],
      cmdclass={
        'uninstall': Uninstall
      },
     )

