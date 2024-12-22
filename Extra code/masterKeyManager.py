from Cryptodome.PublicKey import RSA
from fastapi import APIRouter, FastAPI
import os


router = APIRouter()

#Generate KDC's private key and public key pair
def  generate_kdc_key_pair():
    if not os.path.exists("kdc_private.pem"):
        KDC_private_key = RSA.generate(1024)
        kdcPrivKeyBytes = KDC_private_key.export_key(format="PEM")
        with open ("kdc_private.pem", "wb") as kdc_priv:
            kdc_priv.write(kdcPrivKeyBytes)

        kdc_public_key = KDC_private_key.public_key()
        with open("kdc_public.pem", "wb") as public_file:
            public_file.write(kdc_public_key.export_key(format="PEM"))
        print(f"Generated new RSA key pair")
    else:
        print(f"pair already exists")


async def lifespan(app):
    print("Application startup: Generating KDC key pair if necessary")
    generate_kdc_key_pair()
    yield
    print("Application Shutdown: cleanup tasks (if any)")

app = FastAPI(lifespan=lifespan)

app.include_router(router)
