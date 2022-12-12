RTP Cover Channel - Adv. Computer Networks Class Spring 2022
-
This covert channel exploits the unencrypted audio traffic transmitted by Asterisk servers with
default settings.

We encode the first byte of audio payloads with bytes from the message we wish to exfiltrate from
the host or network.


Instructions
-  

1.) Run PacketReceiver.py on the listening host.  

2.) Run PacketInterceptor.py on Asterisk server during a session.
- User must identify session clients first.

3.) Wait for message to transmit across network.
