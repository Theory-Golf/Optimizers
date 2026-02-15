"""
Trackman Iron Optimizer - Streamlit Dashboard

This application helps golfers optimize their iron shots by:
1. Allowing input of shot data for specific irons
2. Comparing against optimal ranges for each club
3. Providing actionable recommendations to improve performance

Color Palette:
- Primary: Deep Plum (#32174D), Heritage Green (#2D5016)
- Accent: Ivory (#F4EFE2), Charcoal (#2E2E2E), Gold (#C6A75E, #B8956E)
- Status: Success Green (#3FA066), Weakness Red (#B4413D)
"""

import streamlit as st
import pandas as pd
from typing import Optional
import altair as alt

# ============================================================================
# CONFIGURATION & CONSTANTS
# ============================================================================

# Color Palette
COLORS = {
    "deep_plum": "#32174D",
    "heritage_green": "#2D5016",
    "ivory": "#F4EFE2",
    "charcoal": "#2E2E2E",
    "gold_light": "#C6A75E",
    "gold_dark": "#B8956E",
    "success_green": "#3FA066",
    "weakness_red": "#B4413D"
}

# Titleist T-100 Iron Specifications
CLUB_SPECS = {
    "3-iron": {"loft": 21, "length": 39.00, "swing_speed_range": (90, 95)},
    "4-iron": {"loft": 24, "length": 38.50, "swing_speed_range": (87, 92)},
    "5-iron": {"loft": 27, "length": 38.00, "swing_speed_range": (84, 89)},
    "6-iron": {"loft": 31, "length": 37.50, "swing_speed_range": (81, 86)},
    "7-iron": {"loft": 35, "length": 37.00, "swing_speed_range": (78, 83)},
    "8-iron": {"loft": 39, "length": 36.50, "swing_speed_range": (75, 80)},
    "9-iron": {"loft": 43, "length": 36.00, "swing_speed_range": (72, 77)},
    "PW": {"loft": 47, "length": 35.75, "swing_speed_range": (70, 75)}
}

# Optimal Ranges per Club
OPTIMAL_RANGES = {
    "3-iron": {
        "ball_speed": (125, 140),
        "launch_angle": (12, 16),
        "spin_rate": (3000, 5000),
        "smash_factor": (1.35, 1.42),
        "carry_distance": (180, 210)
    },
    "4-iron": {
        "ball_speed": (120, 135),
        "launch_angle": (14, 18),
        "spin_rate": (3500, 5500),
        "smash_factor": (1.34, 1.41),
        "carry_distance": (170, 195)
    },
    "5-iron": {
        "ball_speed": (115, 130),
        "launch_angle": (16, 20),
        "spin_rate": (3800, 5800),
        "smash_factor": (1.33, 1.40),
        "carry_distance": (160, 180)
    },
    "6-iron": {
        "ball_speed": (110, 125),
        "launch_angle": (18, 22),
        "spin_rate": (4000, 6200),
        "smash_factor": (1.32, 1.39),
        "carry_distance": (150, 170)
    },
    "7-iron": {
        "ball_speed": (105, 120),
        "launch_angle": (20, 24),
        "spin_rate": (4500, 6800),
        "smash_factor": (1.31, 1.38),
        "carry_distance": (140, 160)
    },
    "8-iron": {
        "ball_speed": (100, 115),
        "launch_angle": (22, 26),
        "spin_rate": (5000, 7500),
        "smash_factor": (1.30, 1.37),
        "carry_distance": (125, 145)
    },
    "9-iron": {
        "ball_speed": (95, 110),
        "launch_angle": (25, 29),
        "spin_rate": (5500, 8000),
        "smash_factor": (1.29, 1.36),
        "carry_distance": (110, 130)
    },
    "PW": {
        "ball_speed": (90, 105),
        "launch_angle": (28, 33),
        "spin_rate": (6000, 8500),
        "smash_factor": (1.28, 1.35),
        "carry_distance": (95, 115)
    }
}

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="Trackman Iron Optimizer",
    page_icon="⛳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS - Tracker Design System
