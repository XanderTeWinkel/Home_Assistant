import os
from smb.SMBConnection import SMBConnection
from dotenv import load_dotenv


# Load .env file
load_dotenv()

# SMB Configuration
SERVER_IP = os.getenv("SERVER_IP")
SHARE_NAME = os.getenv("SHARE_NAME")
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")
DOMAIN = os.getenv("DOMAIN")
CLIENT_MACHINE_NAME = os.getenv("CLIENT_MACHINE_NAME")
SERVER_NAME = os.getenv("SERVER_NAME")


def get_files_list(path='/Plex/'):
    """
    Returns a list of files in the given path of the SMB share.
    Each file is represented as a dict with name and full path.
    """
    conn = SMBConnection(USERNAME, PASSWORD, CLIENT_MACHINE_NAME, SERVER_NAME, domain=DOMAIN, use_ntlm_v2=True) # type: ignore
    if not conn.connect(SERVER_IP, 139):
        raise ConnectionError(f"Unable to connect to SMB server {SERVER_IP}")
    
    files = []
    try:
        for f in conn.listPath(SHARE_NAME, path):
            if f.filename in ('.', '..'):
                continue
            files.append({
                'name': f.filename,
                'path': f"{path}{f.filename}",
                'isDirectory': f.isDirectory
            })
    finally:
        conn.close()
    
    return files


if __name__ == "__main__":
    # Example usage
    file_list = get_files_list('/Plex/')
    for file in file_list: # type: ignore
        print(file)