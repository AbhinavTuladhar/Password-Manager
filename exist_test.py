import os


if os.path.exists('password.db'):
    print("The file exists")
else:
    print("The file does not exist")