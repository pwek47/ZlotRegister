import streamlit as st
import pandas as pd
from supabase import create_client

# -----------------------------
# SUPABASE CONFIG
# -----------------------------
SUPABASE_URL = "https://ogrrodyxbwhsepgaancv.supabase.co"
SUPABASE_KEY = "sb_publishable_5BjK7_IMz5dlrG5-WZ_5LA_4xpEIk7z"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

st.set_page_config(page_title="Zgłoszenia Zlotowe 68 HRŚ", layout="wide")
st.info("👉 Kliknij w komórkę i wpisz numer Patrolu")

# -----------------------------
# KONFIG TABEL
# -----------------------------
SWIETUCH_GODZINY = ["16:00","16:30","17:00","17:30","18:00","18:30","19:00"]
SWIETUCH_SLOTY = [f"Slot {i}" for i in range(1, 10)]

PROG_GODZINY = ["16:00","17:00","18:00","19:00"]
PROG_SLOTY = ["Slot A", "Slot B"]

# -----------------------------
# DB FUNKCJE
# -----------------------------
def pobierz(event):
    return supabase.table("zlot_slots").select("*").eq("event", event).execute().data

def zapisz(event, hour, slot, patrol):
    return supabase.table("zlot_slots").insert({
        "event": event,
        "hour": hour,
        "slot": slot,
        "patrol": patrol
    }).execute()

def czy_patrol_istnieje(patrol):
    res = supabase.table("zlot_slots").select("*").eq("patrol", patrol).execute()
    return len(res.data) > 0

def wyczysc_event(event):
    supabase.table("zlot_slots").delete().eq("event", event).execute()

# -----------------------------
# BUDOWA TABELI
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
# PANEL
# -----------------------------
def panel(event, hours, slots):

    st.subheader(event)

    df = build_table(event, hours, slots)

    edited = st.data_editor(
        df,
        use_container_width=True,
        num_rows="fixed"
    )

    st.info("👉 Kliknij komórkę i wpisz numer Patrolu")

    if st.button("Zapisz zmiany"):

        flat = edited.values.flatten()

        # -------------------------
        # WALIDACJA DUPLIKATÓW
        # -------------------------
        seen = set()
        for val in flat:
            if val == "":
                continue
            if val in seen:
                st.error("❌ Każdy Patrol może zapisać się na dane zajęcia tylko raz!")
                return
            seen.add(val)

        # -------------------------
        # ZAPIS (SAFE SYNC)
        # -------------------------
        try:
            # czyścimy event
            wyczysc_event(event)

            # zapisujemy od nowa
            for r in hours:
                for c in slots:
                    val = edited.loc[r, c]
                    if val != "":
                        zapisz(event, r, c, val)

            st.success("✔ Zapisano Patrol!")
            st.rerun()

        except Exception:
            st.error("❌ Nie udało się zapisać. Spróbuj ponownie.")

# -----------------------------
# UI
# -----------------------------
st.title("📋 Zgłoszenia Zlotowe 68 HRŚ")

zakladka = st.radio(
    "Wybierz wydarzenie",
    ["Świętuchobranie", "Warsztaty z programowania"]
)

if zakladka == "Świętuchobranie":
    panel("swietuchobranie", SWIETUCH_GODZINY, SWIETUCH_SLOTY)
else:
    panel("warsztaty", PROG_GODZINY, PROG_SLOTY)
