import secrets
import string

class PasswordGenerator:
    def __init__(self):
        self.lower_case_letters = string.ascii_lowercase
        self.upper_case_letters = string.ascii_uppercase
        self.digits = string.digits
        self.punctuations = "$/%*#@+-!"

    # Generates Password
    def generate_password(self, length, input_UpperCase, input_Digits, input_Punctuation):
        # Define characters for the generation
        allowsUpperCase = self.convert_input_to_bool(input_UpperCase)
        allowsDigits = self.convert_input_to_bool(input_Digits)
        allowsPunctuation = self.convert_input_to_bool(input_Punctuation)
        # Base characters definition
        characters = self.lower_case_letters
        # Add characters if allowed
        if allowsUpperCase == True:
            characters += self.upper_case_letters
        if allowsDigits == True:
            characters += self.digits
        if allowsPunctuation == True:
            characters += self.punctuations
        # Generates Password
        password = ''.join(secrets.choice(characters) for _ in range(length))
        if allowsPunctuation == True and not self.contains_punctuation(password):
            password = self.generate_password(length, allowsUpperCase, allowsDigits, allowsPunctuation)
        if allowsDigits == True and not self.contains_numbers(password):
            password = self.generate_password(length, allowsUpperCase, allowsDigits, allowsPunctuation)
        if allowsUpperCase == True and not self.contains_uppercase(password):
            password = self.generate_password(length, allowsUpperCase, allowsDigits, allowsPunctuation)
        return password

    # Check if generated password contains selected characters to be added into it
    def contains_punctuation(self, password):
        return any(char in self.punctuations for char in password)
    
    def contains_numbers(self, password):
        return any(char in self.digits for char in password)
    
    def contains_uppercase(self, password):
        return any(char in self.upper_case_letters for char in password)
    
    def convert_input_to_bool(self, input_value):
        if input_value == 1:
            return True
        elif input_value == 0:
            return False