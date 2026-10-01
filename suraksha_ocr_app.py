import streamlit as st
from ocr_engine import extract_text
from safety_analyzer import analyze_text
from link_checker import check_link
import tempfile
import os


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="SurakshaAI",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# =========================================================
# LOAD CSS
# =========================================================

def load_css():
    try:
        with open("style.css", "r", encoding="utf-8") as file:
            st.markdown(
                f"<style>{file.read()}</style>",
                unsafe_allow_html=True
            )
    except FileNotFoundError:
        pass


load_css()


# =========================================================
# SESSION STATE
# =========================================================

if "active_scanner" not in st.session_state:
    st.session_state.active_scanner = "Home"


# =========================================================
# HEADER
# =========================================================

st.markdown(
    """
    <div class="main-title">
        🛡️ SurakshaAI
    </div>

    <div class="subtitle">
        Your Digital Safety Companion
    </div>

    <p style="text-align:center;">
        Check suspicious messages, screenshots and website links
        before taking action.
    </p>
    """,
    unsafe_allow_html=True
)


# =========================================================
# NAVIGATION
# =========================================================

st.markdown("### 🧭 Navigation")

nav1, nav2, nav3, nav4 = st.columns(4)

with nav1:
    if st.button(
        "🏠 Home",
        use_container_width=True
    ):
        st.session_state.active_scanner = "Home"

with nav2:
    if st.button(
        "💬 Message",
        use_container_width=True
    ):
        st.session_state.active_scanner = "Message"

with nav3:
    if st.button(
        "📷 Screenshot",
        use_container_width=True
    ):
        st.session_state.active_scanner = "Screenshot"

with nav4:
    if st.button(
        "🔗 Link",
        use_container_width=True
    ):
        st.session_state.active_scanner = "Link"


st.divider()


# =========================================================
# HOME DASHBOARD
# =========================================================

if st.session_state.active_scanner == "Home":

    st.markdown(
        '<div class="section-title">🏠 Safety Dashboard</div>',
        unsafe_allow_html=True
    )

    st.write(
        "Choose a tool to check suspicious digital content."
    )

    st.write("")


    # -----------------------------------------------------
    # FEATURE CARDS
    # -----------------------------------------------------

    col1, col2, col3 = st.columns(3)

    with col1:

        st.markdown(
            """
            ## 💬

            ### Message Scanner

            Check SMS, WhatsApp messages and emails
            for suspicious warning signs.
            """
        )

        if st.button(
            "Open Message Scanner",
            key="home_message",
            use_container_width=True
        ):
            st.session_state.active_scanner = "Message"
            st.rerun()


    with col2:

        st.markdown(
            """
            ## 📷

            ### Screenshot Scanner

            Upload a screenshot and extract text
            using OCR technology.
            """
        )

        if st.button(
            "Open Screenshot Scanner",
            key="home_screenshot",
            use_container_width=True
        ):
            st.session_state.active_scanner = "Screenshot"
            st.rerun()


    with col3:

        st.markdown(
            """
            ## 🔗

            ### Link Scanner

            Check website URLs for common suspicious
            patterns and warning signs.
            """
        )

        if st.button(
            "Open Link Scanner",
            key="home_link",
            use_container_width=True
        ):
            st.session_state.active_scanner = "Link"
            st.rerun()


    st.divider()


    # -----------------------------------------------------
    # SAFETY STATUS
    # -----------------------------------------------------

    st.markdown(
        '<div class="section-title">🛡️ Protection Status</div>',
        unsafe_allow_html=True
    )

    status1, status2, status3 = st.columns(3)

    with status1:
        st.success(
            "💬 Message Protection\n\nREADY"
        )

    with status2:
        st.success(
            "📷 Screenshot OCR\n\nREADY"
        )

    with status3:
        st.success(
            "🔗 Link Protection\n\nREADY"
        )


    st.divider()


    # -----------------------------------------------------
    # SAFETY TIPS
    # -----------------------------------------------------

    st.markdown(
        '<div class="section-title">🚨 Digital Safety Tips</div>',
        unsafe_allow_html=True
    )

    tip1, tip2 = st.columns(2)

    with tip1:

        st.info(
            """
            **🔐 Never share sensitive information**

            • OTP  
            • UPI PIN  
            • ATM PIN  
            • CVV  
            • Passwords  
            • Banking credentials
            """
        )

    with tip2:

        st.warning(
            """
            **⚠️ Before clicking a link**

            • Check the sender  
            • Check the domain  
            • Don't trust urgent requests  
            • Verify through an official source
            """
        )


# =========================================================
# MESSAGE SCANNER
# =========================================================

