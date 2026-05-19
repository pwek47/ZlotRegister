import streamlit as st
import pandas as pd

st.set_page_config(page_title="Zlot - Zgłoszenia", layout="wide")

# -----------------------------
# DANE TABLIC
# -----------------------------
if "tabela_swietuchobranie" not in st.session_state:
    godziny = ["16:00","16:30","17:00","17:30","18:00","18:30","19:00"]
    st.session_state.tabela_swietuchobranie = pd.DataFrame(
        "", index=godziny, columns=[f"Slot {i}" for i in range(1, 10)]
    )

if "tabela_programowanie" not in st.session_state:
    godziny = ["16:00","17:00","18:00","19:00"]
    st.session_state.tabela_programowanie = pd.DataFrame(
        "", index=godziny, columns=["Slot A", "Slot B"]
    )

# -----------------------------
# FUNKCJA SPRAWDZAJĄCA CZY PATROL JUŻ JEST
# -----------------------------
def patrol_istnieje(df, patrol):
    return (df == patrol).any().any()

# -----------------------------
# UI
# -----------------------------
st.title("📋 Zgłoszenia na Zlot")

zakladka = st.radio(
    "Wybierz wydarzenie",
    ["Świętuchobranie", "Warsztaty z programowania"]
)

# =============================
# ŚWIĘTUCHOBRANIE
# =============================
if zakladka == "Świętuchobranie":
    st.subheader("Świętuchobranie")

    st.dataframe(st.session_state.tabela_swietuchobranie, use_container_width=True)

    st.subheader("Zgłoszenie patrolu")

    godzina = st.selectbox("Godzina", st.session_state.tabela_swietuchobranie.index)
    slot = st.selectbox("Slot", st.session_state.tabela_swietuchobranie.columns)
    patrol = st.text_input("Nazwa patrolu")

    if st.button("Zapisz się"):
        df = st.session_state.tabela_swietuchobranie

        if patrol_istnieje(df, patrol):
            st.error("Ten patrol już jest zapisany w tej tabeli!")
        elif df.loc[godzina, slot] != "":
            st.error("Ten slot jest już zajęty!")
        else:
            st.session_state.tabela_swietuchobranie.loc[godzina, slot] = patrol
            st.success("Zapisano patrol!")
            st.rerun()

# =============================
# WARSZTATY Z PROGRAMOWANIA
# =============================
elif zakladka == "Warsztaty z programowania":
    st.subheader("Warsztaty z programowania")

    st.dataframe(st.session_state.tabela_programowanie, use_container_width=True)

    st.subheader("Zgłoszenie patrolu")

    godzina = st.selectbox("Godzina", st.session_state.tabela_programowanie.index)
    slot = st.selectbox("Slot", st.session_state.tabela_programowanie.columns)
    patrol = st.text_input("Nazwa patrolu")

    if st.button("Zapisz się"):
        df = st.session_state.tabela_programowanie

        if patrol_istnieje(df, patrol):
            st.error("Ten patrol już jest zapisany w tej tabeli!")
        elif df.loc[godzina, slot] != "":
            st.error("Ten slot jest już zajęty!")
        else:
            st.session_state.tabela_programowanie.loc[godzina, slot] = patrol
            st.success("Zapisano patrol!")
            st.rerun()
