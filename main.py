from gke import *
import random
from beaver import *
from shamir import *
from aes import *
from util import *
import numpy as np

# Global parameters

k = 128             # security parameter
n = 10              # number of clients
m = n // 3          # number of malicious clients
t = m + 1           # threshold
d = 5               # dimention of update vector
c_star = []         # list of malicious clients
c_flag = dict()     # list of reporting of each client
for i in range (n):
  c_flag[i] = []    
field_size = 2**128
prime_modulus = gen_prime_2(k)
precision = 5

##########
# Setup
##########

key_pair = dict() # key pairs of each client
for i in range(n):
  pri_key, pub_key = gen_bd_key_pair(k)
  key_pair[i] = [pri_key, pub_key]

# access the private key or public key of client i with
# key_pair[i][0] or key_pair[i][1]

common_key = dict() # common key between two clients
hash_common_key = dict() # hash value of common key (not same because of i||j)
for i in range(n):
  common_key[i] = []
  hash_common_key[i] = []
  for j in range(n):
    if i == j:
      common_key[i].append(None)
      hash_common_key.append(None)
    else:
      i_j_key = bd_ka(key_pair[i][0], key_pair[j][1])
      common_key[i].append(i_j_key)
      key_string = i_j_key.hex() + "||" + str(i) + "||" + str(j)
      hash_common_key[i].append(hash_(key_string))

# access the common key betwwen client i and j with
# common_key[i][j] or common_key[j][i]

# to compare the hash of common key as client i with
# key_string = i_j_key.hex() + "||" + str(j) + "||" + str(i)
# if (hash_common_key[j][i] == hash_(key_string))

##########
# Round 1
##########

# generate update for each client
local_update = dict()
for i in range(n):
  local_update[i] = np.random.rand(d)

##########
# Round 2
##########

proof = dict()
share_of_update = dict()
share_of_proof_h = dict()
share_of_proof_a = dict()
share_of_proof_b = dict()
share_of_proof_c = dict()
enc_share_u_pi = dict()

for i in range(n):
  # generate the proof
  proof[i] = create_proof(local_update[i], field_size, precision)
  # generate share of update
  share_of_update[i] = generate_shamir_shares(local_update[i], t, n, prime_modulus, precision)
  # generate share of proof
  share_of_proof_h[i] = generate_shamir_shares(proof[i][0], t, n, prime_modulus, precision)
  share_of_proof_a[i] = generate_shamir_shares(proof[i][1][0], t, n - 1, prime_modulus, precision)
  share_of_proof_b[i] = generate_shamir_shares(proof[i][1][1], t, n - 1, prime_modulus, precision)
  share_of_proof_c[i] = generate_shamir_shares(proof[i][1][2], t, n - 1, prime_modulus, precision)
  # Encrypt the share of u and pi
  for j in range(n):
    if i == j:
      enc_share_u_pi[i] = [j, None]
    else:
      if j < i:
        str_wait_for_enc = str(share_of_update[i][j]) + '||' + str(share_of_proof_h[i][j]) + '||'  + str(share_of_proof_a[i][j]) + '||'  + str(share_of_proof_b[i][j]) + '||' + str(share_of_proof_c[i][j])
      else: 
        str_wait_for_enc = str(share_of_update[i][j]) + '||' + str(share_of_proof_h[i][j - 1]) + '||'  + str(share_of_proof_a[i][j - 1]) + '||'  + str(share_of_proof_b[i][j - 1]) + '||' + str(share_of_proof_c[i][j - 1])
    enc_share_u_pi[i] = [j, encrypt_aes(common_key[i][j], str_wait_for_enc)]

##########
# Round 3
##########

dec_share = dict()

for i in range(n):
  dec_share[i] = []
  for j in range(n):
    if i == j:
      dec_share[i].append([j, None])
    else:
      dec_share[i].append([j, decrypt_aes(common_key[i][j], enc_share_u_pi[j][i])])


##########
# Round 4
##########

