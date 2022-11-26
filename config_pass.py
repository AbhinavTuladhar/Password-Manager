"""
Used to configure the master password.
"""

from dotenv.main import load_dotenv
import os
import dotenv
import sys
from Database import Connection
from AES import AESEncryptor
from utils import get_hash


class MasterPasswordConfig:
    
    def __init__(self):
        # Check if the hash of the master password exists.
        if 'MASTER_HASH' in os.environ:
            self.actual_hash = os.environ['MASTER_HASH']
        else:
            self.actual_hash = None
        
    def authenticate(self) -> tuple[bool, str | bool]:
        """
        Prompts the user for the master password.
        
        If the hash of this password matches with the corresponding environmental variable, returns True.
        """
        if self.actual_hash is None:
            print("No master password was found.")
            return True, ''
        else:
            entered_pass = input("Enter the master password: ")
            entered_hash = get_hash(entered_pass)
            if self.actual_hash == entered_hash:
                print("ACCESS GRANTED!")
                return True, entered_pass
            else:
                return False, False
            
    def update_master_password(self) -> tuple[str, str]:
        """
        Updates the master password if one exists.
        
        Creates a new one if it doesn't exist.
        """
        authenticated, original_master_password = self.authenticate()
        if authenticated:
            entered_pass = input("Enter the NEW master password: ")
            entered_hash = get_hash(entered_pass)
            dotenv.set_key('variables.env', 'MASTER_HASH', entered_hash, quote_mode='never')
            print('\nMaster password successfully updated!\n')
            return original_master_password, entered_pass
        else:
            print("BEGONE!")
            sys.exit(1)
            
    def update_website_passwords(self, original_password, new_password) -> None:
        """
        If the master password is updated, then decrypt and re-encrypt the passwords of the websites in the database.
        """
        DB = Connection()
        AES1 = AESEncryptor(original_password)
        AES2 = AESEncryptor(new_password) 
        DB.update_passwords(AES1, AES2)


if __name__ == "__main__":
    # Create a .env file if it doesn't exist.
    env_file = 'variables.env'
    if not os.path.exists(env_file):
        with open(env_file, 'w') as file:
            pass
    load_dotenv(env_file)
    
    config = MasterPasswordConfig()
    original_password, new_password = config.update_master_password()
    
    # Now check if the database exists. If it does, update the passwords.
    if os.path.exists('password.db'):
        config.update_website_passwords(original_password, new_password)
        print('The passwords in the database have also been updated! \n')
        