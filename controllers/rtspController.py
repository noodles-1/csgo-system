import cv2
import socket
from scapy.layers.l2 import ARP, Ether
from scapy.sendrecv import srp

class RTSPController:
    @staticmethod
    def scanNetwork() -> list[tuple]:
        '''
        Identifies all devices on the IP range of the current device.

        returns:
        - devices: list(tuple) => a list containing a 2-element tuple having the IP and MAC address of
        the detected device
        '''
        hostname = socket.gethostname()
        ip_addr = socket.gethostbyname(hostname)
        ip_range = f'{ip_addr}/24'
        arp = ARP(pdst=ip_range)
        ether = Ether(dst='ff:ff:ff:ff:ff:ff')
        packet = ether/arp
        result = srp(packet, timeout=2, verbose=0)[0]
        devices = [(received.psrc, received.hwsrc) for _, received in result]
        return devices
    
    @staticmethod
    def checkRtsp(ip: str, port=554, timeout=0.5) -> bool:
        '''
        Establishes a socket connection and tests for the handshake to verify
        whether the RTSP server is available for the specified IP address.

        params:
        - ip: str => the IP address that will be checked for RTSP server availability
        - port: int => the port location of the device (default is 554)
        - timeout: int => sets the timeout for the blocking socket operation

        returns:
        - True => if the socket successfully establishes connection with the remote socket
        on the IP address
        - False => if the socket fails to establishes connection
        '''
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            res = sock.connect_ex((ip, port))
            return res == 0
        
    @staticmethod
    def validateRtsp(ip: str, port=554) -> bool:
        '''
        Opens the video stream from the RTSP server of an IP address to verify
        whether a stream can be established.

        params: 
        - ip: str => the IP address of the RTSP server that will be checked for 
        video streams
        - port: str => the port location of the device (default is 554)

        returns:
        - True => if the RTSP server successfully provides a video stream of the device
        - False => if the RTSP server fails to provide a video stream of the device
        '''
        url = f'rtsp://{ip}:{port}'
        cap = cv2.VideoCapture(url)
        if cap.isOpened():
            cap.release()
            return True
        return False