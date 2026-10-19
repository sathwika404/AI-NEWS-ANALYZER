import streamlit as st
import requests
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from datetime import datetime, timezone

st.set_page_config(
    page_title="AI News Analyzer",
    page_icon="📰",
    layout="wide"
)

st.title("📰 AI-Powered News Sentiment & Impact Analyzer")
st.write("Discover news and analyze its sentiment using AI.")

analyzer = SentimentIntensityAnalyzer()
def calculate_impact_score(article, sentiment_score):
    # 1. Recency score: maximum 40 points
    published_at = article.get("publishedAt")
    recency_points = 8

    if published_at:
        try:
            published_time = datetime.fromisoformat(
                published_at.replace("Z", "+00:00")
            )
            age_hours = max(
                0,
                (datetime.now(timezone.utc) - published_time).total_seconds()
                / 3600
            )

            if age_hours <= 6:
                recency_points = 40
            elif age_hours <= 24:
                recency_points = 32
            elif age_hours <= 72:
                recency_points = 24
            elif age_hours <= 168:
                recency_points = 16

        except (ValueError, TypeError):
            pass

    # 2. Sentiment intensity: maximum 40 points
    sentiment_points = round(abs(sentiment_score) * 40)

    # 3. Source information: maximum 20 points
    source = article.get("source") or {}
    source_points = 20 if source.get("name") else 10

    total = recency_points + sentiment_points + source_points

    return min(100, total)

topic = st.text_input(
    "Enter a news topic",
    placeholder="Example: Artificial Intelligence"
)

if st.button("Analyze News"):
    if not topic.strip():
        st.warning("Please enter a topic first.")
    else:
        try:
            api_key = st.secrets["NEWS_API_KEY"]

            response = requests.get(
                "https://newsapi.org/v2/everything",
                params={
                    "q": topic,
                    "language": "en",
                    "sortBy": "publishedAt",
                    "pageSize": 10,
                    "apiKey": api_key
                },
                timeout=20
            )

            data = response.json()

            if response.status_code == 200:
                articles = data.get("articles", [])

                if not articles:
                    st.info("No articles found for this topic.")

                else:
                    results = []

                    for article in articles:
                        title = article.get("title") or "Untitled article"
                        description = article.get("description") or ""
                        text = f"{title}. {description}"

                        score = analyzer.polarity_scores(text)["compound"]
                        impact_score = calculate_impact_score(article, score)

                        if score >= 0.05:
                            sentiment = "Positive 😊"
                        elif score <= -0.05:
                            sentiment = "Negative 😟"
                        else:
                            sentiment = "Neutral 😐"

                        results.append({
                            "article": article,
                            "sentiment": sentiment,
                            "score": score,
                            "impact_score": impact_score
                        })

                    positive = sum(
                        r["sentiment"].startswith("Positive")
                        for r in results
                    )
                    negative = sum(
                        r["sentiment"].startswith("Negative")
                        for r in results
                    )
                    neutral = len(results) - positive - negative

                    st.subheader("📊 Sentiment Summary")

                    col1, col2, col3 = st.columns(3)
                    col1.metric("Positive", positive)
                    col2.metric("Negative", negative)
                    col3.metric("Neutral", neutral)
                    st.subheader("📈 Sentiment Visualization")
                    st.write("Chart section reached!")

                    chart_data = {
                        "Sentiment": [
                            "Positive",
                            "Negative",
                            "Neutral"
                        ],
                        "Articles": [
                            positive,
                            negative,
                            neutral
                        ]
                    }

                    st.bar_chart(
                        chart_data,
                        x="Sentiment",
                        y="Articles",
                        color="#4C78A8"
                    )

                    st.subheader("🥧 Sentiment Distribution")

                    st.vega_lite_chart(
                        {
                            "mark": {
                                "type": "arc",
                                "innerRadius": 60
                            },
                            "encoding": {
                                "theta": {
                                    "field": "Articles",
                                    "type": "quantitative"
                                },
                                "color": {
                                    "field": "Sentiment",
                                    "type": "nominal",
                                    "scale": {
                                        "domain": [
                                            "Positive",
                                            "Negative",
                                            "Neutral"
                                        ],
                                        "range": [
                                            "#2E8B57",
                                            "#D9534F",
                                            "#E0A526"
                                        ]
                                    }
                                },
                                "tooltip": [
                                    {
                                        "field": "Sentiment",
                                        "type": "nominal"
                                    },
                                    {
                                        "field": "Articles",
                                        "type": "quantitative"
                                    }
                                ]
                            },
                            "data": {
                                "values": [
                                    {
                                        "Sentiment": "Positive",
                                        "Articles": positive
                                    },
                                    {
                                        "Sentiment": "Negative",
                                        "Articles": negative
                                    },
                                    {
                                        "Sentiment": "Neutral",
                                        "Articles": neutral
                                    }
                                ]
                            }
                        },
                        use_container_width=True
                    )
                    total = positive + negative + neutral  
                    st.subheader("⚡ Estimated News Impact Scores")
                    impact_chart_data = {
                        "Article": [
                            (r["article"].get("title") or "Untitled article")[:40]
                            for r in results
                        ],
                        "Impact Score": [
                            r["impact_score"] for r in results
                        ]
                    }
                    st.bar_chart(
    impact_chart_data,
    x="Article",
    y="Impact Score",
    color="#F2A541"
)
                    st.subheader("📋 Sentiment Percentages")

                    if total > 0:
                        p1, p2, p3 = st.columns(3)

                        p1.metric(
                            "Positive %",
                            f"{positive / total * 100:.1f}%"
                        )
                        p2.metric(
                            "Negative %",
                            f"{negative / total * 100:.1f}%"
                        )
                        p3.metric(
                            "Neutral %",
                            f"{neutral / total * 100:.1f}%"
                        )

                    st.caption(
                        "Sentiment is estimated from each headline and "
                        "description. It may not reflect the full article."
                    )

                    st.divider()
                    st.subheader("📰 Analyzed Articles")

                    for result in results:
                        article = result["article"]

                        st.markdown(
                            f"### {article.get('title') or 'Untitled article'}"
                        )

                        st.write(
                            article.get("description")
                            or "No description available."
                        )

                        st.write(
                            f"**Sentiment:** {result['sentiment']}"
                        )

                        st.write(
                            f"**Sentiment score:** "
                            f"{result['score']:.2f}"
                        )
                        st.metric("Estimated News Impact Score",f"{result['impact_score']}/100")

                        source = article.get("source", {}).get(
                            "name", "Unknown"
                        )
                        st.caption(f"Source: {source}")

                        if article.get("url"):
                            st.link_button(
                                "Read Full Article",
                                article["url"]
                            )

                        st.divider()

            else:
                st.error(
                    data.get("message", "Unable to retrieve news.")
                )

        except KeyError:
            st.error(
                "API key not found. Check .streamlit/secrets.toml."
            )
        except requests.RequestException:
            st.error(
                "Could not connect to the news service. "
                "Check your internet connection and try again."
            )
        except ValueError:
            st.error("The news service returned an invalid response.")

st.caption("Built with Python, Streamlit, NewsAPI and VADER")