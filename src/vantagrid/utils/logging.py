from __future__ import annotations

import logging
from pathlib import Path

LOG_DIR = Path("~/.config/vantagrid/logs").expanduser()


def setup_logging(level: int = logging.INFO) -> logging.Logger:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger("vantagrid")
    logger.setLevel(level)
    if not logger.handlers:
        fh = logging.FileHandler(LOG_DIR / "vantagrid.log")
        fh.setFormatter(
            logging.Formatter(
                "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
            )
        )
        logger.addHandler(fh)
    return logger
