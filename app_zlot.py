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
    return res.data or []


def zapisz(event, hour, slot, patrol):
    return supabase.table("zlot_slots").insert({
        "event": event,
        "hour": hour,
        "slot": slot,
        "patrol": patrol
    }).execute()


def patrol_w_event(event, patrol):
    res = (
        supabase.table("zlot_slots")
        .select("*")
        .eq("event", event)
        .eq("patrol", patrol)
        .execute()
    )
    return len(res.data or []) > 0


# -----------------------------
# TABLE
# -----------------------------
def build_table(event, hours, slots):
    data = pobierz(event)

    df = pd.DataFrame(index=hours, columns=slots)
    df[:] = ""

    for row in data:
        if row["hour"] in df.index and row["slot"] in df.columns:
            df.loc[row["hour"], row["slot"]] = row["patrol"]

    return df


# -----------------------------
# SAVE
# -----------------------------
def zapisz_zmiany(event, df):

    changes = 0

    for hour in df.index:
        for slot in df.columns:

            new = str(df.loc[hour, slot]).strip()
            if new == "" or new == "nan":
                continue

            # czy slot już istnieje
            existing = (
                supabase.table("zlot_slots")
                .select("*")
                .eq("event", event)
                .eq("hour", hour)
                .eq("slot", slot)
                .execute()
            )

            if existing.data:
                if existing.data[0]["patrol"] != new:
                    st.error(f"Slot {hour}/{slot} jest już zajęty!")
                continue

            if patrol_w_event(event, new):
                st.error(f"Patrol {new} został już zapisany na te zajęcia!")
                continue

            zapisz(event, hour, slot, new)
            changes += 1

    return changes


# -----------------------------
# UI STATE INIT
# -----------------------------
def init_state(event, hours, slots):
    key = f"df_{event}"

    if key not in st.session_state:
        st.session_state[key] = build_table(event, hours, slots)


# -----------------------------
# PANEL
# -----------------------------
def panel(event, hours, slots):

    st.subheader(event)

    df = build_table(event, hours, slots)

    editor_key = f"editor_{event}"

    # data_editor zapisuje do session_state automatycznie
    st.data_editor(
        df,
        use_container_width=True,
        num_rows="fixed",
        key=editor_key
    )

    if st.button("💾 Zapisz", key=f"save_{event}"):

        # 🔥 KLUCZOWE: bierzemy NAJNOWSZY stan z session_state
        edited_df = st.session_state[editor_key]

        changes = zapisz_zmiany(event, edited_df)

        # 🔥 zawsze odświeżamy z DB
        fresh_df = build_table(event, hours, slots)
        st.session_state[editor_key] = fresh_df

        if changes > 0:
            st.success(f"Zapisano na zajęcia!")
        else:
            st.warning("Brak zmian lub błędy (stan odświeżony)")

        st.rerun()


# -----------------------------
# APP
# -----------------------------
st.title("📋 Zgłoszenia na zajęcia Zlotowe 68 HRŚ")

zakladka = st.radio(
    "Wybierz wydarzenie",
    ["Świętuchobranie", "Warsztaty z programowania"]
)

if zakladka == "Świętuchobranie":
    panel("Świętuchobranie", SWIETUCH_GODZINY, SWIETUCH_SLOTY)
else:
    panel("Warsztaty z programowania", PROG_GODZINY, PROG_SLOTY)
