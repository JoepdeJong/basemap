from distutils.core import setup, Extension
from distutils.util import convert_path
import sys, glob

def dbf_macros():
    """Return the macros to define when compiling the dbflib wrapper.

    The returned list specifies one macro, HAVE_UPDATE_HEADER, which is
    '1' if the dbflib version we will be compiling with has the
    DBFUpdateHeader function and '0' otherwise.  To check whether
    DBFUpdateHeader is available, we scan shapefil.h for the string
    'DBFUpdateHeader'.
    """
    f = open(convert_path("pyshapelib/shapelib/shapefil.h"))
    contents = f.read()
    f.close()
    if contents.find("DBFUpdateHeader") >= 0:
        return [("HAVE_UPDATE_HEADER", "1")]
    else:
        return [("HAVE_UPDATE_HEADER", "0")]

deps = glob.glob('src/*.c')

extensions = [Extension("proj4",deps,include_dirs = ['src'],)]
packages          = ['matplotlib/toolkits','matplotlib/toolkits/basemap']
package_dirs       = {'':'lib'}

# don't build pyshapelib if it is already installed.

try:
    import shapelib
    import dbflib
except:
    packages = packages + ['shapelib','dbflib']
    package_dirs['shapelib'] ='pyshapelib/lib/shapelib'
    package_dirs['dbflib'] ='pyshapelib/lib/dbflib'
    extensions = extensions + \
             [Extension("shapelibc",
                        ["pyshapelib/shapelib_wrap.c",
                         "pyshapelib/shapelib/shpopen.c",
                         "pyshapelib/shapelib/shptree.c"],
                        include_dirs = ["pyshapelib/shapelib"]),
              Extension("shptree",
                        ["pyshapelib/shptreemodule.c"],
                        include_dirs = ["pyshapelib/shapelib"]),
              Extension("dbflibc",
                        ["pyshapelib/dbflib_wrap.c",
                         "pyshapelib/shapelib/dbfopen.c"],
                        include_dirs = ["pyshapelib/shapelib"],
                        define_macros = dbf_macros()) ]

datadir ='share/basemap-py'+repr(sys.version_info[0])+repr(sys.version_info[1])

setup(
  name              = "basemap",
  version           = "0.6.2",
  description       = "Plot data on map projections with matplotlib",
  long_description  = """
  An add-on toolkit for matplotlib that lets you plot data
  on map projections with coastlines and political boundaries.
  See http://www.scipy.org/wikis/topical_software/Maps for an
  example of what it can do.""",
  url               = "http://matplotlib.sourceforge.net/toolkits.html",
  download_url      = "http://sourceforge.net/projects/matplotlib",
  author            = "Jeff Whitaker",
  author_email      = "jeffrey.s.whitaker@noaa.gov",
  data_files        = [(datadir,['data/countries_c.txt','data/states_c.txt','data/countries_l.txt','data/states_l.txt','data/gshhs_c.txt','data/gshhs_l.txt','data/countries_i.txt','data/states_i.txt','data/gshhs_i.txt'])],
  platforms         = ["any"],
  license           = ["OSI Approved"],
  keywords          = ["python","plotting","plots","graphs","charts","GIS","mapping","map projections","maps"],
  classifiers       = ["Development Status :: 4 - Beta",
			           "Intended Audience :: Science/Research", 
			           "License :: OSI Approved", 
			           "Topic :: Scientific/Engineering :: Visualization",
			           "Topic :: Software Development :: Libraries :: Python Modules",
			           "Operating System :: OS Independent"],
  packages          = packages,
  package_dir       = package_dirs,
  ext_modules       = extensions)

from matplotlib import rcParams
if rcParams['numerix'] == 'Numeric':
    print """WARNING:
Basemap uses numarray for some functions, so to avoid 
potential problems with Numeric --> numarray conversions
it is recommended to set the value of numerix in
matplotlibrc to 'numarray'."""