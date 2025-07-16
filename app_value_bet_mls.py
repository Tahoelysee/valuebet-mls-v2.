
import streamlit as st
import pandas as pd

# Titre
st.title("Analyse Value Bet MLS - 1N2 et Over 2.5")

# Chargement des données
@st.cache_data
def load_data():
    return pd.read_csv("dataset_mls.csv")

df = load_data()

# Filtrage des données
st.sidebar.header("Filtres")
home_team = st.sidebar.selectbox("Équipe à domicile", ["Toutes"] + sorted(df["home_team"].unique().tolist()))
away_team = st.sidebar.selectbox("Équipe à l'extérieur", ["Toutes"] + sorted(df["away_team"].unique().tolist()))

filtered = df.copy()
if home_team != "Toutes":
    filtered = filtered[filtered["home_team"] == home_team]
if away_team != "Toutes":
    filtered = filtered[filtered["away_team"] == away_team]

# Onglets
tab1, tab2 = st.tabs(["Over 2.5", "1N2"])

with tab1:
    st.subheader("Value Bet - Over 2.5")
    if "proba_over25" in filtered.columns:
        filtered["value_over25"] = filtered["proba_over25"] * filtered["cote_over25"]
        value_bets = filtered[filtered["value_over25"] > 1]
        st.dataframe(value_bets[["home_team", "away_team", "proba_over25", "cote_over25", "value_over25"]])
    else:
        st.warning("Colonnes manquantes pour le calcul du Value Bet sur Over 2.5.")

with tab2:
    st.subheader("Value Bet - 1N2")
    if "proba_home_win" in filtered.columns:
        filtered["value_home"] = filtered["proba_home_win"] * filtered["odd_home_win"]
        filtered["value_draw"] = filtered["proba_draw"] * filtered["odd_draw"]
        filtered["value_away"] = filtered["proba_away_win"] * filtered["odd_away_win"]
        filtered["max_value"] = filtered[["value_home", "value_draw", "value_away"]].max(axis=1)
        value_bets_1n2 = filtered[filtered["max_value"] > 1]
        st.dataframe(value_bets_1n2[["home_team", "away_team", "proba_home_win", "odd_home_win",
                                     "proba_draw", "odd_draw", "proba_away_win", "odd_away_win",
                                     "value_home", "value_draw", "value_away"]])
    else:
        st.warning("Colonnes manquantes pour le calcul du Value Bet 1N2.")
