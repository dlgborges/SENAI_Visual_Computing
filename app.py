import io
import numpy as np
import pandas as pd
import streamlit as st
import torch

from PIL import Image, ImageOps
from ultralytics import YOLO


st.set_page_config(
    page_title="Identificação e Segmentação de Imagens",
    page_icon="🧠",
    layout="wide"
)


@st.cache_resource(show_spinner="Carregando modelo YOLO...")
def load_model(model_name: str):
    return YOLO(model_name)


def pil_to_bgr_array(image_pil: Image.Image) -> np.ndarray:
    image_rgb = np.asarray(image_pil.convert("RGB"))
    image_bgr = image_rgb[:, :, ::-1]
    return np.ascontiguousarray(image_bgr)


def get_class_name(names, class_id: int) -> str:
    if isinstance(names, dict):
        return names.get(class_id, str(class_id))
    return names[class_id]


def result_to_dataframe(result) -> pd.DataFrame:
    columns = [
        "objeto",
        "classe",
        "confiança",
        "x1",
        "y1",
        "x2",
        "y2",
        "área_máscara_px"
    ]

    if result.boxes is None or len(result.boxes) == 0:
        return pd.DataFrame(columns=columns)

    boxes_xyxy = result.boxes.xyxy.cpu().numpy()
    classes = result.boxes.cls.cpu().numpy().astype(int)
    confidences = result.boxes.conf.cpu().numpy()

    mask_areas = [None] * len(classes)

    if result.masks is not None and result.masks.data is not None:
        masks = result.masks.data.cpu().numpy()
        for i in range(min(len(mask_areas), masks.shape[0])):
            mask_areas[i] = int(np.count_nonzero(masks[i] > 0.5))

    rows = []

    for i, class_id in enumerate(classes):
        x1, y1, x2, y2 = np.round(boxes_xyxy[i]).astype(int).tolist()

        rows.append({
            "objeto": i + 1,
            "classe": get_class_name(result.names, int(class_id)),
            "confiança": round(float(confidences[i]), 4),
            "x1": x1,
            "y1": y1,
            "x2": x2,
            "y2": y2,
            "área_máscara_px": mask_areas[i]
        })

    return pd.DataFrame(rows, columns=columns)


def image_to_png_bytes(image_rgb: np.ndarray) -> bytes:
    buffer = io.BytesIO()
    Image.fromarray(image_rgb).save(buffer, format="PNG")
    buffer.seek(0)
    return buffer.getvalue()


def run_inference(
    model,
    image_pil: Image.Image,
    conf: float,
    iou: float,
    imgsz: int,
    max_det: int,
    device
):
    image_bgr = pil_to_bgr_array(image_pil)

    results = model.predict(
        source=image_bgr,
        conf=conf,
        iou=iou,
        imgsz=imgsz,
        max_det=max_det,
        device=device,
        verbose=False
    )

    result = results[0]

    annotated_bgr = result.plot(
        masks=True,
        boxes=True,
        labels=True,
        conf=True
    )

    annotated_rgb = annotated_bgr[:, :, ::-1].copy()
    detections_df = result_to_dataframe(result)

    return annotated_rgb, detections_df


st.title("Identificação e Segmentação de Imagens")
st.caption("Envie uma imagem para detectar, classificar e segmentar objetos automaticamente com YOLO.")

gpu_available = torch.cuda.is_available()

with st.sidebar:
    st.header("Configurações")

    model_name = st.selectbox(
        "Modelo YOLO",
        options=[
            "yolov8n-seg.pt",
            "yolov8s-seg.pt"
        ],
        index=0
    )

    conf = st.slider(
        "Confiança mínima",
        min_value=0.05,
        max_value=0.95,
        value=0.35,
        step=0.05
    )

    iou = st.slider(
        "IoU para NMS",
        min_value=0.10,
        max_value=0.90,
        value=0.45,
        step=0.05
    )

    default_imgsz = 640 if gpu_available else 512

    imgsz = st.select_slider(
        "Tamanho de inferência",
        options=[320, 416, 512, 640, 768],
        value=default_imgsz
    )

    max_det = st.slider(
        "Máximo de objetos",
        min_value=1,
        max_value=300,
        value=100,
        step=1
    )

    use_gpu = st.checkbox(
        "Usar GPU se disponível",
        value=gpu_available,
        disabled=not gpu_available
    )

    device = 0 if use_gpu and gpu_available else "cpu"

    st.divider()

    st.write("Dispositivo:", "GPU" if device != "cpu" else "CPU")

    if model_name != "yolov8n-seg.pt" and device == "cpu":
        st.warning("Modelos maiores podem ser lentos em CPU.")


uploaded_files = st.file_uploader(
    "Carregue uma ou mais imagens",
    type=["jpg", "jpeg", "png", "webp"],
    accept_multiple_files=True
)

if not uploaded_files:
    st.info("Faça upload de uma imagem para iniciar a identificação.")
    st.stop()

model = load_model(model_name)

for uploaded_file in uploaded_files:
    with st.expander(f"Imagem: {uploaded_file.name}", expanded=len(uploaded_files) == 1):
        try:
            image_pil = Image.open(uploaded_file)
            image_pil = ImageOps.exif_transpose(image_pil).convert("RGB")
        except Exception:
            st.error("Não foi possível abrir esta imagem.")
            continue

        with st.spinner("Processando imagem..."):
            annotated_rgb, detections_df = run_inference(
                model=model,
                image_pil=image_pil,
                conf=conf,
                iou=iou,
                imgsz=imgsz,
                max_det=max_det,
                device=device
            )

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Imagem original")
            st.image(image_pil, use_container_width=True)

        with col2:
            st.subheader("Imagem segmentada")
            st.image(annotated_rgb, use_container_width=True)

        total_objects = len(detections_df)
        total_classes = detections_df["classe"].nunique() if total_objects > 0 else 0

        metric_col1, metric_col2, metric_col3 = st.columns(3)

        metric_col1.metric("Objetos detectados", total_objects)
        metric_col2.metric("Classes únicas", total_classes)
        metric_col3.metric("Dispositivo", "GPU" if device != "cpu" else "CPU")

        if detections_df.empty:
            st.warning("Nenhum objeto foi detectado com os parâmetros atuais.")
        else:
            summary_df = (
                detections_df["classe"]
                .value_counts()
                .rename_axis("classe")
                .reset_index(name="quantidade")
            )

            st.subheader("Resumo por classe")
            st.dataframe(summary_df, use_container_width=True, hide_index=True)

            st.subheader("Detecções")
            st.dataframe(detections_df, use_container_width=True, hide_index=True)

        st.download_button(
            label="Baixar imagem segmentada",
            data=image_to_png_bytes(annotated_rgb),
            file_name=f"resultado_{uploaded_file.name.rsplit('.', 1)[0]}.png",
            mime="image/png"
        )