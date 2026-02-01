import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def verify_password(stored_hash, entered_password):
    return stored_hash == hash_password(entered_password)

def hash_password(password): 
    # Convert password to bytes
    password_bytes = password.encode('utf-8')
    # Create SHA-256 hash
    hashed = hashlib.sha256(password_bytes).hexdigest()
    return hashed

def verify_password(stored_hash, entered_password):
    # Hash the entered password
    entered_hash = hash_password(entered_password)
    # Compare hashes
    return stored_hash == entered_hash

    # # --- Main Program ---
    # # User registration
    # password = input("Create a password: ") stored_hash = hash_password(password) print("\nPassword stored (hashed):", stored_hash) 
    # # User login login_password = input("\nEnter password to login: ") if verify_password(stored_hash, login_password): print("Login successful ✅") else: print("Wrong password ❌")