import os

def main():
    list = os.listdir(r'C:\Users\Muhammad Reza\KTPDetect\Foto ktp')
    for i,name in enumerate(list):
        src = os.getcwd()
        dst = 'ktp'+str(i)+'.jpg'
        os.rename(r'C:\Users\Muhammad Reza\KTPDetect\Foto ktp'+'\\'+name,r'C:\Users\Muhammad Reza\KTPDetect\Foto ktp'+'\\'+dst)
if __name__ == '__main__':
    main()