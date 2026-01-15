# auth/key_gen.py

from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from pathlib import Path


KEY_DIR = Path("keys")
PRIVATE_KEY_PATH = KEY_DIR / "private_key.pem"
PUBLIC_KEY_PATH = KEY_DIR / "public_key.pem"


def generate_key_pair():
    """
    Generate RSA private/public key pair for Tableau UAT.
    - Private key: used to sign JWTs
    - Public key: uploaded to Tableau Cloud Manager
    """

    KEY_DIR.mkdir(exist_ok=True)

    # 1. Generate private key
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )

    # 2. Derive public key
    public_key = private_key.public_key()

    # 3. Serialize private key (KEEP SECRET)
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

    # 4. Serialize public key (SAFE TO SHARE)
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    # 5. Write to files
    PRIVATE_KEY_PATH.write_bytes(private_pem)
    PUBLIC_KEY_PATH.write_bytes(public_pem)

    return {
        "private_key_path": str(PRIVATE_KEY_PATH),
        "public_key_path": str(PUBLIC_KEY_PATH),
    }


if __name__ == "__main__":
    print("🔐 Generating RSA key pair for Tableau Unified Access Tokens...\n")

    paths = generate_key_pair()

    print("✅ Keys generated successfully:")
    print(f"   🔑 Private Key: {paths['private_key_path']} (KEEP SECRET)")
    print(f"   🔓 Public Key : {paths['public_key_path']} (UPLOAD TO TABLEAU)")
