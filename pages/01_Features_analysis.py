from typing import List
import numpy as np
import pandas as pd

import streamlit as st
import plotly.express as px

from define_objects import (
    df,
    FEATURES_META, CATEGORIES, PALETTE
)


# add selection of a number of clusters (k=2, k=3)
st.sidebar.selectbox(
    label="Number of clusters", options=[2, 3], index=[2, 3].index(st.session_state.get('n_clusters') or 2), key="n_clusters"
)


st.multiselect(
    'Search', options=list(FEATURES_META.keys()), 
    key='feature', help=None, placeholder="Choose a feature", disabled=False, label_visibility="visible"
)

@st.cache_data(ttl=3600)
def display_distribution(features: List[str], k: int):
    for feature_name in features:
        if FEATURES_META[feature_name]['plot'] == 'box':
            f = px.box(
                df, x=feature_name, y=f"k={k}", color=f"k={k}", 
                orientation="h", color_discrete_map=PALETTE[k],
                title=f"{feature_name} by cluster",
                template="simple_white",
                labels={f"k={k}": "Cluster No."}
            )
            st.plotly_chart(f)
        elif FEATURES_META[feature_name]['plot'] == 'bar':
            f = px.bar(
                df.groupby(f"k={k}", sort=True)[feature_name].value_counts(normalize=True).reset_index(name="n").sort_values([f'k={k}', feature_name]), 
                x="n", y=f"k={k}", color=feature_name, 
                orientation="h", 
                title=f"{feature_name} by cluster",
                labels={f"k={k}": "Cluster No.", "n": "%"}
            )
            f.update_layout(yaxis=dict(tickmode = 'array', tickvals=np.sort(df[f'k={k}'].unique())))
            st.plotly_chart(f)


with st.container():
    display_distribution(st.session_state.feature, st.session_state.n_clusters)
