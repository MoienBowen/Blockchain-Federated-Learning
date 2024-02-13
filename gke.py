from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec
import sys

def gen_bd_key_pair(k):
    if k == 128:
        curve = ec.SECP256R1()
    elif k == 256:
        curve = ec.SECP521R1()
    else:
        sys.exit(1)
    private_key = ec.generate_private_key(curve, default_backend())
    public_key = private_key.public_key()

    private_key_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    )
    public_key_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    return private_key_pem, public_key_pem

def bd_ka(private_key, peer_public_key):
    private_key = serialization.load_pem_private_key(private_key, password=None, backend=default_backend())
    peer_public_key = serialization.load_pem_public_key(peer_public_key, backend=default_backend())
    shared_key = private_key.exchange(ec.ECDH(), peer_public_key)
    return shared_key

# # 生成 5 个参与者的密钥对
# participants = []
# for i in range(5):
#     private_key, public_key = gen_bd_key_pair(128)
#     participants.append((private_key, public_key))

# # 执行密钥协商
# shared_keys = []
# for i, (private_key_i, public_key_i) in enumerate(participants):
#     shared_key_i = bd_ka(private_key_i, participants[(i+1) % 5][1])
#     shared_keys.append(shared_key_i)

# # 打印共享的密钥
# for i, shared_key_i in enumerate(shared_keys):
#     print(f"Participant {i+1}'s Shared Key:", shared_key_i.hex())

# print(bd_ka(participants[0][0], participants[1][1]).hex())
# print(bd_ka(participants[1][0], participants[0][1]).hex())


gcc ./u.c -lgmp ; ./a.out
