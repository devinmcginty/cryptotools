#!/usr/bin/env python
from math import sqrt

# Number: Letter dictionary {"A":1, "B":2, ..., "Z": 26}
NUM_LETTERS = {chr(n):n - 64 for n in range(65,91)}

def stripSpaces(message):
    """ Return message string with spaces removed. """
    return "".join([w for w in message.split()])

def rot(message, n):
    """ Rotate Caesar cipher of message by offset n. """
    encoded = ""
    for letter in message:
        lnum = ord(letter)
        if lnum in range(97,123 - n) or lnum in range(65,91 - n):
            encoded += chr(lnum + n)
        elif lnum in range(122 - n, 123) or lnum in range(91 - n, 90):
            encoded += chr(lnum + n - 26)
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
    for i in range(65,91):
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
    for i in range(65,91):
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
        if lnum in range(97,123 - trans) or lnum in range(65,91 - trans):
            encoded += chr(lnum + trans)
        elif lnum in range(122 - trans, 123) or lnum in range(91 - trans, 90):
            encoded += chr(lnum + trans - 26)
        trans = (trans + increment) % 26
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
        if wlist[-i] > 90:
            inc = True
            wlist[-i] -= 26
    rword = "".join([chr(l) for l in wlist])
    if inc:
        rword = "A" + rword
    return rword

def createKey(phrase):
    key = ""
    for letter in stripSpaces(phrase.upper()):
        if letter not in key and ord(letter) in range(65,91):
            key += letter
    return key
