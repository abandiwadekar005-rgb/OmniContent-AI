import os
import streamlit as st

# has to run before the generate import below, otherwise generate.py
# tries to read the key before it's actually set
if "GEMINI_API_KEY" in st.secrets:
    os.environ["GEMINI_API_KEY"] = st.secrets["GEMINI_API_KEY"]

from db import init_db, save_generation, get_generations, update_status
from generate import generate_ad_copy

init_db()  # calling it every run, does nothing if tables already exist

st.title("Vipana — Ad Copy Generator")

campaign_id = 1  # TODO: support multiple campaigns

brief = st.text_area("Campaign brief")

if st.button("Generate"):
    if not brief.strip():
        st.error("Please enter a campaign brief first.")
    else:
        prompt = f"Write 2 short Instagram ad captions for this brief:\n{brief}"
        try:
            result = generate_ad_copy(prompt)
            # need the id back so Approve/Reject/Improve know which row to update
            new_id = save_generation(campaign_id=campaign_id, text=result)
            st.session_state["last_result"] = result
            st.session_state["last_id"] = new_id
        except Exception as e:
            st.error(f"Something went wrong generating content: {e}")

if "last_result" in st.session_state:
    st.write(st.session_state["last_result"])
    col1, col2 = st.columns(2)
    if col1.button("Approve"):
        update_status(st.session_state["last_id"], "approved")
        st.success("Approved")
    if col2.button("Reject"):
        update_status(st.session_state["last_id"], "rejected")
        st.warning("Rejected")

    improve_note = st.text_input("Improve instruction")
    if st.button("Improve") and improve_note:
        # send back the old result + what to change, instead of starting over
        new_prompt = f"{brief}\n\nRevise this: {st.session_state['last_result']}\nInstruction: {improve_note}"
        try:
            new_result = generate_ad_copy(new_prompt)
            new_id = save_generation(
                campaign_id=campaign_id,
                text=new_result,
                parent_id=st.session_state["last_id"]  # links back to the version this improved
            )
            st.session_state["last_result"] = new_result
            st.session_state["last_id"] = new_id
        except Exception as e:
            st.error(f"Something went wrong improving content: {e}")

st.divider()
st.subheader("Past generations")
# without this loop everything would disappear when you close/reopen the app
for gen_id, text, status in get_generations(campaign_id):
    st.write(f"**#{gen_id}** ({status}): {text}")