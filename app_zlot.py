import streamlit as st
import pandas as pd

st.set_page_config(page_title="System Zlotu", layout="wide")

# -----------------------------
# SESSION STATE STORAGE
# -----------------------------
if "uczestnicy" not in st.session_state:
    st.session_state.uczestnicy = []

if "tabela1" not in st.session_state:
    czasy = ["16:00","16:30","17:00","17:30","18:00","18:30","19:00"]
    st.session_state.tabela1 = pd.DataFrame(
        "", index=czasy, columns=[f"Slot {i}" for i in range(1, 10)]
    )

if "tabela2" not in st.session_state:
    godziny = ["16:00","17:00","18:00","19:00"]
    st.session_state.tabela2 = pd.DataFrame(
        "", index=godziny, columns=["Slot A", "Slot B"]
    )

# -----------------------------
# MENU
# -----------------------------
strona = st.sidebar.radio(
    "Menu",
    ["Rejestracja", "Uczestnicy", "Tabela 1", "Tabela 2"]
)

# -----------------------------
# REJESTRACJA
# -----------------------------
if strona == "Rejestracja":
    st.title("Rejestracja Zlotu")

    with st.form("formularz"):
        imie = st.text_input("Imię i nazwisko")
        patrol = st.text_input("Nazwa patrolu")
        platnosc = st.selectbox("Status płatności", ["Nieopłacone", "Opłacone", "Częściowo"])
        wymagania = st.text_area("Specjalne wymagania")

        wyslane = st.form_submit_button("Dodaj uczestnika")

        if wyslane:
            st.session_state.uczestnicy.append({
                "Imię": imie,
                "Patrol": patrol,
                "Płatność": platnosc,
                "Wymagania": wymagania
            })
            st.success("Dodano uczestnika!")

# -----------------------------
# UCZESTNICY
# -----------------------------
elif strona == "Uczestnicy":
    st.title("Lista uczestników")

    df = pd.DataFrame(st.session_state.uczestnicy)

    if not df.empty:
        st.dataframe(df, use_container_width=True)
    else:
        st.info("Brak uczestników.")

# -----------------------------
# TABELA 1
# -----------------------------
elif strona == "Tabela 1":
    st.title("Tabela 1 (9 slotów × 7 godzin)")

    st.dataframe(st.session_state.tabela1, use_container_width=True)

    st.subheader("Przypisz patrol do slotu")

    czas = st.selectbox("Godzina", st.session_state.tabela1.index)
    slot = st.selectbox("Slot", st.session_state.tabela1.columns)
    patrol = st.text_input("Nazwa patrolu")

    if st.button("Przypisz"):
        if st.session_state.tabela1.loc[czas, slot] == "":
            st.session_state.tabela1.loc[czas, slot] = patrol
            st.success("Przypisano patrol!")
            st.rerun()
        else:
            st.error("Ten slot jest już zajęty!")

# -----------------------------
# TABELA 2
# -----------------------------
elif strona == "Tabela 2":
    st.title("Tabela 2 (2 sloty na godzinę)")

    st.dataframe(st.session_state.tabela2, use_container_width=True)

    st.subheader("Przypisz patrol do slotu")

    godzina = st.selectbox("Godzina", st.session_state.tabela2.index)
    slot = st.selectbox("Slot", st.session_state.tabela2.columns)
    patrol = st.text_input("Nazwa patrolu")

    if st.button("Przypisz"):
        if st.session_state.tabela2.loc[godzina, slot] == "":
            st.session_state.tabela2.loc[godzina, slot] = patrol
            st.success("Przypisano patrol!")
            st.rerun()
        else:
            st.error("Ten slot jest już zajęty!")
