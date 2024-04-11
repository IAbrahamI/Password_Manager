import os
import pyotp
import qrcode
from dotenv import load_dotenv, set_key
from cryptography.fernet import Fernet

class KeyManager:
    def __init__(self):
        self.verified = False
        # Get the current directory
        self.current_directory = os.path.dirname(__file__)
        # Get the path to the files relative to the current directory
        self.env_path = os.path.join(self.current_directory, '..', 'Secrets', '.env')
        self.qrcode_path = os.path.join(self.current_directory, '..', 'Secrets', 'otp_auth.png')
        load_dotenv(dotenv_path=self.env_path)

    # Internal Class Functions
    def __get_database_key(self, username):
        load_dotenv(dotenv_path=self.env_path)
        try:
            return os.getenv(f"PWD_MANAGER_KEY_{username}")
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    def __set_database_key(self, username, key_value):
        set_key(self.env_path, f"PWD_MANAGER_KEY_{username}", key_value)

    def __get_totp_key(self, auth_user):
        load_dotenv(dotenv_path=self.env_path)
        try:
            auth_key = os.getenv(f"AUTH_KEY_{auth_user}") 
            if auth_key is not None:
                return auth_key
            else:
                print(f"The TOTP key for user {auth_user} wasn't found")
                return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
    
    def __set_totp_key(self, auth_user, auth_key):
        set_key(self.env_path, f"AUTH_KEY_{auth_user}", auth_key)

    def __generate_auth_key(self, auth_user):
        totp_secret = pyotp.random_base32()
        self.__set_totp_key(auth_user, totp_secret)

    def __generate_database_key(self, username):
        generated_key = Fernet.generate_key()
        fernet_key = generated_key.decode('utf-8')
        self.__set_database_key(username, fernet_key)

    # External Class Functions
    def generate_qrCode_for_auth(self, account_name):
        self.__generate_auth_key(account_name)
        self.__generate_database_key(account_name)
        totp_secret = self.__get_totp_key(account_name)
        if totp_secret:
            totp = pyotp.TOTP(totp_secret)
            provisioning_uri = totp.provisioning_uri(name=account_name, issuer_name='PasswordManager')
            qrcode.make(provisioning_uri).save(self.qrcode_path)

    def delete_qrCode(self):
        try:
            # Attempt to remove the file
            os.unlink(self.qrcode_path)
        except FileNotFoundError:
            # Handle the case where the file does not exist
            print("File does not exist.")
        except Exception as e:
            # Handle any other exceptions that may occur during deletion
            print("An error occurred:", e)

    def verify_auth(self, auth_user, auth_input):
        totp_secret = self.__get_totp_key(auth_user)
        if totp_secret:
            totp = pyotp.TOTP(totp_secret)
            if totp.verify(auth_input):
                self.verified = True
                return True
            else:
                self.verified = False
                return False
        else:
            #print("TOTP key not found for user:", auth_user)
            return False

    def get_verification(self):
        return self.verified
    
    def get_DB_key_for_user(self, username):
        return self.__get_database_key(username)