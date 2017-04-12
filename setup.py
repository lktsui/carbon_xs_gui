from distutils.core import setup
import py2exe
import matplotlib
setup(
    windows = [{"script":"CarbonXS_GUI.py",}],
    data_files = matplotlib.get_py2exe_datafiles(),
    options = {'py2exe':{
        "includes" : ["matplotlib.backends.backend_tkagg",
                      ],
        "packages": ['FileDialog'],
        'excludes':["wx",'email', 'IPython', 'requests', 'tornado', 'jinja2', 'setuptools',
                    'jupyter_client', 'ipykernel', 'jupyter_core', 'sqlite3', 'pygments',
                    'curses', 'future',

                    ],
        'bundle_files':2} # Unbreaks the music
        }
    )