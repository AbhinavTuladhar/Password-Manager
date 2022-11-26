"""
Implementation of the AES algorithm.
"""
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad, unpad
from Cryptodome.Protocol.KDF import PBKDF2
from dotenv.main import load_dotenv
from utils import get_hash


load_dotenv('variables.env')


class AESEncryptor:
    """
    Attrs:
        salt: The salt for performing encryption, stored in the `salt.bin` file.
        password: The string used to generate a key.
        key: The key for encryption or decryption.
    """
    
    def __init__(self, password: str = None):
        """
        A class to represent an AES encryption object.
        
        Args:
            password: A master password used to generate the key.
        """
        self.salt = self.get_salt_value()
        self.password = password
        self.key = self.generate_key()
        
    def encrypt(self, message: str) -> bytes:
        """
        Method used to encrypt `message` using the saved key.
        
        Args:
            message: The message you want to encrypt.
            
        Returns:
            The encoded message in byte form.
        """
        message = message.encode()
        cipher = AES.new(self.key, AES.MODE_CBC)
        padded_message = pad(message, AES.block_size)
        cipher_text = cipher.encrypt(padded_message)
        encrypted_data = cipher.iv + cipher_text
        return encrypted_data
    
    def decrypt(self, message: bytes) -> str:
        """
        Decrypt the ciphertext.
        
        Args:
            message: The message to be deciphered. Needs to be in byte form.
            
        Returns:
            The decrypted message in string form.
        """
        iv = message[:16]
        data_to_decrypt = message[16:]
        
        cipher = AES.new(self.key, AES.MODE_CBC, iv=iv)
        decrypted_data = unpad(cipher.decrypt(data_to_decrypt), AES.block_size)
        decrypted_data = decrypted_data.strip().decode()
        return decrypted_data
    
    def generate_key(self) -> bytes:
        """
        Generate the key for AES using the PBKDF2 algorithm.
        
        It first hashes the supplied master password.
        Then this hash is appended to the master password, and this appended value is hashed again.
        The hash of this appended value is used to generate the key.
        """
        master_hash = get_hash(self.password)
        final_hash = get_hash(self.password + master_hash)
        key = PBKDF2(final_hash, salt=self.salt, dkLen=32)
        return key
        
    def get_salt_value(self):
        with open('salt.bin', 'rb') as file:
            self.salt = file.read()
        return self.salt
