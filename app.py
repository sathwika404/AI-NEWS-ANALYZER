import streamlit as st
import requests
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

st.set_page_config(
    page_title="AI News Analyzer",
    page_icon="📰",
    layout="wide"
)

st.title("📰 AI-Powered News Sentiment & Impact Analyzer")
st.write("Discover news and analyze its sentiment using AI.")

analyzer = SentimentIntensityAnalyzer()

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

                        if score >= 0.05:
                            sentiment = "Positive 😊"
                        elif score <= -0.05:
                            sentiment = "Negative 😟"
                        else:
                            sentiment = "Neutral 😐"

                        results.append({
                            "article": article,
                            "sentiment": sentiment,
                            "score": score
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