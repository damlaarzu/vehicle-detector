import streamlit as st
import tempfile
import cv2
from ultralytics import YOLO
import torch

# GPU kontrolü
device = 'cuda' if torch.cuda.is_available() else 'cpu'
st.sidebar.write(f"**Kullanılan cihaz:** {device}")

# Model yükleme
MODEL_PATH = "yolo11s.pt"  # eğittiğin modelin yolu
model = YOLO(MODEL_PATH)

st.title("Object Detection (YOLO)")

# Menü seçenekleri
option = st.sidebar.selectbox(
    " Choose an option",
    ["Photo", "Video", "Camera (Real-Time)"]
)

# Fotoğraf yükleme ve tespit
if option == "Photo":
    uploaded_file = st.file_uploader("📷 Fotoğraf yükle", type=["jpg", "png", "jpeg"])
    if uploaded_file:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
            temp_file.write(uploaded_file.getbuffer())
            temp_path = temp_file.name

        results = model(temp_path, conf=0.5)
        st.image(results[0].plot(), caption="Tespit Sonucu", channels="BGR")

# Video yükleme ve tespit
elif option == "Video":
    uploaded_file = st.file_uploader("🎥 Video yükle", type=["mp4", "avi", "mov", "mkv"])
    if uploaded_file:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_file:
            temp_file.write(uploaded_file.getbuffer())
            temp_path = temp_file.name

        cap = cv2.VideoCapture(temp_path)
        stframe = st.empty()

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            results = model(frame, conf=0.5)
            stframe.image(results[0].plot(), channels="BGR")
        cap.release()

# Kamera ile gerçek zamanlı tespit
elif option == "Camera (Real-Time)":
    cap = cv2.VideoCapture(0)  # 0 = varsayılan kamera
    stframe = st.empty()

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        results = model(frame, conf=0.5)
        stframe.image(results[0].plot(), channels="BGR")
