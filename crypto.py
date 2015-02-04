#!/usr/bin/env python
from math import sqrt

ALPHA_SIZE = ord('Z') - ord('A') + 1
L_A = ord('A')
L_Z = ord('Z')
CAPS_BOUND = L_Z + 1
L_a = ord('a')
L_z = ord('z')
LC_BOUND = L_z + 1

# Number: Letter dictionary {"A":1, "B":2, ..., "Z": 26}
NUM_LETTERS = {chr(n):n - (LETTER_OFFSET - 1) for n in range(L_A,CAPS_BOUND)}

def stripSpaces(message):
    """ Return message string with spaces removed. """
    return "".join([w for w in message.split()])

def rot(message, n):
    """ Rotate Caesar cipher of message by offset n. """
    encoded = ""
    for letter in message:
        lnum = ord(letter)
        if lnum in range(L_a,LC_BOUND - n) or lnum in range(L_A,CAPS_BOUND - n):
            encoded += chr(lnum + n)
        elif lnum in range(L_z - n, LC_BOUND) or lnum in range(CAPS_BOUND - n, L_Z):
            encoded += chr(lnum + n - ALPHA_SIZE)
        else:
            encoded += letter
    return encoded

def breaklines(message, rowlen):
    """ Return message broken into lines of length rowlen as list. """
    rowlen -= 1
    grid = []
    row = ""
    for char in message:
        row += char
        if len(row) == rowlen + 1:
            grid.append(row)
            row = ""
    if row:
        grid.append(row)
    return grid

def gridCW(message, rowlen):
    """ Perform a clockwise rotational encryption / decryption. """
    grid = breaklines(message, rowlen)
    rstring = ""
    for i in range(len(grid[0])):
        for j in grid[::-1]:
            if i < len(j):
                rstring += j[i]
    return rstring

def vigenere(decoded, keyword1, keyword2=""):
    """ Vigenere encryption. """
    keyABC = keyword2
    for i in range(L_A,CAPS_BOUND):
        c = chr(i)
        if c not in keyABC:
            keyABC += c
    message = ""
    key = 0
    for i in decoded:
        pos = keyABC.find(keyword1[key])
        codeABC = keyABC[pos:] + keyABC[:pos]
        lpos = keyABC.find(i)
        message += codeABC[lpos]
        key = (key + 1) % len(keyword1)
    return message

def reverseVigenere(encoded, keyword1, keyword2=""):
    """ Vigenere decryption. """
    keyABC = keyword2
    for i in range(L_A,CAPS_BOUND):
        c = chr(i)
        if c not in keyABC:
            keyABC += c
    message = ""
    key = 0
    for i in encoded:
        if i == "?":
            message += i
            continue
        pos = keyABC.find(keyword1[key])
        codeABC = keyABC[pos:] + keyABC[:pos]
        lpos = codeABC.find(i)
        message += keyABC[lpos]
        key = (key + 1) % len(keyword1)
    return message

def getFactors(n):
    """ Return list of factors of n. """
    factors = []
    for i in range(2, round(sqrt(n)) + 1):
        if n % i == 0:
            factors.append(i)
            factors.append(int(n / i))
    factors.append(n)
    return sorted(factors)

def kasiski(message):
    """ Perform Kasiski letter frequency analysis.
    Return a dictionary of bigrams as keys and a dict of frequencies as values.
    """
    message = stripSpaces(message)
    bigrams = {}
    for i in range(len(message) - 2):
        pair = message[i:i + 2]
        pos = i
        while pos != -1:
            pos = message.find(pair, pos + 1)
            if pos > 0:
                if pair in bigrams:
                    if (pos - i) not in bigrams[pair]:
                        bigrams[pair].append(pos - i)
                else:
                    bigrams[pair] = [pos - i]
    return dict(bigrams)

def stipRot(message, trans, increment=1):
    """ Perform a skip rotational cipher.
    Perform a Caesar cipher with transposition shifting by increment with each
    letter. """
    encoded = ""
    for letter in message:
        lnum = ord(letter)
        if lnum in range(L_a,LC_BOUND - trans) or lnum in range(L_A,CAPS_BOUND - trans):
            encoded += chr(lnum + trans)
        elif lnum in range(L_z - trans, LC_BOUND) or lnum in range(CAPS_BOUND - trans, L_Z):
            encoded += chr(lnum + trans - ALPHA_SIZE)
        trans = (trans + increment) % ALPHA_SIZE
    return encoded1

def euclid(a, b):
    """ Return the greatest common factor of a and b from Euclid's algorithm """
    if a < b:
        a, b = b, a
    if a % b == 0:
        return b
    return euclid(b, a % b)

def sequentialWord(word):
    """ Increment a work like a number.
    Treats an all-caps word like a base-27 number. """
    wlist = [ord(l) for l in list(word)]
    wlist[-1] += 1
    inc = False
    for i in range(1, len(wlist) + 1):
        if inc:
            inc = False
            wlist[-i] += 1
        if wlist[-i] > L_Z:
            inc = True
            wlist[-i] -= ALPHA_SIZE
    rword = "".join([chr(l) for l in wlist])
    if inc:
        rword = "A" + rword
    return rword

def createKey(phrase):
    key = ""
    for letter in stripSpaces(phrase.upper()):
        if letter not in key and ord(letter) in range(L_A,CAPS_BOUND):
            key += letter
    return key
