#from ast import Param
from datetime import date, datetime, timedelta
from dataclasses import dataclass
from typing import List
import os
import shutil


#Liblary for rotate files
#autor Anton Kralin
#version 1.0


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
    :param deep_find: int = 0 Deep to find file
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
    deep_fild: int = 0

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
        return self.__keep
    
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
    
    def _create_dir(self, path: str) -> None:
        """Create folder from path

        Args:
            path (str): path to folder
        """
        try:
            if not os.path.exists(path):
                os.makedirs(path)
        except OSError:
            return "Error on create directory"
        
    def _form_path(self, path: str) -> str:
        """formation path to file(folder) and return this string

        Args:
            path (str): path to file(folder)

        Returns:
            str: 
        """
        mass_folder = list()
        if path.find('/'):
            mass_folder = path.split('/')
        else:
            mass_folder = path.split('\\')
        path = os.path.join('', *mass_folder)
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
    
    def _create_date_path(self, datet: date = date.today()) -> str:
        """get path to folter with date

        Args:
            date (datetime, optional): date. Defaults to datetime.date.today().

        Returns:
            str: path to folder
        """
        path = self.__path_to
        path = os.path.join(path, datet.year)
        path = os.path.join(path, datet.month)
        path = os.path.join(path, datet.day)
        return path
    
    def get_file(self, path: str) -> FileType:
        """get object FileType of file

        Args:
            path (str): path to file

        Returns:
            FileType: object of filetype
        """
        if os.path.exists(path):
            if os.path.isfile(path):
                #adate = os.path.getatime(path)
                adate = os.path.getmtime(path)
                dates = datetime.fromtimestamp(adate)
                c_path = os.path.split(path)
                file = FileType(c_path[0], c_path[1], dates)
                return file
            return None
        return None
    
    def dir_find_file(self, path: str, deep: int = 0) -> List:
        """Search file in folder and return list FileType

        Args:
            path (str): path to find
            deep (int, optional): current deep

        Returns:
            List: array FileType
        """
        deep_find =  self.keep.deep_fild
        if os.path.isdir(path):
            mass_files = list()

            for i_dir in os.listdir(path):
                new_path = os.path.join(path, i_dir)
                if os.path.isdir(new_path):
                    if deep_find > deep:
                        buf = self.dir_find_file(deep + 1, deep_find)
                        if buf:
                            mass_files.extend(buf)
                elif (deep <= deep_find) and (os.path.isfile(new_path)):
                    mass_files.append(self.get_file(new_path))
                    
            return mass_files
        return None

    def _check_keep_file_day(self, file: FileType) -> bool:
        """check need file to day keep

        Args:
            file (FileType): file to check

        Returns:
            bool: True - need keep, False - need delete
        """
        if self.__keep.day:
            fdate = file.when.date()
            today = date.today()
            if fdate + timedelta(days=self.__keep.day_count) < today:
                return False
            return True
        return False
    
    def _check_keep_file_week(self, file: FileType) -> bool:
        """check need file to week keep

        Args:
            file (FileType): file to check

        Returns:
            bool: True - need keep, False - need delete
        """
        if self.keep.week:
            fdate = file.when.date()
            today = date.today()
            if fdate + timedelta(weeks=self.keep.week_count) < today:
                return False
            return True
        return False
    
    def _check_keep_file_month(self, file: FileType, remove: bool = False) -> bool:
        """check need file to month keep

        Args:
            file (FileType): file to check

        Returns:
            bool: True - need keep, False - need delete
        """
        if self.keep.month:
            fdate = file.when.date()
            today = date.today()
            if fdate + timedelta(days=self.keep.month_count * 30) < today:
                return False
            save_path = os.path.join(self.path_to,
                                     str(file.when.year), str(file.when.month))
            if not os.path.exists(save_path):
                return True
            count = 0
            for i_file in os.listdir(save_path):
                #if i_file != file.filename:
                #    continue
                i_path = os.path.join(save_path, i_file)
                if os.path.isfile(i_path):
                    count += 1
                    buf_file = self.get_file(i_path)
                    if buf_file.when > file.when:
                        return False
                    else:
                        if remove:
                            os.remove(i_path)
                        return True
            if count == 0:
                return True
        return False
    
    def _check_keep_file_year(self, file: FileType, remove: bool = False) -> bool:
        """check need file to year keep and delete oldest year copy

        Args:
            file (FileType): file to check
            remove bool = False need remove old file
        Returns:
            bool: True - need keep, False - need delete
        """
        if self.keep.year:
            fdate = file.when.date()
            today = date.today()
            if fdate.year + self.keep.year < today.year:
                return False
            save_path = os.path.join(self.path_to, str(file.when.year))
            if not os.path.exists(save_path):
                return True
            count = 0
            for i_file in os.listdir(save_path):
                #if i_file != file.filename:
                #    continue
                i_path = os.path.join(save_path, i_file)
                if os.path.isfile(i_path):
                    count += 1
                    buf_file = self.get_file(i_path)
                    if buf_file.when > file.when:
                        return False
                    else:
                        if remove:
                            os.remove(i_path)
                        return True
            if count == 0:
                return True
        return False
    
    def _week_rotate(self, year: int = datetime.today().year) -> None:
        today = date.today()
        for i_path in os.listdir(os.path.join(self.path_to, year)):
            if i_path.find("week"):
                new_path = os.path.join(self.path_to, i_path)
                for i_file in os.listdir(new_path):
                    file_path = os.path.join(new_path, i_file)
                    ftype = self.get_file(file_path)
                    date_between  = today - ftype.when
                    week_befo  = date_between.day % 7
                    if not self._check_keep_file_week(ftype):
                        os.remove(file_path)
                        continue
                    save_path = os.path.join(self.path_to, ftype.when.year,
                                            "week" + week_befo)
                    self._create_dir(save_path)
                    shutil.copyfile(file_path,
                                    os.path.join(save_path, ftype.filename))
                    os.remove(file_path)
                    

    def del_old_file(self) -> None:
        """dell file in path_to
        """
        #check year copy
        for i_path in os.listdir(self.path_to):
            new_path = os.path.join(self.path_to, i_path)
            
            if os.path.isfile(new_path):
                ftype = self.get_file(new_path)
                if not self._check_keep_file_year(ftype):
                    os.remove(new_path)
            if os.path.isdir(new_path):
                #check week copy
                if i_path.find("week") != -1:
                    for i_week in os.listdir(new_path):
                        w_path = os.path.join(new_path, i_week)
                        if os.path.isfile(w_path):
                            ftype = self.get_file(w_path)
                            if not self._check_keep_file_week(ftype):
                                os.remove(w_path)
                else:
                    #check month copy
                    for i_month in os.listdir(new_path):
                        m_path = os.path.join(new_path, i_month)
                        if os.path.isfile(m_path):
                            ftype = self.get_file(m_path)
                            if not self._check_keep_file_month(ftype):
                                os.remove(m_path)
                        if os.path.isdir(m_path):
                            #check day copy
                            for i_day in os.listdir(m_path):
                                d_path = os.path.join(m_path, i_day)
                                if os.path.isfile(d_path):
                                    ftype = self.get_file(d_path)
                                    if not self._check_keep_file_day(ftype):
                                        os.remove(d_path)


    def begin_rotate(self) -> None:
        """start rotate file"""
        f_list = self.dir_find_file(self.path_from)
        today = datetime.today()
        self.del_old_file()
        for i_file in f_list:
            #day copy
            if self.keep.day and self._check_keep_file_day(i_file):
                save_path = os.path.join(self.path_to, str(i_file.when.year),
                                         str(i_file.when.month),
                                         str(i_file.when.day))
                self._create_dir(save_path)
                shutil.copy2(os.path.join(i_file.path, i_file.filename),
                                os.path.join(save_path, i_file.filename))
                if self.keep.move:
                    os.remove(os.path.join(i_file.path, i_file.filename))
            #week copy
            if self.keep.week and self._check_keep_file_week(i_file):
                date_between  = today - i_file.when
                week_befo  = date_between.days % 7
                save_path = os.path.join(self.path_to, str(i_file.when.year),
                                         "week" + str(week_befo))
                self._create_dir(save_path)
                shutil.copy2(os.path.join(i_file.path, i_file.filename),
                                os.path.join(save_path, i_file.filename))
                if self.keep.move:
                    os.remove(os.path.join(i_file.path, i_file.filename))
            #month copy
            if self.keep.month and self._check_keep_file_month(i_file):
                save_path = os.path.join(self.path_to, str(i_file.when.year),
                                         str(i_file.when.month))
                self._create_dir(save_path)
                shutil.copy2(os.path.join(i_file.path, i_file.filename),
                                os.path.join(save_path, i_file.filename))
                if self.keep.move:
                    os.remove(os.path.join(i_file.path, i_file.filename))
            #year copy
            if self._check_keep_file_year(i_file, True):
                save_path = os.path.join(self.path_to, str(i_file.when.year))
                self._create_dir(save_path)
                shutil.copy2(os.path.join(i_file.path, i_file.filename),
                                os.path.join(save_path, i_file.filename))
                if self.keep.move:
                    os.remove(os.path.join(i_file.path, i_file.filename))

        if self.keep.del_empty_folder:
            self.del_empty_dirs(self.path_from)
            self.del_empty_dirs(self.path_to)


if __name__ == '__main__':
    print('start')
    f_keep = SaveKeeping()
    f_keep.move = False
    f_keep.del_empty_folder = True
    f_keep.day_count = 61

    p_from = '/home/anton/temp/backup/'
    p_to = '/home/anton/temp/temp/'

    f_rotate = FileRotate(p_from, p_to, f_keep)
    f_rotate.begin_rotate()
