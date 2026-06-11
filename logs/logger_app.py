import logging

logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(msg)s",datefmt="%y-%m-%d %H:%M:%S",
    level= logging.INFO,
    handlers= [logging.FileHandler("logs/app.log","a",encoding="utf-8"),
               logging.StreamHandler()
               ])


logger = logging.getLogger(__name__)


