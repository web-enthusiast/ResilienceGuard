# Configuration settings for Malawi Vulnerability Dashboard

# API Endpoints
AGWAA_BASE_URL = "https://www.aagwa.org"
FS_COR_BASE_URL = "https://fs-cor.org"

# Alert thresholds
VULNERABILITY_THRESHOLDS = {
    'low': 60,
    'medium': 70,
    'high': 80,
    'critical': 90
}

# Risk level colors
RISK_COLORS = {
    'Low': '#27ae60',
    'Medium': '#f1c40f', 
    'High': '#f39c12',
    'Very High': '#e74c3c'
}

# Chart color schemes
COLOR_SCALES = {
    'vulnerability': ["#27ae60", "#f1c40f", "#f39c12", "#e74c3c"],
    'climate_risk': ["#3498db", "#e67e22", "#e74c3c", "#8e44ad"],
    'food_security': ["#e74c3c", "#f39c12", "#f1c40f", "#27ae60"]
}

# Data refresh settings
CACHE_TTL = 3600  # 1 hour in seconds
API_TIMEOUT = 15  # seconds

# Emergency contacts template
EMERGENCY_CONTACTS = {
    'Malawi': {
        'district_commissioners': {
            'Lilongwe': '+265 123 456 789',
            'Blantyre': '+265 123 456 789',
            'Mangochi': '+265 123 456 789',
        },
        'emergency_services': {
            'Health Emergency': '+265 123 456 ***',
            'Food Security': '+265 123 456 ***',
            'NGO Coordination': '+265 123 456 ***',
            'Police Emergency': '123'
        }
    }
}

# Seasonal adjustment factors
SEASONAL_ADJUSTMENTS = {
    'dry_season': {  # May-October
        'food_security_multiplier': 1.2,
        'water_access_multiplier': 1.3,
        'climate_risk_multiplier': 0.9
    },
    'rainy_season': {  # November-April
        'food_security_multiplier': 0.9,
        'water_access_multiplier': 0.8,
        'climate_risk_multiplier': 1.4
    }
}

# Dashboard layout settings
LAYOUT_CONFIG = {
    'page_title': "Community Vulnerability Dashboard",
    'page_icon': "🛡️",
    'layout': "wide",
    'initial_sidebar_state': "expanded"
}

# Vulnerability indicators and their weights
VULNERABILITY_INDICATORS = {
    'food_security': {'weight': 0.25, 'reverse_score': True},
    'climate_risk': {'weight': 0.20, 'reverse_score': False},
    'poverty_rate': {'weight': 0.15, 'reverse_score': False},
    'healthcare_access': {'weight': 0.15, 'reverse_score': True},
    'water_access': {'weight': 0.10, 'reverse_score': True},
    'nutrition_index': {'weight': 0.10, 'reverse_score': True},
    'infant_mortality': {'weight': 0.05, 'reverse_score': False}
}

# Recommendation priority matrix
RECOMMENDATION_PRIORITIES = {
    'critical': {
        'vulnerability_threshold': 80,
        'max_response_time': 72,  # hours
        'budget_range': (250000, 500000)
    },
    'high': {
        'vulnerability_threshold': 70,
        'max_response_time': 168,  # 1 week in hours
        'budget_range': (100000, 300000)
    },
    'medium': {
        'vulnerability_threshold': 60,
        'max_response_time': 720,  # 1 month in hours
        'budget_range': (50000, 200000)
    },
    'low': {
        'vulnerability_threshold': 0,
        'max_response_time': 2160,  # 3 months in hours
        'budget_range': (20000, 100000)
    }
}

# Export settings
EXPORT_FORMATS = ['json', 'csv', 'xlsx']
EXPORT_FILENAME_PREFIX = 'vulnerability_report'

# Performance settings
MAX_DISTRICTS_DISPLAY = 50
CHART_HEIGHT_DEFAULT = 400
MAP_ZOOM_DEFAULT = 6

# Validation rules
DATA_VALIDATION = {
    'required_columns': ['District', 'Lat', 'Lng', 'Vulnerability', 'Population'],
    'min_districts': 5,
    'max_vulnerability_score': 100,
    'min_vulnerability_score': 0
}

# Regional groupings
REGIONAL_GROUPS = {
    'Malawi': {
        'Southern': ['Blantyre', 'Mangochi', 'Zomba', 'Mulanje', 'Thyolo'],
        'Central': ['Lilongwe', 'Dedza', 'Ntcheu', 'Salima', 'Nkhotakota', 'Kasungu', 'Mchinji'],
        'Northern': ['Mzuzu', 'Karonga', 'Rumphi', 'Nkhata Bay', 'Chitipa']
    }
}