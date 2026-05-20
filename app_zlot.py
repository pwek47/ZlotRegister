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
    page_title="Zgłoszenia na zajęcia Zlotowe 68 HRŚ",
    layout="wide"
)

# -----------------------------
# KONFIG
# -----------------------------
SWIETUCH_GODZINY = ["16:00","16:30","17:00","17:30","18:00","18:30","19:00"]
SWIETUCH_SLOTY = [f"Slot {i}" for i in range(1, 10)]

PROG_GODZINY = ["16:00","17:00","18:00","19:00"]
PROG_SLOTY = ["Slot A", "Slot B"]

# -----------------------------
# DB
# -----------------------------
def pobierz(event):
    res = supabase.table("zlot_slots").select("*").eq("event", event).execute()
    return res.data


def zapisz(event, hour, slot, patrol):
    return supabase.table("zlot_slots").insert({
        "event": event,
        "hour": hour,
        "slot": slot,
        "patrol": patrol
    }).execute()


def patrol_w_event(event, patrol):
    """sprawdza czy patrol już jest w DANYM evencie"""
    res = (
        supabase
        .table("zlot_slots")
        .select("*")
        .eq("event", event)
        .eq("patrol", patrol)
        .execute()
    )
    return len(res.data) > 0


def slot_zajety(event, hour, slot):
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
# TABLE BUILD
# -----------------------------
def build_table(event, hours, slots):
    data = pobierz(event)

    df = pd.DataFrame(index=hours, columns=slots).fillna("")

    for row in data:
        h = row["hour"]
        s = row["slot"]
        p = row["patrol"]

        if h in df.index and s in df.columns:
            df.loc[h, s] = p

    return df

# -----------------------------
# SAVE
# -----------------------------
def zapisz_zmiany(event, original_df, edited_df):

    changed = False

    for hour in edited_df.index:
        for slot in edited_df.columns:

            old = original_df.loc[hour, slot]
            new = edited_df.loc[hour, slot]

            if pd.isna(old): old = ""
            if pd.isna(new): new = ""

            old = str(old).strip()
            new = str(new).strip()

            if old == new:
                continue

            # slot zajęty -> nie nadpisuj
            if old != "":
                st.error(f"Slot {hour} / {slot} jest zajęty")
                continue

            if new == "":
                continue

            # patrol już w tym evencie
            if patrol_w_event(event, new):
                st.error(f"Patrol {new} już jest w tym wydarzeniu")
                continue

            try:
                zapisz(event, hour, slot, new)
                changed = True

            except Exception as e:
                st.error(f"Błąd: {e}")

    if changed:
        st.success("Zapisano zmiany")
        st.rerun()

# -----------------------------
# UI
# -----------------------------
st.title("📋 Zgłoszenia Zlotowe 68 HRŚ")

zakladka = st.radio(
    "Wybierz wydarzenie",
    ["Świętuchobranie", "Warsztaty z programowania"]
)

def panel(event, hours, slots):

    st.subheader(event)

    original_df = build_table(event, hours, slots)

    edited_df = st.data_editor(
        original_df,
        use_container_width=True,
        num_rows="fixed",
        key=f"editor_{event}"
    )

    st.info("Kliknij komórkę i wpisz patrol")

    if st.button("Zapisz", key=f"save_{event}"):

        zapisz_zmiany(event, original_df, edited_df)

# -----------------------------
# EVENTS
# -----------------------------
if zakladka == "Świętuchobranie":
    panel("Świętuchobranie", SWIETUCH_GODZINY, SWIETUCH_SLOTY)
else:
    panel("Warsztaty z programowania", PROG_GODZINY, PROG_SLOTY)
