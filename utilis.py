import streamlit as st
from datetime import datetime
import json

def get_risk_level(score):
    """Convert vulnerability score to risk level and color"""
    if score >= 80: 
        return "Very High", "#e74c3c"
    elif score >= 70: 
        return "High", "#f39c12"
    elif score >= 60: 
        return "Medium", "#f1c40f"
    else: 
        return "Low", "#27ae60"

def load_custom_css():
    """Load custom CSS styling for the dashboard"""
    st.markdown("""
    <style>
        .main-header {
            font-size: 3rem;
            color: #2c3e50;
            text-align: center;
            margin-bottom: 2rem;
            background: linear-gradient(90deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        .metric-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 1rem;
            border-radius: 10px;
            margin: 0.5rem 0;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        
        .alert-banner {
            background: linear-gradient(135deg, #e74c3c, #c0392b);
            color: white;
            padding: 1rem;
            border-radius: 10px;
            margin: 1rem 0;
            animation: pulse 2s infinite;
        }
        
        .critical-priority {
            border-left: 4px solid #e74c3c;
            padding: 15px;
            margin: 10px 0;
            background: linear-gradient(135deg, #ffeaea 0%, #f8f9fa 100%);
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        .high-priority {
            border-left: 4px solid #f39c12;
            padding: 15px;
            margin: 10px 0;
            background: linear-gradient(135deg, #fff3e0 0%, #f8f9fa 100%);
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        .medium-priority {
            border-left: 4px solid #f1c40f;
            padding: 15px;
            margin: 10px 0;
            background: linear-gradient(135deg, #fff9e6 0%, #f8f9fa 100%);
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.8; }
        }
        
        .stSelectbox > div > div > div {
            background-color: #f8f9fa;
            border-radius: 8px;
        }
        
        .emergency-alert {
            background: linear-gradient(135deg, #ff6b6b, #ee5a52);
            color: white;
            padding: 1rem;
            border-radius: 10px;
            margin: 1rem 0;
            border: 2px solid #ff4757;
        }
        
        .info-card {
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
            padding: 1.2rem;
            border-radius: 10px;
            margin: 1rem 0;
            border-left: 4px solid #3498db;
        }
        
        .success-card {
            background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
            padding: 1.2rem;
            border-radius: 10px;
            margin: 1rem 0;
            border-left: 4px solid #28a745;
        }
    </style>
    """, unsafe_allow_html=True)

def format_number(value, format_type="default"):
    """Format numbers for display"""
    if format_type == "currency":
        return f"${value:,.0f}"
    elif format_type == "percentage":
        return f"{value:.1f}%"
    elif format_type == "population":
        if value >= 1000000:
            return f"{value/1000000:.1f}M"
        elif value >= 1000:
            return f"{value/1000:.0f}K"
        else:
            return f"{value:,.0f}"
    else:
        return f"{value:,.0f}"

def calculate_vulnerability_trend(current_value, previous_value):
    """Calculate trend direction and percentage change"""
    if previous_value == 0:
        return "No data", 0
    
    change = ((current_value - previous_value) / previous_value) * 100
    
    if change > 5:
        return "Increasing", change
    elif change < -5:
        return "Decreasing", change
    else:
        return "Stable", change

def get_priority_color(priority):
    """Get color code for priority levels"""
    colors = {
        'CRITICAL': '#e74c3c',
        'HIGH': '#f39c12',
        'MEDIUM': '#f1c40f',
        'LOW': '#27ae60'
    }
    return colors.get(priority.upper(), '#95a5a6')

def validate_district_name(district_name, valid_districts):
    """Validate if district name exists in the dataset"""
    return district_name in valid_districts

