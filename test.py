from logging.config import dictConfig
import time

dictConfig ({
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "[%(levelname)s %(asctime)s %(filename)s %(process)s]:%(message)s"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "default",
        },

    },
    "root": {
        "level": "DEBUG",
        "handlers": ["console"],
    },
})
import zbToolLib as f

d = f.downloadManager.download("https://vip.123pan.cn/1813801926/code/program/zbProgram_setup.exe", f.DOWNLOAD_PATH())
while not d.isFinished():
    print(d.progress())
    time.sleep(1)
    d.cancel()
    break
print(d.result(),d.outputPath())