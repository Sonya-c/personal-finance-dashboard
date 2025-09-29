import streamlit as st

pages = [
    st.Page("home/home_page.py", title="Home"),
    st.Page("parse/parse_page.py", title="Parse PDF"),
]

app = st.navigation(pages)
app.run()
