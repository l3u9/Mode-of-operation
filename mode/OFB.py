# -*- coding: utf-8 -*-
from LEA import LEA
from Utils import to_bytearray, xorAr, pad

class OFB:
    def __init__(self, key,iv, block_size = 16):
        self.crypto = LEA(key)
        self.iv = to_bytearray(iv)
        self.block_size = block_size
        

    def encrypt(self, pt):
        self.buffer = bytearray() #return할 buffer
        self.enciv = bytearray() #암호화 시킨 iv를 한꺼번에 저장할 buffer
        self.pt = to_bytearray(pt)
        self.ptlength = len(pt) #리턴시킬 암호문 길이
        
        
        '''
        block count 설정
        16배수면 그대로
        16배수가 아니면 padding을 통해 16배수로 만들어주고 count 설정
        '''
        cnt = int(len(pad(self.pt))/self.block_size)
        if((len(self.pt)%self.block_size) != 0):
            cnt = len(pad(self.pt))/self.block_size


        '''
        iv 미리 계산
        '''

        tmp = self.iv #입력 iv
        for i in range(cnt-1):
            tmp = self.crypto.encrypt(tmp)
            self.enciv += tmp #iv계산 저장

            

        '''
        암호화 진행
        '''
        for i in range(cnt):
            buf1 = self.enciv[(self.block_size * i) : (self.block_size*i) + self.block_size] #block size에 맞게 미리 계산한 iv 자르기
            buf2 = self.pt[(self.block_size * i) : (self.block_size*i) + self.block_size] #block size로 평문 자르기
            self.buffer += xorAr(buf1,buf2) #xor 진행

        
        return self.buffer[:self.ptlength] #평문 길이만큼 return

    def decrypt(self, ct):
        self.buffer = bytearray() #return buffer
        self.enciv = bytearray() #계산한 iv를 한꺼번에 저장할 buffer
        self.ctlength = len(ct) #return할 cipher text의 길이 저장
        self.ct = ct

        
        '''
        16배수이면 그대로
        16배수가 아니면 패딩해서 16배수로 맞춘다음 count 설정
        '''
        cnt = int(len(pad(self.ct))/self.block_size)
        if((len(self.ct)%self.block_size) != 0):
            cnt = len(pad(self.ct))/self.block_size
        

        '''
        iv 미리 계산
        '''
        tmp = self.iv
        for i in range(cnt-1):
            tmp = self.crypto.encrypt(tmp)
            self.enciv += tmp

        for i in range(cnt):
            buf1 = self.enciv[(self.block_size * i) : (self.block_size*i) + self.block_size] #미리 계산한 enciv buffer를 block size에 맞게 자르기
            buf2 = self.ct[(self.block_size * i) : (self.block_size*i) + self.block_size] #block size에 맞게 cipher text 자르기
            self.buffer += xorAr(buf1,buf2) #xor 진행
        
        return self.buffer[:self.ctlength]


