import random
import math
from sympy import nextprime
from decimal import *

def set_q(n):
    '''find nearest prime greater than n, field for polynomial'''
    shamir_q = nextprime(n)
    return shamir_q

def set_p(shamir_q, n = 0):
    '''find nearest prime greater than n such that p|(q-1), field for commitments'''
    s = shamir_q
    i = 2

    while True:
        p = nextprime(s)
        if (p-1) % shamir_q == 0:
            shamir_p = p
            return shamir_p
        else:
            i += 1
            s *= i

def set_g(p,q):
    a = random.randrange(1,p-1)

    shamir_g = pow(a,((p-1)//q),p)
    return shamir_g


def tncombine(shares,field_size,t=0): #Combines shares using Lagranges interpolation
    '''shares is an array of shares being combined, t is the threshold in the scheme'''

    sums = 0
    prod_arr = []

    if len(shares) < t:
        raise Exception("Shares provided less than threshold. Secret generation not possible")

    for j in range(len(shares)):

        xj,yj = shares[j][0],shares[j][1]
        prod = Decimal(1)
        for i in range(len(shares)):
            xi = shares[i][0]
            if i != j: prod *= Decimal(Decimal(xi)/(xi-xj))
        prod *= yj

        sums += Decimal(prod) % Decimal(field_size)

    return int(round(Decimal(sums),0)) % field_size


def polynom(x,coeff,field_size):
    '''Evaluates a polynomial in x with coeff being the coefficient matrix with a given x'''
    y = 0
    for i in range(len(coeff)):
        y += (x**(len(coeff)-i-1)) * coeff[i]
    return y % field_size


def coeff(t,secret,field_size):
    '''randomly generate a coefficient array for a polynomial with degree t-1 whose constant = secret'''

    coeff = []
    for i in range(t-1):
        coeff.append(random.randrange(0,field_size-1))
    coeff.append(secret)

    return coeff

def gen_shares(secret, n, t, field_size):
    '''Split secret using SSS into n shares with threshold t'''

    cfs = coeff(t,secret,field_size)

    shares = []
    for i in range(1,n+1):

        shares.append([i,polynom(i,cfs,field_size)])

    return [shares,cfs]

def commitments(t,coeff,shamir_g,shamir_p):
    '''generate t commitments'''

    check_string = []

    for i in range(t):
        check_string.append(pow(shamir_g,coeff[i],shamir_p)%shamir_p)

    return check_string

def verify_share(si,shamir_g,shamir_p,check_string):
    '''verify share si with generator = gen, shamir_p and commitments in check_string'''

    lhs = pow(shamir_g,si[1],shamir_p)

    rhs = 1
    for i in range(len(check_string)):
        rhs *= pow(check_string[len(check_string)-i-1],(si[0]**i),shamir_p)
    rhs = rhs % shamir_p
    if lhs == rhs:
        return True
    else:
        return False

def reconstruct_shamir(shares,i,shamir_g,shamir_q, t = 0): #Do we have to mention which additive share these backups belong to? i.e. need for 'i'?
    '''Verify first using VSS and then reconstruct, i is index of the additive share for shamir_p, etc'''

    res = True
    for si in shares:
        if verify_share(si,shamir_g[i],shamir_p[i],check_string[i]) == False:
            res = False
            break

    if res == False:
        print("Share:",si,"invalid")
        raise Exception("Backup Reconstruction Failed")
        return
    else:
        return (ShamirSS.tncombine(shares,shamir_q[i],t))

# def invoke_backup():
#     global share_status
#     global additive_shares
#     global sub_shares

#     for i in range(len(share_status)):
#         if not share_status[i]:
#             print("Share index:",i,"damaged")
#             print("Restore from",additive_shares[i],"to",end=" ")
#             additive_shares[i] = reconstruct_shamir(sub_shares[i],i,shamir_g,shamir_q, t=0)
#             print(additive_shares[i])

def SS_shares(secret, t, n):
    shamir_q = set_q(n)
    shamir_p = set_p(shamir_q)
    shamir_g = set_g(shamir_p,shamir_q)
    shamir_res = gen_shares(secret, n,t,shamir_q)
    shares = shamir_res[0]
    coeffs = shamir_res[1]
    check_string = commitments(t,coeffs,shamir_g,shamir_p)

    return shares, check_string,shamir_g,shamir_p, shamir_q

def debug():
    '''FOR DEBUGGING ONLY'''

    shamir_q = set_q(2 ** (128 - 1))
    shamir_p = set_p(shamir_q)
    #print(shamir_p,shamir_q)

    res = True

    for t in range(1,10):

       n = random.randrange(t,999)
       secret = random.randrange(1,999999)

       shares, check_string,shamir_g,shamir_p, shamir_q = SS_shares(secret, t, n)

       shares.append([random.randrange(1,999),random.randrange(1,999)%shamir_q])
       shares.append([random.randrange(1,999),random.randrange(1,999)%shamir_q])


       test_res = []
       for i in shares:
           if verify_share(i,shamir_g,shamir_p,check_string):
               test_res.append(True)
           else:
               test_res.append(False)

       vef_res = [True for i in range(n)]
       vef_res += [False,False]


       if test_res != vef_res:
           print(shares[-1],shares[-2])
           print(shares[shares[-1][0]-1],shares[shares[-2][0]-1])
           res = False
           break
       break
    print(res)



debug()

# https://github.com/taabishm2/Proactive-FDH-RSA-Signature/tree/69f2889d4dc580b3a958dce75ff651f8cbb7c271
