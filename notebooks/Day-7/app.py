import streamlit as st
import pickle
import numpy as np
import pandas as pd

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Laptop Price Predictor",
    page_icon="💻",
    layout="wide"
)

# ---------------- LOAD MODEL ----------------
pipe = pickle.load(open('pipe.pkl', 'rb'))
df = pickle.load(open('df.pkl', 'rb'))

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;700&display=swap');

    :root {
        --bg-base:       #060B14;
        --bg-surface:    #0D1627;
        --bg-card:       #111827;
        --cyan:          #00D4FF;
        --cyan-glow:     rgba(0, 212, 255, 0.18);
        --amber:         #FF8C00;
        --amber-glow:    rgba(255, 140, 0, 0.15);
        --violet:        #8B5CF6;
        --violet-glow:   rgba(139, 92, 246, 0.18);
        --text-primary:  #F0F4FF;
        --text-secondary:#94A3B8;
        --text-muted:    #4B5A72;
        --border-subtle: rgba(255,255,255,0.06);
        --border-glow:   rgba(0,212,255,0.3);
    }

    html, body, [data-testid="stApp"] {
        background-color: var(--bg-base) !important;
        font-family: 'Space Grotesk', sans-serif !important;
        color: var(--text-primary) !important;
    }

    [data-testid="stApp"]::before {
        content: '';
        position: fixed;
        inset: 0;
        background-image:
            linear-gradient(rgba(0,212,255,0.03) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0,212,255,0.03) 1px, transparent 1px);
        background-size: 48px 48px;
        pointer-events: none;
        z-index: 0;
    }

    .block-container {
        padding: 2rem 2.5rem 3rem !important;
        max-width: 1180px !important;
        position: relative;
        z-index: 1;
    }

    .hero-banner {
        position: relative;
        overflow: hidden;
        background: linear-gradient(120deg, #060B14 0%, #0D1A2E 50%, #060B14 100%);
        border: 1px solid rgba(0,212,255,0.25);
        border-radius: 24px;
        padding: 42px 40px 38px;
        margin-bottom: 32px;
        text-align: center;
        box-shadow:
            0 0 0 1px rgba(0,212,255,0.08),
            0 20px 60px rgba(0,0,0,0.6),
            inset 0 1px 0 rgba(255,255,255,0.05);
    }

    .hero-banner::before {
        content: '';
        position: absolute;
        top: 0; left: 10%; right: 10%;
        height: 2px;
        background: linear-gradient(90deg, transparent, #00D4FF, #8B5CF6, #00D4FF, transparent);
        border-radius: 0 0 2px 2px;
        animation: shimmer-bar 3s ease-in-out infinite;
    }

    .hero-banner::after {
        content: '';
        position: absolute;
        top: -60px; left: 50%;
        transform: translateX(-50%);
        width: 400px; height: 200px;
        background: radial-gradient(ellipse, rgba(0,212,255,0.12) 0%, transparent 70%);
        pointer-events: none;
    }

    @keyframes shimmer-bar {
        0%, 100% { opacity: 0.6; }
        50%       { opacity: 1; }
    }

    .hero-chip {
        display: inline-block;
        background: rgba(0,212,255,0.1);
        border: 1px solid rgba(0,212,255,0.3);
        color: var(--cyan);
        font-family: 'JetBrains Mono', monospace;
        font-size: 11px;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        padding: 4px 14px;
        border-radius: 100px;
        margin-bottom: 18px;
    }

    .hero-title {
        font-size: 48px;
        font-weight: 700;
        letter-spacing: -0.02em;
        background: linear-gradient(135deg, #F0F4FF 30%, #00D4FF 70%, #8B5CF6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 0 0 10px;
        line-height: 1.15;
    }

    .hero-sub {
        color: var(--text-secondary);
        font-size: 16px;
        font-weight: 400;
        margin: 0;
        letter-spacing: 0.01em;
    }

    .section-label {
        font-family: 'JetBrains Mono', monospace;
        font-size: 10px;
        letter-spacing: 0.18em;
        text-transform: uppercase;
        color: var(--text-muted);
        margin-bottom: 4px;
    }

    .section-title {
        font-size: 18px;
        font-weight: 600;
        color: var(--text-primary);
        margin-bottom: 20px;
        display: flex;
        align-items: center;
        gap: 10px;
    }

    .section-title .icon-dot {
        width: 8px; height: 8px;
        border-radius: 50%;
        flex-shrink: 0;
    }

    .card-basic {
        background: var(--bg-card);
        border: 1px solid var(--border-subtle);
        border-top: 2px solid var(--cyan);
        border-radius: 20px;
        padding: 28px 26px 24px;
        margin-bottom: 20px;
        box-shadow:
            0 0 0 1px rgba(0,212,255,0.04),
            0 12px 40px rgba(0,0,0,0.4),
            0 0 30px rgba(0,212,255,0.04) inset;
    }

    .card-display {
        background: var(--bg-card);
        border: 1px solid var(--border-subtle);
        border-top: 2px solid var(--violet);
        border-radius: 20px;
        padding: 28px 26px 24px;
        margin-bottom: 20px;
        box-shadow:
            0 0 0 1px rgba(139,92,246,0.04),
            0 12px 40px rgba(0,0,0,0.4),
            0 0 30px rgba(139,92,246,0.04) inset;
    }

    .stSelectbox label,
    .stNumberInput label,
    .stSlider label {
        color: var(--text-secondary) !important;
        font-size: 13px !important;
        font-weight: 500 !important;
        letter-spacing: 0.02em !important;
        margin-bottom: 6px !important;
    }

    div[data-baseweb="select"] > div {
        background: #0D1627 !important;
        border: 1px solid rgba(255,255,255,0.09) !important;
        border-radius: 12px !important;
        color: var(--text-primary) !important;
        transition: border-color 0.25s, box-shadow 0.25s !important;
    }

    div[data-baseweb="select"] > div:focus-within,
    div[data-baseweb="select"] > div:hover {
        border-color: rgba(0,212,255,0.45) !important;
        box-shadow: 0 0 0 3px rgba(0,212,255,0.1) !important;
    }

    div[data-baseweb="input"] > div {
        background: #0D1627 !important;
        border: 1px solid rgba(255,255,255,0.09) !important;
        border-radius: 12px !important;
        color: var(--text-primary) !important;
        transition: border-color 0.25s, box-shadow 0.25s !important;
    }

    div[data-baseweb="input"] > div:focus-within,
    div[data-baseweb="input"] > div:hover {
        border-color: rgba(0,212,255,0.45) !important;
        box-shadow: 0 0 0 3px rgba(0,212,255,0.1) !important;
    }

    div[data-baseweb="input"] input {
        color: var(--text-primary) !important;
        font-family: 'Space Grotesk', sans-serif !important;
    }

    div[data-testid="stSlider"] > div > div > div {
        background: linear-gradient(90deg, var(--cyan), var(--violet)) !important;
    }

    div[data-testid="stSlider"] > div > div > div > div {
        background: white !important;
        box-shadow: 0 0 10px var(--cyan) !important;
    }

    ul[data-baseweb="menu"] {
        background: #111827 !important;
        border: 1px solid rgba(0,212,255,0.2) !important;
        border-radius: 12px !important;
        box-shadow: 0 20px 50px rgba(0,0,0,0.6) !important;
    }

    li[role="option"]:hover {
        background: rgba(0,212,255,0.1) !important;
        color: var(--cyan) !important;
    }

    div[data-testid="stButton"] > button {
        position: relative;
        width: 100%;
        background: linear-gradient(120deg, #0077B6 0%, #7B2FBE 50%, #0077B6 100%) !important;
        background-size: 200% auto !important;
        color: #fff !important;
        border: none !important;
        border-radius: 16px !important;
        padding: 18px 32px !important;
        font-family: 'Space Grotesk', sans-serif !important;
        font-size: 17px !important;
        font-weight: 700 !important;
        letter-spacing: 0.04em !important;
        cursor: pointer !important;
        transition:
            background-position 0.5s ease,
            transform 0.2s ease,
            box-shadow 0.3s ease !important;
        box-shadow:
            0 0 0 1px rgba(0,212,255,0.25),
            0 8px 32px rgba(0,119,182,0.45),
            0 0 60px rgba(0,212,255,0.1) !important;
        overflow: hidden !important;
    }

    div[data-testid="stButton"] > button::before {
        content: '';
        position: absolute;
        top: -50%; left: -50%;
        width: 200%; height: 200%;
        background: linear-gradient(
            to right,
            transparent 30%,
            rgba(255,255,255,0.08) 50%,
            transparent 70%
        );
        transform: skewX(-20deg);
        animation: btn-sheen 2.8s ease-in-out infinite;
    }

    @keyframes btn-sheen {
        0%   { transform: skewX(-20deg) translateX(-100%); }
        60%, 100% { transform: skewX(-20deg) translateX(250%); }
    }

    div[data-testid="stButton"] > button:hover {
        background-position: right center !important;
        transform: translateY(-3px) !important;
        box-shadow:
            0 0 0 1px rgba(0,212,255,0.4),
            0 16px 48px rgba(0,119,182,0.55),
            0 0 80px rgba(0,212,255,0.18) !important;
    }

    div[data-testid="stButton"] > button:active {
        transform: translateY(0px) !important;
    }

    .result-outer {
        position: relative;
        margin-top: 28px;
        border-radius: 20px;
        padding: 2px;
        background: linear-gradient(135deg, #00D4FF, #8B5CF6, #FF8C00);
        animation: border-spin 3s linear infinite;
        background-size: 200% 200%;
    }

    @keyframes border-spin {
        0%   { background-position: 0% 50%; }
        50%  { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    .result-inner {
        background: #060D1A;
        border-radius: 18px;
        padding: 32px 28px;
        text-align: center;
    }

    .result-label {
        font-family: 'JetBrains Mono', monospace;
        font-size: 11px;
        letter-spacing: 0.2em;
        text-transform: uppercase;
        color: var(--text-muted);
        margin-bottom: 10px;
    }

    .result-price {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 50px;
        font-weight: 700;
        letter-spacing: -0.03em;
        background: linear-gradient(90deg, #00D4FF, #8B5CF6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        line-height: 1.1;
    }

    .result-note {
        color: var(--text-muted);
        font-size: 13px;
        margin-top: 10px;
        letter-spacing: 0.02em;
    }

    .glow-divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(0,212,255,0.25), transparent);
        margin: 8px 0 20px;
    }

    [data-testid="column"] {
        padding: 0 8px !important;
    }

    #MainMenu, footer, header { visibility: hidden; }
    [data-testid="stToolbar"] { display: none; }

    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: var(--bg-base); }
    ::-webkit-scrollbar-thumb {
        background: rgba(0,212,255,0.3);
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown("""
<div class="hero-banner">
    <div class="hero-chip">AI-Powered Estimator</div>
    <div class="hero-title">💻 Laptop Price Predictor</div>
    <p class="hero-sub">Configure your specs below — get an instant price estimate powered by machine learning.</p>
</div>
""", unsafe_allow_html=True)

# ---------------- LAYOUT ----------------
left_col, right_col = st.columns([1.15, 1], gap="large")

# ---------------- LEFT SECTION ----------------
with left_col:
    st.markdown('<div class="card-basic">', unsafe_allow_html=True)
    st.markdown("""
        <div class="section-label">Section 01</div>
        <div class="section-title">
            <span class="icon-dot" style="background: #00D4FF; box-shadow: 0 0 8px #00D4FF;"></span>
            Basic Specifications
        </div>
        <div class="glow-divider"></div>
    """, unsafe_allow_html=True)

    company = st.selectbox('Brand', df['Company'].unique())
    type_name = st.selectbox('Laptop Type', df['TypeName'].unique())

    col1, col2 = st.columns(2)
    with col1:
        ram = st.selectbox('RAM (GB)', [2, 4, 6, 8, 12, 16, 24, 32, 64])
    with col2:
        weight = st.number_input('Weight (kg)', min_value=0.5, step=0.1, value=1.5)

    cpu = st.selectbox('CPU Brand', df['Cpu brand'].unique())
    gpu = st.selectbox('GPU Brand', df['Gpu brand'].unique())
    os = st.selectbox('Operating System', df['os'].unique())

    st.markdown('</div>', unsafe_allow_html=True)

# ---------------- RIGHT SECTION ----------------
with right_col:
    st.markdown('<div class="card-display">', unsafe_allow_html=True)
    st.markdown("""
        <div class="section-label">Section 02</div>
        <div class="section-title">
            <span class="icon-dot" style="background: #8B5CF6; box-shadow: 0 0 8px #8B5CF6;"></span>
            Display &amp; Storage
        </div>
        <div class="glow-divider"></div>
    """, unsafe_allow_html=True)

    col_a, col_b = st.columns(2)
    with col_a:
        touchscreen = st.selectbox('Touchscreen', ['No', 'Yes'])
    with col_b:
        ips = st.selectbox('IPS Display', ['No', 'Yes'])

    screen_size = st.slider('Screen Size (inches)', 10.0, 18.0, 13.0, step=0.1)

    resolution = st.selectbox(
        'Screen Resolution',
        ['1920x1080', '1366x768', '1600x900', '3840x2160',
         '3200x1800', '2880x1800', '2560x1600', '2560x1440', '2304x1440']
    )

    col3, col4 = st.columns(2)
    with col3:
        hdd = st.selectbox('HDD (GB)', [0, 128, 256, 512, 1024, 2048])
    with col4:
        ssd = st.selectbox('SSD (GB)', [0, 8, 128, 256, 512, 1024])

    st.markdown('</div>', unsafe_allow_html=True)

# ---------------- PREDICT BUTTON ----------------
st.markdown("<br>", unsafe_allow_html=True)
predict = st.button('🚀  Predict Laptop Price')

# ---------------- PREDICTION LOGIC ----------------
if predict:
    touchscreen_val = 1 if touchscreen == 'Yes' else 0
    ips_val = 1 if ips == 'Yes' else 0

    X_res = int(resolution.split('x')[0])
    Y_res = int(resolution.split('x')[1])
    ppi = ((X_res ** 2) + (Y_res ** 2)) ** 0.5 / screen_size

    # FIXED QUERY FORMAT
    query = pd.DataFrame([{
        'Company': company,
        'TypeName': type_name,
        'Ram': ram,
        'Weight': weight,
        'Touchscreen': touchscreen_val,
        'Ips': ips_val,
        'ppi': ppi,
        'Cpu brand': cpu,
        'HDD': hdd,
        'SSD': ssd,
        'Gpu brand': gpu,
        'os': os
    }])

    predicted_price = int(np.exp(pipe.predict(query)[0]))

    st.markdown(
        f"""
        <div class="result-outer">
            <div class="result-inner">
                <div class="result-label">Estimated Market Price</div>
                <div class="result-price">₹ {predicted_price:,}</div>
                <div class="result-note">Based on your selected configuration · Prices may vary by retailer</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )