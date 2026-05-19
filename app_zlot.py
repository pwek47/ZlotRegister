import streamlit as st
import pandas as pd

st.set_page_config(page_title="Zlot Registration System", layout="wide")

# -----------------------------
# SESSION STATE STORAGE
# -----------------------------
if "participants" not in st.session_state:
    st.session_state.participants = []

if "table1" not in st.session_state:
    times = ["16:00","16:30","17:00","17:30","18:00","18:30","19:00"]
    st.session_state.table1 = pd.DataFrame(
        "", index=times, columns=[f"Slot {i}" for i in range(1, 10)]
    )

if "table2" not in st.session_state:
    hours = ["16:00","17:00","18:00","19:00"]
    st.session_state.table2 = pd.DataFrame(
        "", index=hours, columns=["Slot A", "Slot B"]
    )

# -----------------------------
# SIDEBAR NAVIGATION
# -----------------------------
page = st.sidebar.radio(
    "Menu",
    ["Register Participant", "Participants", "Schedule Table 1", "Schedule Table 2"]
)

# -----------------------------
# REGISTRATION
# -----------------------------
if page == "Register Participant":
    st.title("Zlot Registration")

    with st.form("reg_form"):
        name = st.text_input("Name")
        patrol = st.text_input("Patrol Name")
        payment = st.selectbox("Payment Status", ["Unpaid", "Paid", "Partial"])
        requirements = st.text_area("Special Requirements")

        submitted = st.form_submit_button("Add Participant")

        if submitted:
            st.session_state.participants.append({
                "Name": name,
                "Patrol": patrol,
                "Payment": payment,
                "Requirements": requirements
            })
            st.success("Participant added!")

# -----------------------------
# PARTICIPANTS LIST
# -----------------------------
elif page == "Participants":
    st.title("Participants")

    df = pd.DataFrame(st.session_state.participants)

    if not df.empty:
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No participants yet.")

# -----------------------------
# TABLE 1 (9 slots × 7 rows)
# -----------------------------
elif page == "Schedule Table 1":
    st.title("Schedule Table 1")

    df = st.session_state.table1.copy()

    st.dataframe(df, use_container_width=True)

    st.subheader("Assign Patrol to Slot")

    time = st.selectbox("Time", df.index)
    slot = st.selectbox("Slot", df.columns)
    patrol = st.text_input("Patrol Name")

    if st.button("Assign"):
        if df.loc[time, slot] == "":
            st.session_state.table1.loc[time, slot] = patrol
            st.success("Assigned!")
        else:
            st.error("Slot already taken!")

    if st.button("Clear All Table 1"):
        st.session_state.table1.iloc[:, :] = ""
        st.warning("Table cleared")

# -----------------------------
# TABLE 2 (2 slots per hour)
# -----------------------------
elif page == "Schedule Table 2":
    st.title("Schedule Table 2")

    df = st.session_state.table2.copy()

    st.dataframe(df, use_container_width=True)

    st.subheader("Assign Patrol to Slot")

    hour = st.selectbox("Hour", df.index)
    slot = st.selectbox("Slot", df.columns)
    patrol = st.text_input("Patrol Name")

    if st.button("Assign"):
        if df.loc[hour, slot] == "":
            st.session_state.table2.loc[hour, slot] = patrol
            st.success("Assigned!")
        else:
            st.error("Slot already taken!")

    if st.button("Clear All Table 2"):
        st.session_state.table2.iloc[:, :] = ""
        st.warning("Table cleared")