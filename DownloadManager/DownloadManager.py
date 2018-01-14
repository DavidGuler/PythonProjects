"""
Name: DownloadManager

Purpose: 
    A manager which process all the downloads and moves them to the correct folder.
    The manager selects the process and the destination depends on the type of the file.

    The Workflow:
                                                            SLEEP       --->    EXIT
                                                          /        ^               ^
                                                         v         \             |        
                  START -> INIT -> LIST_DOWNLOADS_FOLDER -> NO_DOWNLOADS       |
                              v                             \                   |
                      READ_CONFIG -> INIT_CONFIG             ->  [For each download:] HANDLE_DOWNLOADS
                                                                  IDENTIFY  <-,
                                                                  ACTION    <-'  --> In case of archive.
-                                                                  RELOCATE  
                                                                  CLEAN

    TODO:
        1. Generic utils class - Create a utils class which implements 4 unique functions for each category:
            1. identify
            2. action
            3. relocate
            4. clean
            Should I create a generic 
"""
#------ Imports
import json
import os
import magic
import logging
#from downloads_plugins import get_download_plugin

#------ Constants
BASE_DIR = r""
CONFIG_FILE = r""

YES = "Y"
NO = "n"
EXPECTED_ANSWERS = [YES, NO]

def set_attributes(obj, attributes):
    """
    """
    for attribute, value in attributes.items():
            if type(value) is not dict:
                setattr(obj, attribute, value)
            else:
                new_obj = type(attribute, (object,), {})
                setattr(obj, attribute, new_obj)
                set_attributes(new_obj, value)

#------ Classes:
class States():
    START = 0
    INIT = 1
    READ_CONFIG = 2
    INIT_CONFIG = 1
    LIST_DOWNLOADS_FOLDER = 3
    HANDLE_DOWNLOADS = 4
    IDENTIFY = 5
    ACTION = 6
    RELOCATE = 7
    CLEAN = 8
    NO_DOWNLOADS = 9
    SLEEP = 10
    EXIT = 11


class Configuration(object):
    """
    """

    def __init__(self, config_dict):
        set_attributes(self, config_dict)


class DownloadManager(object):
    """
    """

    def __init__(self, verbose=False):
        self.verbose = verbose

        self.state = States.START

        # Tests if the BASE_DIR exists.
        if not os.path.exists(BASE_DIR):
            raise PathDoesNotExist(BASE_DIR) # TODO: create exception class

        # Tests if the __config_path exists.
        self.__config_path = os.path.join(BASE_DIR, CONFIG_FILE)
        if not os.path.exists(self.__config_path):
            raise PathDoesNotExist(self.__config_path)

        self.__read_config()
        self.__init_config()
    
    def __read_config(self):
        self.state = States.READ_CONFIG

        # Reads the configuration.
        self.config = Configuration(json.load(config_path))

        # Tests if the downloads_folder exists.
        if not os.path.exists(self.config.downloads_folder):
            raise PathDoesNotExist(self.config.downloads_folder)

        # Tests if the target_root_folder exists.
        if not os.path.exists(self.config.target_root_folder):
            raise PathDoesNotExist(self.config.target_root_folder)

    def __init_config(self):
        self.state = States.INIT_CONFIG
        self.working_dir = os.path.join(self.config.downloads_folder, self.config.working_dir)
        os.mkdir(self.working_dir)

    def get_downloads(self):
        self.state = States.LIST_DOWNLOADS_FOLDER
        self.downloads = [os.path.join(self.config.downloads_folder, downloads) \
                            for downloads in os.listdir(self.config.downloads_folder)]

        if not self.downloads:
            self.state = States.NO_DOWNLOADS

    def handle_downloads(self):
        """
        """

        self.state = States.HANDLE_DOWNLOADS
        identify_files = magic.Magic(mime=True)

        for download in self.downloads:
            self.state = States.IDENTIFY

            file_type = identify_files.from_file(download)

            print("Found {0}, type {1}".format(download, file_type))

            download_plugin = get_download_plugin(file_type)

            download_plugin.action(download)
            download_plugin.relocate(download)
            download_plugin.clean(download)

    def exit():
        # TODO: Add closing class
        exit()

    def __update_config(self):
        # TODO
        pass


#------ Functions
def prompt_the_user(prompt):
    """
    """

    answer = input(FULL_PROMPT.format(prompt))

    if answer not in EXPECTED_ANSWERS:
        return NO

    return answer

#------ Main
def main():

    # Starting the manager by initializing the manager.
    download_manager = DownloadManager()

    # Main workflow, By steps.
    while not download_manager.state != states.EXIT:

        # Get all downloads.
        download_manager.get_downloads()

        # If there are no downloads, sleep until next check.
        if download_manager.state == States.NO_DOWNLOADS:
            time.sleep(download_manager.config.sleep_length)

        # Organize the downloads.
        download_manager.handle_downloads()

    download_manager.exit()

if __name__ == "__main__":
    main()
