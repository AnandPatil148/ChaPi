import mysql.connector
import secrets
import hashlib
import sys

'''

host = '172.27.224.1'
user = 'login'
password = 'login'

conn = mysql.connector.connect(host=host, user=user, passwd=password, database='login')
cursor = conn.cursor()

PASSWORDS = ['anand', 'anand', 'anand', 'test']
EMAILS = ['royalchiku14@gmail.com', 'anandalt148@gmail.com', 'patiljagadevi71@gmail.com', 'test@test.com']

# Hashes Password
def hash_password(password: str, salt: bytes = None):
    if salt is None:
        salt = secrets.token_bytes(16)  # Generate a random 16-byte salt
    
    # Combine the password and salt, then hash
    hashed_password = hashlib.sha256(password.encode() + salt).hexdigest()
    
    return hashed_password, salt
i = 0
while i < 4:
    PASSWORD = PASSWORDS[i]
    EMAIL = EMAILS[i]
    
    print("Original Password:", PASSWORD)
    
    # Generate new hashed password and salt   
    hashOfOriginal, saltOfOriginal = hash_password(PASSWORD)

    print(f'hash of Original: {hashOfOriginal}')
    print(f'salt of Original: {saltOfOriginal}')
    
    # Update the database with the new hashed password and salt
    update_query = f"UPDATE info SET PASSWD = '{hashOfOriginal}', SALT = %s WHERE EMAIL = '{EMAIL}';"
    cursor.execute(update_query, (saltOfOriginal,))
    conn.commit()  # Commit the changes to the database
    i += 1

conn.close()

'''


s = "yomama"
i = 2
#by = bytes(s, encoding='utf-8')
by = bytes(i)
print(by)

by2 = b"0xAE60E5BF81E6F61C13950E0A06E6F5C0"
inby2 = int.from_bytes(by2, byteorder=sys.byteorder)
print(inby2)

