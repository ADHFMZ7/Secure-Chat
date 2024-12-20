from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import PKCS1_OAEP
from aiosqlite import connect
from fastapi import APIRouter, HTTPException, Depends, Form
from dependencies import get_db
import os

#Generate KDC's private key
router = APIRouter()

def generate_kdc_private_key():
    if not os.path("kdc_private.pem"):
        KDC_private_key = RSA.generate(1024)
        kdcPrivKeyBytes = KDC_private_key.export_key(format="PEM")
        with open ("kdc_private.pem", "wb") as kdc_priv:
            kdc_priv.write(kdcPrivKeyBytes)
        
    else:
        print(f"priv key already exists")

def generate_kdc_public_key():
    if not os.path("kdc_public.pem"):
        KDC_public_key = RSA.generate(1024)
        kdcPublicBytes = KDC_public_key.export_key(format = "PEM")
        with open("kdc_public.pem", "wb") as kdc_pub:
            kdc_pub.write(kdcPublicBytes)
    else:
        print(f"pub key already exists")




@router.on_event("startup")
async def startup_event():
    """Ensure the private key and public key is available at application start up"""
    generate_kdc_private_key()
    generate_kdc_public_key()


