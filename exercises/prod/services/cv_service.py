import cv2
import numpy as np
from PIL import Image

class CVService:
    @staticmethod
    def analyze_image(image_bytes):
        # Converter bytes para array OpenCV
        nparr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Nitidez (Laplacian variance)
        sharpness = cv2.Laplacian(gray, cv2.CV_64F).var()
        
        # Luminosidade
        luminosity = np.mean(gray)

        # Detecção de rostos (Haar Cascade)
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        
        return {
            "luminosidade": round(float(luminosity), 2),
            "nitidez": round(float(sharpness), 2),
            "rostos": len(faces),
            "resolucao": f"{img.shape[1]}x{img.shape[0]}",
            "cores": "RGB", # Placeholder para análise real de histograma
            "descricao": "Imagem capturada via webcam"
        }