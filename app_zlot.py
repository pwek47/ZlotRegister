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


# patrol może zapisać się tylko raz
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


# slot może być zajęty tylko raz
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

    st.dataframe(
        df,
        use_container_width=True
    )

    st.info(
        "👉 Wybierz wolny slot i wpisz numer patrolu"
    )

    komorki = [
        (h, s)
        for h in hours
        for s in slots
    ]

    wybor = st.selectbox(
        "Wybierz pole",
        komorki,
        format_func=lambda x: f"{x[0]} - {x[1]}"
    )

    hour, slot = wybor

    st.write(f"Wybrano: {hour} / {slot}")

    patrol = st.text_input(
        "Numer patrolu"
    )

    patrol = patrol.strip().upper()

    if st.button("Zapisz"):

        if patrol == "":
            st.error("Podaj numer patrolu")
            return

        # blokada duplikatu patrolu
        if czy_patrol_istnieje(event, patrol):
            st.error(
                "Ten patrol jest już zapisany!"
            )
            return

        # blokada zajętego slotu
        if czy_slot_zajety(event, hour, slot):
            st.error(
                "Ten slot jest już zajęty!"
            )
            return

        try:

            zapisz(
                event,
                hour,
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