st.markdown("""
<style>
    /* Reset & Base */
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
    
    body {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        color: #1a1a1a;
        background: #f5f5f5;
        line-height: 1.6;
    }
    
    /* Main background */
    .stApp {
        background-color: #f5f5f5;
    }
    
    /* Headers */
    h1, h2, h3, h4 {
        color: #1b5e20;
        font-weight: 600;
    }
    
    h1 { font-size: 1.75rem; }
    h2 { font-size: 1.4rem; margin-bottom: 0.5rem; }
    h3 { font-size: 1.15rem; margin-bottom: 0.25rem; }
    h4 { font-size: 1rem; }
    
    /* Body text */
    .stMarkdown, .stText, p, div, span {
        color: #1a1a1a;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #1b5e20;
    }
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3, 
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] .stMarkdown {
        color: #fff;
    }
    
    /* Sidebar selectbox */
    [data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] > div {
        background-color: white !important;
        color: #1a1a1a !important;
        border: 1px solid #ccc !important;
        border-radius: 6px !important;
    }
    [data-testid="stSidebar"] .stSelectbox label {
        color: #fff !important;
        font-weight: 600;
    }
    
    /* Primary Button - Green */
    .stButton>button {
        background-color: #2e7d32;
        color: #fff;
        border: none;
        border-radius: 6px;
        font-size: 1rem;
        font-weight: 600;
        padding: 0.6rem 1rem;
        transition: background 0.15s;
    }
    .stButton>button:hover {
        background-color: #1b5e20;
    }
    
    /* Form inputs */
    .stNumberInput input, 
    .stTextInput input,
    .stSelectbox div[data-baseweb="select"] > div {
        background-color: white !important;
        color: #1a1a1a !important;
        border: 1px solid #ccc !important;
        border-radius: 6px !important;
        padding: 0.5rem 0.65rem !important;
        font-size: 0.95rem !important;
    }
    
    /* Input labels */
    .stNumberInput label, 
    .stTextInput label, 
    .stSelectbox label {
        color: #1a1a1a !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
    }
    
    /* Success metrics */
    .metric-success {
        color: #2e7d32;
        font-weight: 600;
    }
    
    /* Weakness metrics */
    .metric-weakness {
        color: #c62828;
        font-weight: 600;
    }
    
    /* Form-style container cards */
    .tracker-form {
        display: flex;
        flex-direction: column;
        gap: 1rem;
        background: #fff;
        padding: 1.25rem;
        border-radius: 10px;
        box-shadow: 0 1px 4px rgba(0,0,0,0.08);
        margin-bottom: 1.5rem;
    }
    
    /* Recommendation cards */
    .recommendation-card {
        background-color: #fff;
        color: #1a1a1a;
        padding: 1rem 1.25rem;
        border-radius: 8px;
        margin: 0.75rem 0;
        border-left: 4px solid #2e7d32;
        box-shadow: 0 1px 4px rgba(0,0,0,0.08);
    }
    .recommendation-card h4 {
        color: #1b5e20;
        margin-bottom: 0.5rem;
    }
    .recommendation-card ul {
        margin: 0.5rem 0 0 1.25rem;
        padding: 0;
    }
    .recommendation-card li {
        margin: 0.35rem 0;
    }
    
    /* Info boxes */
    .info-box {
        background-color: #1b5e20;
        color: #fff;
        padding: 1rem 1.25rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    /* Tracker container */
    .tracker-container {
        max-width: 600px;
        margin: 0 auto;
        padding: 0 1rem;
    }
    
    /* Progress bar */
    .stProgress > div > div > div > div {
        background-color: #2e7d32;
    }
    
    /* Footer */
    .app-footer {
        text-align: center;
        padding: 2rem 1rem;
        color: #757575;
        font-size: 0.85rem;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def calculate_smash_factor(ball_speed: float, club_speed: float) -> float:
    """Calculate smash factor from ball and club speed."""
    if club_speed <= 0:
        return 0.0
    return round(ball_speed / club_speed, 3)

def check_metric_status(value: float, optimal_range: tuple, metric_name: str) -> dict:
    """Check if a metric is within optimal range."""
    low, high = optimal_range
    
    if low <= value <= high:
        return {
            "status": "success",
            "message": f"{metric_name}: {value} ✓ (Optimal)",
            "icon": "✅",
            "class": "metric-success"
        }
    elif value < low:
        return {
            "status": "warning_low",
            "message": f"{metric_name}: {value} (Below Optimal)",
            "icon": "⬇️",
            "class": "metric-weakness"
        }
    else:
        return {
            "status": "warning_high",
            "message": f"{metric_name}: {value} (Above Optimal)",
            "icon": "⬆️",
            "class": "metric-weakness"
        }

def generate_recommendations(club: str, metrics: dict) -> list:
    """Generate actionable recommendations based on metrics."""
    recommendations = []
    optimal = OPTIMAL_RANGES[club]
    
    # Launch Angle recommendations
    launch_check = check_metric_status(metrics['launch_angle'], 
                                       optimal['launch_angle'], 
                                       "Launch Angle")
    if launch_check['status'] != 'success':
        if metrics['launch_angle'] < optimal['launch_angle'][0]:
            recommendations.append({
                "area": "Launch Angle",
                "issue": "Too Low",
                "fixes": [
                    "Increase angle of attack - swing more upward through impact",
                    "Move ball position slightly forward in your stance",
                    "Ensure proper weight transfer to front foot",
                    "Check for early extension causing low point behind"
                ]
            })
        else:
            recommendations.append({
                "area": "Launch Angle", 
                "issue": "Too High",
                "fixes": [
                    "Decrease angle of attack - swing more downward",
                    "Move ball position slightly back in your stance",
                    "Reduce forward shaft lean at impact",
                    "Check for casting or early release"
                ]
            })
    
    # Spin Rate recommendations
    spin_check = check_metric_status(metrics['spin_rate'],
                                     optimal['spin_rate'],
                                     "Spin Rate")
    if spin_check['status'] != 'success':
        if metrics['spin_rate'] < optimal['spin_rate'][0]:
            recommendations.append({
                "area": "Spin Rate",
                "issue": "Too Low",
                "fixes": [
                    "Swing more downward for increased compression",
                    "Ensure crisp contact - avoid fat or thin shots",
                    "Increase dynamic loft at impact",
                    "Strike lower on the clubface for more spin"
                ]
            })
        else:
            recommendations.append({
                "area": "Spin Rate",
                "issue": "Too High",
                "fixes": [
                    "Swing slightly more upward through impact",
                    "Reduce dynamic loft at impact",
                    "Strike higher on the clubface",
                    "Check for excessive hand action or flipping"
                ]
            })
    
    # Smash Factor recommendations
    if metrics['smash_factor'] < optimal['smash_factor'][0]:
        recommendations.append({
            "area": "Smash Factor",
            "issue": "Too Low (Inefficient Energy Transfer)",
            "fixes": [
                "Focus on center face contact",
                "Improve timing and swing sequence",
                "Align club face properly at impact",
                "Ensure proper ball position",
                "Work on lag and release timing"
            ]
        })
    
    # Distance recommendations
    if 'carry_distance' in metrics and metrics['carry_distance'] > 0:
        dist_check = check_metric_status(metrics['carry_distance'],
                                          optimal['carry_distance'],
                                          "Carry Distance")
        if dist_check['status'] != 'success':
            if metrics['carry_distance'] < optimal['carry_distance'][0]:
                recommendations.append({
                    "area": "Distance",
                    "issue": "Below Expected",
                    "fixes": [
                        "Review launch angle and spin rate optimization",
                        "Check swing speed matches club capability",
                        "Improve impact location (center face)",
                        "Focus on compression and solid contact"
                    ]
                })
            else:
                recommendations.append({
                    "area": "Distance",
                    "issue": "Above Expected",
                    "fixes": [
                        "Great compression and efficiency!",
                        "Verify measurements are accurate",
                        "Good trajectory optimization"
                    ]
                })
    
    return recommendations

def display_club_info(club: str):
    """Display club specifications."""
    specs = CLUB_SPECS[club]
    st.markdown(f"""
    <div class="info-box">
        <strong>📊 {club} Specifications</strong><br>
        Loft: {specs['loft']}° | Length: {specs['length']}" | 
        Typical Swing Speed: {specs['swing_speed_range'][0]}-{specs['swing_speed_range'][1]} mph
    </div>
    """, unsafe_allow_html=True)

def display_optimal_ranges(club: str):
    """Display optimal ranges for the selected club."""
    optimal = OPTIMAL_RANGES[club]
    
    st.markdown("### 🎯 Optimal Ranges")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div style="text-align: center; padding: 15px; 
                    background-color: white; 
                    border: 1px solid #ccc;
                    color: #1a1a1a; border-radius: 8px;">
            <strong style="color: #1b5e20;">Ball Speed</strong><br>
            {optimal['ball_speed'][0]}-{optimal['ball_speed'][1]} mph
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style="text-align: center; padding: 15px; 
                    background-color: white; 
                    border: 1px solid #ccc;
                    color: #1a1a1a; border-radius: 8px;">
            <strong style="color: #1b5e20;">Launch Angle</strong><br>
            {optimal['launch_angle'][0]}-{optimal['launch_angle'][1]}°
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div style="text-align: center; padding: 15px; 
                    background-color: white; 
                    border: 1px solid #ccc;
                    color: #1a1a1a; border-radius: 8px;">
            <strong style="color: #1b5e20;">Spin Rate</strong><br>
            {optimal['spin_rate'][0]}-{optimal['spin_rate'][1]} RPM
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div style="text-align: center; padding: 15px; 
                    background-color: white; 
                    border: 1px solid #ccc;
                    color: #1a1a1a; border-radius: 8px;">
            <strong style="color: #1b5e20;">Smash Factor</strong><br>
            {optimal['smash_factor'][0]}-{optimal['smash_factor'][1]}
        </div>
        """, unsafe_allow_html=True)


def create_metric_chart(metric_name: str, user_value: float, optimal_range: tuple, 
                       unit: str, max_value: Optional[float] = None) -> None:
    """
    Create a vertical bar chart showing optimal range and user value using Altair.
    """
    low, high = optimal_range
    
    # Calculate chart boundaries
    if max_value is None:
        if high > 100:
            max_value = high * 1.3
        else:
            max_value = high * 1.2
    
    # Determine status and colors
    if low <= user_value <= high:
        status_color = "#3FA066"  # Success Green
        status_text = "✓ Optimal"
    elif user_value < low:
        status_color = "#B4413D"  # Weakness Red
        status_text = "⬇ Below"
    else:
        status_color = "#B4413D"  # Weakness Red
        status_text = "⬆ Above"
    
    # Create data for the chart
    # Background bar (0 to max)
    data = pd.DataFrame({
        'value': [0, max_value],
        'label': ['Start', 'End']
    })
    
    # Optimal range rectangle
    opt_data = pd.DataFrame({
        'xmin': [0],
        'xmax': [high],
        'ymin': [0],
        'ymax': [1]
    })
    
    # Main chart - horizontal bar showing range
    base = alt.Chart(pd.DataFrame({
        'position': [0.5],
        'value': [max_value]
    })).encode(
        y=alt.Y('position:O', axis=None)
    ).properties(height=50)
    
    # Background bar
    bar = base.mark_bar(color='#F5F5F5', cornerRadiusTopRight=4, cornerRadiusBottomRight=4).encode(
        x=alt.X('value:Q', scale=alt.Scale(domain=[0, max_value]), axis=None)
    )
    
    # Optimal range highlight
    opt_range = alt.Chart(pd.DataFrame({
        'start': [low],
        'end': [high]
    })).encode(
        x='start:Q',
        x2='end:Q'
    ).mark_rect(color='#2D5016', opacity=0.25)
    
    # User value marker line
    user_line = alt.Chart(pd.DataFrame({
        'x': [user_value]
    })).encode(
        x='x:Q'
    ).mark_rule(color=status_color, strokeWidth=3)
    
    # User value dot
    user_dot = alt.Chart(pd.DataFrame({
        'x': [user_value],
        'y': [0.5]
    })).encode(
        x='x:Q',
        y='y:Q'
    ).mark_point(color=status_color, size=100, shape='triangle-up', filled=True)
    
    # Combine all
    chart = (bar + opt_range + user_line + user_dot).properties(
        width=400,
        height=60
    )
    
    # Display chart
    st.altair_chart(chart, use_container_width=True)
    
    # Show values below chart
    col_left, col_right = st.columns([1, 1])
    with col_left:
        st.markdown(f"""
        <div style="text-align: center;">
            <span style="color: #2D5016; font-weight: bold;">Optimal Range</span><br>
            <span style="font-size: 14px;">{low}-{high}{unit}</span>
        </div>
        """, unsafe_allow_html=True)
    with col_right:
        st.markdown(f"""
        <div style="text-align: center;">
            <span style="color: {status_color}; font-weight: bold;">Your Value</span><br>
            <span style="font-size: 14px;">{user_value:.1f}{unit} - {status_text}</span>
        </div>
        """, unsafe_allow_html=True)


