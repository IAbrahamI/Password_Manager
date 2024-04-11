from cryptography.fernet import Fernet
from Scripts.KeyManager import KeyManager
import sqlite3
import os

class PasswordManager:
    def __init__(self, user):
        keyManager = KeyManager()
        # Create a Fernet cipher instance with the key
        self.cipher_suite = Fernet(keyManager.get_DB_key_for_user(user))
        # Generates connection to database
        self.current_directory = os.path.dirname(__file__)
        db_name = f"PasswordManager_{user}.db"
        self.db_path = os.path.join(self.current_directory, '..', '_internal', db_name)
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()

    def encrypt_data(self, input):
        # Encrypting data
        bytes_literal = input.encode('utf-8')
        cipher_text = self.cipher_suite.encrypt(bytes_literal)
        return cipher_text

    def decrypt_data(self, input):
        # Decrypting data
        decrypted_text = self.cipher_suite.decrypt(input)
        decrypted_text = decrypted_text.decode('utf-8')
        return decrypted_text
        
    def store_data_into_sqlite3(self, encrypted_app_name, encrypted_username, encrypted_password):
        # Creates table to store data if doesn't exists
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS manager (id INTEGER PRIMARY KEY, app_name TEXT ,user_name TEXT, password TEXT)''')
        # Stores data into the manager table
        self.cursor.execute("INSERT INTO manager (app_name, user_name, password) VALUES (?, ?, ?)", (encrypted_app_name, encrypted_username, encrypted_password))
        self.conn.commit()

    def modify_entry_in_sqlite3(self, entry_id, entry_username, entry_password):
        encrypted_username_entry = self.encrypt_data(entry_username)
        encrypted_password_entry = self.encrypt_data(entry_password)
        values_to_be_updated = (encrypted_username_entry, encrypted_password_entry)
        query = f"UPDATE manager SET user_name = ?, password = ? WHERE id = ?"
        self.cursor.execute(query, (*values_to_be_updated, entry_id))
        self.conn.commit()

    def get_data_from_sqlite3(self, query):
        data_per_row_list = []
        self.cursor.execute(query)
        # Get data from database and store 
        for row in self.cursor.fetchall():
            entry_id = row[0]
            app_name = self.decrypt_data(row[1])
            user_name = self.decrypt_data(row[2])
            data_per_row_list.append([entry_id, app_name, user_name])
        return data_per_row_list

    def set_entries_to_be_stored(self, input_app_name, input_username, input_password):
        # Ecrypts the input data
        encrypted_app_name = self.encrypt_data(input_app_name)
        encrypted_username = self.encrypt_data(input_username)
        encrypted_password = self.encrypt_data(input_password)
        # Stores data into database
        self.store_data_into_sqlite3(encrypted_app_name,encrypted_username, encrypted_password)

    def get_all_data_from_db(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS manager (id INTEGER PRIMARY KEY, app_name TEXT ,user_name TEXT, password TEXT)''')
        query_sqlite3 = "SELECT * FROM manager"
        return self.get_data_from_sqlite3(query_sqlite3)
    
    def get_entry_by_id(self, entry_id):
        query_sqlite3 = "SELECT * FROM manager WHERE id = ?"
        self.cursor.execute(query_sqlite3, (entry_id,))
        return self.get_data_from_sqlite3(self.cursor.fetchall())
    
    def get_password_by_id(self, entry_id):
        query_sqlite3 = "SELECT password FROM manager WHERE id = ?"
        self.cursor.execute(query_sqlite3, (entry_id,))
        encrypted_pwd = self.cursor.fetchone()
        decrypted_pwd = self.decrypt_data(encrypted_pwd[0])
        return decrypted_pwd
    
    def get_all_ids(self):
        ids = []
        complet_data = self.get_all_data_from_db()
        for data in complet_data:
            ids.append(data[0])
        return ids

    def remove_entry_by_id(self, entry_id):
        query = f"DELETE FROM manager WHERE id = ?"
        self.cursor.execute(query, (entry_id,))
        self.conn.commit()