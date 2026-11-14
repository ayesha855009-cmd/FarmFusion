# FarmFusion 🌾

### NASA-Powered Agricultural Water Analysis

FarmFusion is a data-driven agricultural research prototype developed for the NASA challenge **“Field Shift: Adapting Farms with NASA Data.”**

The project explores how NASA Earth observation and climate data can support agricultural water analysis by examining weather conditions, soil wetness, crop water demand, and soil-water availability.

The initial case study focuses on wheat cultivation in Phalia, Punjab, Pakistan.

FarmFusion combines NASA POWER datasets with reference crop-water calculations and a layered soil-water balance simulation to explore how different soil textures and initial moisture conditions may influence water availability during the wheat growing season.
## Project Objectives

- Retrieve climate and soil-wetness data from NASA POWER.
- Analyze temperature, rainfall, humidity, solar radiation, and soil wetness.
- Estimate reference evapotranspiration (ET₀) using the FAO-56 Penman–Monteith method.
- Estimate wheat crop evapotranspiration (ETc) using crop coefficients.
- Simulate water movement and crop-water extraction across 150 soil sublayers.
- Compare 36 hypothetical combinations of soil texture and initial moisture conditions.
- Visualize crop-water demand, rainfall, soil-water storage, and unmet demand.

## Study Area

- **Location:** Phalia, Punjab, Pakistan
- **Latitude:** 32.43° N
- **Longitude:** 73.58° E
- **Crop:** Wheat
- **Study period:** November 23, 2023 – April 20, 2024
- **Growing season:** 150 days
## Data Sources

### NASA POWER

NASA POWER provides the daily climate and soil-wetness data used in this project.

Variables include:

- `T2M` — Mean air temperature
- `T2M_MAX` — Maximum air temperature
- `T2M_MIN` — Minimum air temperature
- `T2MDEW` — Dew-point temperature
- `PRECTOTCORR` — Corrected precipitation
- `RH2M` — Relative humidity
- `WS10M` — Wind speed at 10 metres
- `ALLSKY_SFC_SW_DWN` — All-sky surface shortwave downward radiation
- `GWETTOP` — Surface soil wetness
- `GWETROOT` — Root-zone soil wetness
- `GWETPROF` — Profile soil wetness

Source: https://power.larc.nasa.gov/

## Methodology

1. **Data collection:** Retrieve daily climate and soil-wetness data from NASA POWER.
2. **Reference evapotranspiration:** Estimate ET₀ using the FAO-56 Penman–Monteith method.
3. **Crop-water demand:** Estimate wheat ETc using reference ET₀ and crop growth-stage coefficients.
4. **Root development:** Represent wheat root growth using an assumed linear root-depth function.
5. **Layered soil model:** Divide the soil profile into five original depth zones and 150 one-centimetre sublayers.
6. **Scenario analysis:** Simulate 12 soil textures under three hypothetical initial moisture conditions: Wet, Moderate, and Dry.
7. **Validation:** Check water conservation and crop-water demand accounting across all 36 scenarios.
8. **Visualization:** Generate charts comparing water demand, soil-water storage, rainfall, and unmet demand.
## Simulation Results

The layered soil-water model was tested using 12 soil textures and three hypothetical initial moisture conditions: Wet, Moderate, and Dry.

This produced 36 scenarios, each simulated over a 150-day wheat growing season.

### Example: Sandy Loam — Wet Scenario

| Metric | Simulated result |
|---|---:|
| Initial soil-water storage | 147.30 mm |
| Total rainfall | 193.38 mm |
| Potential crop-water demand (ETc) | 404.39 mm |
| Actual water extracted | 295.86 mm |
| Unmet potential water demand | 108.53 mm |
| Final soil-water storage | 44.82 mm |
| Total drainage | 0.00 mm |

### Scenario Validation

- 36 soil and moisture scenarios completed.
- 5,400 daily simulation records generated.
- Maximum water-balance error: 0.0 mm.
- Maximum crop-water demand accounting error: 0.0 mm.
- All scenarios passed the numerical accounting checks.

The simulated unmet demand ranged from 0.00 mm to approximately 201.35 mm across the scenarios.

These results are outputs of a simplified simulation under assumed initial soil conditions and root-growth parameters. They are not direct measurements of field moisture, crop stress, yield loss, or irrigation requirements.

## Visualizations

FarmFusion generates the following visualizations:

- `unmet_demand_comparison.png` — Compares unmet potential crop-water demand across soil and moisture scenarios.
- `water_demand_comparison.png` — Compares extracted water and unmet demand.
- `daily_water_trends.png` — Shows daily soil-water storage and unmet demand.
- `cumulative_water_comparison.png` — Compares cumulative rainfall with cumulative potential crop-water demand (ETc) throughout the wheat growing season.
## Model Limitations and Assumptions

FarmFusion is an experimental research prototype. Its current simulation has the following limitations:

1. **Initial soil moisture:** Wet, Moderate, and Dry conditions are hypothetical scenarios, not measured field conditions.
2. **Soil properties:** Soil available-water-capacity values come from reference datasets and have not been calibrated using Phalia soil samples.
3. **Root development:** Wheat root growth is represented by a linear function, rather than locally measured root-growth observations.
4. **Water extraction:** Crop-water uptake is distributed across accessible soil layers without a calibrated root-density or hydraulic uptake function.
5. **Rainfall infiltration:** The model assumes rainfall infiltrates from the top downward. It does not explicitly simulate runoff or infiltration-rate limitations.
6. **Water stress:** Potential ETc is calculated independently of simulated water availability. Unmet demand is therefore an accounting estimate, not a measured crop-stress indicator.
7. **Field validation:** The model has passed numerical water-accounting checks but has not yet been validated against field measurements.

### Interpretation

FarmFusion currently supports exploratory scenario analysis. Its results should not be interpreted as precise irrigation recommendations or predictions of crop yield.

Further development requires local soil measurements, field observations, improved soil-water physics, and independent model validation.

## Project Status

**Backend development:** Core data processing, crop-water calculations, layered simulation, scenario analysis, and visualization scripts have been developed.

**Frontend:** Not yet implemented.

**Validation:** Numerical accounting checks completed; field validation remains future work.
## Backend Setup and Execution Guide

### Requirements

- Python 3.11 or later
- pip
- Internet connection for API-based data retrieval
- Required Python libraries listed in `requirements.txt`

### 1. Clone or Download the Project

Open the project folder in VS Code and open a terminal at the project root.

### 2. Create a Virtual Environment

```powershell
python -m venv venv
```

### 3. Activate the Environment

For Windows PowerShell:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\venv\Scripts\Activate.ps1
```

### 4. Install Dependencies

```powershell
python -m pip install -r requirements.txt
```

### 5. Run the Backend Pipeline

Run the following commands from the main project directory, in this order:

```powershell
python src/calculate_eto.py
python src/calculate_annual_etc.py
python src/run_layered_water_balance.py
```

These scripts calculate reference evapotranspiration, estimate wheat crop-water demand, and execute the layered soil-water simulations.

### 6. Generate Visualizations

```powershell
python src/plot_scenario_comparison.py
python src/plot_water_demand_comparison.py
python src/plot_daily_water_trends.py
python src/plot_cumulative_water.py
```

The generated charts are saved in:

`data/processed/`

### Required Input Data

The main calculation pipeline expects the following NASA POWER dataset:

`data/processed/phalia_complete_nasa_data_2023-11-23_2024-12-31.csv`

This dataset must be available before running the ET₀ calculation.

### Output Files

The pipeline generates processed datasets, simulation results, scenario summaries, and visualizations in `data/processed/`.