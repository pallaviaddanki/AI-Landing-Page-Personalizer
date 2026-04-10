import streamlit as st
import requests
import os
from openai import OpenAI

# ---------------- API SETUP ----------------
api_key = os.getenv("OPENAI_API_KEY")

client = None
if api_key:
    client = OpenAI(api_key=api_key)

# ---------------- UI ----------------
st.set_page_config(page_title="AI Landing Page Personalizer", layout="wide")

st.title("🚀 AI Landing Page Personalizer")

ad_text = st.text_area("📢 Enter Ad Creative")

url = st.text_input("🌐 Enter Landing Page URL", value="https://example.com")

# ---------------- SCRAPER ----------------
def scrape_website(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        res = requests.get(url, headers=headers, timeout=5)

        soup = BeautifulSoup(res.text, "html.parser")
        texts = soup.find_all(['h1', 'h2', 'h3', 'p'])

        content = " ".join([t.get_text().strip() for t in texts])

        return content[:1000] if content else "Basic product landing page"
    except:
        return "Basic product landing page"

# ---------------- AI FUNCTION ----------------
def generate_ai(ad, page):
    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[{
                "role": "user",
                "content": f"""
Ad: {ad}
Landing Page: {page}

Generate:
HEADLINE:
SUBHEADLINE:
CTA:
SECTION 1:
SECTION 2:
SECTION 3:
"""
            }],
            temperature=0.3
        )

        return response.choices[0].message.content

    except:
        return None

# ---------------- FALLBACK (VERY IMPORTANT) ----------------
def fallback_output(ad):
    return f"""
HEADLINE: Get Amazing Results Today!
SUBHEADLINE: Inspired by your ad: {ad[:50]}
CTA: Shop Now

SECTION 1: Discover a product designed to meet your needs.
SECTION 2: Experience high-quality results with proven benefits.
SECTION 3: Limited time offer — act now!
"""

# ---------------- HTML RENDER ----------------
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
    <div style="padding:40px; font-family:sans-serif">
        <h1>{headline}</h1>
        <h3>{subheadline}</h3>
        <button style="padding:10px 20px; background:black; color:white;">
            {cta}
        </button>
        <hr>
    """

    for sec in sections:
        html += f"<p>{sec}</p>"

    html += "</div>"
    return html

# ---------------- MAIN ----------------
if st.button("✨ Generate Personalized Page"):

    if not ad_text:
        st.warning("⚠️ Please enter Ad Creative")
        st.stop()

    with st.spinner("Generating..."):

        page_data = scrape_website(url)

        ai_output = None
        if client:
            ai_output = generate_ai(ad_text, page_data)

        # ✅ fallback if API fails
        if not ai_output:
            ai_output = fallback_output(ad_text)

        html_output = render_html(ai_output)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🧠 AI Output")
        st.text(ai_output)

    with col2:
        st.subheader("🌐 Preview")
        st.components.v1.html(html_output, height=500)
