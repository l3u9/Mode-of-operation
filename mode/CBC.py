# -*- coding: utf-8 -*-


from LEA import LEA
from Utils import to_bytearray, xorAr, pad, unpad

class CBC:
    def __init__(self, key,iv, block_size = 16):
        self.crypto = LEA(key)
        self.iv = to_bytearray(iv)
        self.block_size = block_size
        

    def encrypt(self, pt):
        self.buffer = bytearray() #return시킬 값을 저장하는 buffer
        self.pt = pad(pt) #padding
        self.pt = to_bytearray(self.pt)
        
        
        cnt = int(len(self.pt)/self.block_size)
        c0 = self.iv #초기 cipher block
        for i in range(cnt):
            buf = bytearray(self.pt[(self.block_size * i) : (self.block_size*i) + self.block_size]) #블록 사이즈 크기로 평문을 잘라서 저장
            c0 = xorAr(buf,c0) #평문 블록과 xor연산
            c0 = self.crypto.encrypt(c0) #cipher block update
            self.buffer += c0 #cipher block 추가

        
        return self.buffer

    def decrypt(self, ct):
        self.buffer = bytearray() #return buffer
        self.ct = ct

        cnt = int(len(self.ct)/self.block_size) #count       
        c0 = self.iv #초기 cipher block

        '''
        복호화 진행
        '''
        for i in range(cnt):
            buf = bytearray(self.ct[(self.block_size * i) : (self.block_size*i) + self.block_size]) #block 자르기
            dec = self.crypto.decrypt(buf)
            tmp = xorAr(c0,dec) #xor 진행
            self.buffer += tmp
            c0 = buf #cipher block update



        self.buffer = unpad(self.buffer) #unpadding
        return self.buffer




