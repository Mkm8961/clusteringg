import streamlit as st
import pandas as pd

# -------------------------------
# Page Config
# -------------------------------
st.set_page_config(
    page_title="🧠 Material Clustering Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------------
# Load Data
# -------------------------------
@st.cache_data
def load_data():
    df = pd.read_excel("Material_Cluster_Summary.xlsx")
    df.rename(columns={"Max_MATERIAL_NUMBER": "Suggested_Material_Number"}, inplace=True)
    return df

df = load_data()

# -------------------------------
# Sidebar - Cluster Selector
# -------------------------------
st.sidebar.header("🔎 Filter")
cluster_ids = sorted(df['Cluster_ID'].dropna().unique())
selected_cluster = st.sidebar.selectbox("📦 Select Cluster ID", cluster_ids)

# -------------------------------
# Title and Description
# -------------------------------
st.markdown("""
    <h1 style='text-align: center; color: #4B8BBE;'>🔍 Semantic Material Clustering Explorer</h1>
    <p style='text-align: center; font-size: 18px;'>Analyze material descriptions grouped using SBERT embeddings & DBSCAN clustering.</p>
    <hr style="margin-top: 0;">
""", unsafe_allow_html=True)

# -------------------------------
# Optional: Show Entire Summary Table
# -------------------------------
with st.expander("📋 Show Full Cluster Summary"):
    st.dataframe(df, use_container_width=True)

# -------------------------------
# Clustered Details Section
# -------------------------------
cluster_df = df[df['Cluster_ID'] == selected_cluster]

st.subheader(f"🧪 Cluster {selected_cluster} Details")

col1, col2 = st.columns([3, 2])

with col1:
    st.markdown("#### 🔢 Clustered Material Descriptions")
    st.dataframe(
        cluster_df[['Cluster_Members_Unique', 'Cluster_MATERIAL_NUMBERS']],
        use_container_width=True,
        hide_index=True
    )

with col2:
    st.markdown("#### ✅ Suggested Standard Material Number")
    st.success(cluster_df['Suggested_Material_Number'].values[0])

    member_string = cluster_df['Cluster_Members_All'].values[0]
    item_count = len(member_string.split(" | "))
    st.markdown("#### 📌 Total Items in Cluster")
    st.metric(label="Total Items in Cluster", value=item_count)

# -------------------------------
# Footer
# -------------------------------
st.markdown("""
    <hr>
    <div style='text-align: center; font-size: 14px;'>
        Created with ❤️ by <b>Your Team</b> | Powered by <b>Streamlit + SBERT</b>
    </div>
""", unsafe_allow_html=True)
