import os
import streamlit as st
import requests
import pandas as pd

API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")

st.set_page_config(page_title="Media Monitoring Dashboard", layout="wide")
st.title("📊 Media Monitoring Dashboard")

# Tab Layout
tab1, tab2 = st.tabs(["Analytics & Stats", "Search Mentions"])

with tab1:
    st.header("Overall Analytics")
    try:
        res = requests.get(f"{API_BASE_URL}/mentions/stats")
        if res.status_code == 200:
            stats = res.json()
            
            col1, col2 = st.columns(2)
            col1.metric("Total Mentions", stats.get("total_mentions", 0))
            col2.metric("Total Engagement", stats.get("total_engagement", 0))

            st.subheader("Breakdown per Source")
            df_source = pd.DataFrame(stats.get("by_source", []))
            if not df_source.empty:
                st.dataframe(df_source, use_container_width=True)
                st.bar_chart(df_source.set_index("source")["mentions_count"])
            else:
                st.info("Belum ada data stats.")
    except Exception as e:
        st.error(f"Gagal menghubungkan ke backend FastAPI: {e}")

with tab2:
    st.header("Search & Filter Mentions")
    
    col_search, col_source = st.columns(2)
    search_query = col_search.text_input("Cari kata kunci (Title / Content):")
    source_filter = col_source.text_input("Filter Source (cth: instagram, the star):")

    if st.button("Cari Data"):
        params = {}
        if search_query:
            params["q"] = search_query
        if source_filter:
            params["source"] = source_filter

        try:
            res = requests.get(f"{API_BASE_URL}/mentions", params=params)
            if res.status_code == 200:
                data = res.json()
                st.write(f"Total Hasil: {data.get('total_items', 0)}")
                df_mentions = pd.DataFrame(data.get("data", []))
                if not df_mentions.empty:
                    st.dataframe(df_mentions[["id", "source", "title", "content", "engagement", "published_at"]], use_container_width=True)
                else:
                    st.warning("Data tidak ditemukan.")
        except Exception as e:
            st.error(f"Error fetching data: {e}")