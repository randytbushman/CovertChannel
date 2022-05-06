



def encodePacket2(rawLoad, message, bitCounter):
    rawData = bytearray(packet[Raw].load)
    k = 12  # Audio begins at 12th bit of raw load

    while bitCounter < len(message) << 4 and k < len(rawData):
        # Encode the least significant bit.
        rawData[k] = rawData[k] | 1 if (ord(message[bitCounter >> 4]) >> (bitCounter & 7)) & 1 else rawData[k] & ~1
        bitCounter += 1
        k += 1

    packet[Raw].load = bytes(rawData)
    return packet, bitCounter


if __name__ == '__main__':
    f = open("VoicemailRaw", "rb")
    rawData = bytearray(f.readlines()[0])

    print(rawData)
    message = "Hello from the raw audio!"
    bitCounter = 0
    k = 0
    while bitCounter < len(message) << 4:
        rawData[k] = rawData[k] | 1 if (ord(message[bitCounter >> 4]) >> (bitCounter & 7)) & 1 else rawData[k] & ~1
        bitCounter += 1
        k += 1

    print(rawData)

