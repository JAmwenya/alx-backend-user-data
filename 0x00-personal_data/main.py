from encrypt_password import hash_password, is_valid

password = "MyAmazingPassw0rd"
hashed_password = hash_password(password)
print(hashed_password)
print(is_valid(hashed_password, password))
print(is_valid(hashed_password, "WrongPassword"))
