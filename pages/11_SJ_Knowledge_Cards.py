import streamlit as st
from utils.content_loader import load_yaml

st.title("🧠 SJ Knowledge Cards")
kb=load_yaml("content/tutorials/harada_sj_deep_dive.yaml")
st.caption(kb["scope"])
for node in kb["nodes"]:
    with st.expander(f"🟢 {node['title']} · PDF {','.join(map(str,node['pdf_pages']))}"):
        for fact in node["facts"]: st.write("•",fact)

st.subheader("External research extensions")
for item in kb["web_research"]:
    with st.expander("🔷 "+item["title"]):
        st.write(item["finding"])
        st.code("DOI: "+item["doi"])
st.info("🟢 = Tutorial direct. 🔷 = external literature extension. Keep the two evidence streams separate.")