def export_data_to_json(data, filename_prefix="malawi_vulnerability"):
    """Export data to JSON format"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M')
    filename = f"{filename_prefix}_{timestamp}.json"
    
    export_data = {
        'metadata': {
            'timestamp': datetime.now().isoformat(),
            'source': 'Malawi Vulnerability Dashboard',
            'version': '1.0'
        },
        'data': data
    }
    
    return json.dumps(export_data, indent=2), filename

def create_alert_message(district, vulnerability_score, threshold):
    """Create formatted alert message"""
    return f"""
    🚨 HIGH VULNERABILITY ALERT
    
    District: {district}
    Vulnerability Score: {vulnerability_score}%
    Threshold: {threshold}%
    
    Immediate assessment and intervention required.
    """

def get_intervention_icon(intervention_type):
    """Get appropriate icon for intervention type"""
    icons = {
        'food_security': '🍽️',
        'healthcare': '🏥',
        'water_sanitation': '💧',
        'climate_adaptation': '🌡️',
        'economic_empowerment': '💼',
        'education': '📚',
        'infrastructure': '🏗️',
        'emergency_response': '🚨'
    }
    return icons.get(intervention_type.lower().replace(' ', '_'), '📋')

def calculate_implementation_timeline(recommendations):
    """Calculate overall implementation timeline"""
    timelines = []
    for rec in recommendations:
        timeline_str = rec.get('timeline', '').lower()
        
        if 'hour' in timeline_str:
            hours = int([x for x in timeline_str.split() if x.isdigit()][0])
            timelines.append(hours / 24)  # Convert to days
        elif 'day' in timeline_str:
            days = int([x for x in timeline_str.split() if x.isdigit()][0])
            timelines.append(days)
        elif 'week' in timeline_str:
            weeks = int([x for x in timeline_str.split() if x.isdigit()][0])
            timelines.append(weeks * 7)
        elif 'month' in timeline_str:
            months = int([x for x in timeline_str.split() if x.isdigit()][0])
            timelines.append(months * 30)
    
    if timelines:
        return max(timelines)  # Return longest timeline
    return 30  # Default to 30 days

def generate_dashboard_summary(df, high_risk_districts):
    """Generate executive summary of dashboard findings"""
    summary = {
        'total_districts': len(df),
        'high_risk_districts': len(high_risk_districts),
        'average_vulnerability': df['Vulnerability'].mean(),
        'population_at_risk': df[df['Vulnerability'] >= 70]['Population'].sum(),
        'most_vulnerable_district': df.loc[df['Vulnerability'].idxmax(), 'District'],
        'least_vulnerable_district': df.loc[df['Vulnerability'].idxmin(), 'District'],
        'key_findings': []
    }
    
    # Generate key findings
    if len(high_risk_districts) > 0:
        summary['key_findings'].append(f"{len(high_risk_districts)} districts require immediate intervention")
    
    if df['Food_Security'].mean() < 65:
        summary['key_findings'].append("Food security is below acceptable levels nationally")
    
    if df['Climate_Risk'].mean() > 75:
        summary['key_findings'].append("Climate risk is at critical levels across the country")
    
    return summary

def create_district_profile_card(district_data):
    """Create formatted district profile card"""
    risk_level, color = get_risk_level(district_data['Vulnerability'])
    
    return f"""
    <div style="border-left: 4px solid {color}; padding: 15px; margin: 10px 0; 
                background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); 
                border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
        <h4 style="color: {color}; margin: 0 0 10px 0;">{district_data['District']}</h4>
        <p><strong>Risk Level:</strong> {risk_level}</p>
        <p><strong>Population:</strong> {format_number(district_data['Population'], 'population')}</p>
        <p><strong>Vulnerability Score:</strong> {district_data['Vulnerability']}%</p>
        <p><strong>Primary Concerns:</strong> 
        {"Climate Risk, " if district_data.get('Climate_Risk', 0) > 75 else ""}
        {"Food Insecurity, " if district_data.get('Food_Security', 100) < 65 else ""}
        {"Healthcare Access" if district_data.get('Healthcare_Access', 100) < 50 else ""}
        </p>
    </div>
    """

def get_seasonal_adjustments():
    """Get seasonal adjustment factors for vulnerability calculations"""
    current_month = datetime.now().month
    
    # Malawi seasons: Dry season (May-Oct), Rainy season (Nov-Apr)
    if current_month >= 5 and current_month <= 10:  # Dry season
        return {
            'food_security_multiplier': 1.2,  # Food security risks higher
            'water_access_multiplier': 1.3,   # Water access challenges
            'climate_risk_multiplier': 0.9    # Lower immediate climate risk
        }
    else:  # Rainy season
        return {
            'food_security_multiplier': 0.9,  # Generally better food security
            'water_access_multiplier': 0.8,   # Better water availability
            'climate_risk_multiplier': 1.4    # Higher climate risks (floods, storms)
        }