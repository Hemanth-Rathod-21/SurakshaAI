import streamlit as st
from ocr_engine import extract_text
from safety_analyzer import analyze_text


# -----------------------------
# Page configuration
# -----------------------------
st.set_page_config(
    page_title="SurakshaAI",
    page_icon="🛡️",
    layout="centered"
)


# -----------------------------
# Header
# -----------------------------
st.title("🛡️ SurakshaAI")
st.subheader("AI-Powered Digital Safety Companion")

st.write(
    "Upload a screenshot of a suspicious message and "
    "SurakshaAI will extract the text and check for "
    "potential safety risks."
)

st.divider()


# -----------------------------
# Image upload
# -----------------------------
uploaded_file = st.file_uploader(
    "📷 Upload a screenshot",
    type=["png", "jpg", "jpeg"]
)


# -----------------------------
# Analyze image
# -----------------------------
if uploaded_file is not None:

    st.image(
        uploaded_file,
        caption="Uploaded Screenshot",
        use_container_width=True
    )

    if st.button("🔍 Analyze Screenshot", type="primary"):

        # Save uploaded image temporarily
        temp_image = "uploaded_image.png"

        with open(temp_image, "wb") as file:
            file.write(uploaded_file.getbuffer())

        # OCR
        with st.spinner("Reading screenshot..."):
            extracted_text = extract_text(temp_image)

        if not extracted_text:

            st.error("❌ No readable text was detected.")

        else:

            # Display extracted text
            st.subheader("📝 Extracted Text")

            st.text_area(
                "OCR Result",
                extracted_text,
                height=180
            )

            # Analyze
            with st.spinner("Analyzing message..."):
                result = analyze_text(extracted_text)

            st.divider()

            # Risk result
            st.subheader("🛡️ Safety Analysis")

            risk_level = result["risk_level"]
            risk_score = result["risk_score"]

            if risk_level == "HIGH RISK":

                st.error(
                    f"🚨 {risk_level} — Risk Score: {risk_score}/100"
                )

            elif risk_level == "MEDIUM RISK":

                st.warning(
                    f"⚠️ {risk_level} — Risk Score: {risk_score}/100"
                )

            else:

                st.success(
                    f"✅ {risk_level} — Risk Score: {risk_score}/100"
                )

            # Indicators
            st.subheader("🔎 Warning Indicators")

            if result["high_risk_indicators"]:

                st.write("**High-risk indicators:**")

                for item in result["high_risk_indicators"]:
                    st.write(f"• {item}")

            if result["medium_risk_indicators"]:

                st.write("**Medium-risk indicators:**")

                for item in result["medium_risk_indicators"]:
                    st.write(f"• {item}")

            if not (
                result["high_risk_indicators"]
                or result["medium_risk_indicators"]
            ):

                st.write("No major warning indicators detected.")

            # URLs
            if result["detected_urls"]:

                st.subheader("🔗 Detected Links")

                for url in result["detected_urls"]:
                    st.code(url)

            # Recommendation
            st.subheader("💡 Safety Recommendation")

            st.info(result["recommendation"])


# -----------------------------
# Footer
# -----------------------------
st.divider()

st.caption(
    "SurakshaAI V1 — Prototype for digital safety awareness"
)