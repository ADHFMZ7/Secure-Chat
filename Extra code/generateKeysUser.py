from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import PKCS1_v1_5

def usrMasterKeyGenerator():
        user_master_key = RSA.generate(1024)

        masKeyBytes = user_master_key.export_key(format='PEM')

        ##here i will need to add a way to have differences between the pem file names.
        with open ("masUserpublic.pem", "wb") as mas_file:
            mas_file.write(masKeyBytes)


