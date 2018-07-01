import socket
import codecs

class WakeOnLAN:
    """Send Wake On LAN magic packets."""

    def __init__(self):
        self.broadcast_address = '255.255.255.255'
        self.port = 9
        # Sequence of bytes which indicates a WOL magic packet.
        self.SYNC_STREAM  = b'\xff\xff\xff\xff\xff\xff'

    def send(self, mac_address):
        """Send a magic wake packet to the target MAC address."""
        payload = self.SYNC_STREAM + codecs.decode(mac_address * 16, 'hex')

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.sendto(payload, (self.broadcast_address, self.port))
        sock.close()

class SleepOnLAN(WakeOnLAN):
    def __init__(self):
        super().__init__()
        self.SYNC_STREAM = b'\x7f\x7f\x7f\x7f\x7f\x7f'

if __name__ == "__main__":
    wol = WakeOnLAN()
    wol.send('e0d55e204bb3')
