from config_pass import MasterPasswordConfig
from Database import Connection
import os
from AES import AESEncryptor
from utils import bytes_to_string, string_to_bytes
import sys
from textwrap import dedent
import pyperclip


def input_data_from_CLI() -> dict:
    """
    Asks for user input from the CLI.
    
    Returns:
        A dictionary containing the information to be inserted.
    """
    website = input("Enter the website: ")
    URL = input("Enter the URL: ")
    email = input("Enter the email: ")
    username = input("Enter the username: ")
    password = input("Enter the password for the site: ")
    data = {
        'website': website,
        'URL': URL,
        'email': email,
        'username': username,
        'password': password
    }
    return data

def input_data(AES: AESEncryptor, DB: Connection):
    """
    Ask information from the CLI to be inserted into the database.
    
    Args:
        AES: An AESEncryptor object for encrypting the password,
        DB: A connection to the passwords database.
    """
    data = input_data_from_CLI()
    
    # Encrypt the password and convert it into string form.
    encrypted_password = AES.encrypt(data['password'])
    encrypted_password = bytes_to_string(encrypted_password)
    data['password'] = encrypted_password
    DB.insert_data_from_input(data=data)


def get_website_info(website_name: str) -> None:
    """
    Display all the information stored in the database for the website `website_name`.
    Also copies the retrieved decrypted password into the clipboard.
    
    Args:
        website_name: The name of the website. Should match exactly with the corresponding row of the database,
            else returns None.
            
    Returns:
        None.
    """
    result = DB.get_information(website_name)
    
    if result is None:
        print(f'Records of {website_name} were not found.')
        return
    
    ID, website, URL, email, username, encrypted_password = result
    answer = string_to_bytes(encrypted_password)
    actual_password = AES.decrypt(answer)
    
    print(f'\nFollowing are the records for {website_name}:')
    
    message = dedent(f"""
        ID = {ID}
        website = {website}
        URL = {URL}
        email = {email}
        username = {username}
        password = {actual_password}
    """)
    print(message)
    
    pyperclip.copy(actual_password)
    print("The password has also been copied into the clipboard.")


def display_menu() -> None:
    """
    Displays the menu for the CLI. That's it.
    """
    print(f'\n{"Choice":<10} {"Operation":<50}')
    print(f'{"1":<10} {"Insert information into database":<50}')
    print(f'{"2":<10} {"Get all details of website":<50}')
    print(f'{"3":<10} {"Exit the program.":<50}')


if __name__ == "__main__":
    # Testing if the env variable exists
    if 'MASTER_HASH' not in os.environ:
        print("Environment variable not set. Please run \'config_pass.py\' first.")
        sys.exit(254)
    
    print("The master password is required before doing anything else.\n")
    config = MasterPasswordConfig()
    authentication_status, password_received = config.authenticate()
    
    if not authentication_status:
        print("Master password does not match. Try again.")
        sys.exit(123)

    AES = AESEncryptor(password=password_received)
    DB = Connection()
    
    while True:
        display_menu()
        choice = input("\nEnter your choice: ")
        match choice:
            case "1":
                input_data(AES=AES, DB=DB)
            case "2":
                website = input("Enter the website name: ")
                get_website_info(website_name=website)
            case "3":
                print("See you again!")
                sys.exit(100)
            case _:
                print("Wrong input.")
             
