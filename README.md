# Supermarket Sales Dashboard

This repository contains an interactive Streamlit dashboard for analyzing supermarket sales data. The application helps users explore transaction trends, review key performance metrics, and export filtered data for further analysis.

---

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Installation and Setup](#installation-and-setup)
- [Running the Application](#running-the-application)
- [Dashboard Guide](#dashboard-guide)
- [Data Processing](#data-processing)
- [Troubleshooting](#troubleshooting)
- [License](#license)

---

## Overview

The dashboard provides a professional interface for reviewing supermarket transaction data. It includes real-time filters, summary metrics, visual analytics, and data export capabilities to support business analysis.

---

## Features

### Dashboard Metrics
The application displays eight key performance indicators:
1. Total Sales
2. Total Transactions
3. Average Rating
4. Total Quantity
5. Gross Profit
6. Profit Margin
7. Customer Types
8. Average Sale Value

### Visual Analytics
- Sales trend over time
- Top products by revenue
- Sales distribution by payment method
- Product performance by weekday
- Sales by hour of the day
- Customer type and branch comparison

### Data Management
- Real-time filtering without page reload
- CSV export for filtered results
- Expandable data table view
- Summary statistics such as minimum, maximum, and standard deviation

---

## Technology Stack

- Python 3.10 or newer
- Streamlit
- Pandas
- Plotly
- Matplotlib
- Seaborn
- NumPy

---

## Project Structure

```text
Supermarket/
├── app.py
├── SuperMarket Analysis.csv
├── requirements.txt
├── README.md
└── .venv/
```

---

## Installation and Setup

### 1. Prerequisites
Ensure that Python is installed on your system.

```bash
python --version
```

### 2. Create a Virtual Environment

Windows:
```bash
python -m venv .venv
.\.venv\Scripts\activate
```

macOS/Linux:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Verify the Dataset
Confirm that the CSV file is present in the project directory.

```bash
# Windows
dir SuperMarket*.csv

# macOS/Linux
ls SuperMarket*.csv
```

---

## Running the Application

Start the dashboard with the following command:

```bash
streamlit run app.py
```

The app will open locally at:
- http://localhost:8501

To run it on a different port:

```bash
streamlit run app.py --server.port 8502
```

To stop the app, press Ctrl+C in the terminal.

---

## Dashboard Guide

The dashboard is organized into a sidebar for filters and a main panel for analytics.

### Sidebar Filters
Users can filter the dataset by:
- Date range
- City
- Product line
- Payment method

### Main Analysis Area
The main view includes:
- KPI cards
- Interactive charts
- Summary sections
- Export and table options

### Example Workflow
1. Select a date range.
2. Apply one or more filters.
3. Review KPI values and charts.
4. Export the filtered data if needed.

---

## Data Processing

The application loads the CSV file, converts date and time values, derives useful fields, and applies user-defined filters before generating visual outputs.

### Data Loading
```python
data = pd.read_csv("SuperMarket Analysis.csv")
data['Date'] = pd.to_datetime(data['Date'])
data['Time'] = pd.to_datetime(data['Time'], format='%H:%M')
data['Day'] = data['Date'].dt.day_name()
data['Hour'] = data['Time'].dt.hour
```

### Filtering Logic
User selections are converted into a boolean mask and applied to the dataset so the dashboard updates dynamically.

---

## Troubleshooting

### ModuleNotFoundError
If Streamlit is not installed, reinstall dependencies:

```bash
pip install -r requirements.txt
```

### Dataset File Not Found
Ensure the file name matches exactly and that it is stored in the project folder.

### Port Already in Use
If port 8501 is unavailable, start the app on another port:

```bash
streamlit run app.py --server.port 8502
```

### Virtual Environment Issues
If activation fails, recreate the environment:

```bash
python -m venv .venv
```

---

## License

This project is open source and available under the MIT License.