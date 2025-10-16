import logging

error_logger = logging.getLogger("uvicorn.error")
error_logger.setLevel(logging.ERROR)


info_logger = logging.getLogger("uvicorn.access")
info_logger.setLevel(logging.INFO)