AI News Analyzer

An interactive Python web application that fetches news articles and analyzes their sentiment using Natural Language Processing (NLP).

Project Overview

AI News Analyzer helps users explore news on a chosen topic and view the estimated sentiment of each article. It presents the results through an interactive dashboard with charts, percentages, and an experimental News Impact Score.

Features

- Fetches news articles using NewsAPI.
- Classifies article headlines and descriptions as Positive, Negative, or Neutral using VADER Sentiment Analysis.
- Displays sentiment summaries and percentages.
- Visualizes sentiment distribution using bar and pie charts.
- Calculates an estimated News Impact Score out of 100.
- Displays a chart comparing estimated impact scores across articles.
- Provides links to the original news articles.
- Handles empty searches and common API or connection errors.

Technologies Used

- Python
- Streamlit
- NewsAPI
- VADER Sentiment Analysis
- Requests
- Git and GitHub

How It Works

1. The user enters a news topic.
2. The application requests relevant articles from NewsAPI.
3. VADER analyzes each article's headline and description.
4. The application classifies sentiment and calculates an estimated impact score.
5. Streamlit displays the results through metrics, charts, and article summaries.

Run Locally

1. Clone this repository:
   
   "git clone https://github.com/sathwika404/AI-NEWS-ANALYZER.git"

2. Open the project directory:
   
   "cd AI-NEWS-ANALYZER"

3. Create and activate a Python virtual environment.

4. Install dependencies:
   
   "pip install -r requirements.txt"

5. Create ".streamlit/secrets.toml" and add your NewsAPI key:
   
   Configure the API Key

This project uses NewsAPI to fetch news articles. To run the application locally, you need your own NewsAPI key.

     1. Obtain an API key from "NewsAPI" (https://newsapi.org/).

     2. Create a file named "secrets.toml" inside the ".streamlit" folder.

     3. Add the following line to the file:
   
        NEWS_API_KEY = "YOUR_NEWSAPI_KEY"

     4. Replace "YOUR_NEWSAPI_KEY" with your own API key.

      Important: Never share your actual API key publicly or commit "secrets.toml" to GitHub. 

6. Start the application:
   
   "streamlit run app.py"

Limitations

- Sentiment is estimated from headlines and descriptions, not the full article.
- The News Impact Score is an experimental heuristic based on recency, sentiment intensity, and source information. It is not a verified measure of real-world impact, factual accuracy, or credibility.
- Article availability depends on NewsAPI and its access limits.

Future Improvements

- Add filtering by sentiment.
- Improve impact scoring using more relevant features.
- Add historical sentiment trends.
- Improve automated testing and error handling.

Live Demo

https://ai-news-analyzer-dntpswpts86tsrqr8x4bdn.streamlit.app/