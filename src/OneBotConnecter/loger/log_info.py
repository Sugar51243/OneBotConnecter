import builtins, logging, os, sys
from datetime import datetime

def create_dir():
    try:
        main_file = sys.modules["__main__"].__file__
        path = os.path.dirname(os.path.abspath(main_file))
    except (AttributeError, KeyError):
        path = os.path.dirname(os.path.abspath(__file__))
    if getattr(sys, 'frozen', False):
        path = os.path.dirname(os.path.abspath(sys.argv[0]))
    path = os.path.join(path, "logs")
    if not os.path.exists(path):
        os.makedirs(path)
    return path

path = create_dir()
filename = datetime.today().strftime('%Y_%m_%d %H_%M_%S')
file_path = os.path.join(path, f"{filename}.log")
print(f"日志将储存至: {file_path}")

logging.basicConfig(
    filename=file_path,
    filemode="a", # append mode
    encoding="utf-8",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def print(text: str):
    create_dir()
    builtins.print(text)
    logging.info(text)

def log(text: str):
    create_dir()
    logging.info(text)

def error(text: str):
    create_dir()
    logging.error(text)
    builtins.print(f"ERROR: {text}")

def warning(text: str):
    create_dir()
    logging.warning(text)

def debug(text: str):
    create_dir()
    logging.debug(text)