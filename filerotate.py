from ast import Param
from datetime import date, datetime, timedelta
from typing import List, Tuple
import os


"""
Liblary for rotate files
autor Anton Kralin
version 1.0
"""

class FileType:
    def __init(self, path: str = '', filename: str = '', date: datetime = datetime.today()):
        """
        :param path: str (path to file) filename: str (file name) date: (date, time last edit time) datetime
        :return: None
        """
        self.__path = path
        self.__filename = filename
        self.__date = date
    
    @property
    def path(self) -> str:
        return self.__path
    
    @path.setter
    def path(self, path: str):
        self.__path = path
        
    @property
    def filename(self) -> str:
        return self.__filename
    
    @filename.setter
    def filename(self, filename: str):
        self.__filename = filename
        
    @property    
    def date(self) -> datetime:
        return self.__date
    
    @date.setter
    def date(self, date: datetime):
        self.__date = date


class FileRotate:
    def __init__(self, path_from: str, path_to: str, keep_day: int = 7, del_empty_folder: bool = True, move: bool = True):
        """
        :param path_from: str (path to folder where is file to rotate) path_to: str (path to folder where will be files after rotate)
            keep_day: int=7 (how day keep in rotate folder) del_empty_folder: bool=True (delete empty folder after delete files)
            move: bool=True (move file if True, Copy file if False from path where is file to rotate)
        :return: None
        """
        self.__path_from = self.form_path(path_from)
        self.__path_to = self.form_path(path_to)   
        self.__keep_day = keep_day
        self.__del_empty_folder = del_empty_folder
        self.__move = move
        
        self.__year = False
        self.__year_count = 0
        
        self.__month = False
        self.__month_count = 0
        
        self.__week = False
        self.__week_count = 0
        
        self.__ignore_file = list()

    @property
    def path_from(self) -> str:
        return self.__path_from

    @path_from.setter    
    def path_from(self, path_from: str):
        self.__path_from = self.form_path(path_from)
    
    @property
    def path_to(self) -> str:
        return self.__path_to    
    
    @path_to.setter
    def path_to(self, path_to: str):
        self.__path_to = self.form_path(path_to)
        
    @property    
    def keep_day(self) -> int:
        return self.__keep_day
    
    @keep_day.setter
    def set_keep_day(self, keep_day: int):
        self.__keep_day = keep_day

    @property    
    def del_empty_folder(self) -> bool:
        return self.__del_empty_folder
    
    @del_empty_folder.setter
    def del_empty_folder(self, del_empty_folder: bool):
        self.__del_empty_folder = del_empty_folder
        
    def get_year(self) -> Tuple[bool, int]:
        """
        get year settings
        :return Tuple(bool, int)
        """
        return self.__year, self.__year_count
    
    def set_year(self, year: bool = True, year_count: int = 10):
        """
        set year settings 
        :param year: bool, year_count: int
        """
        self.__year = year
        self.__year_count = year_count
  
    def set_month(self, month: bool = True, month_count: int = 12):
        """
        set month settings
        :param month: bool, month_count: int
        """
        self.__month = month
        self.__month_count = month_count
        
    def get_month(self) -> Tuple[bool, int]:
        """
        get month settings
        :return Tuple(bool, int)
        """
        return self.__month, self.__month_count
    
    def set_week(self, week: bool = True, week_count: int = 5):
        """
        set week settings
        :param week: bool, week_count: int
        """
        self.__week = week
        self.__week_count = week_count
    
    def get_week(self) -> Tuple[bool, int]:
        """
        get week settings
        :return Tuple(bool, int)
        """
        return self.__week, self.__week_count
    
    def set_ignore_file(self, ignore_file: List):
        """
        set file that was ignoring
        :param List[filename: str]
        """
        self.__ignore_file

    def append_ignore_file(self, filename: str):
        """
        append filename to ignore file list
        :param filename: str
        """
        self.__ignore_file.append(filename)
        
    def get_ignore_file(self) -> List:
        """
        return list of ignore files
        :return List
        """
        return self.__ignore_file
    
    @property
    def move(self) -> bool:
        return self.__move

    @move.setter
    def set_move(self, move: bool):
        self.__move = move
           
    
    def _create_dir(self, path: str):
        try:
            if not os.path.exist(path):
                os.path.makedirs(path)
        except OSError:
            return "Error on create directory"
        
    def _form_path(self, path: str):
        mass_folder = list()
        if path.find('/'):
            mass_folder = path.split('/')
        else:
            mass_folder = path.split('\\')
        path = os.path.join(mass_folder)
        path = os.path.abspath(path)
        return path
        
    def del_empty_dirs(self, path: str):
        for dir in os.listdir(self.__path_to):
            dir_path = os.path.join(path, dir)
            if os.path.isdir(dir_path):
                if not os.path.listdir(dir_path):
                    os.rmdir(dir_path)
                else:
                    self.del_empty_dirs(dir_path)
    
    def create_date_path(self, date: datetime = datetime.date.today()) -> str:
        path = self.__path_to
        path = os.path.join(path, date.year)
        path = os.path.join(path, date.month)
        path = os.path.join(path, date.day)
        return path
    
    def get_file(self, path: str) -> FileType:
        adate = os.path.getatime(path)
        date = timedelta(adate)
        c_path = os.path.split(path)
        file = FileType(c_path[0], c_path[1], date)
        return file
    
    def dir_find_file(self, path: str, deep_find: int, deep: int = 0) -> List:
        if os.path.isdir(path):
            mass_files = list()
            
            for i_dir in os.listdir(path):
                new_path = os.join(path, i_dir)
                if os.path.isdir(new_path):
                    if deep_find > deep:
                        buf = self.dir_find_file(deep + 1, deep_find)
                        if buf:
                            mass_files.extend(buf)
                elif (deep == deep_find) and (os.path.isfile(new_path)):
                    mass_files.append(self.get_file(new_path))
                    
            return mass_files

    def del_old_file(self, deep_find):
        l_files = self.dir_find_file(deep_find)
        