import streamlit as st
import pandas as pd
import plotly.express as px
from src.data_loader import load_data_from_pdf
from src.validators import validate_data
from src.anomaly_detection import detect_anomalies

st.set_page_config(layout="wide")

st.title("🩺 Anomaly Detection în Date Medicale")

# Încarcă și procesează datele - foarte ineficient, datele dupa prima incarcare necesitand din nou incarcare
#with st.spinner("Se încarcă și procesează datele..."):
#    df = load_data_from_pdf("dataset.pdf")
#    df = validate_data(df)
#    df = detect_anomalies(df)

@st.cache_data
def load_and_process():
    df = load_data_from_pdf("dataset.pdf")
    df = validate_data(df)
    df = detect_anomalies(df)
    return df

df = load_and_process()


# Selectare tip de date afișate
filt = st.radio(
    "🔍 Ce vrei să vezi?",
    ["Toate datele", "Numai valide", "Numai invalide", "Anomalii AI", "Vârstnici obezi suspecți"],
    horizontal=True
)

if filt == "Numai valide":
    df_show = df[df["valid"]]
elif filt == "Numai invalide":
    df_show = df[~df["valid"]]
elif filt == "Anomalii AI":
    df_show = df[df["ai_anomaly"]]
elif filt == "Vârstnici obezi suspecți":
    df_show = df[df["suspect_elderly_obese"]]
else:
    df_show = df

# Afișare tabel
st.subheader("📊 Tabelul cu date")
st.dataframe(df_show, use_container_width=True)

# Afișare statistici
# ----------------------------------------
# 📉 1. Distribuția BMI
st.subheader("📉 Distribuția valorilor BMI")

fig_bmi = px.histogram(
    df[df["bmi"].notna()],
    x="bmi",
    nbins=40,
    title="Distribuție BMI",
    labels={"bmi": "BMI"},
    color_discrete_sequence=["indianred"]
)
st.plotly_chart(fig_bmi, use_container_width=True)

# ----------------------------------------
# ⚖️ 2. Distribuția greutății
st.subheader("⚖️ Distribuția greutății (kg)")

fig_weight = px.histogram(
    df[df["weight"].notna()],
    x="weight",
    nbins=40,
    title="Distribuție Greutate",
    labels={"weight": "Greutate (kg)"},
    color_discrete_sequence=["royalblue"]
)
st.plotly_chart(fig_weight, use_container_width=True)

# ----------------------------------------
# ✅ 3. Comparativ: valid vs. invalid vs. AI anomaly
st.subheader("📌 Validare vs. Anomalii AI")

df_stats = pd.DataFrame({
    "Categorie": ["Valide", "Invalide", "AI Anomalii"],
    "Număr": [
        df["valid"].sum(),
        (~df["valid"]).sum(),
        df["ai_anomaly"].sum()
    ]
})

fig_compare = px.bar(
    df_stats,
    x="Categorie",
    y="Număr",
    title="Comparativ: Cazuri Valide / Invalide / AI",
    color="Categorie",
    color_discrete_map={
        "Valide": "green",
        "Invalide": "red",
        "AI Anomalii": "orange"
    }
)
st.plotly_chart(fig_compare, use_container_width=True)

# ----------------------------------------
# 🧭 4. Scatter plot Age vs BMI
st.subheader("🧭 Vârstă vs. BMI (colorat după AI anomaly)")

fig_scatter = px.scatter(
    df[df["bmi"].notna() & df["age"].notna()],
    x="age",
    y="bmi",
    color="ai_anomaly",
    labels={"age": "Vârstă", "bmi": "BMI"},
    title="Distribuție Vârstă vs. BMI (AI Anomaly)",
    color_discrete_map={True: "red", False: "blue"},
    hover_data=["weight", "height"]
)
st.plotly_chart(fig_scatter, use_container_width=True)

# ----------------------------------------
# 📏 5. Distribuția înălțimii
st.subheader("📏 Distribuția înălțimii (cm)")

fig_height = px.histogram(
    df[df["height"].notna()],
    x="height",
    nbins=40,
    title="Distribuție Înălțime",
    labels={"height": "Înălțime (cm)"},
    color_discrete_sequence=["purple"]
)
st.plotly_chart(fig_height, use_container_width=True)


