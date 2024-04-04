import re  # Import the regular expressions library for pattern matching
def check_password(password):
    # Ensure the password is at least 8 characters long
    if len(password) < 8:
        return False

    # Ensure there is at least one uppercase letter and one lowercase letter
    if not re.search("[a-z]", password) or not re.search("[A-Z]", password):
        return False

    # Ensure there is at least one digit
    if not re.search("[0-9]", password):
        return False
    # Ensure there is at least one special character
    if not re.search("[!@#$%^&*()-_=+]", password):
        return False
    return True
def password_verification(try1, try2):
    if try1 == try2:
        return True
    return False
