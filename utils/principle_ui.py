import streamlit as st

def evidence_badge(kind):
    m={"tutorial":"🟢 Tutorial direct","literature":"🔷 External literature","model":"🟠 Engineering model","pending":"🟣 Pending verification"}
    st.caption(m.get(kind,kind))

def causal_chain(items):
    st.markdown(" → ".join([f"**{x}**" for x in items]))

def takeaway(text):
    st.info("💡 "+text)

def why_it_matters(text):
    st.success("🔧 Engineering meaning: "+text)
