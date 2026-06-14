import logging

logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(msg)s",datefmt="%y-%m-%d %H:%M:%S",
    level= logging.INFO,
    handlers= [logging.FileHandler("logs/app.log","a",encoding="utf-8"),
               logging.StreamHandler()
               ])

logging.getLogger("uvicorn.access").propagate=False
logging.getLogger("uvicorn.error").propagate=False


logger = logging.getLogger(__name__)


