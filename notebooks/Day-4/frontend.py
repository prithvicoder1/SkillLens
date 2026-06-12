import streamlit as st
import requests

# ---------------- PAGE CONFIG ---------------- #
st.set_page_config(
    page_title="Insurance Premium Predictor",
    page_icon="🏥",
    layout="wide"
)

API_URL = "http://127.0.0.1:8000/predict"

# ---------------- CUSTOM CSS ---------------- #
st.markdown("""
<style>
.main {
    background-color: #0E1117;
}

.hero {
    padding: 2rem;
    border-radius: 20px;
    background: linear-gradient(135deg,#4F46E5,#06B6D4);
    text-align: center;
    color: white;
    margin-bottom: 2rem;
}

.hero h1{
    font-size: 3rem;
    margin-bottom:0;
}

.hero p{
    font-size:1.1rem;
    opacity:0.9;
}

.card {
    background-color: #1E1E1E;
    padding: 20px;
    border-radius: 15px;
    border: 1px solid #333;
}

.result-card {
    background: linear-gradient(135deg,#16A34A,#22C55E);
    padding: 20px;
    border-radius: 15px;
    color: white;
    text-align:center;
    margin-top:20px;
}

.stButton > button {
    width: 100%;
    height: 55px;
    border-radius: 12px;
    font-size: 18px;
    font-weight: bold;
    background: linear-gradient(90deg,#4F46E5,#06B6D4);
    color: white;
    border: none;
}

.stButton > button:hover {
    transform: scale(1.02);
    transition: 0.3s;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HERO SECTION ---------------- #
st.markdown("""
<div class="hero">
    <h1>🏥 Insurance Premium Predictor</h1>
    <p>AI Powered Insurance Risk & Premium Prediction System</p>
</div>
""", unsafe_allow_html=True)

# ---------------- INPUT SECTION ---------------- #
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 👤 Personal Information")
    age = st.number_input(
        "Age",
        min_value=1,
        max_value=119,
        value=30
    )

    weight = st.number_input(
        "Weight (kg)",
        min_value=1.0,
        value=70.0
    )

    height = st.number_input(
        "Height (m)",
        min_value=0.5,
        max_value=2.5,
        value=1.75
    )

    smoker = st.selectbox(
        "Smoking Status",
        [False, True]
    )

with col2:
    st.markdown("### 💼 Financial Information")

    income_lpa = st.number_input(
        "Annual Income (LPA)",
        min_value=0.1,
        value=10.0
    )

    city = st.text_input(
        "City",
        value="Delhi"
    )

    occupation = st.selectbox(
        "Occupation",
        [
            "retired",
            "freelancer",
            "student",
            "government_job",
            "business_owner",
            "unemployed",
            "private_job"
        ]
    )

# ---------------- BMI DISPLAY ---------------- #
bmi = weight / (height ** 2)

st.markdown("---")
col_a, col_b, col_c = st.columns(3)

with col_a:
    st.metric("📅 Age", age)

with col_b:
    st.metric("⚖️ Weight", f"{weight} kg")

with col_c:
    st.metric("📊 BMI", f"{bmi:.2f}")

st.markdown("---")

# ---------------- PREDICT BUTTON ---------------- #
if st.button("🚀 Predict Insurance Premium"):

    payload = {
        "age": age,
        "weight": weight,
        "height": height,
        "income_lpa": income_lpa,
        "smoker": smoker,
        "city": city,
        "occupation": occupation
    }

    try:
        with st.spinner("Analyzing Risk Profile..."):

            response = requests.post(
                API_URL,
                json=payload
            )

        if response.status_code == 200:

            result = response.json()

            st.success("Prediction Completed Successfully ✅")

            if "predicted_premium" in result:

                premium = result["predicted_premium"]

                st.markdown(f"""
                <div class="result-card">
                    <h2>Predicted Insurance Premium</h2>
                    <h1>₹ {premium:,.2f}</h1>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("### 📋 API Response")
            st.json(result)

        else:
            st.error(f"API Error: {response.status_code}")
            st.json(response.json())

    except requests.exceptions.ConnectionError:
        st.error(
            "❌ Unable to connect to FastAPI server.\n\n"
            "Make sure FastAPI is running:\n"
            "uvicorn app:app --reload"
        )

    except Exception as e:
        st.error(f"Error: {str(e)}")

# ---------------- FOOTER ---------------- #
st.markdown("---")
st.markdown(
    "<center>Made with ❤️ using FastAPI + Streamlit + Machine Learning</center>",
    unsafe_allow_html=True
)