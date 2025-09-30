import streamlit as st
from app.common.widgets import movements_data_editor
from app.parse.parse_service import parse
from app.common.types import Account

st.title("Extract Transactions from Statement PDF")

uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])
account = st.selectbox("Select Account", options=[account.value for account in Account])

if uploaded_file and account:
    movements = None # pylint: disable=invalid-name

    try:
        with st.spinner("Parsing PDF...", show_time=True):
            movements = parse(Account(account), uploaded_file.getvalue())
    except KeyError:
        st.error(f"Parser for account {account} is not avaliable")
    except Exception:
        st.error("Error while parsing PDF")

    movements_data_editor(movements)
