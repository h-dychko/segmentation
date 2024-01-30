from typing import List
import numpy as np
import pandas as pd

import streamlit as st
import plotly.express as px

from define_objects import (
    df,
    FEATURES_META, CATEGORIES, PALETTE
)

st.text_input(
    'ID', value="", max_chars=5, key='ID', type="default", help=None
)

if st.session_state.get('ID'):
    user_info = df[df.ID.astype(str) == st.session_state.get('ID')]
    if not user_info.empty:
        st.table(user_info)
    else:
        st.warning(f'There is no customer with `ID`={st.session_state.get("ID")}')


