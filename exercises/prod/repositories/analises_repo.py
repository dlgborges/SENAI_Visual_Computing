from sqlalchemy.orm import Session
from models.analises import Analise

class AnaliseRepository:
    @staticmethod
    def create(db: Session, data: dict):
        db_item = Analise(**data)
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return db_item

    @staticmethod
    def get_all(db: Session):
        return db.query(Analise).order_by(Analise.created_at.desc()).all()