import streamlit as st #the python library which allows for quick creation of an interface
from db import init_db, save_generation, get_conn 
from generate import call_claude

init_db() 

st.title("OmniContent — Ad Copy Generator")

brief = st.text_area("Campaign brief")

if st.button("Generate"):
    prompt = f"Write 2 short Instagram ad captions for this brief:\n{brief}"
    result = call_claude(prompt)
    # naive split, might need tidying depending on how Claude formats it
    save_generation(campaign_id=1, text=result)
    st.session_state["last_result"] = result

if "last_result" in st.session_state:
    st.write(st.session_state["last_result"])
    col1, col2 = st.columns(2)
    if col1.button("Approve"):
        st.success("Approved")
    if col2.button("Reject"):
        st.warning("Rejected")
    improve_note = st.text_input("Improve instruction")
    if st.button("Improve") and improve_note:
        new_prompt = f"{brief}\n\nRevise this: {st.session_state['last_result']}\nInstruction: {improve_note}"
        new_result = call_claude(new_prompt)
        save_generation(campaign_id=1, text=new_result, parent_id=1)
        st.session_state["last_result"] = new_result