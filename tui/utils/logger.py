from os import path

BASE_DIR = path.dirname(path.abspath(__file__))

LOGFILE_PATH = path.join(BASE_DIR, "log.txt")
ENABLE_LOGGING = False

if ENABLE_LOGGING is True:
    with open(LOGFILE_PATH, "w", encoding="utf-8") as f:
        pass

def log(*args):
    if ENABLE_LOGGING is True:
        with open(LOGFILE_PATH, "a", encoding="utf-8") as file:
            file.write(" ".join(map(str, args)) + "\n")
