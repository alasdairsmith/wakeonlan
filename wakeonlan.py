"""Send Wake-On-LAN magic packets using UDP."""
import socket
import codecs

def wakeonlan(mac_address, broadcast_address='255.255.255.255', port=9):
    """Send a Wake-On-LAN magic packet using UDP.
    
    :param str mac_address: MAC address of the device to be wakened.
    :param str broadcast_address: Broadcast address to be used (default
    =255.255.255.255).
    :param int port: UDP port to be used (default=9).
    :return: If the packet was sent; there is no acknowledgement upon 
    receipt.
    :rtype: bool
    """

    # Sequence of six bytes indicating start of a WOL magic packet.
    SYNC_STREAM  = b'\xff\xff\xff\xff\xff\xff'

    if mac_address is None:
        raise TypeError('MAC address must be provided.')

    # Translation table to remove common separator characters
    table = str.maketrans(dict.fromkeys(':-. '))
    mac_address = mac_address.translate(table)
            
    if len(mac_address) != 12:
        raise ValueError('MAC address is the wrong length.')

    # The datagram must contain the six byte sequence followed by the
    # MAC address repeated 16 times.
    data = SYNC_STREAM + codecs.decode(mac_address * 16, 'hex')

    # Broadcast the datagram
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.sendto(data, (broadcast_address, port))
        return True
