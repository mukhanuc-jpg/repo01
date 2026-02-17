#
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import streamlit as st
import base64
import pandas as pd

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="2026 Goals Dashboard", layout="wide")

# ---------------- LOAD IMAGE ----------------
# Using your local path
image_path = "/Users/cynthiamukhanu/Documents/Rorisang/Cynthia's 2026 goals in focus.png"

try:
    with open(image_path, "rb") as img_file:
        encoded = base64.b64encode(img_file.read()).decode()
except FileNotFoundError:
    encoded = ""

# ---------------- PINK THEME CUSTOM CSS ----------------
st.markdown(
  f"""
    <style>
    /* Main background - Pastel Orchid (The Pink-Purple Mix) */
    .stApp {{
        background-color: #F4BBFF; 
    }}

    /* Sidebar - The Deep Pink you loved (#C71585) */
    [data-testid="stSidebar"] {{
        background-color: #C71585 !important;
    }}

    /* Sidebar Text - Bold White */
    [data-testid="stSidebar"] .stRadio label, [data-testid="stSidebar"] h1 {{
        color: white !important;
        font-weight: bold;
    }}

    /* Headers and Text - Deep Pink to pop against the Orchid background */
    h1, h2, h3 {{
        color: #C71585 !important;
        font-weight: 800;
    }}
    
    p, label {{
        color: #4B0082 !important; /* Deep Indigo for clear reading */
    }}

    /* Sliders & Progress Bars - Deep Pink to match the sidebar */
    .stSlider > div [data-baseweb="slider"] > div {{
        background-color: #C71585; 
    }}

    .stProgress > div > div > div > div {{
        background-color: #C71585;
    }}

    .goal-image {{
        display:flex;
        justify-content:center;
        padding-bottom: 20px;
    }}
    </style>

    <div class="goal-image">
        {"<img src='data:image/png;base64," + encoded + "' width='500'>" if encoded else ""}
    </div>
    """,
    unsafe_allow_html=True
)

# ---------------- DATA ----------------
goals_dict = {
    "q1": ["Do 21 days fasting", "Buy two books 📚", "Gym 4x/week", "Create Streamlit vision board", "Monthly self pamper", "Reduce sugar intake"],
    "q2": ["Read at least two books 📚", "Gym 4x/week", "Monthly self pamper", "Master software installation", "Garden Route vacation 🏖️", "Max TFSA for the Quarter"],
    "q3": ["Max TFSA for the Quarter", "Lesotho Camp", "Read two books 📚", "Gym 4x/week", "Monthly self pamper"],
    "q4": ["Present at a Conference", "Finish PhD lab work", "MSC Cruise 🏖️", "Max TFSA", "Publish a paper", "Get Rorisang a school"]
}

# ---------------- SESSION STATE ----------------
for key, goals in goals_dict.items():
    if key not in st.session_state:
        st.session_state[key] = {g: 0 for g in goals}

# ---------------- SIDEBAR ----------------
st.sidebar.title("Navigation")
menu = st.sidebar.radio(
    "Go to:",
    ["Home", "1st Quarter", "2nd Quarter", "3rd Quarter", "4th Quarter", "Updates", "Rewards"]
)

# ---------------- GOAL PAGE FUNCTION ----------------
def goal_page(title, state_key):
    st.header(title)
    progress_data = []

    for g in goals_dict[state_key]:
        col1, col2 = st.columns([4, 1])
        with col1:
            val = st.slider(g, 0, 100, int(st.session_state[state_key][g]), key=f"s_{state_key}_{g}")
        with col2:
            done = st.checkbox("Done", key=f"d_{state_key}_{g}", value=(val == 100))
            if done: val = 100
        
        st.session_state[state_key][g] = val
        progress_data.append({"Goal": g, "Progress": val})

    st.subheader("📊 Progress Overview")
    df = pd.DataFrame(progress_data)
    st.bar_chart(df.set_index("Goal"), color="#D81B60")

# ---------------- PAGES ----------------
if menu == "Home":
    st.title("🎯 Cynthia's 2026 Goals Dashboard")
    st.write("### Focus: Career • Health • Family • Growth")
    
    st.divider()
    
    # Calculate Total Progress
    all_vals = []
    for q in goals_dict.keys():
        all_vals.extend(st.session_state[q].values())
    
    overall = sum(all_vals) / len(all_vals) if all_vals else 0
    
    col1, col2 = st.columns(2)
    col1.metric("Overall 2026 Progress", f"{overall:.1f}%")
    col2.progress(overall/100)
    
    st.write("---")
    st.info("Tip: Use the sidebar to update your quarterly milestones!")

elif menu == "1st Quarter": goal_page("📅 Q1: Fresh Starts", "q1")
elif menu == "2nd Quarter": goal_page("📅 Q2: Building Momentum", "q2")
elif menu == "3rd Quarter": goal_page("📅 Q3: Staying Consistent", "q3")
elif menu == "4th Quarter": goal_page("📅 Q4: Finishing Strong", "q4")

elif menu == "Updates":
    st.header("📝 Notes & Reflections")
    notes = st.text_area("What's on your mind today?", height=300)

elif menu == "Rewards":
    st.header("🎁 Rewards")
    rewards = [
        ("Baking gloves", ""),
        ("Apron", ""),
        ("Country Road caramel bag", "https://www.countryroad.com/Product/60261122-119/?colour=Sand"),
        ("Steve Madden sandals brown", "https://stevemadden.co.za/products/arrows-bone"),
        ("Ted Baker laptop bag", "https://tedbaker.co.za/collections/womens-designer-bags/products/womens-crikon-extra-large-icon-bag-283872-001"),
        ("Tall champagne glasses", "https://www.mrphome.com/en_za/4-pack-vin-champagne-flutes-102443128"),
        ("Small black designer bag 🛍️", ""),
        ("K-Way small travel bag", "https://www.capeunionmart.co.za/products/k-way-contour-100l-luggage-bag/105185083.html")
    ]
    for name, url in rewards:
        st.checkbox(name, key=f"reward_{name}")
        if url:
            st.markdown(f"   [🔗 View item]({url})")