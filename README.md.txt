# Orbital Sentinel

Orbital Sentinel is a real-time satellite tracking and telemetry dashboard. It provides a visual interface to monitor the current position of orbital assets like the International Space Station (ISS), Starlink constellations, and weather satellites using high-precision orbital mechanics.

## How it Works
The application establishes a connection to **CelesTrak** to retrieve the latest Two-Line Element (TLE) datasets. TLEs serve as the "orbital DNA" for objects in space. 

To determine the satellite's exact position at any given moment, the engine utilizes the **SGP4 (Simplified General Perturbations-4)** propagation model. This allows the software to calculate latitude, longitude, and altitude with professional-grade accuracy. All telemetry outputs have been cross-verified against official tracking sources.

## Core Features
* **3D Interactive Globe:** Visualizes the satellite's ground track on an orthographic projection.
* **Live Telemetry:** Real-time updates for Altitude, Latitude, and Longitude.
* **Multi-Category Tracking:** Toggle between space stations, communication satellites, and scientific payloads.

## Installation and Setup

To run this project on your local machine, follow these steps:

### 1. Prerequisites
Ensure you have **Python 3.10 or higher** installed on your system. You can check your version by running:
```bash
python --version
2. Clone the Repository
Bash
git clone [https://github.com/michael9765440546/random-codes.git](https://github.com/michael9765440546/random-codes.git)
cd Orbital-Sentinel
3. Install Dependencies
The project requires a few specific libraries for physics calculations and the web interface. Install them using pip:

Bash
python -m pip install skyfield streamlit plotly requests
4. Configure API Key
The app uses the N2YO API for specific data calls.

Open app.py in a text editor.

Locate the variable N2YO_API_KEY.

Replace the placeholder with your own API key from n2yo.com.

5. Launch the Application
Start the dashboard by running the following command in your terminal:

Bash
python -m streamlit run app.py
The dashboard will automatically open in your default web browser (usually at http://localhost:8501).