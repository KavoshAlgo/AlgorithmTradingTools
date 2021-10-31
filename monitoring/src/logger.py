import logging
from colorlog import ColoredFormatter
from datetime import datetime
from playsound import playsound
from _utils.utils import *


class Logger:

    def __init__(self, main, file_name,
                 format="%(white)s%(asctime)s - %(log_color)s%(levelname)s - %(log_color)s%(message)s",
                 dateformat="%I:%M:%S %p", info_audio="Info1", critical_audio="Critical1"):
        self.file_name = file_name
        logging.addLevelName(60, "SUCCESS")
        logging.addLevelName(70, "REPORT")
        self.logger = logging.getLogger()
        self.logger.propagate = False
        self.logger.setLevel(logging.INFO)
        self.ch = logging.StreamHandler()
        self.ch.setLevel(logging.DEBUG)
        self.formatter = logging.Formatter(format, dateformat)
        self.ch.setFormatter(ColoredFormatter(format, dateformat, log_colors={'DEBUG': 'white',
                                                                              'INFO': 'blue',
                                                                              'WARNING': 'yellow',
                                                                              'ERROR': 'red',
                                                                              'CRITICAL': 'black,bg_red',
                                                                              'SUCCESS': 'green',
                                                                              'REPORT': "purple"
                                                                              }))
        self.info_audio_path = root_path("_utils/Alarms/%s.mp3" % info_audio)
        self.critical_audio_path = root_path("_utils/Alarms/%s.mp3" % critical_audio)
        if main:
            self.logger.addHandler(self.ch)

    def _write_log(self, level, msg):
        pass
        # with open(root_path(self.file_name), "a", encoding='utf-8') as log_file:
        #     log_file.write("[{0}] {1} {2}\n".format(level, datetime.now().strftime("%H:%M:%S"), msg))

    def critical(self, msg):
        playsound(self.critical_audio_path)
        self.logger.critical(msg)
        self._write_log("CRITICAL", msg)

    def error(self, msg):
        self.logger.error(msg)
        self._write_log("ERROR", msg)

    def info(self, msg, sound=False):
        if sound is True:
            playsound(self.info_audio_path)
        self.logger.info(msg)
        self._write_log("INFO", msg)

    def warning(self, msg):
        self.logger.warn(msg)
        self._write_log("WARNING", msg)

    def debug(self, msg):
        self.logger.debug(msg)
        self._write_log("DEBUG", msg)

    def success(self, msg):
        self.logger.log(60, msg)
        self._write_log("SUCCESS", msg)

    def report(self, msg):
        self.logger.log(70, msg)
        self._write_log("REPORT", msg)

    def start(self):
        with open(self.file_name, "a") as log_file:
            log_file.write(datetime.now().strftime("%H:%M:%S") + "===================START===================\n")