elif st.session_state.active_scanner == "Message":

    st.markdown(
        '<div class="section-title">💬 Message Scanner</div>',
        unsafe_allow_html=True
    )

    st.write(
        "Paste a suspicious SMS, WhatsApp message or email."
    )

    message = st.text_area(
        "Message",
        height=200,
        placeholder=(
            "Example:\n\n"
            "URGENT! Your bank account will be blocked.\n"
            "Verify your account immediately.\n"
            "Send your OTP."
        )
    )

    if st.button(
        "🔍 Analyze Message",
        key="analyze_message",
        use_container_width=True
    ):

        if not message.strip():

            st.warning(
                "Please enter a message first."
            )

        else:

            result = analyze_text(message)

            st.subheader("📊 Analysis Result")

            if result["risk_level"] == "HIGH RISK":

                st.error(
                    f"🔴 HIGH RISK\n\n"
                    f"Risk Score: {result['risk_score']}/100"
                )

            elif result["risk_level"] == "MEDIUM RISK":

                st.warning(
                    f"🟡 MEDIUM RISK\n\n"
                    f"Risk Score: {result['risk_score']}/100"
                )

            else:

                st.success(
                    f"🟢 LOW RISK\n\n"
                    f"Risk Score: {result['risk_score']}/100"
                )


            if result["high_risk_indicators"]:

                st.write("### 🚨 High-Risk Indicators")

                for item in result["high_risk_indicators"]:
                    st.write(f"• {item}")


            if result["medium_risk_indicators"]:

                st.write("### ⚠️ Warning Indicators")

                for item in result["medium_risk_indicators"]:
                    st.write(f"• {item}")


            if result["detected_urls"]:

                st.write("### 🔗 Detected Links")

                for url in result["detected_urls"]:
                    st.code(url)


            st.write("### 🛡️ Safety Recommendation")

            st.info(
                result["recommendation"]
            )


# =========================================================
# SCREENSHOT SCANNER
# =========================================================

elif st.session_state.active_scanner == "Screenshot":

    st.markdown(
        '<div class="section-title">📷 Screenshot Scanner</div>',
        unsafe_allow_html=True
    )

    st.write(
        "Upload a screenshot of a suspicious message."
    )

    uploaded_file = st.file_uploader(
        "Choose an image",
        type=["png", "jpg", "jpeg"]
    )


    if uploaded_file is not None:

        st.image(
            uploaded_file,
            caption="Uploaded Screenshot",
            use_container_width=True
        )


        if st.button(
            "🔍 Analyze Screenshot",
            key="analyze_screenshot",
            use_container_width=True
        ):

            temp_path = None

            try:

                with tempfile.NamedTemporaryFile(
                    delete=False,
                    suffix=".png"
                ) as temp_file:

                    temp_file.write(
                        uploaded_file.getbuffer()
                    )

                    temp_path = temp_file.name


                # OCR
                extracted_text = extract_text(
                    temp_path
                )


                st.subheader("📝 Extracted Text")


                if extracted_text:

                    st.text_area(
                        "OCR Result",
                        extracted_text,
                        height=200
                    )


                    # Analyze OCR text
                    result = analyze_text(
                        extracted_text
                    )


                    st.subheader(
                        "📊 Analysis Result"
                    )


                    if result["risk_level"] == "HIGH RISK":

                        st.error(
                            f"🔴 HIGH RISK\n\n"
                            f"Risk Score: "
                            f"{result['risk_score']}/100"
                        )

                    elif result["risk_level"] == "MEDIUM RISK":

                        st.warning(
                            f"🟡 MEDIUM RISK\n\n"
                            f"Risk Score: "
                            f"{result['risk_score']}/100"
                        )

                    else:

                        st.success(
                            f"🟢 LOW RISK\n\n"
                            f"Risk Score: "
                            f"{result['risk_score']}/100"
                        )


                    st.write(
                        "### 🛡️ Safety Recommendation"
                    )

                    st.info(
                        result["recommendation"]
                    )


                else:

                    st.warning(
                        "No readable text was detected."
                    )


            except Exception as error:

                st.error(
                    f"OCR Error: {error}"
                )


            finally:

                if (
                    temp_path
                    and os.path.exists(temp_path)
                ):
                    os.remove(temp_path)


# =========================================================
# LINK SCANNER
# =========================================================

elif st.session_state.active_scanner == "Link":

    st.markdown(
        '<div class="section-title">🔗 Link Scanner</div>',
        unsafe_allow_html=True
    )

    st.write(
        "Paste a website URL to check common warning signs."
    )

    url = st.text_input(
        "Website URL",
        placeholder="https://example.com"
    )


    if st.button(
        "🔍 Check Link",
        key="analyze_link",
        use_container_width=True
    ):

        if not url.strip():

            st.warning(
                "Please enter a website URL."
            )

        else:

            result = check_link(url)


            st.subheader(
                "📊 Link Analysis"
            )


            if result["risk_level"] == "HIGH RISK":

                st.error(
                    f"🔴 HIGH RISK\n\n"
                    f"Risk Score: "
                    f"{result['risk_score']}/100"
                )

            elif result["risk_level"] == "MEDIUM RISK":

                st.warning(
                    f"🟡 MEDIUM RISK\n\n"
                    f"Risk Score: "
                    f"{result['risk_score']}/100"
                )

            else:

                st.success(
                    f"🟢 LOW RISK\n\n"
                    f"Risk Score: "
                    f"{result['risk_score']}/100"
                )


            st.write(
                "### ⚠️ Detected Indicators"
            )


            for reason in result["reasons"]:

                st.write(
                    f"• {reason}"
                )


            st.info(
                "A low-risk result does not guarantee that "
                "a website is completely safe. Always verify "
                "the source before entering sensitive information."
            )


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.markdown(
    """
    <div class="footer">

        🛡️ <b>SurakshaAI V1</b>

        <br><br>

        Digital Safety Awareness Prototype

        <br><br>

        Stay Alert • Stay Safe • Think Before You Click

    </div>
    """,
    unsafe_allow_html=True
)