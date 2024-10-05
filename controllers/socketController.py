import cv2
import numpy as np

class SocketController:
    @staticmethod
    def sendImage(sock, image):
        _, buffer = cv2.imencode('.jpg', image)
        data = buffer.tobytes()
        sock.send(len(data).to_bytes(4, byteorder='big'))
        sock.send(data)

    @staticmethod
    def receiveImage(sock):
        length = int.from_bytes(sock.recv(4), byteorder='big')
        data = b''
        while len(data) < length:
            packet = sock.recv(length - len(data))
            if not packet:
                return None
            data += packet
        
        image = np.frombuffer(data, dtype=np.uint8)
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)
        return image