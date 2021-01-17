운용모드 소스코드 입니다.
현재는 각 운용모드에는 LEA 암호 알고리즘을 사용하고 있습니다.
다른 암호 알고리즘을 사용하고 싶으면 각 운용모드에 self.crypto = (원하는 암호 알고리즘) 으로 설정하면 됩니다.

CipherMode.py는 LEA 코드와 암께 들어있던 파일 입니다.

각 운용모드의 입력값:
    (key, iv가 있으면 iv, blocksize = 16)
block size는 default값으로 16으로 저장되어있습니다.
block size가 16이 아닌 암호 알고리즘을 추가로 block size를 입력해주면 됩니다.


Util.py에는 필요한 함수들을 저장해놓았습니다.
xorAr은 블록 사이즈에 맞게 xor연산을 진행합니다. 현재 block size는 BLOCK_SIZE변수에 16으로 설정되어 있습니다. 만약 block size를 변경하고 싶으면 BLOCK_SIZE값을 수정하면 됩니다.
pad도 마찬가지로 block size에 맞게 padding을 합니다. 이도 똑같이 BLOCK_SIZE 변수를 바꿔서 진행합니다.
unpad는 unpadding 합니다.



TestVector_LEA.py에는 LEA128,192,256 mmt test vector 테스트가 있습니다.

