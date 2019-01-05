""" Key signing excercise"""
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.exceptions import InvalidSignature

def generate_keys():
    """Generates public and private key"""
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=1024,
                                           backend=default_backend())
    return private_key, private_key.public_key()

def sign(message, private):
    """Generates signature for the message from the private key"""
    return private.sign(bytes(str(message), "utf-8"),
                        padding.PSS(# salt
                            mgf=padding.MGF1(hashes.SHA256()),
                            salt_length=padding.PSS.MAX_LENGTH
                        ),
                        hashes.SHA256())

def verify(message, sig, public):
    """Verifies signature with the public key"""
    try:
        public.verify(
            sig,
            bytes(str(message), "utf-8"),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256())
        return True
    except InvalidSignature:
        return False
    except:
        print("Error executing public key verifification")
        return False

if __name__ == '__main__':
    pr, pu = generate_keys()
    print(pr)
    print(pu)
    message = "This is a secret message"
    sig = sign(message, pr)
    print(sig)
    correct = verify(message, sig, pu)
    print(correct)

    if correct:
        print("Success! Good sig")
    else:
        print ("ERROR! Signature is bad")

    # Generate an attacker's public and private keys
    pr2, pu2 = generate_keys()

    # Try to sign with the attacker's private key and pass it off as
    # another user's signature
    sig2 = sign(message, pr2)

    correct= verify(message, sig2, pu)
    if correct:
        print("ERROR! Bad signature checks out!")
    else:
        print("Success! Bad sig detected")

    # Modify the message and try to pass the original signature
    badmess = message + "Q"
    correct= verify(badmess, sig, pu)
    if correct:
        print("ERROR! Tampered message checks out!")
    else:
        print("Success! Tampering detected")
