import os
from typing import Final
from dotenv import load_dotenv

load_dotenv()
TOKEN: Final = os.getenv('TOKEN') or ""
BOT_USERNAME: Final = os.getenv('USERNAME') or ""
