from sqlalchemy import Column, Integer, String, DateTime, Float, JSON
from datetime import datetime
from config.database import Base

class Analise(Base):
    __tablename__ = "analises"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    image_path = Column(String)
    descricao = Column(String)
    objetos = Column(JSON)
    quantidade_pessoas = Column(Integer)
    rostos = Column(Integer)
    idade = Column(String, nullable=True)
    emocao = Column(String, nullable=True)
    cores = Column(JSON)
    luminosidade = Column(Float)
    nitidez = Column(Float)
    json_resultado = Column(JSON)