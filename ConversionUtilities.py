import binascii
import audioop


def hexStringToRaw(hexstring):
    """
    Converts string of hex values to raw bytes.
    @param hexstring: string of hex values
    @return: the converted raw bytes
    """
    return binascii.unhexlify(''.join(hexstring.split()))


def rawToHexString(raw):
    """
    Converts raw bytes to string of hex values.
    @param raw: raw bytes
    @return: the converted string fo hex values
    """
    return binascii.hexlify(raw)


def normalizeTo8BitRange(a, b, x):
    """
    Normalizes the given value to the given range.
    @param a: the lower range value
    @param b: the greater range value
    @param x: the value we normalize
    @return: a normalized value defined for the given range
    """
    return (b - a) * (x / 255) + a


def getAudacityFormat(rawStream):
    """
    Returns the ydata of a given raw byte data stream.
    @param rawStream: a stream of raw bytes
    @return: the ydata of the given stream
    """
    hexStream = rawToHexString(audioop.ulaw2lin(hexStringToRaw(rawStream), 1))
    yArr = []
    for i in range(0, len(hexStream) - 2, 2):
        norm = normalizeTo8BitRange(-1, 1, int(hexStream[i:i + 2], 16))
        if norm > 0:
            yArr.append(norm - 1)
        else:
            yArr.append(norm + 1)
    return yArr

