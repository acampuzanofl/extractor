import os, sys
import struct

def carve_mpg(fileContent):
    mpgStart = b"\x00\x00\x01\xba"
    mpgEnd   = b"\x00\x00\x01\xb9"
    marker = -1
    start = 0
    while marker != 33:
        start = fileContent.find(mpgStart, start + len(mpgStart))

        marker = fileContent[start+4]

        if(start == -1):
            return -1, fileContent
       

    end = fileContent.find(mpgEnd, start) + len(mpgEnd)
    print("[*] found mpgStart: {0:x} mpgEnd: {1:x}".format(start, end))
    image = bytearray()

    image.extend(fileContent[start:end])
    del fileContent[start:end]

    return image, fileContent


fileName = sys.argv[1]
fileContent = bytearray()
try:
    with open(fileName, mode="rb") as f:
        fileContent = bytearray(f.read())
        print("[*] incoming length: {0}".format(len(fileContent)))
except:
    print("could not read file")

number = 1
while True:
    mpg, fileContent = carve_mpg(fileContent)
    if mpg == -1:
        print("no more mpg :(")
        break

    with open("video{0}.mpg".format(number), "wb") as f:
        print("creating video{0}".format(number))
        f.write(mpg)
    number += 1

with open("carved.bin", "wb") as f:
    print("[*] outgoing length: {0}".format(len(fileContent)))
    f.write(fileContent)