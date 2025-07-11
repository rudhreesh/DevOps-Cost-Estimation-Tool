import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd

# Simulated recommendation generator
def get_recommendations(domain):
    if domain == "Spark Jobs":
        return [
            {"description": "Reduce number of executors", "impact": "High", "risk": "Low", "savings": "$120/month"},
            {"description": "Optimize shuffle partitions", "impact": "Medium", "risk": "Medium", "savings": "$75/month"}
        ]
    elif domain == "Kubernetes":
        return [
            {"description": "Right-size CPU request for nginx-pod", "impact": "High", "risk": "Low", "savings": "$90/month"},
            {"description": "Remove idle pod: old-worker", "impact": "Medium", "risk": "Low", "savings": "$45/month"}
        ]
    elif domain == "Cloud Services":
        return [
            {"description": "Downsize VM instance: db-server", "impact": "High", "risk": "Low", "savings": "$200/month"},
            {"description": "Move logs to cold storage", "impact": "Medium", "risk": "Low", "savings": "$60/month"}
        ]
    elif domain == "Databases":
        return [
            {"description": "Downscale rarely used DB instance", "impact": "Medium", "risk": "Low", "savings": "$80/month"},
            {"description": "Add index to slow query table", "impact": "Medium", "risk": "Low", "savings": "$50/month"}
        ]
    else:
        return []

# -------------------------------
# Streamlit App UI
# -------------------------------

st.set_page_config(page_title="Cost Optimization Planner", layout="wide")
st.title("💰 Cloud Cost Optimization Planner")

st.markdown("Select a domain below to view optimization recommendations.")

domain_options = [
    "Spark Jobs",
    "Kubernetes",
    "Cloud Services",
    "Databases"
]

# Use option_menu for a non-typeable clickable menu
selected_domain = option_menu(
    menu_title="Choose a domain:",
    options=domain_options,
    icons=["cpu", "cloud", "server", "database"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",  # You can use "vertical" if you prefer
)

# Get recommendations based on selected domain
recommendations = get_recommendations(selected_domain)

if recommendations:
    st.subheader(f"🔍 Recommendations for {selected_domain}")

    df = pd.DataFrame(recommendations)
    st.dataframe(df)

    total_savings = sum(int(r['savings'].replace('$', '').split("/")[0]) for r in recommendations)
    st.success(f"✅ Estimated Monthly Savings: **${total_savings}**")
else:
    st.warning("No recommendations found for this domain.")
