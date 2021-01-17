#!/usr/bin/env python
# coding=utf8
from LEA import LEA
from Utils import to_bytearray, xorAr, pad

class CTR:
    def __init__(self,key, ctr, block_size = 16):
        self.crypto = LEA(key)
        self.ctr = to_bytearray(ctr)
        self.bloc_size = block_size
    
    '''
    ctr을 +1 씩 업데이트 하는 함수
    '''
    def cal_ctr(self):
        for i in range((self.bloc_size - 1), (self.bloc_size -1) - self.bloc_size, - 1):
            if self.ctr[i] != 0xff:
                self.ctr[i] += 1
                break
            else:
                self.ctr[i] = 0 
 
        
        

    def encrypt(self, pt):
        self.buffer = bytearray() #return buffer
        self.pt = to_bytearray(pt)
        self.ptlength = len(pt) #return length
        
        '''
        16의 배수에 맞게 cnt 설정
        '''
        cnt = int(len(self.pt)/self.bloc_size)
        if((len(self.pt)/self.bloc_size) != 0):
            cnt = len(pad(self.pt))


        for i in range(cnt):
            self.buffer += xorAr(self.crypto.encrypt(self.ctr), self.pt[(self.bloc_size * i) : (self.bloc_size*i) + self.bloc_size]) #암호화 진행
            self.cal_ctr()#ctr update

        
        return self.buffer[:self.ptlength]


    def decrypt(self, ct):
        self.buffer = bytearray() #return buffer
        self.ct = ct
        self.ctlength = len(ct) #return length

        '''
        16의 배수에 맞게 cnt 설정
        '''
        cnt = int(len(self.ct)/self.bloc_size)
        if((len(self.ct)/self.bloc_size) != 0):
            cnt = len(pad(self.ct))
        
        for i in range(cnt):
            self.buffer += xorAr(self.crypto.encrypt(self.ctr), self.ct[(self.bloc_size * i) : (self.bloc_size*i) + self.bloc_size]) #암호화 진행
            self.cal_ctr() #ctr update
        

        return self.buffer[:self.ctlength]










