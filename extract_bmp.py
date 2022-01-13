import os, sys
import struct

def carve_bmp(fileContent, offset):
    bmpStart = b"BM"
    unused = -1
    start = offset
    while unused != 0:
        start = fileContent.find(bmpStart, start + len(bmpStart))
        size  = start + 2
        unused = start + 6
        
        size = struct.unpack("I",fileContent[size:size+4])[0]
        unused = struct.unpack("I",fileContent[unused:unused+4])[0]

        if(start == -1):
            return -1, fileContent, offset

    end = start + size
    print("[*] found image at: {0:x} size: {1:x}".format(start, size))
    image = bytearray()
    try:
        image.extend(fileContent[start:end])
        del fileContent[start:end]
    except:
        offset = start + 2
    return image, fileContent, offset


fileName = sys.argv[1]
fileContent = bytearray()
try:
    with open(fileName, mode="rb") as f:
        fileContent = bytearray(f.read())
        print("[*] incoming length: {0}".format(len(fileContent)))
except:
    print("could not read file")

number = 1
offset = 0
while True:
    bmp, fileContent, offset = carve_bmp(fileContent, offset)
    if bmp == -1:
        print("no more bmp :(")
        break

    with open("image{0}.bmp".format(number), "wb") as f:
        print("creating image{0}".format(number))
        f.write(bmp)
    number += 1

with open("carved.bin", "wb") as f:
    print("[*] outgoing length: {0}".format(len(fileContent)))
    f.write(fileContent)