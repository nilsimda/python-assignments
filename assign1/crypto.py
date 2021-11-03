#!/usr/bin/env python3 -tt
"""
File: crypto.py
---------------
Assignment 1: Cryptography
Course: CS 41
Name: <YOUR NAME>
SUNet: <SUNet ID>

Replace this with a description of the program.
"""
import utils
import random
import math

# Caesar Cipher

def encrypt_caesar(plaintext):
    """Encrypt plaintext using a Caesar cipher.

    Add more implementation details here.
    """
    res = ""
    for c in plaintext:
        if c.isalpha():
            c = chr(65 + ((ord(c) - 65 + 3) % 26))
        res += c
    return res

def decrypt_caesar(ciphertext):
    """Decrypt a ciphertext using a Caesar cipher.

    Add more implementation details here.
    """
    res = ""
    for c in ciphertext:
        if c.isalpha():
            c = chr(65 + ((ord(c) - 65 - 3) % 26))
        res += c
    return res 

# Vigenere Cipher

def encrypt_vigenere(plaintext, keyword):
    """Encrypt plaintext using a Vigenere cipher with a keyword.

    Add more implementation details here.
    """
    cypher = ""
    wrap = len(keyword)
    for index, c in enumerate(plaintext):
        offset = keyword[index % wrap]
        mid = ord(c) + ord(offset) - 130
        c = chr(65 + (mid % 26))
        cypher += c
    return cypher 

def decrypt_vigenere(ciphertext, keyword):
    """Decrypt ciphertext using a Vigenere cipher with a keyword.

    Add more implementation details here.
    """
    res = ""
    wrap = len(keyword)
    for index, c in enumerate(ciphertext):
        off_set = keyword[index % wrap]
        c = chr(65 + ((ord(c) - ord(off_set)) % 26))
        res += c
    return res


# Merkle-Hellman Knapsack Cryptosystem

def generate_private_key(n=8):
    """Generate a private key for use in the Merkle-Hellman Knapsack Cryptosystem.

    Following the instructions in the handout, construct the private key components
    of the MH Cryptosystem. This consistutes 3 tasks:

    1. Build a superincreasing sequence `w` of length n
        (Note: you can check if a sequence is superincreasing with `utils.is_superincreasing(seq)`)
    2. Choose some integer `q` greater than the sum of all elements in `w`
    3. Discover an integer `r` between 2 and q that is coprime to `q` (you can use utils.coprime)

    You'll need to use the random module for this function, which has been imported already

    Somehow, you'll have to return all of these values out of this function! Can we do that in Python?!

    @param n bitsize of message to send (default 8)
    @type n int

    @return 3-tuple `(w, q, r)`, with `w` a n-tuple, and q and r ints.
    """
    w = []
    for i in range(n):
        total = sum(w)
        w.append(random.randint(total+1, 2*total+10))

    q = random.randint(sum(w)+1, 2*sum(w))

    r = 0 #zero is not coprime with any number
    while math.gcd(r,q) != 1:
        r = random.randint(2, q-1)
    
    return (tuple(w), q, r)


def create_public_key(private_key):
    """Create a public key corresponding to the given private key.

    To accomplish this, you only need to build and return `beta` as described in the handout.

        beta = (b_1, b_2, ..., b_n) where b_i = r × w_i mod q

    Hint: this can be written in one line using a list comprehension

    @param private_key The private key
    @type private_key 3-tuple `(w, q, r)`, with `w` a n-tuple, and q and r ints.

    @return n-tuple public key
    """
    w, q, r = private_key #can easily be rewritten to one line, but is more readable this way
    return tuple([r*w_i % q for w_i in w])

def encrypt_mh(message, public_key):
    """Encrypt an outgoing message using a public key.

    1. Separate the message into chunks the size of the public key (in our case, fixed at 8)
    2. For each byte, determine the 8 bits (the `a_i`s) using `utils.byte_to_bits`
    3. Encrypt the 8 message bits by computing
         c = sum of a_i * b_i for i = 1 to n
    4. Return a list of the encrypted ciphertexts for each chunk in the message

    Hint: think about using `zip` at some point

    @param message The message to be encrypted
    @type message bytes
    @param public_key The public key of the desired recipient
    @type public_key n-tuple of ints

    @return list of ints representing encrypted bytes
    """
    cypher = [] 
    for c in message:
        a = utils.byte_to_bits(c)
        cypher.append(sum([a_i + b_i for a_i, b_i in zip(a, public_key)]))

    return cypher

def decrypt_mh(message, private_key):
    """Decrypt an incoming message using a private key

    1. Extract w, q, and r from the private key
    2. Compute s, the modular inverse of r mod q, using the
        Extended Euclidean algorithm (implemented at `utils.modinv(r, q)`)
    3. For each byte-sized chunk, compute
         c' = cs (mod q)
    4. Solve the superincreasing subset sum using c' and w to recover the original byte
    5. Reconsitite the encrypted bytes to get the original message back

    @param message Encrypted message chunks
    @type message list of ints
    @param private_key The private key of the recipient
    @type private_key 3-tuple of w, q, and r

    @return bytearray or str of decrypted characters
    """
    w, q, r = private_key
    s = utils.modinv(r, q)
    w_length = len(w)
    indices = []
    plain = []
    
    for c in message:
        c_prime = c*s %q
        for i in range(w_length-1, -1, -1):
            if w[i] <= c_prime:
                indices.append(i+1) 
                c_prime -= w[i]
        plain.append(sum([2**(w_length-j) for j in indices]))
        indices = []

    return [chr(x) for x in plain]

def main():
    pr_k = generate_private_key() 
    pub_k = create_public_key(pr_k)
    s = "HELLO"
    to_encrypt = [ord(c) for c in s]
    cipher = encrypt_mh(to_encrypt, pub_k)
    print(f"Cipher: {cipher}")
    decipher = decrypt_mh(cipher, pr_k)
    print(f"Deciphered: {decipher}")


if __name__ == "__main__":
    main()






