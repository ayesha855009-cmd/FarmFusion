# FarmFusion 🌾
### Field Shift: Adapting Farms with NASA Data

**An agricultural water-analysis research prototype**

<p align="center">
  <a href="https://farmfusion-nasa.streamlit.app/">🚀 Open the FarmFusion Dashboard</a>
</p>

## About FarmFusion

FarmFusion is a student-developed research prototype created for the NASA Space Apps Challenge. It explores how climate data and soil-water conditions can help us understand agricultural water availability.

Our first case study focuses on wheat cultivation in Phalia, Punjab, Pakistan.

The project uses daily climate data from NASA POWER to examine rainfall and weather conditions during the wheat-growing season. We use these data to calculate reference evapotranspiration and estimate crop-water demand. We then run a soil-water simulation to compare how different soil textures and starting moisture conditions affect the amount of water available in the soil.

The results are presented through an interactive Streamlit dashboard, where users can explore climate trends, water demand, soil-water storage, and different simulation scenarios.

## Live Application

**Dashboard:** https://farmfusion-nasa.streamlit.app/

The application is hosted on Streamlit Community Cloud.

## Project Objectives

FarmFusion was developed to:

- Analyze daily climate conditions during a wheat-growing season.
- Use NASA POWER data in a local agricultural research case study.
- Calculate reference evapotranspiration using the FAO-56 approach.
- Estimate wheat crop-water demand using crop coefficients.
- Simulate soil-water conditions across a layered soil profile.
- Compare different soil textures and initial moisture assumptions.
- Present the results through interactive charts and scenario comparisons.

## Study Area

| Parameter | Details |
|---|---|
| Location | Phalia, Punjab, Pakistan |
| Latitude | 32.43° N |
| Longitude | 73.58° E |
| Crop | Wheat |
| Growing period studied | 23 November 2023 – 20 April 2024 |
| Simulation duration | 150 days |

## NASA Data Source

### NASA POWER

We used the NASA POWER data service to obtain daily climate data for the study area.

**Source:** https://power.larc.nasa.gov/

The project uses meteorological variables such as:

| Variable | Description |
|---|---|
| T2M | Mean air temperature |
| T2M_MAX | Maximum air temperature |
| T2M_MIN | Minimum air temperature |
| T2MDEW | Dew-point temperature |
| PRECTOTCORR | Corrected precipitation |
| RH2M | Relative humidity |
| WS10M | Wind speed at 10 metres |
| ALLSKY_SFC_SW_DWN | Surface shortwave downward radiation |

These variables are used in the climate analysis and evapotranspiration calculations. The soil-water scenarios are modelled separately using assumed soil properties and initial moisture conditions; they should not be interpreted as direct NASA soil-moisture measurements.

## How the Model Works

The project follows these main steps:

1. **Climate data collection:** Retrieve daily meteorological data from NASA POWER for the selected location and period.
2. **Reference evapotranspiration:** Calculate reference evapotranspiration (ET₀) using the implemented FAO-56 method.
3. **Crop-water demand:** Estimate wheat crop evapotranspiration (ETc) using ET₀ and crop coefficients.
4. **Root development:** Represent root-depth development using an assumed linear growth function.
5. **Soil profile:** Represent the soil profile using 150 one-centimetre sublayers, organised into five depth zones.
6. **Water-balance simulation:** Simulate soil-water storage and crop-water extraction over the growing period.
7. **Scenario comparison:** Run 36 combinations using 12 soil textures and three assumed initial moisture conditions: Wet, Moderate, and Dry.
8. **Results:** Compare rainfall, potential crop-water demand, water extracted, final soil-water storage, and unmet potential demand.

## Simulation Results

The model was run for 150 days across 36 scenarios.

The following table shows one example of the reported simulation outputs:

| Metric | Simulated Result |
|---|---:|
| Initial soil-water storage | 147.30 mm |
| Total rainfall | 193.38 mm |
| Potential crop-water demand (ETc) | 404.39 mm |
| Actual water extracted | 295.86 mm |
| Unmet potential water demand | 108.53 mm |
| Final soil-water storage | 44.82 mm |
| Total drainage | 0.00 mm |

These values are model outputs, not field measurements. The scenario label should be checked against the corresponding simulation output before assigning it to a particular soil texture or moisture condition.

### Numerical Checks

In the reported simulation run:

