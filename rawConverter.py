import binascii
import numpy as np
import matplotlib
from matplotlib import pyplot as plt
from IPython.display import Audio
from scipy import signal
import audioop

def encodeMessageSegmentInAudioPayload(asciiHexPayload, asciiHexMsgSegment, index=0):
    """

    :param asciiHexPayload:
    :param asciiHexMsgSegment: ascii Hex string of length 2
    :param index: must be an even number less than len(asciiHexLine)
    :return:
    """
    return asciiHexPayload[0:index] + asciiHexMsgSegment + asciiHexPayload[index + 2:]


def extractMessageSegmentFromAudioPayload(asciiHexLine, index=0):
    """

    :param asciiHexLine:
    :param index: must match the encoded index
    :return:
    """
    return asciiHexLine[index:index + 2]


def messageToAsciiHexString(message):
    return ''.join(format(ord(m), "x") for m in message)


def asciiHexStringToMessage(message):
    return bytearray.fromhex(message).decode()


def encodeMessagesInAudioPayloads(asciiHexPayloads, asciiHexMessage, index=0):
    """

    :param asciiHexPayloads:
    :param asciiHexMessage: Message must be even length
    :param index:
    :return:
    """
    i = 0
    for segmentIndex in range(0, len(asciiHexMessage), 2):
        asciiHexPayloads[i] = encodeMessageSegmentInAudioPayload(asciiHexPayloads[i], asciiHexMessage[segmentIndex:segmentIndex+2])
        i += 1
    return asciiHexPayloads


def decodeMessagesInAudioPayloads(asciiHexPayloads, msgLength, index=0):
    return "".join(payload[index:index+2] for payload in asciiHexPayloads[:msgLength])


def savePayloads(lines, filename):
    outfile = open(filename, "wb")
    for line in lines:
        outfile.write(hexStringToRaw(line))
    outfile.close()


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


if __name__ == '__main__':

    file = open("VoicemailASCIIHex", "r")  # Original voicemail file
    lines = file.readlines()

    message = "The nukes will go off at 0300 in kiyv"
    if len(message) % 2 != 0:
        message += " "

    print(type(lines[0]))
    lines = encodeMessagesInAudioPayloads(lines, messageToAsciiHexString(message))


    intensity = []
    for line in lines:
        intensity += getAudacityFormat(line)

    signal.find_peaks(intensity)
    peaks = signal.find_peaks(intensity)[0]
    print(len(peaks))
    # plt.plot(peaks[0], intensity[peaks[0]])
    plt.plot(intensity)
    plt.show()

    # savePayloads(lines, "outputTest1")
