Malawi Community Vulnerability Dashboard

Track 2: Community Vulnerability Analysis & Early Warning Systems
Access the ResilienceGuard Here: https://resilienceguard.streamlit.app/

An AI-powered early warning system for resilience planning in Malawi.
Built for policymakers, NGOs, and community planners to make data-driven decisions on food security, climate risk, and community vulnerability.

OVERVIEW

This interactive dashboard transforms complex vulnerability and nutrition data into actionable visual insights, enabling users to:

Anticipate Shocks: Early warning system with real-time risk assessment
Design Targeted Interventions: AI-powered policy recommendations
Strengthen Community Resilience: Resource allocation and implementation planning


1. Dashboard Navigation
Use the sidebar controls to filter data and adjust alert thresholds
Select different vulnerability types for focused analysis
Adjust time periods to view historical trends

2. Risk Assessment
Monitor the geographic map for spatial risk patterns
Check key metrics for overall vulnerability status
Review priority districts requiring immediate attention

3. AI Recommendations
Access district-specific intervention suggestions
Review regional strategies for coordinated response
 Analyze resource allocation recommendations

4. Emergency Response
 Monitor high-risk alerts for immediate action items
Use emergency contacts for rapid response coordination
Activate alert protocols when thresholds are exceeded

5. Data Export
Export dashboard data in JSON format
Generate reports for stakeholder sharing
Validate data quality and API connections


DATA SOURCES

AGWAA API → Climate & vulnerability data
FS-COR Platform → Food security & crisis response
Sample Data → Built-in fallback for demos


Quick Start
Prerequisites

Python 3.8+
Streamlit
Internet connection for API data fetching

Installation
git clone 
cd malawi-vulnerability-dashboard
pip install -r requirements.txt
streamlit run main.py

Open http://localhost:8501 in your browser.


Future Roadmap

Multi-country support (Ghana, Uganda, Senegal, Benin)
Predictive ML vulnerability forecasting
Mobile app integration
Satellite imagery for real-time risk mapping
Community Feedback: Crowdsourced vulnerability reporting


Deliverable

Clear visual insights
Real-time data integration
Accessible, non-technical design
AI-powered decision support


Methodology

Scores are classified into four levels:
Low (0-39)
Moderate (40-59)
High (60-74)
Extremely High (75-100)


Built with love to strengthen community resilience in Malawi
