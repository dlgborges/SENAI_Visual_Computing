import streamlit as st
import pandas as pd
from config.database import SessionLocal, engine, Base
from services.cv_service import CVService
from repositories.analises_repo import AnaliseRepository
import os

# Init DB
Base.metadata.create_all(bind=engine)

st.set_page_config(page_title="CV Analyzer", layout="wide")

st.title("👁️ Computer Vision System")

menu = st.sidebar.selectbox("Menu", ["Câmera", "Histórico", "Dashboard"])

if menu == "Câmera":
    img_file = st.camera_input("Capture uma foto")
    
    if img_file:
        st.success("Foto capturada!")
        
        if st.button("Analisar Imagem"):
            # Processar
            results = CVService.analyze_image(img_file.getvalue())
            
            # Salvar no DB
            db = SessionLocal()
            analise_data = {
                "image_path": "temp_path", # Logica de upload S3/Local
                "descricao": results["descricao"],
                "objetos": {},
                "quantidade_pessoas": results["rostos"],
                "rostos": results["rostos"],
                "cores": {},
                "luminosidade": results["luminosidade"],
                "nitidez": results["nitidez"],
                "json_resultado": results
            }
            AnaliseRepository.create(db, analise_data)
            st.json(results)

elif menu == "Histórico":
    db = SessionLocal()
    data = AnaliseRepository.get_all(db)
    df = pd.DataFrame([vars(x) for x in data])
    st.dataframe(df)
    
    # Export
    csv = df.to_csv(index=False)
    st.download_button("Exportar CSV", csv, "historico.csv", "text/csv")