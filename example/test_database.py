import os
from heydocker.database import Database

database = Database(os.path.expanduser("~/.heydocker/heydocker.db"))

print(database.get())