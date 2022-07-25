import os
import time
import platform
import subprocess
from datetime import datetime


# ----- Helpers -----
def get_python_path():
    python_path = subprocess.check_output("which python", shell=True).strip()
    python_path = python_path.decode('utf-8')
    return python_path

class MyLogger:
    def __init__(self, path_log):
        self.path_log = path_log
        self.pid = os.getpid()

    def log(self, message):
        now = datetime.utcnow()
        content = f"[{now.strftime('%Y-%m-%dT%H:%M:%SZ')} | PID={self.pid}] {message}\n"
        print(content[:-1])
        with open(self.path_log, 'a') as f:
            f.write(content)

# ----- /Helpers -----


# ----- Globals -----
PATH_LOG = "log-myservice.log"


if __name__ == '__main__':
    logger = MyLogger(path_log=PATH_LOG)
    logger.log("Starting service...")
    logger.log(f"Using python {platform.python_version()} at '{get_python_path()}'.")

    count = 1
    while True:
        logger.log(f"Hello world - {count}")
        count += 1
        time.sleep(1)

    logger.log("Starting Terminated.")
