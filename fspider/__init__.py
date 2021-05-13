

import pkgutil
import sys
__version__ = pkgutil.get_data(__package__, 'VERSION').decode('ascii').strip()
version_info = tuple(int(v) if v.isdigit() else v for v in __version__.split('.'))

# Check minimum required Python version
if sys.version_info < (3, 7):
    print("Scrapy %s requires Python 3.7+" % __version__)
    sys.exit(1)
