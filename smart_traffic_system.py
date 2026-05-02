# ============================================================
# Real-Time AI Smart Traffic Management System (Cloud Version)
# Author: [Your Name]
# Class: XII AI Project
# Tech Stack: Streamlit, OpenCV, NumPy
# ============================================================

import cv2
import numpy as np
import streamlit as st
import time
from collections import deque

# ---------------------- Streamlit Config ----------------------
st.set_page_config(
    page_title="AI Smart Traffic Management",
    layout="wide"
)

# ---------------------- Sidebar ----------------------
st.sidebar.title("⚙️ Controls")

video_source = st.sidebar.selectbox("Video Source", ["Sample Video"])
run = st.sidebar.toggle("▶ Run System")

# ---------------------- Signal Logic ----------------------
def calculate_signal_timing(vehicle_count):
    if vehicle_count < 10:
        return "🟢 Green", 10
    elif vehicle_count < 25:
        return "🟡 Yellow", 20
    else:
        return "🔴 Red", 30

# ---------------------- Vehicle Detection (Stable Version) ----------------------
def detect_vehicles(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    _, thresh = cv2.threshold(blur, 80, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    vehicle_count = len(contours) // 15
    return vehicle_count

# ---------------------- UI Layout ----------------------
st.title("🚦 Smart Traffic Management System")

col1, col2 = st.columns([2, 1])

video_placeholder = col1.empty()

col2.subheader("📊 Analytics")
vehicle_metric = col2.metric("Vehicles", 0)
signal_metric = col2.metric("Signal", "🔴 Red")

traffic_data = deque(maxlen=30)
chart = col2.line_chart([])

# ---------------------- Run System ----------------------
if run:
    cap = cv2.VideoCapture("sample_traffic.mp4")

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            st.warning("Video ended")
            break

        frame = cv2.resize(frame, (640, 480))

        count = detect_vehicles(frame)
        signal, duration = calculate_signal_timing(count)

        vehicle_metric.metric("Vehicles", count)
        signal_metric.metric("Signal", signal)

        traffic_data.append(count)
        chart.line_chart(list(traffic_data))

        # Overlay text
        cv2.putText(frame, f'Count: {count}', (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
        cv2.putText(frame, f'Signal: {signal}', (20, 80),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        video_placeholder.image(frame, channels="BGR")

        time.sleep(0.05)

    cap.release()
else:
    st.info("Click ▶ Run System")

# ---------------------- Footer ----------------------
st.markdown("<hr><center>AI Traffic System | Class XII Project</center>", unsafe_allow_html=True)
