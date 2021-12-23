import logging
import sys
import getpass



class Logger(object):
    
    LOGGER_NAME = getpass.getuser()  
    LEVEL_DEFAULT = logging.DEBUG
    
    _logger_obj = None
    
    
    @classmethod
    def logger_exists(cls):
        return cls.LOGGER_NAME in logging.Logger.manager.loggerDict.keys()
    
    
    @classmethod
    def logger_obj(cls):
        if not cls._logger_obj:
            if cls.logger_exists():
                cls._logger_obj = logging.getLogger(cls.LOGGER_NAME)
                
            else: 
                cls._logger_obj = logging.getLogger(cls.LOGGER_NAME)
                cls._logger_obj.setLevel(cls.LEVEL_DEFAULT)
                
                formatter = logging.Formatter("[%(name)s][%(levelname)s] %(message)s")
                
                handler = logging.StreamHandler(sys.stderr)
                handler.setFormatter(formatter)
                
                cls._logger_obj.addHandler(handler)
        
        return cls._logger_obj
    
    @classmethod
    def set_level(cls, level):
        lg = cls.logger_obj()
        lg.setLevel(level)
    
    
    @classmethod
    def debug(cls, msg, *args, **kwargs):
        lg = cls.logger_obj()
        lg.debug(msg, *args, **kwargs)
        
    @classmethod
    def info(cls, msg, *args, **kwargs):
        lg = cls.logger_obj()
        lg.info(msg, *args, **kwargs)
        
    @classmethod
    def warning(cls, msg, *args, **kwargs):
        lg = cls.logger_obj()
        lg.warning(msg, *args, **kwargs)
        
    @classmethod
    def error(cls, msg, *args, **kwargs):
        lg = cls.logger_obj()
        lg.error(msg, *args, **kwargs)
        
    @classmethod
    def critical(cls, msg, *args, **kwargs):
        lg = cls.logger_obj()
        lg.critical(msg, *args, **kwargs)
        
    @classmethod
    def log(cls, level, msg, *args, **kwargs):
        lg = cls.logger_obj()
        lg.log(level, msg, *args, **kwargs)
        
    @classmethod
    def exception(cls, level, msg, *args, **kwargs):
        lg = cls.logger_obj()
        lg.exception(level, msg, *args, **kwargs)
        
    @classmethod
    def write_to_file(cls, path, level=logging.WARNING):
        file_handler = logging.FileHandler(path)
        file_handler.setLevel(level)
        
        formatter = logging.Formatter("[%(asctime)s][%(levelname)s] %(message)s")
        
        file_handler.setFormatter(formatter)
        logger = cls.logger_obj()
        logger.addHandler(file_handler)
        
        
if __name__ == "__main__":
    Logger.set_level(logging.WARNING)
    
    Logger.write_to_file("/home/hernan/Desktop/test.log")
    
    Logger.debug("Debug message")
    Logger.info("Info Message")
    Logger.warning("Warning message")
    Logger.error("Error message")
    Logger.critical("Critical Message")
    Logger.log(5, "Log message")
        
        
            
    
        
    
    

        
