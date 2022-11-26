"""
For generating passwords.
"""
import secrets
import string
import pyperclip


symbols = string.ascii_letters + string.digits + """!@#$%^&*()-+=[]{};:|<>,.?/"""


def generate_password(length=20):
    password = ''.join(secrets.choice(symbols) for _ in range(length))  # for a 20-character password
    print(password)
    pyperclip.copy(password)
    print('The password has been copied into the clipboard!')

   
if __name__ == "__main__":
    password_length = int(input("Enter the length of the password: "))
    generate_password(length=password_length)
