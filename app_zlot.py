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
# FUNKCJA EDYCJI
# =============================
def tabela_edytowalna(df, klucz):
    st.info("👉 Kliknij w komórkę i wpisz numer patrolu (tylko jedno pole)")

    edited = st.data_editor(
        df,
        key=klucz,
        use_container_width=True,
        num_rows="fixed"
    )

    if st.button("Zapisz zmiany", key=f"save_{klucz}"):
        # sprawdzanie duplikatów patrolu
        for val in edited.values.flatten():
            if val != "" and list(edited.values.flatten()).count(val) > 1:
                st.error("Jeden patrol może być tylko raz!")
                return

        st.session_state[klucz] = edited
        st.success("Zapisano!")
        st.rerun()

# =============================
# ŚWIĘTUCHOBRANIE
# =============================
if zakladka == "Świętuchobranie":
    st.subheader("Świętuchobranie")
    tabela_edytowalna(st.session_state.tabela_swietuchobranie, "swietuch")

# =============================
# WARSZTATY
# =============================
else:
    st.subheader("Warsztaty z programowania")
    tabela_edytowalna(st.session_state.tabela_programowanie, "prog")
