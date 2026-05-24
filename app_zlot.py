import streamlit as st
import pandas as pd
from supabase import create_client

# -----------------------------
# SUPABASE CONFIG
# -----------------------------
SUPABASE_URL = "https://ogrrodyxbwhsepgaancv.supabase.co"
SUPABASE_KEY = "sb_publishable_5BjK7_IMz5dlrG5-WZ_5LA_4xpEIk7z"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

st.set_page_config(
    page_title="Zgłoszenia na grę Świętuchobranie na Zlocie 68 HRŚ",
    layout="wide"
)

# -----------------------------
# KONFIG TABELI
# -----------------------------
SWIETUCH_GODZINY = [
    "16:00",
    "16:30",
    "17:00",
    "17:30",
    "18:00",
    "18:30",
    "19:00"
]

SWIETUCH_SLOTY = [
    f"Patrol {i}" for i in range(1, 10)
]

EVENT_NAME = "Świętuchobranie"

# -----------------------------
# SESSION STATE
# -----------------------------
if "selected_hour" not in st.session_state:
    st.session_state.selected_hour = SWIETUCH_GODZINY[0]

# -----------------------------
# FUNKCJE DB
# -----------------------------
def pobierz(event):

    res = (
        supabase
        .table("zlot_slots")
        .select("*")
        .eq("event", event)
        .execute()
    )

    return res.data


def zapisz(event, hour, slot, patrol):

    return (
        supabase
        .table("zlot_slots")
        .insert({
            "event": event,
            "hour": hour,
            "slot": slot,
            "patrol": patrol
        })
        .execute()
    )


def czy_patrol_istnieje(event, patrol):

    res = (
        supabase
        .table("zlot_slots")
        .select("*")
        .eq("event", event)
        .eq("patrol", patrol)
        .execute()
    )

    return len(res.data) > 0


def czy_slot_zajety(event, hour, slot):

    res = (
        supabase
        .table("zlot_slots")
        .select("*")
        .eq("event", event)
        .eq("hour", hour)
        .eq("slot", slot)
        .execute()
    )

    return len(res.data) > 0


# -----------------------------
# GENEROWANIE TABELI
# -----------------------------
def build_table(event, hours, slots):

    data = pobierz(event)

    df = pd.DataFrame(
        "",
        index=hours,
        columns=slots
    )

    for row in data:

        h = row["hour"]
        s = row["slot"]
        p = row["patrol"]

        if h in df.index and s in df.columns:
            df.loc[h, s] = p

    return df


# -----------------------------
# UI
# -----------------------------
st.title("📋 Zgłoszenia na grę Zlotową 68 HRŚ")


def panel(event, hours, slots):

    df = build_table(event, hours, slots)

    st.subheader(event)

    # -----------------------------
    # WYBÓR GODZINY
    # -----------------------------
    wybrana_godzina = st.selectbox(
        "Wybierz godzinę",
        hours,
        index=hours.index(st.session_state.selected_hour)
    )

    st.session_state.selected_hour = wybrana_godzina

    # -----------------------------
    # TABELA TYLKO DLA GODZINY
    # -----------------------------
    st.write(f"### Sloty dla godziny {wybrana_godzina}")

    godzina_df = pd.DataFrame(
        [df.loc[wybrana_godzina]],
        index=[wybrana_godzina]
    )

    st.dataframe(
        godzina_df,
        use_container_width=True
    )

    st.info(
        "👉 Wybierz patrol dla tej godziny"
    )

    # -----------------------------
    # WYBÓR SLOTU
    # -----------------------------
    slot = st.selectbox(
        "Wybierz patrol",
        slots
    )

    st.write(f"Wybrano: {wybrana_godzina} / {slot}")

    patrol = st.text_input(
        "Numer patrolu"
    )

    patrol = patrol.strip().upper()

    # -----------------------------
    # ZAPIS
    # -----------------------------
    if st.button("Zapisz"):

        if patrol == "":
            st.error("Podaj numer patrolu")
            return

        if czy_patrol_istnieje(event, patrol):
            st.error(
                "Ten patrol jest już zapisany!"
            )
            return

        if czy_slot_zajety(event, wybrana_godzina, slot):
            st.error(
                "Ten slot jest już zajęty!"
            )
            return

        try:

            zapisz(
                event,
                wybrana_godzina,
                slot,
                patrol
            )

            st.success(
                "Zapisano na grę!"
            )

            st.rerun()

        except Exception as e:
            st.error(f"Błąd zapisu: {e}")


# -----------------------------
# START
# -----------------------------
panel(
    EVENT_NAME,
    SWIETUCH_GODZINY,
    SWIETUCH_SLOTY
)
