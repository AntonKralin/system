#from ast import Param
from datetime import datetime, timedelta
from dataclasses import dataclass
from typing import List
import os


"""
Liblary for rotate files
autor Anton Kralin
version 1.0
"""

@dataclass
class FileType:
    """
    class for representation file in folders
    :param path: str (path to file) 
    :param filename: str (file name) 
    :param date: (date, time last edit time) datetime
    """
    path: str = ''
    filename: str = ''
    when: datetime = datetime.today()

    def __init__(self, path: str = '', filename: str = '',
                 datet: datetime = datetime.today()):
        """
        :param path: str (path to file)
        :param filename: str (file name)
        :param date: (date, time last edit time) datetime
        :return: None
        """
        self.path = path
        self.filename = filename
        self.when = datet

@dataclass
class SaveKeeping:
    """
    :param year: bool = True create year copy
    :param year_count: int = 3 count year copy for safe
    :param month: bool = True create month copy
    :param month_count: int = 12 count month copy for safe
    :param week: bool = True create week copy
    :param week_count: int = 4 count week copy for safe
    :param day: bool = True create day copy
    :param day_count: bool = 7 count day copy for safe
    :param move: bool = True true-move, false - copy
    :param del_empty_folder: bool = True delete empty folder
    """
    year: bool = True
    year_count: int = 3
    month: bool = True
    month_count: int = 12
    week: bool = True
    week_count: int = 4
    day: bool = True
    day_count: int = 7
    move: bool = True
    del_empty_folder: bool = True

class FileRotate:
    """class for 
    """
    
    def __init__(self, path_from: str, path_to: str, keep: SaveKeeping=SaveKeeping()):
        """
        :param path_from: str (path to folder where is file to rotate) path_to: str (path to folder where will be files after rotate)
        :keep: SaveKeeping() keep rule
        :return: None
        """
        self.__path_from = self._form_path(path_from)
        self.__path_to = self._form_path(path_to)
        self.__keep = keep
        self.__ignore_file = list()

    @property
    def path_from(self) -> str:
        return self.__path_from

    @path_from.setter
    def path_from(self, path_from: str):
        self.__path_from = self._form_path(path_from)
    
    @property
    def path_to(self) -> str:
        return self.__path_to    
    
    @path_to.setter
    def path_to(self, path_to: str):
        self.__path_to = self._form_path(path_to)
        
    @property
    def keep(self) -> SaveKeeping:
        return self.keep
    
    @keep.setter
    def keep(self, keep:SaveKeeping) -> None:
        self.__keep = keep
    
    def set_ignore_file(self, ignore_file: List):
        """
        set file that was ignoring
        :param List[filename: str]
        """
        self.__ignore_file = ignore_file

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
    
    def _create_dir(self, path: str):
        try:
            if not os.path.exists(path):
                os.makedirs(path)
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
        """Del empty dirs

        Args:
            path (str): path to remove empty folders
        """
        for dirs in os.listdir(path):
            dir_path = os.path.join(path, dirs)
            if os.path.isdir(dir_path):
                if not os.listdir(dir_path):
                    os.rmdir(dir_path)
                else:
                    self.del_empty_dirs(dir_path)
    
    def _create_date_path(self, date: datetime = datetime.date.today()) -> str:
        """get path to folter with date

        Args:
            date (datetime, optional): date. Defaults to datetime.date.today().

        Returns:
            str: path to folder
        """
        path = self.__path_to
        path = os.path.join(path, date.year)
        path = os.path.join(path, date.month)
        path = os.path.join(path, date.day)
        return path
    
    def get_file(self, path: str) -> FileType:
        """get object FileType of file

        Args:
            path (str): path to file

        Returns:
            FileType: object of filetype
        """
        adate = os.path.getatime(path)
        dates = timedelta(adate)
        c_path = os.path.split(path)
        file = FileType(c_path[0], c_path[1], dates)
        return file
    
    def dir_find_file(self, path: str, deep_find: int, deep: int = 0) -> List:
        """Search file in folder and return list path to files

        Args:
            path (str): path to find
            deep_find (int): max deep find file
            deep (int, optional): current deep

        Returns:
            List: array path (str) to files
        """
        if os.path.isdir(path):
            mass_files = list()
            
            for i_dir in os.listdir(path):
                new_path = os.path.join(path, i_dir)
                if os.path.isdir(new_path):
                    if deep_find > deep:
                        buf = self.dir_find_file(deep + 1, deep_find)
                        if buf:
                            mass_files.extend(buf)
                elif (deep == deep_find) and (os.path.isfile(new_path)):
                    mass_files.append(self.get_file(new_path))
                    
            return mass_files
        return None

    def del_old_file(self, deep_find):
        """dell file

        Args:
            deep_find (_type_): _description_
        """
        l_files = self.dir_find_file(self.path_to, deep_find)
        