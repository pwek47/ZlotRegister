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

# -----------------------------
# SPRAWDZENIE DUPLIKATÓW
# -----------------------------
def patrol_istnieje(df, patrol):
    return (df == patrol).any().any()

# -----------------------------
# FUNKCJA EDYTORA
# -----------------------------
def tabela_edytowalna(klucz, tytul):
    st.subheader(tytul)

    df = st.session_state[klucz]

    st.info("👉 Kliknij w komórkę i wpisz numer patrolu")

    edited = st.data_editor(
        df,
        use_container_width=True,
        num_rows="fixed",
        key=f"editor_{klucz}"
    )

    if st.button("Zapisz zmiany", key=f"save_{klucz}"):

        # sprawdzenie duplikatów patrolu
        flat = edited.values.flatten()
        for val in set(flat):
            if val != "" and list(flat).count(val) > 1:
                st.error("❌ Jeden patrol może być tylko raz w tabeli!")
                return

        # aktualizacja danych (bez crashy Streamlit)
        st.session_state[klucz].iloc[:, :] = edited.values

        st.success("✔ Zapisano!")
        st.rerun()

# -----------------------------
# UI
# -----------------------------
st.title("📋 Zgłoszenia Zlotowe 68 HRŚ")

zakladka = st.radio(
    "Wybierz wydarzenie",
    ["Świętuchobranie", "Warsztaty z programowania"]
)

# -----------------------------
# ŚWIĘTUCHOBRANIE
# -----------------------------
if zakladka == "Świętuchobranie":
    tabela_edytowalna("tabela_swietuchobranie", "Świętuchobranie")

# -----------------------------
# WARSZTATY
# -----------------------------
else:
    tabela_edytowalna("tabela_programowanie", "Warsztaty z programowania")
