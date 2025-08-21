import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

class VulnerabilityVisualizer:
    """Handle all visualization components for the vulnerability dashboard"""
    
    def __init__(self):
        self.color_scale = ["#27ae60", "#f1c40f", "#f39c12", "#e74c3c"]
        self.risk_colors = {
            'Low': '#27ae60',
            'Medium': '#f1c40f', 
            'High': '#f39c12',
            'Very High': '#e74c3c'
        }
    
    def create_vulnerability_map(self, df):
        """Create the main geographic vulnerability map"""
        fig_map = px.scatter_mapbox(
            df, 
            lat="Lat", 
            lon="Lng",
            size="Population",
            color="Vulnerability",
            hover_name="District",
            hover_data={
                "Vulnerability": True,
                "Population": ":,",
                "Food_Security": True,
                "Climate_Risk": True,
                "Nutrition_Index": True,
                "Rainfall_Deviation": True,
                "Lat": False,
                "Lng": False
            },
            color_continuous_scale=self.color_scale,
            size_max=25,
            zoom=5.5,
            center={"lat": -13.2543, "lon": 34.3015},
            mapbox_style="open-street-map",
            height=500,
            title="Malawi Districts Vulnerability Map"
        )
        
        fig_map.update_layout(
            coloraxis_colorbar=dict(title="Vulnerability %"),
            font=dict(size=12)
        )
        
        return fig_map
    
    def create_risk_distribution_pie(self, df):
        """Create pie chart for risk distribution"""
        risk_counts = pd.cut(df['Vulnerability'], 
                           bins=[0, 60, 70, 80, 100], 
                           labels=['Low', 'Medium', 'High', 'Very High']).value_counts()
        
        fig_pie = px.pie(
            values=risk_counts.values,
            names=risk_counts.index,
            color_discrete_map=self.risk_colors,
            title="Risk Level Distribution"
        )
        fig_pie.update_layout(height=300)
        return fig_pie
    
    def create_trends_chart(self, time_series):
        """Create multi-line trend chart"""
        fig_trend = px.line(
            time_series, 
            x='Month', 
            y=['Vulnerability', 'Food_Insecurity', 'Climate_Risk'],
            title="Multi-dimensional Vulnerability Analysis",
            labels={'value': 'Score (%)', 'variable': 'Indicator'}
        )
        fig_trend.update_layout(height=350)
        return fig_trend
    
    def create_district_comparison(self, df):
        """Create horizontal bar chart for district comparison"""
        fig_bar = px.bar(
            df.sort_values('Vulnerability', ascending=True),
            x='Vulnerability',
            y='District',
            color='Vulnerability',
            color_continuous_scale=self.color_scale,
            orientation='h',
            title="District Vulnerability Ranking"
        )
        fig_bar.update_layout(height=350, showlegend=False)
        return fig_bar
    
    def create_sunburst_chart(self, df):
        """Create sunburst chart for population vulnerability distribution"""
        fig_sunburst = px.sunburst(
            df, 
            path=['District'], 
            values='Population',
            color='Vulnerability',
            title="Population Vulnerability Distribution",
            color_continuous_scale="reds"
        )
        return fig_sunburst
    
    def create_treemap_chart(self, df):
        """Create treemap for climate risk concentration"""
        fig_treemap = px.treemap(
            df,
            path=['District'],
            values='Vulnerability',
            color='Climate_Risk',
            title="Climate Risk Concentration",
            color_continuous_scale="reds"
        )
        return fig_treemap
    
    def create_correlation_matrix(self, df):
        """Create correlation matrix heatmap"""
        # Select only numeric columns for correlation
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        correlation_matrix = df[numeric_cols].corr()
        
        fig_corr = px.imshow(
            correlation_matrix,
            title="Correlation Between Vulnerability Indicators",
            color_continuous_scale="RdBu_r",
            aspect="auto"
        )
        return fig_corr
    
    def create_risk_projection_chart(self, high_risk_districts):
        """Create risk projection timeline"""
        if high_risk_districts.empty:
            return None
            
        projection_data = {
            'Days': [0, 7, 14, 21, 30],
            'Risk_Level': [
                high_risk_districts['Vulnerability'].mean(),
                high_risk_districts['Vulnerability'].mean() * 1.05,
                high_risk_districts['Vulnerability'].mean() * 1.10,
                high_risk_districts['Vulnerability'].mean() * 1.15,
                high_risk_districts['Vulnerability'].mean() * 1.20
            ]
        }
        
        fig_proj = px.line(
            projection_data, 
            x='Days', 
            y='Risk_Level', 
            title="Risk Escalation Projection Without Intervention",
            markers=True
        )
        fig_proj.add_hline(y=90, line_dash="dash", line_color="red", 
                          annotation_text="Critical Threshold")
        return fig_proj
    
    def create_regional_analysis(self, df):
        """Create regional comparison charts"""
        regions = {
            'Southern': ['Blantyre', 'Mangochi', 'Zomba'],
            'Central': ['Lilongwe', 'Dedza', 'Ntcheu', 'Salima', 'Nkhotakota'],
            'Northern': ['Mzuzu', 'Karonga']
        }
        
        # Create regional data
        regional_data = []
        for region, districts in regions.items():
            region_df = df[df['District'].isin(districts)]
            if not region_df.empty:
                regional_data.append({
                    'Region': region,
                    'Vulnerability': region_df['Vulnerability'].mean(),
                    'Food_Security': region_df['Food_Security'].mean(),
                    'Climate_Risk': region_df['Climate_Risk'].mean(),
                    'Population': region_df['Population'].sum()
                })
        
        regional_df = pd.DataFrame(regional_data)
        
        fig_regional = px.bar(
            regional_df, 
            x='Region', 
            y='Vulnerability', 
            title="Average Vulnerability by Region",
            color='Vulnerability',
            color_continuous_scale=self.color_scale
        )
        return fig_regional
    
    def create_resource_allocation_pie(self):
        """Create resource allocation visualization"""
        allocation_data = {
            'Category': ['High Risk', 'Medium Risk', 'Prevention', 'Monitoring'],
            'Percentage': [40, 30, 20, 10]
        }
        
        colors = ['#e74c3c', '#f39c12', '#27ae60', '#3498db']
        
        fig_alloc = px.pie(
            allocation_data, 
            values='Percentage', 
            names='Category', 
            title="Optimal Resource Allocation Strategy",
            color_discrete_sequence=colors
        )
        return fig_alloc
    
    def create_cost_benefit_analysis(self):
        """Create cost-benefit scatter plot"""
        cost_benefit_data = {
            'Intervention': ['Food Security', 'Healthcare', 'Water Access', 'Climate Adaptation'],
            'Cost (USD)': [200000, 300000, 150000, 250000],
            'Benefit Score': [85, 75, 90, 80],
            'Timeframe (months)': [3, 6, 4, 8]
        }
        
        cost_benefit_df = pd.DataFrame(cost_benefit_data)
        
        fig_cost_benefit = px.scatter(
            cost_benefit_df, 
            x='Cost (USD)', 
            y='Benefit Score',
            size='Timeframe (months)', 
            color='Intervention',
            title="Cost-Benefit Analysis of Interventions",
            hover_name='Intervention'
        )
        return fig_cost_benefit
    
    def create_multi_indicator_radar(self, district_data):
        """Create radar chart for multi-indicator analysis"""
        categories = ['Food_Security', 'Healthcare_Access', 'Water_Access', 
                     'Nutrition_Index', 'Climate_Risk']
        
        values = [district_data.get(cat, 50) for cat in categories]
        
        fig_radar = go.Figure()
        
        fig_radar.add_trace(go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            name=district_data['District']
        ))
        
        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )),
            showlegend=True,
            title=f"Multi-Indicator Profile: {district_data['District']}"
        )
        
        return fig_radar
    
    def create_vulnerability_heatmap(self, df):
        """Create district-indicator heatmap"""
        # Select key indicators for heatmap
        indicators = ['Vulnerability', 'Food_Security', 'Climate_Risk', 
                     'Poverty_Rate', 'Healthcare_Access', 'Water_Access']
        
        # Prepare data for heatmap
        heatmap_data = df[['District'] + indicators].set_index('District')
        
        fig_heatmap = px.imshow(
            heatmap_data.T,
            title="District-Indicator Vulnerability Heatmap",
            color_continuous_scale="reds",
            aspect="auto"
        )
        
        fig_heatmap.update_layout(
            xaxis_title="Districts",
            yaxis_title="Indicators"
        )
        
        return fig_heatmap
    
    def create_population_risk_bubble(self, df):
        """Create population-risk bubble chart"""
        fig_bubble = px.scatter(
            df,
            x="Population",
            y="Vulnerability",
            size="Climate_Risk",
            color="Food_Security",
            hover_name="District",
            title="Population vs Vulnerability (Bubble size = Climate Risk)",
            size_max=60,
            color_continuous_scale="RdYlGn_r"
        )
        
        fig_bubble.update_layout(
            xaxis_title="Population",
            yaxis_title="Vulnerability Score (%)"
        )
        
        return fig_bubble