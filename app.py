import streamlit as st
import json
import matplotlib.pyplot as plt

from prompt import prompt_template
from model import generate_response
from parser import PostAnalysis

# Page Config
st.set_page_config(
    page_title="Social Media Post Analyzer",
    page_icon="📱",
    layout="centered"
)

# Custom CSS
st.markdown("""
<style>

.main {
    padding-top: 2rem;
}

.stTextArea textarea {
    border-radius: 10px;
    border: 2px solid #4CAF50;
}

.result-box {
    padding: 15px;
    border-radius: 10px;
    margin-bottom: 15px;
    color: white;
    font-size: 18px;
}

.tone {
    background-color: #1f77b4;
}

.intent {
    background-color: #2ca02c;
}

.style {
    background-color: #ff9800;
}

.summary {
    background-color: #9c27b0;
}

</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:

    st.title("📌 About Project")

    st.write("""
    Generative AI application that analyzes:
    
    - Tone
    - Intent
    - Communication Style
    - Summary
    """)

    st.divider()

    st.subheader("🧪 Example Posts")

    st.markdown("""
    **Promotional**
    > Huge discounts available this weekend only!
    
    **Complaint**
    > Very disappointed with customer service today.
    
    **Informative**
    > Office closed tomorrow due to maintenance.
    
    **Engagement**
    > What is your favorite programming language?
    """)

# Main Title
st.title("📱 Social Media Post Analyzer")

st.markdown("""
Analyze social media posts using Generative AI and structured output parsing.
""")

st.divider()

# Input Box
post = st.text_area(
    "Enter Social Media Post",
    height=150,
    placeholder="Type your social media post here..."
)

# Analyze Button
if st.button("Analyze Post"):

    if post.strip() == "":
        st.warning("⚠ Please enter a social media post.")

    else:

        with st.spinner("Analyzing post using AI..."):

            try:

                # Prompt
                final_prompt = prompt_template.format(post=post)

                # Generate response
                result = generate_response(final_prompt)

                # Clean response
                cleaned_result = result.strip()
                cleaned_result = cleaned_result.replace("```json", "")
                cleaned_result = cleaned_result.replace("```", "")

                # Parse JSON
                parsed_json = json.loads(cleaned_result)

                # Validate
                validated_output = PostAnalysis(**parsed_json)

                st.success("✅ Analysis Completed Successfully")

                st.divider()

                # Tone Card
                st.markdown(f"""
                <div class="result-box tone">
                    <b>🎭 Tone:</b><br>
                    {validated_output.tone}
                </div>
                """, unsafe_allow_html=True)

                # Intent Card
                st.markdown(f"""
                <div class="result-box intent">
                    <b>🎯 Intent:</b><br>
                    {validated_output.intent}
                </div>
                """, unsafe_allow_html=True)

                # Style Card
                st.markdown(f"""
                <div class="result-box style">
                    <b>💬 Communication Style:</b><br>
                    {validated_output.communication_style}
                </div>
                """, unsafe_allow_html=True)

                # Summary Card
                st.markdown(f"""
                <div class="result-box summary">
                    <b>📝 Summary:</b><br>
                    {validated_output.summary}
                </div>
                """, unsafe_allow_html=True)

                # Sentiment Score Logic
                tone = validated_output.tone.lower()

                score_map = {
                    "positive": 90,
                    "excited": 85,
                    "neutral": 50,
                    "negative": 20,
                    "angry": 10,
                    "friendly": 75,
                    "inspirational": 88
                }

                sentiment_score = score_map.get(tone, 50)

                st.subheader("📊 Sentiment Score")

                st.progress(sentiment_score)

                st.write(f"Sentiment Score: {sentiment_score}/100")

                # Pie Chart
                fig, ax = plt.subplots()

                labels = ["Positive Impact", "Remaining"]

                values = [sentiment_score, 100 - sentiment_score]

                ax.pie(values, labels=labels, autopct="%1.1f%%")

                st.pyplot(fig)

                # Download Button
                st.download_button(
                    label="📥 Download Result as JSON",
                    data=json.dumps(parsed_json, indent=4),
                    file_name="analysis_result.json",
                    mime="application/json"
                )

            except json.JSONDecodeError:

                st.error("❌ AI returned invalid JSON.")

            except Exception as e:

                st.error("❌ Something went wrong.")

                st.write(e)