import logging, pathlib, sys

def setup(log_path="logs/porteiro.log"):
    pathlib.Path(log_path).parent.mkdir(exist_ok=True)
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(log_path, encoding="utf-8"),
            logging.StreamHandler(sys.stdout)          # também no console
        ]
    )
    return logging.getLogger("porteiro")