- 36 scenarios were completed.
- 5,400 daily simulation records were generated.
- Maximum reported water-balance error: 0.0 mm.
- Maximum reported crop-water-demand accounting error: 0.0 mm.
- All scenarios passed the implemented numerical accounting checks.

Unmet potential water demand varied between scenarios, ranging from 0.00 mm to approximately 201.35 mm in the reported results.

These checks assess numerical accounting within the model. They do not establish that the model accurately represents field conditions.

## What the Dashboard Includes

The Streamlit application is organised into several sections:

- **Overview:** A summary of the study and its main results.
- **Climate Insights:** Daily climate trends, including temperature, rainfall, and other meteorological variables.
- **Soil Intelligence:** Comparisons of soil textures and initial moisture scenarios.
- **Water Analysis:** Rainfall, estimated crop-water demand, water extraction, and final storage.
- **Scenario Explorer:** Comparisons of the 36 simulation scenarios.
- **Methodology:** An explanation of the data and modelling approach.

## Visualizations

The project generates the following charts:

| File | Purpose |
|---|---|
| `unmet_demand_comparison.png` | Compares unmet potential water demand across scenarios |
| `water_demand_comparison.png` | Compares actual extracted water with unmet demand |
| `daily_water_trends.png` | Shows daily soil-water trends |
| `cumulative_water_comparison.png` | Compares cumulative rainfall and potential crop-water demand |

## Model Limitations

FarmFusion is an exploratory research prototype. Some parts of the model are simplified and require further testing.

- Initial soil-moisture conditions are hypothetical.
- Soil-water properties are based on reference assumptions, not laboratory measurements from local Phalia farms.
- Root development is represented using a simplified linear function.
- Water extraction does not yet use a locally calibrated root-density or hydraulic uptake model.
- Runoff and infiltration-rate limitations are not fully represented.
- Unmet potential water demand is a model-based estimate. It is not a direct measurement of crop stress.
- The model has not yet been validated against field observations.

For these reasons, FarmFusion should be used to explore possible scenarios, not to provide precise irrigation recommendations or predict crop yields.

## Technology Used

The project was developed using:

- **Python** – Main programming language.
- **NumPy** – Numerical calculations and array operations.
- **Pandas** – Data processing and analysis.
- **Matplotlib** – Charts and visualizations.
- **Streamlit** – Interactive dashboard.
- **NASA POWER** – Daily meteorological data.
- **FAO-56** – Reference evapotranspiration methodology.

## Running the Project Locally

### Requirements

- Python 3.11 or later
- pip
- Internet connection for NASA POWER data retrieval

### 1. Clone the repository

```bash
git clone https://github.com/ayesha855009-cmd/FarmFusion.git
cd FarmFusion
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the environment

For Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 5. Run the dashboard

```bash
streamlit run app.py
```

The application should open at:

```text
http://localhost:8501
```

## Reproducing the Simulation

The following commands can be used to run the backend scripts, provided the required input files are available at the paths configured in the scripts.

```bash
python src/calculate_eto.py
python src/calculate_annual_etc.py
python src/run_layered_water_balance.py
```

To generate the charts:

```bash
python src/plot_scenario_comparison.py
python src/plot_water_demand_comparison.py
python src/plot_daily_water_trends.py
python src/plot_cumulative_water.py
```

Processed datasets and generated charts are stored in `data/processed/`.

## Project Structure

```text
FarmFusion/
│
├── app.py
├── data/
├── models/
├── src/
├── requirements.txt
├── README.md
└── .gitignore
```

## Team

FarmFusion was developed by a two-member team for the NASA Space Apps Challenge.

- **Ayesha Arshad** – Project Developer
- **Wania Rizwan** – Project Developer

Both team members contributed to the research, data processing, modelling, and dashboard development.

## Use of AI Tools

ChatGPT was used during project development for brainstorming, research assistance, coding support, debugging, and editing project documentation and presentation content.

The team reviewed and tested the project implementation and remains responsible for the final code, analysis, and reported results.

## Future Work

There are several areas we would like to improve:

- Collect soil samples and use measured local soil properties.
- Compare model outputs with observations from actual agricultural fields.
- Improve the representation of infiltration, runoff, drainage, and root-water uptake.
- Extend the analysis to other crops and growing seasons.
- Explore additional agricultural locations and climate conditions.

---

**FarmFusion — Exploring agricultural water availability with NASA climate data.**

*An independent research prototype developed for the NASA Space Apps Challenge.*