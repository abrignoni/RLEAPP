import time as timex
import os
import tarfile

from pathlib import Path
from scripts.ilapfuncs import *
from zipfile import ZipFile

from fnmatch import _compile_pattern
from functools import lru_cache

normcase = lru_cache(maxsize=None)(os.path.normcase)

class FileSeekerBase:
    # This is an abstract base class
    def search(self, filepattern_to_search, return_on_first_hit=False):
        '''Returns a list of paths for files/folders that matched'''
        pass

    def cleanup(self):
        '''close any open handles'''
        pass

class FileSeekerDir(FileSeekerBase):
    def __init__(self, directory):
        FileSeekerBase.__init__(self)
        self.directory = directory
        self._all_files = []
        logfunc('Building files listing...')
        self.build_files_list(directory)
        logfunc(f'File listing complete - {len(self._all_files)} files')
        self.searched = {}

    def build_files_list(self, directory):
        '''Populates all paths in directory into _all_files'''
        try:
            files_list = os.scandir(directory)
            for item in files_list:
                self._all_files.append(item.path)
                if item.is_dir(follow_symlinks=False):
                    self.build_files_list(item.path)
        except Exception as ex:
            logfunc(f'Error reading {directory} ' + str(ex))

    def search(self, filepattern, return_on_first_hit=False):
        pat = _compile_pattern( normcase(filepattern) )
        root = normcase("root/")
        if return_on_first_hit:
            for item in self._all_files:
                if pat( root + normcase(item) ) is not None:
                    self.searched[filepattern] = [item]
                    return [item]
            self.searched[filepattern] = []
            return []
        pathlist = []
        for item in self._all_files:
            if pat( root + normcase(item) ) is not None:
                pathlist.append(item)
        self.searched[filepattern] = pathlist
        return pathlist

        return pathlist

class FileSeekerTar(FileSeekerBase):
    def __init__(self, tar_file_path, data_folder):
        FileSeekerBase.__init__(self)
        self.is_gzip = tar_file_path.lower().endswith('gz')
        mode ='r:gz' if self.is_gzip else 'r'
        self.tar_file = tarfile.open(tar_file_path, mode)
        self.data_folder = data_folder
        self.searched = {}
        self.copied = set()

    def search(self, filepattern, return_on_first_hit=False):
        pathlist = []
        pat = _compile_pattern( normcase(filepattern) )
        root = normcase("root/")
        for member in self.tar_file.getmembers():
            if pat( root + normcase(member.name) ) is not None:
                clean_name = sanitize_file_path(member.name)
                full_path = os.path.join(self.data_folder, Path(clean_name))
                if member.name not in self.copied:
                    try:
                        if member.isdir():
                            os.makedirs(full_path, exist_ok=True)
                        else:
                            parent_dir = os.path.dirname(full_path)
                            if not os.path.exists(parent_dir):
                                os.makedirs(parent_dir)
                            with open(full_path, "wb") as fout:
                                fout.write(tarfile.ExFileObject(self.tar_file, member).read())
                                fout.close()
                                self.copied.add(member.name)
                            os.utime(full_path, (member.mtime, member.mtime))
                    except Exception as ex:
                        logfunc(f'Could not write file to filesystem, path was {member.name} ' + str(ex))
                pathlist.append(full_path)
        self.searched[filepattern] = pathlist
        return pathlist

    def cleanup(self):
        self.tar_file.close()

class FileSeekerZip(FileSeekerBase):
    def __init__(self, zip_file_path, data_folder):
        FileSeekerBase.__init__(self)
        self.zip_file = ZipFile(zip_file_path)
        self.name_list = self.zip_file.namelist()
        self.data_folder = data_folder
        self.searched = {}
        self.copied = set()

    def search(self, filepattern, return_on_first_hit=False):
        pathlist = []
        pat = _compile_pattern( normcase(filepattern) )
        root = normcase("root/")
        for member in self.name_list:
            if member.startswith("__MACOSX"):
                continue
            if pat( root + normcase(member) ) is not None:
                if member not in self.copied:
                    try:
                        extracted_path = self.zip_file.extract(member, path=self.data_folder) # already replaces illegal chars with _ when exporting
                        self.copied.add(member)
                        f = self.zip_file.getinfo(member)
                        date_time = f.date_time
                        date_time = timex.mktime(date_time + (0, 0, -1))
                        os.utime(extracted_path, (date_time, date_time))
                    except Exception as ex:
                        member = member.lstrip("/")
                        logfunc(f'Could not write file to filesystem, path was {member} ' + str(ex))
                if member.startswith("/"):
                    member = member[1:]
                filepath = os.path.join(self.data_folder, member)
                if is_platform_windows():
                    filepath = filepath.replace('/', '\\')
                pathlist.append(filepath)
        self.searched[filepattern] = pathlist
        return pathlist

    def cleanup(self):
        self.zip_file.close()
        