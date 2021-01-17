#!/usr/bin/env python
# coding=utf8

from LEA import LEA
from Utils import to_bytearray, xorAr, pad

class CFB:
    def __init__(self, key,iv, block_size = 16):
        self.crypto = LEA(key) #암호 알고리즘 선언
        self.iv = to_bytearray(iv) #iv convert to byte array
        self.block_size = block_size #block size setting
        

    def encrypt(self, pt):
        self.buffer = bytearray() #return buffer
        self.pt = to_bytearray(pt) #plain text convert to bytearray
        self.ptlength = len(pt) #return할 cipher ptext 길이
        
        
        '''
        평문의 길이가 16의 배수이면 그대로 cnt설정
        16의 배수가 아니면 padding을 해서 16의 배수로 만든 다음 cnt 설정
        '''
        cnt = int(len(self.pt)/self.block_size)
        if((len(self.pt)/self.block_size) != 0):
            cnt = len(pad(self.pt))
        
        c0 = self.iv #cipher block
        for i in range(cnt-1):
            buf = self.pt[(self.block_size * i) : (self.block_size*i) + self.block_size] #block size로 plain text 자르기
            c0 = self.crypto.encrypt(c0) #암호화
            c0 = xorAr(buf, c0) #xor 진행 and cipher block update
            self.buffer += c0 #adding block
            

        
        return self.buffer[:self.ptlength]

    def decrypt(self, ct):
        self.buffer = bytearray() #return buffer
        self.enciv = bytearray() #미리 계산할 iv를 저장하는 buffer
        self.ct = ct
        self.ctlength = len(ct) #return length

        '''
        만약 cipher block의 크기가 16의 배수가 아니면 padding해서 16배수로 맞춘다.
        '''
        if len(self.ct)%self.block_size != 0:
            self.ct = pad(ct)

        cnt = int(len(self.ct)/self.block_size)   #count setting    
        c0 = self.iv #초기 입력
        
        '''
        iv 미리 계산
        '''
        self.enciv += self.crypto.encrypt(c0) #cipher block 저장 (미리 iv 계산)
        for i in range(cnt-1):
            buf = self.ct[(self.block_size * i) : (self.block_size * i) + self.block_size] #cipher text 자르기
            self.enciv += self.crypto.encrypt(buf) #cipher block 추가

        '''
        복호화 진행
        '''
        for i in range(cnt):
            buf1 = self.enciv[(self.block_size * i) : (self.block_size*i) + self.block_size] #미리 계산한 iv를 block size에 맞게 자르기
            buf2 = self.ct[(self.block_size * i) : (self.block_size*i) + self.block_size] #block size에 맞게 cipher text 자르기
            self.buffer += xorAr(buf1,buf2)   #xor 진행
        return self.buffer[:self.ctlength]
