import streamlit as st
from PIL import Image

class SimpleVisionSystem:
    """
    Sistema de Visão Computacional baseado em Regras.
    Simula detecção de objetos sem Deep Learning.
    """

    RULES = {
        "person": {
            "skin_tone": 0.25,
            "face_features": 0.30,
            "clothing": 0.20,
            "human_proportion": 0.25
        },
        "car": {
            "metal_surface": 0.25,
            "wheels": 0.30,
            "rectangular_shape": 0.20,
            "glass_windows": 0.25
        },
        "animal": {
            "fur": 0.30,
            "four_legs": 0.25,
            "snout": 0.25,
            "tail": 0.20
        }
    }

    CONFIDENCE_THRESHOLD = 0.55

    def __init__(self, image_features: dict):
        self.features = image_features
        self.scores = {}

    def apply_rules(self):
        for category, rules in self.RULES.items():
            score = sum(
                min(self.features.get(feature, 0), weight)
                for feature, weight in rules.items()
            )
            self.scores[category] = score
        return self.scores

    def classify(self):
        self.apply_rules()
        best_match = max(self.scores, key=self.scores.get)
        if self.scores[best_match] >= self.CONFIDENCE_THRESHOLD:
            return best_match, self.scores[best_match]
        return "unknown", 0


# Streamlit UI
st.title("Sistema de Visão Computacional Simples")

# Image upload field
uploaded_image = st.file_uploader("Faça upload de uma imagem para classificar", type=["jpg", "jpeg", "png"])

if uploaded_image:
    # Display the uploaded image
    image = Image.open(uploaded_image)
    st.image(image, caption="Imagem Carregada", use_column_width=True)

# Sidebar for input features
st.sidebar.header("Parâmetros de Entrada")
image_features = {}
for category, rules in SimpleVisionSystem.RULES.items():
    st.sidebar.subheader(f"Características para {category}")
    for feature in rules.keys():
        image_features[feature] = st.sidebar.slider(
            f"{feature} ({category})", 0.0, 1.0, 0.0, 0.05
        )

# Instantiate the vision system
vision_system = SimpleVisionSystem(image_features)

# Display classification results
if st.button("Classificar"):
    if uploaded_image:
        category, confidence = vision_system.classify()
        st.write(f"Categoria detectada: **{category}**")
        st.write(f"Confiança: **{confidence:.2f}**")
    else:
        st.warning("Por favor, faça upload de uma imagem antes de classificar.")

# Display scores for all categories
st.subheader("Pontuações por Categoria")
scores = vision_system.apply_rules()
for category, score in scores.items():
    st.write(f"{category}: {score:.2f}")