
from typing import List
import streamlit as st
from app.common.types import Account, Movement
from app.common.utils import movements_to_df


def movements_data_editor(movements: List[Movement] | None):
    """Create a movements data editor

    Args:
        movements (List[Movement]): Movements
    """

    if not movements: return 

    movements_df = movements_to_df(movements)
    
    st.data_editor(
        movements_df, 
        hide_index=True,
        column_order=[
            "id", "account", "date", "amount", "description"
        ],
        column_config = {
            "id": st.column_config.TextColumn(
                "ID",
                disabled=True,
                pinned=True
            ),
            "account": st.column_config.SelectboxColumn(
                "Account",
                options = [account.value for account in Account],
                required=True
            ),
            "date": st.column_config.DateColumn(
                "Date"
            ),
            "amount": st.column_config.NumberColumn(
                "Amount",
                format="dollar",
                required=True
            ),
            "description": st.column_config.TextColumn(
                "Description"
            ),
            # Currently hide 
            "ref": st.column_config.TextColumn(
                "Reference",
                help="When the origin of a movement comes from another account",
            )
        } 
    )
