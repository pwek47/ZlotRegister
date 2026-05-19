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

st.title("📋 Zgłoszenia Zlotowe 68 HRŚ")

st.info("👉 Kliknij komórkę i wpisz numer Patrolu")

# -----------------------------
# KONFIG
# -----------------------------
SWIETUCH_GODZINY = ["16:00","16:30","17:00","17:30","18:00","18:30","19:00"]
SWIETUCH_SLOTY = [f"Slot {i}" for i in range(1, 10)]

PROG_GODZINY = ["16:00","17:00","18:00","19:00"]
PROG_SLOTY = ["Slot A", "Slot B"]

# -----------------------------
# STATE INIT
# -----------------------------
if "duplicate_error" not in st.session_state:
    st.session_state.duplicate_error = None

# -----------------------------
# DB
# -----------------------------
def pobierz(event):
    res = supabase.table("zlot_slots").select("*").eq("event", event).execute()
    return res.data

def zapisz(event, hour, slot, patrol):
    return supabase.table("zlot_slots").upsert(
        {
            "event": event,
            "hour": hour,
            "slot": slot,
            "patrol": patrol
        },
        on_conflict=["event", "hour", "slot"]
    ).execute()

# -----------------------------
# BUILD GRID
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
# VALIDATION (LIVE)
# -----------------------------
def validate(df):
    flat = df.values.flatten()

    seen = set()
    for v in flat:
        if v == "":
            continue
        if v in seen:
            st.session_state.duplicate_error = f"❌ Patrol '{v}' występuje więcej niż raz!"
            return False
        seen.add(v)

    st.session_state.duplicate_error = None
    return True

# -----------------------------
# RENDER GRID STYLE (duplikaty)
# -----------------------------
def style_duplicates(df):
    flat = df.values.flatten()
    dup = {x for x in flat if x != "" and list(flat).count(x) > 1}

    return df.style.applymap(
        lambda v: "background-color: #ffcccc" if v in dup else ""
    )

# -----------------------------
# PANEL
# -----------------------------
def panel(event, hours, slots):

    st.subheader(event)

    df = build_table(event, hours, slots)

    styled_df = style_duplicates(df)

    edited = st.data_editor(
        styled_df,
        use_container_width=True,
        key=f"grid_{event}",
        on_change=lambda: validate(st.session_state[f"grid_{event}"])
    )

    # zapis stanu do session
    st.session_state[f"grid_{event}"] = edited

    # ERROR UI
    if st.session_state.duplicate_error:
        st.error(st.session_state.duplicate_error)
        st.stop()

    # SAVE
    if st.button("💾 Zapisz zmiany"):

        if not validate(edited):
            st.error("❌ Popraw duplikaty przed zapisem")
            return

        try:
            for r in hours:
                for c in slots:
                    val = edited.loc[r, c]
                    if val != "":
                        zapisz(event, r, c, val)

            st.success("✔ Zapisano poprawnie")
            st.rerun()

        except Exception as e:
            st.error(f"❌ Błąd zapisu: {e}")

# -----------------------------
# UI SWITCH
# -----------------------------
zakladka = st.radio(
    "Wybierz wydarzenie",
    ["Świętuchobranie", "Warsztaty z programowania"]
)

if zakladka == "Świętuchobranie":
    panel("swietuchobranie", SWIETUCH_GODZINY, SWIETUCH_SLOTY)
else:
    panel("warsztaty", PROG_GODZINY, PROG_SLOTY)
