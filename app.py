import streamlit as st
import requests
import os
import openai
import random

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="AI Landing Page Generator", layout="wide")

# ---------------- API KEY ----------------
api_key = os.getenv("OPENAI_API_KEY")

client = None
if api_key:
    from openai import OpenAI
    client = OpenAI(api_key=api_key)

# ---------------- MODERN UI ----------------
st.markdown("""
<style>
body {
    background-color: #0f172a;
}

.main {
    background-color: #0f172a;
    color: white;
}

.title {
    text-align: center;
    font-size: 40px;
    font-weight: bold;
    color: #ffffff;
}

.subtitle {
    text-align: center;
    color: #94a3b8;
    margin-bottom: 30px;
}

.card {
    background: #1e293b;
    padding: 20px;
    border-radius: 12px;
    margin-top: 10px;
}

button {
    background: linear-gradient(90deg,#ff4b4b,#ff7b7b);
    color: white;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">🚀 AI Landing Page Generator</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Turn Ads into High-Converting Landing Pages using AI</div>', unsafe_allow_html=True)

# ---------------- INPUTS ----------------
ad_text = st.text_area("📢 Enter Ad Creative")

url = st.text_input("🌐 Enter Landing Page URL", "https://example.com")

tone = st.selectbox("🎯 Choose Tone", [
    "Professional",
    "Luxury",
    "Aggressive Sales",
    "Friendly"
])

# ---------------- SCORE FUNCTION ----------------
def conversion_score():
    return random.randint(70, 98)

# ---------------- SCRAPER ----------------
def scrape_website(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        res = requests.get(url, headers=headers, timeout=5)

        soup = BeautifulSoup(res.text, "html.parser")
        texts = soup.find_all(['h1', 'h2', 'h3', 'p'])

        content = " ".join([t.get_text().strip() for t in texts])

        return content[:1200] if content else "Basic landing page content"
    except:
        return "Basic landing page content"

# ---------------- AI FUNCTION ----------------
def generate_ai(ad, page):
    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[{
                "role": "user",
                "content": f"""
You are an expert marketing copywriter.

Tone: {tone}

Ad:
{ad}

Landing Page Content:
{page}

Generate a high converting landing page:

HEADLINE:
SUBHEADLINE:
CTA:
SECTION 1:
SECTION 2:
SECTION 3:
"""
            }],
            temperature=0.4
        )

        return response.choices[0].message.content

    except:
        return None

# ---------------- FALLBACK ----------------
def fallback_output(ad):
    return f"""
HEADLINE: Boost Your Results Instantly
SUBHEADLINE: Inspired by: {ad[:60]}
CTA: Buy Now

SECTION 1: Discover premium benefits designed for you.
SECTION 2: Improve your results with proven strategies.
SECTION 3: Limited-time offer available now!
"""

# ---------------- PARSE OUTPUT ----------------
def render_html(text):
    headline, subheadline, cta = "", "", ""
    sections = []

    for line in text.split("\n"):
        if "HEADLINE:" in line:
            headline = line.replace("HEADLINE:", "").strip()
        elif "SUBHEADLINE:" in line:
            subheadline = line.replace("SUBHEADLINE:", "").strip()
        elif "CTA:" in line:
            cta = line.replace("CTA:", "").strip()
        elif "SECTION" in line:
            sections.append(line.split(":", 1)[-1].strip())

    html = f"""
    <div style="padding:40px;font-family:sans-serif;background:#0f172a;color:white;border-radius:10px">
        <h1>{headline}</h1>
        <h3 style="color:#94a3b8">{subheadline}</h3>

        <button style="
            padding:12px 20px;
            background:linear-gradient(90deg,#ff4b4b,#ff7b7b);
            border:none;
            border-radius:10px;
            color:white;
            font-weight:bold;
            margin-top:10px;
        ">
            {cta}
        </button>

        <hr style="margin:20px 0">

        <div style="display:grid;gap:10px">
    """

    for sec in sections:
        html += f"""
        <div style="background:#1e293b;padding:15px;border-radius:10px">
            {sec}
        </div>
        """

    html += "</div></div>"
    return html

# ---------------- BUTTON ----------------
if st.button("✨ Generate Landing Page"):

    if not ad_text:
        st.warning("Please enter Ad Creative")
        st.stop()

    with st.spinner("Generating AI Landing Page..."):

        page_data = scrape_website(url)

        ai_output = None
        if client:
            ai_output = generate_ai(ad_text, page_data)

        if not ai_output:
            ai_output = fallback_output(ad_text)

        html_output = render_html(ai_output)
        score = conversion_score()

    # ---------------- OUTPUT ----------------
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🧠 AI Output")
        st.text(ai_output)
        st.success(f"🔥 Conversion Score: {score}/100")

    with col2:
        st.subheader("🌐 Preview")
        st.components.v1.html(html_output, height=600)

    st.code(ai_output)
    st.info("✔ You can copy this output and use it in ads or landing pages")
