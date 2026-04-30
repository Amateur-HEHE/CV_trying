# ============================================================
# Real-Time AI Smart Traffic Management System
# Author: [Ayush Ojha]
# Class: XII AI Project
# Tech Stack: Streamlit, OpenCV, NumPy
# ============================================================

import cv2
import numpy as np
import streamlit as st
import time
from collections import deque

# ---------------------- Streamlit Page Config ----------------------
st.set_page_config(
    page_title="AI Smart Traffic Management",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------- Custom CSS (Dark + Glassmorphism) ----------------------
st.markdown("""
    <style>
    /* Global style */
    body {
        background-color: #0e1117;
        color: #ffffff;
        font-family: 'Poppins', sans-serif;
    }
    /* Glassmorphic sidebar */
    section[data-testid="stSidebar"] {
        background: rgba(25, 25, 25, 0.35);
        backdrop-filter: blur(10px);
        border-radius: 15px;
    }
    /* Rounded corners for all containers */
    .stMetric, .stDataFrame, .stButton>button {
        border-radius: 10px !important;
    }
    /* Traffic Status Indicator */
    .status-light {
        padding: 10px;
        border-radius: 50%;
        height: 25px;
        width: 25px;
        display: inline-block;
        margin-right: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------------- Sidebar Controls ----------------------
st.sidebar.title("⚙️ System Controls")
st.sidebar.markdown("Real-Time AI Smart Traffic Management Prototype")

video_source = st.sidebar.selectbox("Select Video Source:", ("Webcam", "Sample Traffic Video"))
emergency_vehicle = st.sidebar.checkbox("🚨 Emergency Vehicle Detected", False)
run_system = st.sidebar.toggle("▶ Run Detection")

# ---------------------- Utility Function: Signal Timing ----------------------
def calculate_signal_timing(vehicle_count: int) -> tuple:
    """
    Calculate optimal green light duration based on vehicle density.

    Args:
        vehicle_count (int): Number of vehicles detected.

    Returns:
        tuple: (signal_status: str, duration: int)
    """
    if vehicle_count < 10:
        return "Low", 10
    elif vehicle_count < 25:
        return "Medium", 20
    else:
        return "High", 30

# ---------------------- Placeholder YOLO/Haar Cascade ----------------------
# NOTE: Replace 'cars.xml' with your own detector, or plug in YOLO later.
def detect_vehicles(frame):
    """
    Placeholder detection using simple motion detection or Haar Cascade.
    """
    # Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)

    # Simple thresholding for simulation
    _, thresh = cv2.threshold(gray, 80, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    vehicle_count = len(contours) // 20  # simulation scaling factor
    return vehicle_count

# ---------------------- Dashboard Layout ----------------------
st.title("🚦 Real-Time AI Smart Traffic Management System")
col1, col2 = st.columns([2, 1], gap="large")

# Live video feed placeholder
video_placeholder = col1.empty()

# Vehicle metrics
col2.subheader("📊 Live Analytics")
vehicle_count_display = col2.metric("Detected Vehicles", 0)
signal_status_display = col2.metric("Signal Status", "🔴 Red")

# Graph — traffic flow over time
traffic_flow = deque(maxlen=50)
chart_area = col2.line_chart([])

# ---------------------- Camera/Video Setup ----------------------
if run_system:
    if video_source == "Webcam":
        cap = cv2.VideoCapture(0)
    else:
        cap = cv2.VideoCapture("sample_traffic.mp4")  # add your sample video filename

    prev_vehicle_count = 0

    # Main live loop
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            st.warning("Video stream ended or not available.")
            break

        # Resize for performance
        frame = cv2.resize(frame, (640, 480))

        # Run detection
        vehicle_count = detect_vehicles(frame)

        # Handle emergency override
        if emergency_vehicle:
            signal_status = "🟢 Priority Green"
            duration = "∞"
        else:
            density, duration = calculate_signal_timing(vehicle_count)
            if density == "Low":
                signal_status = "🟢 Green"
            elif density == "Medium":
                signal_status = "🟡 Yellow"
            else:
                signal_status = "🔴 Red"

        # Update metrics
        vehicle_count_display.metric("Detected Vehicles", vehicle_count)
        signal_status_display.metric("Signal Status", signal_status)

        # Update chart
        traffic_flow.append(vehicle_count)
        chart_area.line_chart(list(traffic_flow))

        # Display feed with overlay
        cv2.putText(frame, f'Count: {vehicle_count}', (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
        cv2.putText(frame, f'Status: {signal_status}', (20, 80),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        video_placeholder.image(frame, channels="BGR")

        # Sleep simulates frame rate
        time.sleep(0.05)

    cap.release()
else:
    st.info("Toggle ▶ 'Run Detection' to start the system.")

# ---------------------- Footer ----------------------
st.markdown(
    "<hr><center>Developed by <b>[Your Name]</b> | "
    "Class 12 AI Capstone Project © 2026</center>",
    unsafe_allow_html=True
)
