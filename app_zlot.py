import streamlit as st
import pandas as pd

st.set_page_config(page_title="Zgłoszenia na zajęcia Zlotowe 68 HRŚ", layout="wide")

# -----------------------------
# DANE
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

def patrol_istnieje(df, patrol):
    return (df == patrol).any().any()

st.title("📋 Zgłoszenia na zajęcia Zlotowe 68 HRŚ")

zakladka = st.radio(
    "Wybierz wydarzenie",
    ["Świętuchobranie", "Warsztaty z programowania"]
)

# =============================
# ŚWIĘTUCHOBRANIE
# =============================
if zakladka == "Świętuchobranie":
    st.subheader("Świętuchobranie")

    df = st.session_state.tabela_swietuchobranie
    st.dataframe(df, use_container_width=True)

    st.subheader("Zgłoszenie patrolu")

    # --- wybór tylko KOMÓRKI ---
    komorki = [(t, s) for t in df.index for s in df.columns]

    wybor = st.selectbox(
        "Wybierz dostępny slot",
        komorki,
        format_func=lambda x: f"{x[0]} - {x[1]}"
    )

    godzina, slot = wybor

    st.info(f"Wybrano: godzina **{godzina}**, slot **{slot}**")

    patrol = st.text_input("Nazwa patrolu")

    if st.button("Zapisz się"):
        df = st.session_state.tabela_swietuchobranie

        if patrol_istnieje(df, patrol):
            st.error("Ten patrol już jest zapisany!")
        elif df.loc[godzina, slot] != "":
            st.error("Ten slot jest już zajęty!")
        else:
            st.session_state.tabela_swietuchobranie.loc[godzina, slot] = patrol
            st.success("Zapisano patrol!")
            st.rerun()

# =============================
# WARSZTATY
# =============================
else:
    st.subheader("Warsztaty z programowania")

    df = st.session_state.tabela_programowanie
    st.dataframe(df, use_container_width=True)

    st.subheader("Zgłoszenie patrolu")

    komorki = [(t, s) for t in df.index for s in df.columns]

    wybor = st.selectbox(
        "Wybierz dostępny slot",
        komorki,
        format_func=lambda x: f"{x[0]} - {x[1]}"
    )

    godzina, slot = wybor

    st.info(f"Wybrano: godzina **{godzina}**, slot **{slot}**")

    patrol = st.text_input("Nazwa patrolu")

    if st.button("Zapisz się"):
        df = st.session_state.tabela_programowanie

        if patrol_istnieje(df, patrol):
            st.error("Ten patrol już jest zapisany!")
        elif df.loc[godzina, slot] != "":
            st.error("Ten slot jest już zajęty!")
        else:
            st.session_state.tabela_programowanie.loc[godzina, slot] = patrol
            st.success("Zapisano patrol!")
            st.rerun()
