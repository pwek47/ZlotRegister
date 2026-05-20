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
    page_title="Zgłoszenia Zlotowe 68 HRŚ",
    layout="wide"
)

# -----------------------------
# KONFIG TABEL
# -----------------------------
SWIETUCH_GODZINY = ["16:00","16:30","17:00","17:30","18:00","18:30","19:00"]
SWIETUCH_SLOTY = [f"Slot {i}" for i in range(1, 10)]

PROG_GODZINY = ["16:00","17:00","18:00","19:00"]
PROG_SLOTY = ["Slot A", "Slot B"]

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

def czy_patrol_istnieje(patrol):
    res = (
        supabase
        .table("zlot_slots")
        .select("*")
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

    df = pd.DataFrame("", index=hours, columns=slots)

    for row in data:
        h = row["hour"]
        s = row["slot"]
        p = row["patrol"]

        if h in df.index and s in df.columns:
            df.loc[h, s] = p

    return df

# -----------------------------
# ZAPIS ZMIAN
# -----------------------------
def zapisz_zmiany(event, original_df, edited_df):

    for hour in edited_df.index:

        for slot in edited_df.columns:

            old_value = str(original_df.loc[hour, slot]).strip()
            new_value = str(edited_df.loc[hour, slot]).strip()

            # nic nie zmieniono
            if old_value == new_value:
                continue

            # nie można nadpisywać istniejących slotów
            if old_value != "":
                st.error(f"{hour} / {slot} jest już zajęty")
                continue

            # puste pole
            if new_value == "":
                continue

            # patrol już istnieje
            if czy_patrol_istnieje(new_value):
                st.error(f"Patrol {new_value} już istnieje")
                continue

            try:
                zapisz(event, hour, slot, new_value)
                st.success(f"Zapisano patrol {new_value}")

            except Exception as e:
                st.error(f"Błąd: {e}")

# -----------------------------
# UI
# -----------------------------
st.title("📋 Zgłoszenia Zlotowe 68 HRŚ")

zakladka = st.radio(
    "Wybierz wydarzenie",
    ["Świętuchobranie", "Warsztaty z programowania"]
)

# -----------------------------
# PANEL
# -----------------------------
def panel(event, hours, slots):

    st.subheader(event)

    original_df = build_table(event, hours, slots)

    edited_df = st.data_editor(
        original_df,
        use_container_width=True,
        num_rows="fixed",
        disabled=False
    )

    st.info("👉 Kliknij pustą komórkę i wpisz numer patrolu")

    if st.button("Zapisz zmiany"):

        zapisz_zmiany(event, original_df, edited_df)

        st.rerun()

# -----------------------------
# EVENTS
# -----------------------------
if zakladka == "Świętuchobranie":
    panel("Świętuchobranie", SWIETUCH_GODZINY, SWIETUCH_SLOTY)

else:
    panel("Warsztaty z programowania", PROG_GODZINY, PROG_SLOTY)
