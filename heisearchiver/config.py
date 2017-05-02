# Configuration for the script
import os


cwd = os.path.dirname(__file__)
ARCHIVE_PATH = os.path.join(cwd, '../archive/')
PATH_FOR_TEST_FILES = os.path.join(cwd, '../testarchive/')
BASE_URL = 'https://www.heise.de/'
# URL = 'https://www.heise.de/newsticker'
# https://www.heise.de/newsticker/archiv/?jahr=2017;woche=3
ARCHIVE_BASE_URL = 'https://www.heise.de/newsticker/archiv/'
