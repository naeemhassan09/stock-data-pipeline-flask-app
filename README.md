# Stock Data Pipeline Flask App
## Data Acquisition and Preprocessing Pipeline Project

**Student Name:** Naeem ul Hassan  
**Student ID:** 20054701  
**Module Title:** Programming for Data Analysis  
**Module Code:** B9AI108  
**Lecturer:** Paul Laird  
**Programme/Cohort:** 2425_TMD2  
**Assessment Number:** 2  
**Institution:** Dublin Business School  
**Issue Date:** January 2025  
**Submission Date:** 13/04/2025  
**Feedback Date:** In-class (by 11/05/2025)

---

*By submitting this assignment, I confirm that this work is entirely my own, and all sources used have been properly referenced in accordance with Dublin Business School guidelines.*

### AI Assistance and Attribution

For this project, I used AI-based tools (e.g., ChatGPT) as a collaborative assistant to help generate ideas, structure documentation, and refine deployment-related details. The AI was utilized in the following ways:

- **Documentation and Comments:**  
  AI helped draft initial versions of documentation comments and inline code comments, which were then carefully reviewed and refined by me to ensure clarity and accuracy.

- **Project Structure and Deployment Guidance:**  
  AI provided suggestions for the overall project structure and best practices for deployment (including Google Cloud App Engine configurations). I evaluated and integrated these suggestions to suit the project's requirements.

- **Idea Generation:**  
  AI assisted in brainstorming ways to present data analyses and to articulate the use case scenarios, ensuring that the final documentation clearly explains the objectives and methodologies used in the project.

All AI-generated content was critically reviewed and adapted by me, ensuring that the final submission reflects my own work and understanding. This collaboration adheres to Dublin Business School's guidelines on the use of AI, and proper attribution is provided as required.

# Stock Data Pipeline Flask App

This repository contains a data acquisition and preprocessing pipeline project, built to demonstrate Python programming skills. The project fetches historical stock data using the yfinance API, processes the data to calculate daily returns and cumulative (long hold) returns, and compares the performance of top active stocks against benchmark assets (S&P 500, Gold, Silver, and Oil). The processed data is also served via a simple Flask web application.

## Project Overview

This project is designed as an end-to-end demonstration of data acquisition, preprocessing, and basic statistical analysis using Python. The primary goals include:
- **Stock Price Direction Prediction:**  
  Predict whether a stock's closing price will increase or decrease on the next day based on its daily returns.
  
- **Correlation Analysis:**  
  Compute and analyze the correlation matrix among the top 10 active stocks to understand their interrelationships.

- **Percentage Returns Comparison:**  
  Compare the average daily returns and cumulative returns (long hold) of various stocks along with benchmark assets such as S&P funds, Gold, Silver, and Oil. The focus is on analyzing the US market.

- **Long Hold Analysis:**  
  Evaluate a long-term holding strategy by analyzing cumulative returns over a multi-year period.


## Project Setup

Follow these steps to set up and run the project on your local machine:

1. **Clone the Repository:**

   Open your terminal and run the following command to clone the repository:

```bash
   git clone https://github.com/naeemhassan09/stock-data-pipeline-flask-app.git
   cd stock-data-pipeline-flask-app
```

2.	**Create a Virtual Environment:**

    It is recommended to use a virtual environment to manage dependencies. You can create one using Python’s built-in venv module.
```bash
python -m venv venv
```

3.	**Activate the Virtual Environment:**

	•	On Windows:
```bash
venv\Scripts\activate
```
    •	On macOS and Linux:
```bash
source venv/bin/activate
```
    After activation, your terminal prompt should display the name of your virtual environment (e.g., (venv)).

4.	**Install Dependencies:**
    With the virtual environment activated, install the required packages using the requirements.txt file:

```bash
pip install -r requirements.txt
```

5.	**Run the Application Locally:**
    Start the Flask application by running:

```bash
python app.py
```