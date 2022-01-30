import os
from dotenv import load_dotenv

dotenv_path = "../../config.env"


HOU_FULL_NAME = "hfs19.0.383"
HOU_INSTALLATION = "/opt/hfs19.0.383/"
HOU_VERSION = "hfs19.0"

if os.path.exists(dotenv_path):
    print("Exists")