def display_shot_comparison_charts(metrics: dict, optimal: dict):
    """Display vertical bar charts for all metrics."""
    st.markdown("### 📊 Your Shot vs Optimal")
    
    # Ball Speed
    st.markdown(f"""<div style="background-color: white; padding: 15px; 
                border-radius: 8px; margin: 10px 0; border: 1px solid #2E2E2E;">
        <strong style="color: #32174D; font-size: 16px;">Ball Speed</strong>
        </div>""", unsafe_allow_html=True)
    create_metric_chart("Ball Speed", metrics['ball_speed'], optimal['ball_speed'],
                       " mph", max_value=optimal['ball_speed'][1] * 1.4)
    
    # Launch Angle
    st.markdown(f"""<div style="background-color: white; padding: 15px; 
                border-radius: 8px; margin: 10px 0; border: 1px solid #2E2E2E;">
        <strong style="color: #32174D; font-size: 16px;">Launch Angle</strong>
        </div>""", unsafe_allow_html=True)
    create_metric_chart("Launch Angle", metrics['launch_angle'], optimal['launch_angle'],
                       "°", max_value=optimal['launch_angle'][1] * 1.3)
    
    # Smash Factor
    st.markdown(f"""<div style="background-color: white; padding: 15px; 
                border-radius: 8px; margin: 10px 0; border: 1px solid #2E2E2E;">
        <strong style="color: #32174D; font-size: 16px;">Smash Factor</strong>
        </div>""", unsafe_allow_html=True)
    create_metric_chart("Smash Factor", metrics['smash_factor'], optimal['smash_factor'],
                       "", max_value=optimal['smash_factor'][1] * 1.15)
    
    # Spin Rate
    st.markdown(f"""<div style="background-color: white; padding: 15px; 
                border-radius: 8px; margin: 10px 0; border: 1px solid #2E2E2E;">
        <strong style="color: #32174D; font-size: 16px;">Spin Rate</strong>
        </div>""", unsafe_allow_html=True)
    create_metric_chart("Spin Rate", metrics['spin_rate'], optimal['spin_rate'],
                       " RPM", max_value=optimal['spin_rate'][1] * 1.3)
    
    # Carry Distance
    st.markdown(f"""<div style="background-color: white; padding: 15px; 
                border-radius: 8px; margin: 10px 0; border: 1px solid #2E2E2E;">
        <strong style="color: #32174D; font-size: 16px;">Carry Distance</strong>
        </div>""", unsafe_allow_html=True)
    create_metric_chart("Carry Distance", metrics['carry_distance'], optimal['carry_distance'],
                       " yds", max_value=optimal['carry_distance'][1] * 1.3)
    
    # Legend
    st.markdown("""
    <div style="padding: 10px; background-color: #F5F5F5; border-radius: 8px; margin-top: 15px;">
        <strong style="color: #32174D;">Legend:</strong>
        <span style="color: #2E2E2E; margin-left: 15px;">
            <span style="background-color: rgba(46, 80, 22, 0.3); padding: 2px 8px; 
                        border-radius: 4px;">Optimal Range</span>
            <span style="color: #3FA066; font-weight: bold; margin-left: 15px;">✓ Optimal</span>
            <span style="color: #B4413D; font-weight: bold; margin-left: 15px;">⬇/⬆ Above/Below</span>
        </span>
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# MAIN APPLICATION
# ============================================================================

def main():
    """Main application function."""
    
    # Title and header
    st.markdown("""
    <div style="text-align: center; padding: 2rem 1rem 1.5rem; background: #1b5e20; color: #fff;">
        <h1 style="color: #fff; font-size: 2rem;">⛳ Trackman Iron Optimizer</h1>
        <p style="font-size: 1rem; opacity: 0.85; margin-top: 0.25rem;">
            Optimize your iron shots with data-driven recommendations
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Main container
    st.markdown('<div class="tracker-container">', unsafe_allow_html=True)
    
    st.markdown("""<hr>""", unsafe_allow_html=True)
    
    # Sidebar - Club Selection
    with st.sidebar:
        st.markdown("""
        <h2 style="color: #F4EFE2;">🎯 Club Selection</h2>
        """, unsafe_allow_html=True)
        
        selected_club = st.selectbox(
            "Select Iron",
            options=list(CLUB_SPECS.keys()),
            index=4,  # Default to 7-iron
            help="Select the iron you're optimizing"
        )
        
        st.markdown("---")
        
        st.markdown(f"""
        <h3 style="color: #C6A75E;">📖 About</h3>
        <p style="color: #F4EFE2;">
            This optimizer uses Trackman metrics to help you 
            optimize your iron shots. Enter your shot data 
            to get personalized recommendations.
        </p>
        """, unsafe_allow_html=True)
    
    # Display club info
    display_club_info(selected_club)
    
    # Input section
    st.markdown("### 📝 Shot Data Input")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        club_speed = st.number_input(
            "Club Speed (mph)",
            min_value=0.0,
            max_value=150.0,
            value=80.0,
            step=0.5,
            help="Speed of club head at impact"
        )
    
    with col2:
        ball_speed = st.number_input(
            "Ball Speed (mph)",
            min_value=0.0,
            max_value=200.0,
            value=105.0,
            step=0.5,
            help="Speed of ball immediately after impact"
        )
    
    with col3:
        carry_distance = st.number_input(
            "Carry Distance (yards)",
            min_value=0.0,
            max_value=300.0,
            value=150.0,
            step=1.0,
            help="Distance ball travels through the air"
        )
    
    col4, col5, col6 = st.columns(3)
    
    with col4:
        launch_angle = st.number_input(
            "Launch Angle (°)",
            min_value=0.0,
            max_value=50.0,
            value=22.0,
            step=0.1,
            help="Angle of ball launch relative to ground"
        )
    
    with col5:
        spin_rate = st.number_input(
            "Spin Rate (RPM)",
            min_value=0,
            max_value=15000,
            value=5500,
            step=100,
            help="Backspin rate of the ball"
        )
    
    with col6:
        descent_angle = st.number_input(
            "Descent Angle (°)",
            min_value=0.0,
            max_value=80.0,
            value=45.0,
            step=0.1,
            help="Angle of ball descent"
        )
    
    # Calculate smash factor
    smash_factor = calculate_smash_factor(ball_speed, club_speed)
    
    # Store metrics
    metrics = {
        "club_speed": club_speed,
        "ball_speed": ball_speed,
        "smash_factor": smash_factor,
        "launch_angle": launch_angle,
        "spin_rate": spin_rate,
        "carry_distance": carry_distance,
        "descent_angle": descent_angle
    }
    
    st.markdown("---")
    
    # Analysis section
    st.markdown("### 📊 Shot Analysis")
    
    # Display optimal ranges
    display_optimal_ranges(selected_club)
    
    # Current metrics comparison with charts
    optimal = OPTIMAL_RANGES[selected_club]
    display_shot_comparison_charts(metrics, optimal)
    
    # Calculate overall optimization score
    total_checks = 5
    success_count = 0
    
    checks = [
        check_metric_status(metrics['ball_speed'], optimal['ball_speed'], ""),
        check_metric_status(metrics['launch_angle'], optimal['launch_angle'], ""),
        check_metric_status(metrics['spin_rate'], optimal['spin_rate'], ""),
        check_metric_status(metrics['smash_factor'], optimal['smash_factor'], ""),
        check_metric_status(metrics['carry_distance'], optimal['carry_distance'], "")
    ]
    
    for check in checks:
        if check['status'] == 'success':
            success_count += 1
    
    optimization_score = (success_count / total_checks) * 100
    
    # Display optimization score
    st.markdown("#### Optimization Score")
    
    score_col1, score_col2 = st.columns([1, 3])
    
    with score_col1:
        if optimization_score >= 80:
            score_color = "#2e7d32"
            score_message = "Excellent!"
        elif optimization_score >= 60:
            score_color = "#C6A75E"
            score_message = "Good"
        else:
            score_color = "#c62828"
            score_message = "Needs Work"
        
        st.markdown(f"""
        <div style="text-align: center; padding: 20px; 
                    background-color: #fff; 
                    border-radius: 10px; border: 2px solid {score_color};">
            <h2 style="color: {score_color}; margin: 0;">{optimization_score:.0f}%</h2>
            <p style="color: #1a1a1a; margin: 0;">{score_message}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with score_col2:
        progress_bar = st.progress(optimization_score / 100)
        st.write(f"**{success_count} of {total_checks} metrics in optimal range**")
    
    st.markdown("""<hr>""", unsafe_allow_html=True)
    
    # Recommendations section
    st.markdown("### 💡 Optimization Recommendations")
    
    recommendations = generate_recommendations(selected_club, metrics)
    
    if recommendations:
        for i, rec in enumerate(recommendations, 1):
            st.markdown(f"""
            <div class="recommendation-card">
                <h4 style="color: #C6A75E; margin: 0 0 10px 0;">
                    {i}. {rec['area']} - {rec['issue']}
                </h4>
                <ul style="margin: 0; padding-left: 20px;">
                    {''.join([f'<li style="margin: 5px 0;">{fix}</li>' for fix in rec['fixes']])}
                </ul>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style="text-align: center; padding: 1.5rem; 
                    background-color: #fff; border-radius: 8px; 
                    border: 2px solid #2e7d32; margin: 1rem 0;">
            <h3 style="color: #1b5e20;">🎉 Great shot!</h3>
            <p style="color: #1a1a1a;">All metrics are within optimal ranges for the {selected_club}. 
            Keep doing what you're doing!</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Quick tips section
    st.markdown("""<hr>""", unsafe_allow_html=True)
    st.markdown("### 💪 Quick Tips for Iron Play")
    
    tip_col1, tip_col2, tip_col3 = st.columns(3)
    
    with tip_col1:
        st.markdown(f"""
        <div style="padding: 15px; background-color: #fff; 
                    color: #1a1a1a; border-radius: 8px; border-left: 4px solid #1b5e20;">
            <strong style="color: #1b5e20;">🎯 Launch Angle</strong><br>
            <small>For better green holding: 
            Increase launch angle for longer irons, 
            decrease for scoring irons.</small>
        </div>
        """, unsafe_allow_html=True)
    
    with tip_col2:
        st.markdown(f"""
        <div style="padding: 15px; background-color: #fff; 
                    color: #1a1a1a; border-radius: 8px; border-left: 4px solid #2e7d32;">
            <strong style="color: #1b5e20;">🌀 Spin Rate</strong><br>
            <small>Too much spin = loss of distance. 
            Too little = ball doesn't stop. 
            Find the balance for your clubs.</small>
        </div>
        """, unsafe_allow_html=True)
    
    with tip_col3:
        st.markdown(f"""
        <div style="padding: 15px; background-color: #fff; 
                    color: #1a1a1a; border-radius: 8px; border-left: 4px solid #C6A75E;">
            <strong style="color: #1b5e20;">⚡ Smash Factor</strong><br>
            <small>Focus on center face contact. 
            A miss just 1/4 inch off center 
            can cost 2-3 mph ball speed.</small>
        </div>
        """, unsafe_allow_html=True)
    
    # Footer
    st.markdown('</div>', unsafe_allow_html=True)  # Close tracker-container
    
    st.markdown("""<hr>""", unsafe_allow_html=True)
    st.markdown(f"""
    <div class="app-footer">
        <p>Based on Titleist T-100 iron specifications and Trackman optimization principles</p>
        <p>Optimize your game with data-driven insights</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
