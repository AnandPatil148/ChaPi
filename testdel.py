import mysql.connector
import secrets
import hashlib

host = '172.27.224.1'
user = 'login'
password = 'login'

conn = mysql.connector.connect(host=host, user=user, passwd=password, database='login')
cursor = conn.cursor()


query = f"SELECT PASSWD,SALT FROM info WHERE EMAIL = 'test@test.com';"
cursor.execute(query)
result = cursor.fetchone()
storedHashOfPassword = result[0]
storedSalt = result[1]
#print(result)
print(storedHashOfPassword)
print(storedSalt)


#Hashes Password
def hash_password(passwordToHash, salt=None):
    if salt is None:
        salt = secrets.token_bytes(16)  # Generate a random 16-byte salt
    
    # Combine the password and salt, then hash
    hashed_password = hashlib.sha256(passwordToHash.encode() + salt).hexdigest()
    
    return hashed_password, salt

# Verifies password
def check_password(passwordToCheck, storedHashOfPassword, storedSalt):
    # Use the same process to hash the given password,
    # and compare it with the stored password
    generated_password = hash_password(passwordToCheck, storedSalt)[0]
    return generated_password == storedHashOfPassword

'''
OriginalPassword = 'test'

hashOfOriginal, saltOfOriginal = hash_password(OriginalPassword)

print(f'hash of Original: {hashOfOriginal}')
print(f'salt of Original: {saltOfOriginal}')
'''

print( check_password( 'test', storedHashOfPassword, storedSalt ) )

# Update the database with the new hashed password and salt
conn.commit()  # Commit the changes to the database

conn.close()
