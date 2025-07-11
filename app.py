# using new_app.py here

import streamlit as st
from ingest.spark_ingest import load_spark_data
from ingest.k8s_ingest import load_k8s_data
from ingest.cloud_ingest import load_cloud_data
from ingest.db_ingest import load_db_data
from core.recommender import Recommender
from core.cost_estimator import CostEstimator

st.set_page_config(page_title="Cost Optimization Planner", layout="wide")
st.title("🧠 AI-Powered Cost Optimization Planner")

@st.cache_data
def load_all_data():
    spark = load_spark_data("data/spark_sample.json")
    k8s = load_k8s_data("data/k8s_sample.json")
    cloud = load_cloud_data("data/cloud_sample.json")
    db = load_db_data("data/db_sample.json")
    return spark, k8s, cloud, db

spark_data, k8s_data, cloud_data, db_data = load_all_data()

if st.button("🔍 Analyze & Generate Recommendations"):
    recommender = Recommender()
    recommendations = recommender.generate_recommendations(spark_data, k8s_data, cloud_data, db_data)

    estimator = CostEstimator()
    savings = estimator.estimate_savings(recommendations)

    st.header("📋 Recommendations")
    if recommendations:
        st.dataframe(recommendations)
    else:
        st.info("No actionable recommendations found.")

    st.header("💰 Estimated Savings")
    savings['hourly_saving'] = savings['monthly_saving'] / 30 / 24  # 🔥 Added this line
    st.metric("Hourly Saving", f"${savings['hourly_saving']:.2f}")
    st.metric("Monthly Saving", f"${savings['monthly_saving']:.2f}")

else:
    st.info("Click the button above to start analysis.")