#!/usr/bin/env python
# coding=utf8
from LEA import LEA
from Utils import to_bytearray, xorAr,pad,unpad

class ECB:
    def __init__(self, key, block_size = 16):
        self.crypto = LEA(key) #암호 알고리즘 호출
        self.block_size = block_size #block size

    def encrypt(self, pt):
        self.buffer = bytearray() #리턴할 buffer
        
        self.pt = pad(pt) #padding
        self.pt = to_bytearray(self.pt) #to bytearray
        cnt = int(len(self.pt)/self.block_size) #count
        

        '''
        암호화 진행
        '''
        for i in range(cnt):
            buf = self.pt[(self.block_size * i) : (self.block_size *i) + self.block_size] #block 자르기
            enc = self.crypto.encrypt(buf)
            self.buffer += enc
            

        return self.buffer

    def decrypt(self, ct):
        self.buffer = bytearray() #리턴할 buffer
        self.ct = ct
        cnt = int(len(self.ct)/self.block_size) #count
        
        '''
        복호화 진행
        '''
        for i in range(cnt):
            buf = self.ct[(self.block_size * i) : (self.block_size*i) + self.block_size] #block 자르기
            dec = self.crypto.decrypt(buf)
            self.buffer += dec

        self.buffer = unpad(self.buffer) #unpadding
        return self.buffer








       


        

