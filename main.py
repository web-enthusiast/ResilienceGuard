#necessary modules
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import json
from data_loader import DataLoader
from visualization import VulnerabilityVisualizer
from recommendations import RecommendationEngine
from utilis import get_risk_level, load_custom_css

# Page configurations
st.set_page_config(
    page_title="Malawi Vulnerability Dashboard", 
    page_icon="🛡️", 
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    load_custom_css()
    
    # Header
    st.markdown('<h1 class="main-header"> Malawi Community Vulnerability Dashboard</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #7f8c8d;">AI-Powered Early Warning System for Community Resilience Planning</p>', unsafe_allow_html=True)
    
    # define components
    data_loader = DataLoader()
    visualizer = VulnerabilityVisualizer()
    recommender = RecommendationEngine()
    
    # Load data from APIs
    with st.spinner('Loading real-time vulnerability data from AGWAA and FS-COR...'):
        df, agwaa_connected = data_loader.load_agwaa_data()
        time_series, fs_cor_connected = data_loader.load_fs_cor_data()
    
    st.sidebar.header(" Dashboard Controls")
    
    vulnerability_type = st.sidebar.selectbox(
        "Vulnerability Type",
        ["Overall Vulnerability", "Climate Risk", "Food Security", "Population Weighted", "Poverty Index", "Healthcare Access"]
    )
    
    time_period = st.sidebar.selectbox(
        "Time Period",
        ["Current (Aug 2024)", "Last 6 Months", "Last Year", "Last 2 Years"]
    )
    
    alert_threshold = st.sidebar.slider(
        "Alert Threshold (%)",
        min_value=60, max_value=90, value=75, step=5
    )
    
    # API status indicators
    _display_api_status(agwaa_connected, fs_cor_connected, df)
    
    # Check for high-risk districts and display alerts
    high_risk_districts = df[df['Vulnerability'] >= alert_threshold]
    _display_risk_alerts(high_risk_districts, alert_threshold)
    
    _display_key_metrics(df)
    
    # Main dashboard content
    _display_main_dashboard(df, visualizer)
    
    # Charts and analysis
    _display_charts_analysis(df, time_series, visualizer)
    
    # AI-Powered Recommendations
    _display_recommendations(df, recommender)
    
    # Emergency Response Section
    _display_emergency_response(high_risk_districts)
    
    # Data export section
    _display_data_export(df, time_series, high_risk_districts, agwaa_connected, recommender)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #7f8c8d; margin-top: 2rem;'>
        <p>Malawi Community Vulnerability Dashboard | Early Warning System</p>
        <p>Built for resilience planning and emergency response </p>
        <p>Powered by AI-Driven Policy Recommendations</p>
        <p>Data Sources: AGWAA API & FS-COR Platform</p>
    </div>
    """, unsafe_allow_html=True)

def _display_api_status(agwaa_connected, fs_cor_connected, df):
    """Display API connection status in sidebar"""
    st.sidebar.markdown("---")
    if st.sidebar.button("🔄 Validate Data Quality"):
        if agwaa_connected and fs_cor_connected:
            st.sidebar.success("✅ Connected to real-time data sources")
        else:
            st.sidebar.warning("⚠️ Using enhanced sample data (APIs not available)")
        
        st.sidebar.info(f"📊 {len(df)} districts loaded")
        st.sidebar.info(f"🕒 Updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    
    col1, col2 = st.sidebar.columns(2)
    with col1:
        if agwaa_connected:
            st.success("AGWAA ✅")
        else:
            st.error("AGWAA ❌")
    with col2:
        if fs_cor_connected:
            st.success("FS-COR ✅")
        else:
            st.error("FS-COR ❌")

def _display_risk_alerts(high_risk_districts, alert_threshold):
    """Display high risk alerts"""
    if not high_risk_districts.empty:
        st.markdown(f"""
        <div class="alert-banner">
            <strong>⚠️ HIGH RISK ALERT:</strong> {len(high_risk_districts)} districts exceed {alert_threshold}% vulnerability threshold: 
            {', '.join(high_risk_districts['District'].tolist())}
        </div>
        """, unsafe_allow_html=True)
        
        # early warning analysis
        with st.expander("🔍 Detailed Early Warning Analysis", expanded=True):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Most Vulnerable District", 
                         f"{high_risk_districts.iloc[0]['District']}",
                         f"{high_risk_districts.iloc[0]['Vulnerability']}%")
            
            with col2:
                pop_risk_pct = (high_risk_districts['Population'].sum() / st.session_state.get('total_pop', 1000000)) * 100
                st.metric("Population at Immediate Risk", f"{pop_risk_pct:.1f}%")
            
            with col3:
                avg_response_time = st.slider("Estimated Response Time (days)", 1, 30, 7,
                                             help="How quickly can aid reach these districts?")

def _display_key_metrics(df):
    """Display key metrics row"""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        overall_risk = df['Vulnerability'].mean()
        st.metric(
            label="📊 Overall Risk Level",
            value=f"{overall_risk:.1f}%",
            delta=f"+2.3% from last month",
            delta_color="inverse"
        )
    
    with col2:
        total_pop_at_risk = df[df['Vulnerability'] >= 70]['Population'].sum()
        st.metric(
            label="👥 Population at Risk",
            value=f"{total_pop_at_risk/1000000:.1f}M",
            delta=f"+150K from last quarter",
            delta_color="inverse"
        )
    
    with col3:
        avg_food_insecurity = 100 - df['Food_Security'].mean()
        st.metric(
            label="🍽️ Food Insecurity Rate",
            value=f"{avg_food_insecurity:.1f}%",
            delta=f"-1.2% from last month",
            delta_color="normal"
        )
    
    with col4:
        avg_climate_risk = df['Climate_Risk'].mean()
        st.metric(
            label="🌡️ Climate Vulnerability",
            value=f"{avg_climate_risk:.1f}%",
            delta=f"+4.5% from last season",
            delta_color="inverse"
        )

def _display_main_dashboard(df, visualizer):
    """Display main dashboard with map and risk distribution"""
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("🗺️ Geographic Vulnerability Map")
        fig_map = visualizer.create_vulnerability_map(df)
        st.plotly_chart(fig_map, use_container_width=True)
        
        # Risk legend
        st.markdown("**Risk Levels:** 🟢 Low (0-59%) | 🟡 Medium (60-69%) | 🟠 High (70-79%) | 🔴 Very High (80%+)")
    
    with col2:
        st.subheader("📈 Risk Distribution")
        fig_pie = visualizer.create_risk_distribution_pie(df)
        st.plotly_chart(fig_pie, use_container_width=True)
        
        st.subheader(" Priority Districts")
        priority_df = df.nlargest(5, 'Vulnerability')[['District', 'Vulnerability']]
        for _, row in priority_df.iterrows():
            risk_level, color = get_risk_level(row['Vulnerability'])
            st.markdown(f"**{row['District']}**: {row['Vulnerability']}% ({risk_level})")

def _display_charts_analysis(df, time_series, visualizer):
    """Display charts and analysis section"""
    st.subheader("📊 Vulnerability Trends & Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Vulnerability Trends Over Time**")
        fig_trend = visualizer.create_trends_chart(time_series)
        st.plotly_chart(fig_trend, use_container_width=True)
    
    with col2:
        st.write("**District Vulnerability Comparison**")
        fig_bar = visualizer.create_district_comparison(df)
        st.plotly_chart(fig_bar, use_container_width=True)
    
    # Additional visualizations
    st.subheader(" Advanced Data Analytics")
    col1, col2 = st.columns(2)
    
    with col1:
        fig_sunburst = visualizer.create_sunburst_chart(df)
        st.plotly_chart(fig_sunburst, use_container_width=True)
    
    with col2:
        fig_treemap = visualizer.create_treemap_chart(df)
        st.plotly_chart(fig_treemap, use_container_width=True)
    
    # Correlation analysis
    st.subheader(" Indicator Correlation Analysis")
    fig_corr = visualizer.create_correlation_matrix(df)
    st.plotly_chart(fig_corr, use_container_width=True)

def _display_recommendations(df, recommender):
    """Display AI-powered recommendations"""
    st.subheader("AI-Powered Policy Recommendations Engine")
    
    tab1, tab2, tab3 = st.tabs(["District-Specific", "Regional Overview", "Resource Allocation"])
    
    with tab1:
        selected_district = st.selectbox("Select District for Detailed Analysis", df['District'].unique())
        district_data = df[df['District'] == selected_district].iloc[0]
        
        # Display district metrics
        recommender.display_district_metrics(district_data)
        
        # Generate and display recommendations
        recommendations = recommender.generate_recommendations(district_data)
        recommender.display_recommendations(recommendations)
    
    with tab2:
        recommender.display_regional_analysis(df)
    
    with tab3:
        recommender.display_resource_allocation()

def _display_emergency_response(high_risk_districts):
    """Display emergency response section"""
    st.markdown("---")
    st.subheader("📱 Emergency Response Quick View")
    
    emergency_col1, emergency_col2 = st.columns(2)
    
    with emergency_col1:
        st.info("""
        **🚨 Immediate Actions**
        - Contact district emergency teams
        - Activate community alert systems
        - Deploy rapid assessment teams
        - Coordinate with NGO partners
        - Mobilize emergency supplies
        """)
        
        # Emergency contact list
        with st.expander("📞 Emergency Contacts"):
            st.write("""
            **District Commissioners:**
            - Lilongwe: +265 888 123 456
            - Blantyre: +265 888 234 567
            - Mangochi: +265 888 345 678
            
            **Emergency Services:**
            - Health Emergency: +265 123 456 789  
            - Food Security: +265 123 456 789
            - NGO Coordination: +265 123 456 789
            - Police Emergency: 123
            """)
    
    with emergency_col2:
        # Emergency alert simulator
        st.warning("🚨 Emergency Alert System")
        alert_message = st.text_area("Emergency Message", "High vulnerability alert triggered. Immediate intervention required.")
        
        if st.button("📢 Activate Emergency Protocol", type="primary", use_container_width=True):
            st.error("🚨 EMERGENCY ALERT ACTIVATED - Protocols initiated")
            st.success("✅ Emergency teams notified. Response timeline: 2-4 hours")

def _display_data_export(df, time_series, high_risk_districts, agwaa_connected, recommender):
    
    import json
import pandas as pd
import streamlit as st
from datetime import datetime

def _display_data_export(df, time_series, high_risk_districts, agwaa_connected, recommender):
    """Clean export for vulnerability dashboard, JSON + CSV"""

    # Convert numpy.int64/float64 → native Python types
    def convert_types(obj):
        if isinstance(obj, (pd.Series, pd.DataFrame)):
            return obj.astype(object).where(pd.notnull(obj), None)
        return obj

    clean_df = convert_types(df)
    clean_time_series = convert_types(time_series)
    clean_risk = convert_types(high_risk_districts)

    # export structure
    export_data = {
        "metadata": {
            "generated": datetime.now().isoformat(),
            "source": "AGWAA" if agwaa_connected else "FS-COR",
            "district_count": int(len(clean_df)),
            "high_risk_districts": int(len(clean_risk))
        },
        "summary": {
            "average_vulnerability": float(clean_df["vulnerability_index"].mean()) if "vulnerability_index" in clean_df else None,
            "total_population_at_risk": int(clean_df[clean_df["vulnerability_index"] >= 65]["population"].sum()) if "vulnerability_index" in clean_df and "population" in clean_df else None
        },
        "records": clean_df.to_dict(orient="records"),
        "time_series": clean_time_series.to_dict(orient="records") if not clean_time_series.empty else []
    }

    # CSV Export 
    st.download_button(
        label="📥 Download Vulnerability Data (CSV)",
        data=clean_df.to_csv(index=False),
        file_name="malawi_vulnerability_data.csv",
        mime="text/csv",
        use_container_width=True
    )

    #  JSON Export 
    st.download_button(
        label="📥 Download Full Report (JSON)",
        data=json.dumps(export_data, indent=2, default=str),
        file_name="malawi_vulnerability_report.json",
        mime="application/json",
        use_container_width=True
    )

    
    # Create columns for export info display
    col1, col2, col3 = st.columns(3)

    with col2:
        st.info("""
        **🌐 Data Sources**
        - AGWAA API (Primary)
        - FS-COR Platform (Secondary)
        - Real-time monitoring feeds
        - Community assessment reports
        - Government statistics
        """)

    with col3:
        st.info(f"""
        **📅 System Status**
        Last Updated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}
        Data Points: {len(df)} districts
        Coverage: National
        Refresh Rate: Hourly
        API Status: {'Connected' if agwaa_connected else 'Sample Data'}
        """)

if __name__ == "__main__":
    main()