import binascii
import audioop


def hexStringToRaw(hexstring):
    return binascii.unhexlify(''.join(hexstring.split()))


def rawToHexString(raw):
    return binascii.hexlify(raw)


def normalizeTo8BitRange(a, b, x):
    return (b - a) * (x / 255) + a


def getAudacityFormat(rawStream):
    hexStream = rawToHexString(audioop.ulaw2lin(hexStringToRaw(rawStream), 1))
    yArr = []
    for i in range(0, len(hexStream) - 2, 2):
        norm = normalizeTo8BitRange(-1, 1, int(hexStream[i:i + 2], 16))
        if norm > 0:
            yArr.append(norm - 1)
        else:
            yArr.append(norm + 1)
    return yArr

