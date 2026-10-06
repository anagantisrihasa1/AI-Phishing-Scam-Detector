import streamlit as st
import re
from urllib.parse import urlparse

# ---------------- PAGE SETTINGS ----------------
st.set_page_config(
    page_title="AI Phishing & Msg Scam Detector",
    page_icon="🛡️",
    layout="centered"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
.main {
    max-width: 850px;
    margin: auto;
}

.title {
    text-align: center;
    font-size: 42px;
    font-weight: bold;
}

.subtitle {
    text-align: center;
    font-size: 18px;
    margin-bottom: 25px;
}

.result-box {
    padding: 20px;
    border-radius: 12px;
    margin-top: 20px;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# ---------------- TITLE ----------------
st.markdown(
    '<div class="title">🛡️ AI Phishing & Scam Detector</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Analyze messages and identify possible phishing or scam attempts.</div>',
    unsafe_allow_html=True
)

# ---------------- INPUT ----------------
message = st.text_area(
    "📩 Enter Message",
    placeholder="Paste an SMS, email, or suspicious message here...",
    height=180
)

# ---------------- DETECTION FUNCTION ----------------
def detect_scam(text):

    text_lower = text.lower()

    scam_keywords = [
        "urgent",
        "click here",
        "verify your account",
        "bank account",
        "password",
        "otp",
        "free money",
        "lottery",
        "winner",
        "claim now",
        "limited time",
        "gift card",
        "congratulations",
        "account suspended",
        "update payment",
        "login now",
        "send money",
        "prize",
        "refund",
        "kyc",
        "deactivate"
    ]

    found = []

    for word in scam_keywords:
        if word in text_lower:
            found.append(word)

    # URL detection
    urls = re.findall(
        r'https?://[^\s]+|www\.[^\s]+',
        text
    )

    suspicious_urls = []

    for url in urls:

        if not url.startswith("http"):
            url = "http://" + url

        try:
            domain = urlparse(url).netloc.lower()

            suspicious_words = [
                "login",
                "verify",
                "secure",
                "account",
                "update",
                "bank",
                "free",
                "claim"
            ]

            if any(word in domain for word in suspicious_words):
                suspicious_urls.append(domain)

        except:
            pass

    # ---------------- RISK SCORE ----------------
    score = 0

    score += len(found) * 8
    score += len(suspicious_urls) * 20

    # Cap score at 100
    score = min(score, 100)

    if score >= 50:
        result = "🚨 High Risk Scam"
    elif score >= 20:
        result = "⚠️ Suspicious Message"
    else:
        result = "✅ Looks Safe"

    return result, found, suspicious_urls, score


# ---------------- BUTTON ----------------
if st.button("🔍 Analyze Message", use_container_width=True):

    if message.strip() == "":
        st.warning("Please enter a message first.")

    else:

        result, keywords, suspicious_urls, score = detect_scam(message)

        st.divider()

        # ---------------- RESULT ----------------
        st.subheader("🔎 Detection Result")

        if score >= 50:
            st.error(f"{result}")

        elif score >= 20:
            st.warning(f"{result}")

        else:
            st.success(f"{result}")

        # ---------------- RISK SCORE ----------------
        st.subheader("📊 Risk Score")

        st.progress(score / 100)

        st.write(f"**Risk Level: {score}%**")

        # ---------------- KEYWORDS ----------------
        if keywords:

            st.subheader("🚩 Detected Scam Indicators")

            for keyword in keywords:
                st.write(f"🔴 `{keyword}`")

        else:

            st.info("No obvious scam keywords detected.")

        # ---------------- URL CHECK ----------------
        st.subheader("🔗 URL Analysis")

        if suspicious_urls:

            st.error("⚠️ Potentially suspicious URL detected.")

            for url in suspicious_urls:
                st.write(f"🔴 `{url}`")

        elif re.findall(r'https?://[^\s]+|www\.[^\s]+', message):

            st.success("No obvious suspicious URL pattern detected.")

        else:

            st.info("No URL found in the message.")

        # ---------------- SAFETY ADVICE ----------------
        st.subheader("🛡️ Safety Recommendation")

        if score >= 50:

            st.error(
                "Do not click links, share OTPs, passwords, "
                "bank details, or other personal information."
            )

        elif score >= 20:

            st.warning(
                "Be careful. Verify the sender through an official "
                "website or trusted contact before taking action."
            )

        else:

            st.success(
                "No obvious scam indicators were found. "
                "Still verify unexpected messages before responding."
            )