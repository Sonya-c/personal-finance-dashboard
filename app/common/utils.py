from typing import List
import pandas as pd
from app.common.types import Movement


def movements_to_df(movements: List[Movement]) -> pd.DataFrame: 
    """Given a list of movements it returns a data frame

    Args:
        movements (List[Movement]): Movements

    Returns:
        pd.DataFrame: Data frame
    """
    movements_df = pd.DataFrame(movements)
    movements_df["account"] = movements_df["account"]\
        .apply(lambda account: account.value)
    
    return movements_df

