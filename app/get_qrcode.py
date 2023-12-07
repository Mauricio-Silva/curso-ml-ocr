from socket import socket, AF_INET, SOCK_DGRAM
from qrcode.constants import ERROR_CORRECT_L
from qrcode.image.pil import PilImage
from qrcode.main import QRCode
from common import PORT


class GetQrCode:
    HOST = "10.253.155.219"
    BASE_URL = "http://{ip}:{port}"
    PATH = "app/static/images/qrcode.png"
    IMAGE = None

    @classmethod
    def render(cls) -> None:
        with socket(AF_INET, SOCK_DGRAM) as s:
            s.connect((cls.HOST, 58162))
            ip = str(s.getsockname()[0])
        url = cls.BASE_URL.format(ip=ip, port=PORT)

        qr = QRCode(
            version=1,
            error_correction=ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(url)
        qr.make(fit=True)
        cls.IMAGE: PilImage = qr.make_image(fill_color="black", back_color="white")
        cls.IMAGE.save(cls.PATH)
        cls.IMAGE.show()
