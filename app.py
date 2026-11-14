
from pathlib import Path

import pandas as pd
import streamlit as st

# --------------------------------------------------
# 1. PAGE CONFIGURATION
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data" / "processed"

st.set_page_config(
    page_title="FarmFusion | Agricultural Intelligence",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------------------------------
# 2. CUSTOM DESIGN
# --------------------------------------------------

st.markdown("""
<style>
    .stApp {
        background-color: #F3F5EF;
        color: #26352C;
    }

    [data-testid="stSidebar"] {
        background-color: #202B27;
    }

    [data-testid="stSidebar"] * {
        color: #F3F5EF;
    }

    h1, h2, h3 {
        color: #263D30;
    }

    div[data-testid="stMetric"] {
        background: #FFFFFF;
        border: 1px solid #E1E8DC;
        padding: 18px;
        border-radius: 14px;
    }

    div[data-testid="stMetricValue"] {
        color: #385B3D;
    }

    .hero {
        background: linear-gradient(110deg, #DCE8D7, #EEF2E9);
        padding: 28px;
        border-radius: 18px;
        border: 1px solid #D6E1D0;
        margin-bottom: 20px;
    }

    .hero p {
        color: #526454;
        font-size: 15px;
    }

    .note {
        background: #E8EFE3;
        padding: 14px;
        border-radius: 10px;
        color: #344936;
        border-left: 4px solid #8DAE63;
    }

    div[data-testid="stTabs"] button {
        color: #385B3D;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# 3. LOAD PROJECT DATA
# --------------------------------------------------

def load_csv(filename):
    """Load a processed CSV if it exists."""
    path = DATA_DIR / filename

    if path.exists():
        return pd.read_csv(path)

    return None


scenario_df = load_csv("all_36_scenario_summary.csv")

daily_df = load_csv(
    "layered_daily_simulation_sandy_loam_wet.csv"
)

climate_df = load_csv(
    "phalia_complete_nasa_data_2023-11-23_2024-12-31_with_eto.csv"
)

etc_df = load_csv("phalia_complete_wheat_etc.csv")


# Prepare date columns
for dataframe in [daily_df, climate_df, etc_df]:
    if dataframe is not None and "date" in dataframe.columns:
        dataframe["date"] = pd.to_datetime(
            dataframe["date"], errors="coerce"
        )


# --------------------------------------------------
# 4. SIDEBAR
# --------------------------------------------------

with st.sidebar:
    st.markdown("# 🌱 FarmFusion")
    st.caption("NASA-powered agricultural intelligence")

    st.divider()

    st.markdown("### Study location")
    st.markdown("**Phalia, Punjab**")
    st.caption("Pakistan · 32.43° N, 73.58° E")

    st.divider()

    st.markdown("### Research period")
    st.write("23 Nov 2023 – 20 Apr 2024")

    st.divider()

    st.caption("Data source: NASA POWER")
    st.caption("Research prototype · 2026")


# --------------------------------------------------
# 5. HEADER
# --------------------------------------------------

st.markdown("""
<div class="hero">
    <h1>FarmFusion 🌾</h1>
    <h3>Intelligent Agricultural Water Analysis</h3>
    <p>
        Exploring how NASA Earth observation and climate data
        can support agricultural water analysis in Phalia, Pakistan.
    </p>
</div>
""", unsafe_allow_html=True)


# --------------------------------------------------
# 6. NAVIGATION TABS
# --------------------------------------------------

overview, climate, soil, water, scenarios, methodology = st.tabs([
    "🌿 Overview",
    "☀️ Climate Insights",
    "🌱 Soil Intelligence",
    "💧 Water Analysis",
    "📊 Scenario Explorer",
    "ℹ️ Methodology"
])


# --------------------------------------------------
# TAB 1: OVERVIEW
# --------------------------------------------------

with overview:
    st.subheader("Project Overview")

    st.write(
        "FarmFusion analyzes climate conditions, crop-water demand, "
        "and hypothetical soil-water scenarios for wheat cultivation."
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Scenarios", "36")
    col2.metric("Simulation days", "150")
    col3.metric("Soil sublayers", "150")
    col4.metric("Crop", "Wheat")

    st.divider()

    left, right = st.columns([1.5, 1])

    with left:
        st.subheader("Study Area")
        st.markdown("**Phalia, Punjab, Pakistan**")
        st.write("Coordinates: 32.43° N, 73.58° E")
        st.write("Crop: Wheat (Rabi season)")
        st.write("Study period: 23 November 2023 to 20 April 2024")

    with right:
        st.subheader("Data and Model")
        st.write("🛰️ NASA POWER climate data")
        st.write("🌧️ Daily rainfall analysis")
        st.write("🌱 Soil-water scenario simulation")
        st.write("💧 FAO-56 reference ET₀ method")

    st.divider()

    st.subheader("Research Focus")
    st.write(
        "How do different soil-water storage capacities and "
        "initial moisture assumptions influence modeled crop-water "
        "availability during the wheat growing season?"
    )

    st.markdown("""
    <div class="note">
        FarmFusion is an exploratory research prototype.
        Its soil-moisture scenarios are hypothetical, not measured
        field conditions.
    </div>
    """, unsafe_allow_html=True)


# --------------------------------------------------
# TAB 2: CLIMATE INSIGHTS
# --------------------------------------------------

with climate:
    st.subheader("Climate Insights")
    st.write("Explore NASA POWER daily climate observations.")

    if climate_df is None:
        st.warning("Climate dataset was not found.")
    else:
        if "T2M" in climate_df.columns:
            st.markdown("### Daily temperature")
            st.line_chart(
                climate_df.set_index("date")[["T2M"]].dropna()
            )

        if "PRECTOTCORR" in climate_df.columns:
            st.markdown("### Daily rainfall")
            st.bar_chart(
                climate_df.set_index("date")[["PRECTOTCORR"]].dropna()
            )

        if "RH2M" in climate_df.columns:
            st.markdown("### Relative humidity")
            st.line_chart(
                climate_df.set_index("date")[["RH2M"]].dropna()
            )

        if "ET0_mm_day" in climate_df.columns:
            st.markdown("### Reference evapotranspiration (ET₀)")
            st.line_chart(
                climate_df.set_index("date")[["ET0_mm_day"]].dropna()
            )

        st.caption(
            "NASA POWER data are model-derived Earth observation and "
            "meteorological products, not local weather-station readings."
        )


# --------------------------------------------------
# TAB 3: SOIL INTELLIGENCE
# --------------------------------------------------

with soil:
    st.subheader("Soil Intelligence")

    st.write(
        "Compare modeled water availability across soil texture "
        "and initial moisture scenarios."
    )

    if scenario_df is None:
        st.warning("Scenario summary dataset was not found.")
    else:
        if "soil_texture" in scenario_df.columns:
            soil_options = sorted(
                scenario_df["soil_texture"].dropna().unique()
            )

            selected_soil = st.selectbox(
                "Select soil texture",
                soil_options
            )

            soil_data = scenario_df[
                scenario_df["soil_texture"] == selected_soil
            ]

            st.markdown(f"### {selected_soil}")

            if "moisture_scenario" in soil_data.columns:
                st.dataframe(
                    soil_data[
                        [
                            col for col in [
                                "moisture_scenario",
                                "water_extracted_mm",
                                "unmet_demand_mm",
                                "final_storage_mm"
                            ]
                            if col in soil_data.columns
                        ]
                    ],
                    use_container_width=True,
                    hide_index=True
                )

            if "unmet_demand_mm" in soil_data.columns:
                chart_data = soil_data.set_index("moisture_scenario")
                st.markdown("### Unmet potential demand")
                st.bar_chart(chart_data[["unmet_demand_mm"]])

    st.info(
        "Soil texture properties are reference values. "
        "They have not been measured from Phalia agricultural fields."
    )


# --------------------------------------------------
# TAB 4: WATER ANALYSIS
# --------------------------------------------------

with water:
    st.subheader("Water Analysis")

    if daily_df is None:
        st.warning("Daily simulation dataset was not found.")
    else:
        total_rainfall = daily_df["rainfall_mm"].sum()
        total_etc = daily_df["ETc_mm"].sum()
        total_extracted = daily_df["water_extracted_mm"].sum()
        total_unmet = daily_df["unmet_demand_mm"].sum()
        final_storage = daily_df["soil_storage_mm"].iloc[-1]

        col1, col2, col3 = st.columns(3)

        col1.metric("Rainfall", f"{total_rainfall:.2f} mm")
        col2.metric("Potential ETc", f"{total_etc:.2f} mm")
        col3.metric("Final storage", f"{final_storage:.2f} mm")

        col4, col5 = st.columns(2)

        col4.metric("Water extracted", f"{total_extracted:.2f} mm")
        col5.metric("Unmet potential demand", f"{total_unmet:.2f} mm")

        st.divider()

        st.markdown("### Daily soil-water storage")

        if "soil_storage_mm" in daily_df.columns:
            st.line_chart(
                daily_df.set_index("date")[["soil_storage_mm"]]
            )

        st.markdown("### Daily crop-water demand")

        if "ETc_mm" in daily_df.columns:
            demand_columns = [
                col for col in ["ETc_mm", "water_extracted_mm"]
                if col in daily_df.columns
            ]

            st.line_chart(
                daily_df.set_index("date")[demand_columns]
            )

        st.markdown("""
        <div class="note">
            The unmet potential demand shown here is a modelled
            accounting residual. It is not a direct measurement
            of crop stress or irrigation requirement.
        </div>
        """, unsafe_allow_html=True)


# --------------------------------------------------
# TAB 5: SCENARIO EXPLORER
# --------------------------------------------------

with scenarios:
    st.subheader("Scenario Explorer")

    st.write(
        "Explore the results of 36 combinations of soil texture "
        "and hypothetical initial moisture conditions."
    )

    if scenario_df is None:
        st.warning("Scenario summary dataset was not found.")
    else:
        if "moisture_scenario" in scenario_df.columns:
            moisture_options = [
                option for option in ["Wet", "Moderate", "Dry"]
                if option in scenario_df["moisture_scenario"].values
            ]

            selected_moisture = st.selectbox(
                "Select initial moisture scenario",
                moisture_options
            )

            filtered = scenario_df[
                scenario_df["moisture_scenario"] == selected_moisture
            ]

            st.markdown(f"### {selected_moisture} conditions")

            st.dataframe(
                filtered,
                use_container_width=True,
                hide_index=True
            )

            if "soil_texture" in filtered.columns:
                st.markdown("### Unmet demand by soil texture")

                chart = filtered.set_index("soil_texture")[
                    ["unmet_demand_mm"]
                ]

                st.bar_chart(chart)

        st.caption(
            "The scenarios represent assumed starting moisture "
            "conditions, not measured soil moisture."
        )


# --------------------------------------------------
# TAB 6: METHODOLOGY
# --------------------------------------------------

with methodology:
    st.subheader("Methodology and Data Sources")

    st.markdown("### Data source")
    st.write(
        "NASA POWER provides daily climate and soil-wetness variables "
        "used in the FarmFusion analysis."
    )

    st.markdown(
        "[NASA POWER Data Access Viewer](https://power.larc.nasa.gov/)"
    )

    st.divider()

    st.markdown("### Model workflow")

    st.markdown("""
    1. Retrieve daily NASA POWER data.
    2. Calculate reference evapotranspiration (ET₀) using FAO-56
       Penman–Monteith.
    3. Estimate wheat crop-water demand (ETc).
    4. Represent the soil profile with 150 one-centimetre sublayers.
    5. Simulate rainfall movement and crop-water extraction.
    6. Compare 36 soil-texture and initial-moisture scenarios.
    """)

    st.divider()

    st.markdown("### Model limitations")

    st.markdown("""
    - Initial soil moisture conditions are hypothetical.
    - Soil properties are reference values, not local soil samples.
    - Root growth is represented using a linear assumption.
    - Root-water extraction is simplified.
    - Runoff and infiltration-rate limitations are not represented.
    - The model has not been validated against field measurements.
    """)

    st.warning(
        "FarmFusion is a research prototype. Its outputs should not "
        "be used as precise irrigation recommendations or yield predictions."
    )

    st.divider()

    st.markdown("### Project")
    st.write("FarmFusion — Field Shift: Adapting Farms with NASA Data")
    st.write("Study location: Phalia, Punjab, Pakistan")
