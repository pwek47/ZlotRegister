import streamlit as st
import pandas as pd

st.set_page_config(page_title="Zgłoszenia Zlotowe 68 HRŚ", layout="wide")

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

st.title("📋 Zgłoszenia Zlotowe 68 HRŚ")

zakladka = st.radio(
    "Wybierz wydarzenie",
    ["Świętuchobranie", "Warsztaty z programowania"]
)

# =============================
# FUNKCJA UI
# =============================
def zapis(df):
    st.dataframe(df, use_container_width=True)

    # wszystkie komórki jako lista (bez pokazywania struktury)
    komorki = [(r, c) for r in df.index for c in df.columns]

    wybor = st.selectbox("Wybierz pole w tabeli", komorki)

    patrol = st.text_input("Numer patrolu")

    if st.button("Zapisz"):
        r, c = wybor

        if patrol_istnieje(df, patrol):
            st.error("Ten patrol już jest zapisany!")
        elif df.loc[r, c] != "":
            st.error("To pole jest już zajęte!")
        else:
            df.loc[r, c] = patrol
            st.success("Zapisano!")
            st.rerun()

# =============================
# ŚWIĘTUCHOBRANIE
# =============================
if zakladka == "Świętuchobranie":
    st.subheader("Świętuchobranie")
    zapis(st.session_state.tabela_swietuchobranie)

# =============================
# WARSZTATY
# =============================
else:
    st.subheader("Warsztaty z programowania")
    zapis(st.session_state.tabela_programowanie)
