"""
Everything database-related is in here!
"""
from sqlalchemy import (
    create_engine, 
    MetaData,
    select,
    update,
    Table, Column,
    Integer, String
)
import pandas as pd
from AES import AESEncryptor
from utils import string_to_bytes, bytes_to_string


class Connection:
    def __init__(self):
        self.engine = create_engine("sqlite:///password.db")
        self.connection = self.engine.connect()
        self.metadata = MetaData()
        self.create_tables()
        
    def create_tables(self) -> None:
        """
        Create the table.
        
        If the table already exists, then nothing is done.
        """
        self.websites = Table(
            'websites', self.metadata,
            Column('ID', Integer(), primary_key=True),
            Column('website', String()),
            Column('URL', String()),
            Column('email', String()),
            Column('username', String()),
            Column('password', String())
        )
        self.metadata.create_all(self.engine)
        
    def insert_data_from_input(self, data: dict) -> None:
        """
        Insert rows into the table from the dictionary `data`.
        
        Args:
            data: A dictionary containing the information to be inserted into the database.
            
        Returns:
            None.
        """
        # Empty string = NULL value.
        for key, item in data.items():
            if item == '':
                data[key] = None
        
        ins = self.websites.insert()
        self.connection.execute(ins, data)
        print("Data has successfully been inserted into the database!")
        
    def update_passwords(self, AES1: AESEncryptor, AES2: AESEncryptor) -> None:
        """
        Update the passwords in the database when the master password is updated.
        
        Args:
            AES1: The encryptor which takes the old master password.
            AES2: The encryptor which takes the updated master password.
        """    
        query = select([self.websites.c.ID, self.websites.c.password])
        proxy = self.connection.execute(query)
        results = proxy.fetchall()
        
        ID_numbers = []
        original_passwords = []
        new_passwords = []
        
        for row in results:
            ID_numbers.append(row[0])
            original_passwords.append(row[1])
            
        for ID, password in zip(ID_numbers, original_passwords):
            # Decrypt the stored password using the original master password.
            password_byte = string_to_bytes(password)
            old_decrypted_password = AES1.decrypt(password_byte)
            
            # Then encrypt the password using the new master password.
            new_encrypted_password_bytes = AES2.encrypt(old_decrypted_password)
            new_encrypted_password = bytes_to_string(new_encrypted_password_bytes)
            new_passwords.append(new_encrypted_password)
            
            query = update(self.websites).where(self.websites.c.ID == ID)
            query = query.values(
                password=new_encrypted_password
            )
            self.connection.execute(query)
        
    def get_information(self, website: str) -> tuple:
        """
        Gets login information of `website`.
        
        Args:
            website: The name of the website. Needs to be an exact match.
            
        Return:
            A tuple containing all the details of `website.`
        """
        query = select([self.websites])
        query = query.where(self.websites.c.website == website)
        proxy = self.connection.execute(query)
        row = proxy.fetchone()
        return row
