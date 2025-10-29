# 🌾 Project Samarth Prototype
### Prototype Project for **Build for Bharat Fellowship - 2026 Cohort (Data Science)**

---

## 📘 Overview

This project is a **Flask-based Question Answering (QA) Web Application** designed to analyze agricultural datasets and provide instant insights.  
Users can ask questions about crop production, rainfall patterns, and agricultural trends, and the system fetches relevant data from a SQLite database and presents clean tabular results.

This prototype was developed as part of the **Build for Bharat Fellowship 2026 (Data Science Track)** — focusing on empowering farmers and policymakers with easy access to data-driven insights.

---

## 🚀 Features

- 🧠 **Natural Question Understanding**  
  Ask questions in plain English like:  
  - “Compare production of Rice and Wheat”  
  - “Show trend of Maize”  
  - “Average annual rainfall for the last 5 years”

- 📊 **Dynamic Data Querying**  
  Automatically fetches relevant data from a SQLite database and computes averages, trends, and comparisons.

- 🌦️ **Multi-domain Support**  
  Works for both **crop production** and **climate data** (rainfall, etc.)

- 💬 **Interactive Web Interface**  
  Simple, fast, and responsive Flask frontend built with HTML + CSS + JS.

- 🧩 **Extendable**  
  Easy to add more question types or datasets (e.g., tea, wheat, sugarcane, etc.)

---

## 🛠️ Tech Stack

| Component | Technology |
|------------|-------------|
| Backend | Python (Flask) |
| Database | SQLite3 |
| Data Processing | Pandas |
| Fuzzy Matching | FuzzyWuzzy |
| Frontend | HTML, CSS, JavaScript |
| Visualization | Tabulate, Pandas |

---

## 📂 Project Structure

📦 Project Samarth
├── app.py # Flask main app
├── qa_engine.py # Core QA logic
├── db.sqlite3 # Local database
├── templates/
│ └── index.html # Frontend page
├── static/
│ └── style.css # Styling (optional)
├── example_input.txt # Sample questions
├── requirements.txt # Dependencies
└── README.md # Project info

yaml
Copy code

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the repository
```bash
git clone https://github.com/Krup1205/flask-qa-app.git
cd flask-qa-app
2️⃣ Create a virtual environment
bash
Copy code
python -m venv venv
venv\Scripts\activate  # (Windows)
source venv/bin/activate  # (Mac/Linux)
3️⃣ Install dependencies
bash
Copy code
pip install -r requirements.txt
4️⃣ Run the app
bash
Copy code
python app.py
5️⃣ Open in your browser
Visit 👉 http://127.0.0.1:5000

💡 Example Questions
Example	Description
Compare production of Rice and Wheat	Compares two crops across years
Show trend of Maize	Displays the production trend of a single crop
Average annual rainfall for the last 5 years	Shows rainfall averages
Compare production of Tea and Coffee	Example of adding custom crop data
