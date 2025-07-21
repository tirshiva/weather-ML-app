# Weather Stats ML Web App

A modern, full-stack machine learning web application that predicts and visualizes daily weather statistics for any city worldwide. Built with FastAPI, scikit-learn, and a beautiful vanilla JS frontend, this project demonstrates end-to-end data engineering, ML, and web development skills.

---

## 🌟 Features
- **Predicts average temperature for any city and date (past, present, or future)**
- **Supports city autocomplete with global suggestions**
- **Shows 7-day average, max/min temperature, and precipitation**
- **Uses real weather data (Open-Meteo API) and machine learning (Ridge Regression)**
- **Automatic model training for new cities**
- **Modern, responsive, and user-friendly UI**
- **Handles missing data and provides clear feedback**

---

## 🚀 Demo
![Weather Stats ML Web App Screenshot](./web/demo-screenshot.png)

---

## 🛠️ Tech Stack
- **Backend:** Python, FastAPI, scikit-learn, pandas, joblib
- **Frontend:** HTML5, CSS3, Vanilla JavaScript
- **Data:** Open-Meteo API (historical & forecast), city geocoding
- **ML:** Ridge Regression with lag/rolling features & seasonality encoding
- **Deployment:** Uvicorn, Python HTTP server, Docker-ready

---

## 📊 How It Works
1. **User enters a city and date.**
2. **City autocomplete** helps users find valid locations worldwide.
3. **Backend fetches weather data** for the city (historical or forecast).
4. **If no forecast is available for future dates,** the app uses a trained ML model to predict the temperature.
5. **The result card** shows predicted average temperature, 7-day average, max/min, precipitation, and whether the value is a forecast, ML prediction, or historical/statistical.

---

## 🏗️ Project Structure
```
weather-ml-app/
├── data/                # Weather data CSVs (per city)
├── models/              # Trained ML models (per city)
├── src/
│   ├── data_ingest/     # Data fetching utilities
│   ├── features/        # Feature engineering
│   ├── service/         # FastAPI backend
│   ├── utils/           # Geocoding, city suggest, etc.
├── web/                 # Frontend (HTML, JS, CSS)
├── requirements.txt     # Python dependencies
├── train.py             # Model training script
├── run_app.py           # Entry point to run backend & frontend
└── README.md            # This file
```

---

## ⚡ Quickstart

### 1. **Clone & Install**
```bash
# Clone the repo
https://github.com/yourusername/weather-ml-app.git
cd weather-ml-app

# (Optional) Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. **Run the App**
```bash
python run_app.py
```
- Backend: [http://localhost:8000](http://localhost:8000)
- Frontend: [http://localhost:8080](http://localhost:8080)

### 3. **Use the App**
- Open the frontend in your browser.
- Start typing a city name and pick a suggestion.
- Select a date (past, present, or future).
- Click **Get Weather** to see detailed stats and predictions.

---

## 🧠 ML & Data Engineering Highlights
- **Lag features:** Uses previous days' weather as input for prediction.
- **Rolling averages:** 7-day and 30-day rolling means for temperature and precipitation.
- **Seasonality encoding:** Sine/cosine of day-of-year for annual weather cycles.
- **Automatic model training:** Trains a new Ridge Regression model for each city as needed.
- **Hybrid prediction:** Uses real forecast if available, otherwise falls back to ML prediction for future dates.

---

## 🌍 Deployment

### **A. Local (for demo/interview):**
- Just run `python run_app.py` and open [http://localhost:8080](http://localhost:8080)

### **B. Production (Cloud, Docker, or PaaS):**
- **Cloud VM:**
  - Use `gunicorn -k uvicorn.workers.UvicornWorker src.service.api:app --bind 0.0.0.0:8000` for backend
  - Serve `web/` with Nginx or a static server
- **Docker:**
  - Add a `Dockerfile` for backend and a static server for frontend
  - Use `docker-compose` for orchestration
- **Render/Heroku:**
  - Add a `Procfile` and serve static files from FastAPI or a CDN

---

## 📸 Screenshots
> _Add screenshots of the UI here to impress recruiters!_

---

## 💡 Why This Project Stands Out
- **End-to-end ML + web engineering:** Data ingestion, feature engineering, model training, API, and UI
- **Real-world data:** Uses live weather APIs and adapts to any city
- **Robust error handling:** User-friendly messages for missing data
- **Modern UX:** Responsive, accessible, and visually appealing
- **Scalable:** Easily extendable to more features, cities, or ML models

---

## 🙋 About the Author
**Your Name**  
_Machine Learning & Full-Stack Developer_  
[LinkedIn](https://www.linkedin.com/in/yourprofile) | [GitHub](https://github.com/yourusername)

---

## 📬 Contact
For questions, feedback, or collaboration, open an issue or reach out on LinkedIn! 