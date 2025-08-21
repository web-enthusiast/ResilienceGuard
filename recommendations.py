import streamlit as st
import plotly.express as px
import pandas as pd
from visualization import VulnerabilityVisualizer

class RecommendationEngine:
    """AI-powered policy recommendation system"""
    
    def __init__(self):
        self.visualizer = VulnerabilityVisualizer()
    
    def generate_recommendations(self, district_data):
        """Generate AI-powered policy recommendations based on district data"""
        recommendations = []
        
        # Critical vulnerability threshold
        if district_data['Vulnerability'] > 80:
            recommendations.append({
                'priority': 'CRITICAL',
                'action': 'Immediate humanitarian intervention required',
                'timeline': 'Within 72 hours',
                'resources': 'Emergency response teams, food aid, medical supplies',
                'impact': 'Prevent loss of life and livelihood',
                'cost_estimate': '$250K - $500K',
                'expected_outcome': 'Stabilize immediate threats to vulnerable populations',
                'success_metrics': 'Zero casualties, food distributed to 90% of population'
            })
        
        # Food security interventions
        if district_data['Food_Security'] < 65:
            recommendations.append({
                'priority': 'HIGH',
                'action': 'Scale up food distribution and agricultural support',
                'timeline': '1-2 weeks',
                'resources': 'Seeds, fertilizers, food packages, training programs',
                'impact': 'Ensure food security for vulnerable populations',
                'cost_estimate': '$100K - $200K',
                'expected_outcome': 'Increase food security index by 15-20%',
                'success_metrics': 'Food security improved to >70% within 3 months'
            })
        
        # Climate adaptation measures
        if district_data['Climate_Risk'] > 75:
            recommendations.append({
                'priority': 'HIGH', 
                'action': 'Climate adaptation and resilience measures',
                'timeline': '2-4 weeks',
                'resources': 'Irrigation systems, drought-resistant crops, early warning systems',
                'impact': 'Build long-term climate resilience',
                'cost_estimate': '$150K - $300K',
                'expected_outcome': 'Reduce climate vulnerability by 20%',
                'success_metrics': 'Climate risk index reduced to <70% within 6 months'
            })
        
        # Economic empowerment
        if district_data.get('Poverty_Rate', 0) > 55:
            recommendations.append({
                'priority': 'MEDIUM',
                'action': 'Economic empowerment and livelihood programs',
                'timeline': '1-3 months',
                'resources': 'Microfinance, vocational training, job creation initiatives',
                'impact': 'Reduce poverty and economic vulnerability',
                'cost_estimate': '$200K - $400K',
                'expected_outcome': 'Reduce poverty rate by 10-15%',
                'success_metrics': 'Poverty rate decreased to <50% within 12 months'
            })
        
        # Healthcare access improvement
        if district_data.get('Healthcare_Access', 100) < 50:
            recommendations.append({
                'priority': 'HIGH',
                'action': 'Healthcare infrastructure and access improvement',
                'timeline': '2-6 weeks',
                'resources': 'Mobile clinics, medical supplies, health workers',
                'impact': 'Improve health outcomes and reduce mortality',
                'cost_estimate': '$180K - $350K',
                'expected_outcome': 'Improve healthcare access by 25%',
                'success_metrics': 'Healthcare access >65% within 4 months'
            })
        
        # Water and sanitation
        if district_data.get('Water_Access', 100) < 60:
            recommendations.append({
                'priority': 'MEDIUM',
                'action': 'Water access and sanitation improvement',
                'timeline': '3-8 weeks',
                'resources': 'Boreholes, water purification systems, sanitation facilities',
                'impact': 'Improve water security and reduce water-borne diseases',
                'cost_estimate': '$120K - $250K',
                'expected_outcome': 'Increase water access by 20%',
                'success_metrics': 'Water access >75% within 6 months'
            })
        
        # Nutrition interventions
        if district_data.get('Nutrition_Index', 100) < 55:
            recommendations.append({
                'priority': 'HIGH',
                'action': 'Nutrition supplementation and education programs',
                'timeline': '2-4 weeks',
                'resources': 'Nutritional supplements, feeding programs, education',
                'impact': 'Improve nutritional status, especially for children',
                'cost_estimate': '$80K - $150K',
                'expected_outcome': 'Improve nutrition index by 15%',
                'success_metrics': 'Child malnutrition reduced by 20% within 6 months'
            })
        
        # Drought mitigation
        if district_data.get('Rainfall_Deviation', 0) < -20:
            recommendations.append({
                'priority': 'MEDIUM',
                'action': 'Drought mitigation and water conservation',
                'timeline': '1-2 months',
                'resources': 'Water conservation systems, drought-resistant crops',
                'impact': 'Reduce impact of rainfall deficit on agriculture',
                'cost_estimate': '$100K - $200K',
                'expected_outcome': 'Increase agricultural resilience by 25%',
                'success_metrics': 'Crop yield maintained despite rainfall deficit'
            })
        
        # Default monitoring recommendation
        if not recommendations:
            recommendations.append({
                'priority': 'LOW',
                'action': 'Maintain current monitoring and support programs',
                'timeline': 'Ongoing',
                'resources': 'Regular assessment teams, community support',
                'impact': 'Sustain current stability and preparedness',
                'cost_estimate': '$50K - $100K',
                'expected_outcome': 'Maintain current vulnerability levels',
                'success_metrics': 'No deterioration in key indicators'
            })
        
        return recommendations
    
    def display_district_metrics(self, district_data):
        """Display comprehensive district metrics"""
        # Basic metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Vulnerability Score", f"{district_data['Vulnerability']}%")
            st.metric("Food Security", f"{district_data['Food_Security']}%")
        with col2:
            st.metric("Climate Risk", f"{district_data['Climate_Risk']}%")
            st.metric("Poverty Rate", f"{district_data.get('Poverty_Rate', 'N/A')}%")
        with col3:
            st.metric("Healthcare Access", f"{district_data.get('Healthcare_Access', 'N/A')}%")
            st.metric("Water Access", f"{district_data.get('Water_Access', 'N/A')}%")
        
        # Additional metrics
        col4, col5, col6 = st.columns(3)
        with col4:
            st.metric("Nutrition Index", f"{district_data.get('Nutrition_Index', 'N/A')}%")
        with col5:
            st.metric("Rainfall Deviation", f"{district_data.get('Rainfall_Deviation', 'N/A')}%")
        with col6:
            st.metric("Infant Mortality", f"{district_data.get('Infant_Mortality', 'N/A')}%")
        
        # Multi-indicator radar chart
        fig_radar = self.visualizer.create_multi_indicator_radar(district_data)
        st.plotly_chart(fig_radar, use_container_width=True)
    
    def display_recommendations(self, recommendations):
        """Display formatted recommendations with priority styling"""
        st.subheader("🎯 Recommended Interventions")
        
        for i, rec in enumerate(recommendations):
            priority_class = ""
            icon = ""
            
            if rec['priority'] == 'CRITICAL':
                priority_class = "critical-priority"
                icon = "🔴"
            elif rec['priority'] == 'HIGH':
                priority_class = "high-priority" 
                icon = "🟠"
            else:
                priority_class = "medium-priority"
                icon = "🟡"
            
            with st.expander(f"{icon} {rec['priority']} PRIORITY: {rec['action']}", expanded=(i==0)):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**Timeline:** {rec['timeline']}")
                    st.write(f"**Resources Needed:** {rec['resources']}")
                    st.write(f"**Expected Impact:** {rec['impact']}")
                
                with col2:
                    st.write(f"**Cost Estimate:** {rec['cost_estimate']}")
                    st.write(f"**Expected Outcome:** {rec.get('expected_outcome', 'To be determined')}")
                    st.write(f"**Success Metrics:** {rec.get('success_metrics', 'To be defined')}")
                
                # Progress tracking placeholder
                if rec['priority'] == 'CRITICAL':
                    st.progress(0.0)
                    st.caption("Implementation Progress: Not Started")
    
    def display_regional_analysis(self, df):
        """Display regional overview and analysis"""
        st.subheader("Regional Intervention Strategy")
        
        # Regional priority information
        st.info("""
        **🌍 Regional Priority Areas:**
        - **Southern Region:** Focus on climate adaptation and food security (Blantyre, Mangochi, Zomba)
        - **Central Region:** Address urban vulnerability and healthcare access (Lilongwe, Dedza, Ntcheu)
        - **Northern Region:** Combat poverty and improve infrastructure (Mzuzu, Karonga)
        """)
        
        # Regional comparison chart
        fig_regional = self.visualizer.create_regional_analysis(df)
        st.plotly_chart(fig_regional, use_container_width=True)
        
        # Regional intervention matrix
        st.subheader("📋 Regional Intervention Matrix")
        
        regional_matrix = {
            'Region': ['Southern', 'Central', 'Northern'],
            'Priority Interventions': [
                'Climate adaptation, Food security, Drought mitigation',
                'Healthcare access, Urban resilience, Economic empowerment', 
                'Infrastructure development, Poverty reduction, Water access'
            ],
            'Estimated Cost': ['$2.5M - $4M', '$2M - $3.5M', '$1.8M - $3M'],
            'Timeline': ['6-12 months', '4-8 months', '8-15 months'],
            'Expected Impact': ['High', 'Medium-High', 'Medium']
        }
        
        st.dataframe(pd.DataFrame(regional_matrix), use_container_width=True)
    
    def display_resource_allocation(self):
        """Display optimal resource allocation strategy"""
        st.subheader("Optimal Resource Allocation Strategy")
        
        # Resource allocation visualization
        fig_alloc = self.visualizer.create_resource_allocation_pie()
        st.plotly_chart(fig_alloc, use_container_width=True)
        
        st.warning("""
        **💰 Recommended Resource Distribution:**
        - **40%** to high-vulnerability districts (Mangochi, Kasungu, Mchinji)
        - **30%** to medium-vulnerability districts (Blantyre, Zomba, Nkhotakota)  
        - **20%** to prevention programs in lower-risk areas
        - **10%** to monitoring, evaluation, and capacity building
        """)
        
        # Cost-benefit analysis
        st.subheader("💡 Cost-Benefit Analysis")
        fig_cost_benefit = self.visualizer.create_cost_benefit_analysis()
        st.plotly_chart(fig_cost_benefit, use_container_width=True)
        
        # Investment priorities table
        st.subheader("📊 Investment Priorities Ranking")
        
        investment_data = {
            'Intervention Type': ['Food Security Programs', 'Healthcare Infrastructure', 
                                'Water & Sanitation', 'Climate Adaptation', 'Economic Empowerment'],
            'ROI Score': [92, 85, 88, 78, 75],
            'Urgency Level': ['Very High', 'High', 'High', 'Medium', 'Medium'],
            'Implementation Complexity': ['Low', 'Medium', 'Medium', 'High', 'High'],
            'Recommended Budget %': [35, 25, 20, 15, 5]
        }
        
        investment_df = pd.DataFrame(investment_data)
        st.dataframe(investment_df, use_container_width=True)
        
        # Funding sources and partnerships
        st.subheader("🤝 Recommended Funding Sources & Partnerships")
        
        funding_info = """
        **International Partners:**
        - World Food Programme (WFP) - Food security interventions
        - UNICEF - Healthcare and nutrition programs  
        - World Bank - Infrastructure and economic development
        - USAID - Agricultural development and climate adaptation
        
        **Regional Partners:**
        - African Development Bank - Infrastructure financing
        - COMESA - Regional trade and food security
        - SADC - Climate adaptation initiatives
        
        **Implementation Timeline:**
        - Phase 1 (0-3 months): Emergency interventions and immediate relief
        - Phase 2 (3-12 months): Infrastructure development and capacity building
        - Phase 3 (12+ months): Long-term resilience and sustainability programs
        """
        
        st.info(funding_info)
    
    def generate_implementation_plan(self, recommendations):
        """Generate detailed implementation plan"""
        implementation_phases = {
            'Immediate (0-1 month)': [],
            'Short-term (1-6 months)': [],
            'Medium-term (6-12 months)': [],
            'Long-term (12+ months)': []
        }
        
        for rec in recommendations:
            timeline = rec['timeline'].lower()
            if 'hour' in timeline or 'day' in timeline or 'week' in timeline:
                if 'week' in timeline and int(timeline.split()[0]) <= 4:
                    implementation_phases['Immediate (0-1 month)'].append(rec)
                else:
                    implementation_phases['Short-term (1-6 months)'].append(rec)
            elif 'month' in timeline:
                months = int(timeline.split()[0]) if timeline.split()[0].isdigit() else 6
                if months <= 6:
                    implementation_phases['Short-term (1-6 months)'].append(rec)
                else:
                    implementation_phases['Medium-term (6-12 months)'].append(rec)
            else:
                implementation_phases['Long-term (12+ months)'].append(rec)
        
        return implementation_phases
    
    def calculate_total_investment(self, recommendations):
        """Calculate total investment requirements"""
        total_min = 0
        total_max = 0
        
        for rec in recommendations:
            cost_range = rec['cost_estimate']
            if '$' in cost_range and 'K' in cost_range:
                # Parse cost range like "$100K - $200K"
                costs = cost_range.replace('$', '').replace('K', '').replace(' ', '').split('-')
                if len(costs) == 2:
                    total_min += int(costs[0]) * 1000
                    total_max += int(costs[1]) * 1000
        
        return total_min, total_max