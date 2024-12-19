from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import PKCS1_OAEP
from aiosqlite import connect

async def decrypt_and_store_master_key(user_id: int, master_key: str, kdc_public_key_path: str, database_url: str):
    #Load with  KDC's 




    with open(kdc_public_key_path, "rb") as key_file:
        kdc_public_key = RSA.import_key(key_file.read())
    
    #Encrypt the master key using KDC's public key

    cipher_rsa = 