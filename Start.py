import argparse
import pandas as pd

import streamlit as st
import plotly.express as px

from define_objects import (
    df, df_stats_by_clst, df_stats_by_cat,
    FEATURES_META, CATEGORIES, PALETTE
)


# # parse arguments from the command line
# parser = argparse.ArgumentParser()
# parser.add_argument("--local", action='store_true', help="If local data is taken from the local folder")
# args = parser.parse_args()

# set page configuration
st.set_page_config("Segmentation", layout="wide")

# set headers
st.markdown("# Customer Personality Analysis. Q1-2023")

################################################################################################
# TODO: Add heading level 2 with the text: Wines, Fruits, Meat, Fish, Sweet, Gold.
# Hint: Level 2 heading start with 2 hashtags.
################################################################################################
# Expected solution: st.markdown("## " + ", ".join(categories) + ".")


# add selection of a number of clusters (k=2, k=3)
st.sidebar.selectbox(
    label="Number of clusters", options=[2, 3], index=0, key="n_clusters"
)


with st.container():
    st_cols = st.columns([0.4, 1.2, 1.2, 1.2])
    
    # st_cols[0].empty()
    st_cols[0].write("#")

    st_cols[0].metric(label="\# of customers", value=df.shape[0])

    st_cols[0].metric(label="**Avg. spend**", value=f"${round(df[CATEGORIES].sum(axis=1).mean(), 1)}")

    with st_cols[1]:
        f = px.bar(
            df_stats_by_cat, 
            y="sum",
            title="Total Income by Category",
            text_auto='$.2s',
            color_discrete_sequence=['#002561'],
            labels={'index': '', 'n': ''},
            height=300, width=450
        )
        st.plotly_chart(f)

    with st_cols[2]:
        # st.bar_chart(data=df_stats_by_cat, y='mean', color='#5674a5', height=300, width=450, use_container_width=True)
        f = px.bar(
            df_stats_by_cat, 
            y="mean",
            title="Average Income by Category",
            text_auto='$.2s',
            color_discrete_sequence=['#5674a5'],
            labels={'index': '', 'n': ''},
            height=300, width=450
        )
        st.plotly_chart(f)

    with st_cols[3]:
        fig = px.scatter_3d(
            df, x='PCA.1', y='PCA.2', z='PCA.3',size=[1]*len(df), size_max=7, opacity=0.5,
            color=f'k={st.session_state.n_clusters}',
            color_discrete_map=PALETTE[st.session_state.n_clusters], 
            height=300, width=450,
            template="plotly_white",
            title="3d projection of clusters"
        )                    
        st.plotly_chart(fig)


df_selected_stats = df_stats_by_clst[f'k={st.session_state.n_clusters}']
n_features = df_selected_stats.shape[1]

with st.expander("Averages by clusters:", expanded=True):
    tab_1, tab_2 = st.tabs(['Metrics', 'Tables'])

    with tab_1:
        for c in range(st.session_state.n_clusters):
            with st.container(height=200):
                st.markdown(f":blue[Cluster #{c}: ]")
                st_cols = st.columns(n_features)
                for i, col_name in enumerate(df_selected_stats.columns):
                    st.write(
                        """
                        <style>
                        [data-testid="stMetricDelta"] svg {
                        display: none;
                        }
                        </style>
                        """,
                        unsafe_allow_html=True,
                    )
                
                    st_cols[i].metric(
                        label=col_name, 
                        value=f"{int(df_selected_stats.loc[str(c), col_name])}" \
                            if FEATURES_META[col_name]['type'] == int \
                                else FEATURES_META[col_name]['format'].format(df_selected_stats.loc[str(c), col_name]), 
                        delta=f"{int(df_selected_stats.loc['Overall', col_name])}" \
                            if FEATURES_META[col_name]['type'] == int \
                                else FEATURES_META[col_name]['format'].format(df_selected_stats.loc['Overall', col_name]), 
                        delta_color='off'
                    )
    with tab_2:
        st.dataframe(df_stats_by_clst[f'k={st.session_state.n_clusters}'])