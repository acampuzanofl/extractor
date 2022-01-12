import os, sys

def carve_png(fileContent):
    pngStart = b"\x89\x50\x4E\x47\x0D\x0A\x1A\x0A"
    pngEnd = b"\x49\x45\x4E\x44\xAE\x42\x60\x82"
    start = fileContent.find(pngStart)
    if start == -1:
        return b'\x00', fileContent
    end = fileContent.find(pngEnd) + 8
    print("[*] found image at: {0:x} end at: {1:x} of size: {2}".format(start, end, end - start))
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
    png, fileContent = carve_png(fileContent)
    if png == b'\x00':
        print("no more pngs :(")
        break
    with open("image{0}.png".format(number), "wb") as f:
        print("creating image{0}".format(number))
        f.write(png)
    number += 1

with open("carved.bin", "wb") as f:
    print("[*] outgoing length: {0}".format(len(fileContent)))
    f.write(fileContent)