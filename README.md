# FarmFusion 🌾
### Field Shift: Adapting Farms with NASA Data

**NASA Earth Observation-Based Agricultural Water Analysis and Decision Support Prototype**

<p align="center">
  <a href="https://farmfusion-nasa.streamlit.app/">🚀 Live FarmFusion Application</a>
</p>

## 🌍 About the Project

FarmFusion is a data-driven agricultural research and decision-support prototype developed for the NASA challenge **"Field Shift: Adapting Farms with NASA Data."**

The project explores how NASA Earth observation and climate data can support agricultural water analysis by combining climate conditions, soil wetness, crop-water demand, and simulated soil-water availability.

The initial case study focuses on wheat cultivation in **Phalia, Punjab, Pakistan**.

FarmFusion integrates NASA POWER datasets, reference evapotranspiration calculations, crop-water demand estimation, and a layered soil-water balance simulation to explore how different soil textures and initial moisture conditions influence water availability throughout the wheat growing season.

## 🚀 Live Application

**Explore FarmFusion:** https://farmfusion-nasa.streamlit.app/

The application is deployed using Streamlit Community Cloud.

## 🎯 Project Objectives

- Retrieve climate and soil-wetness data from NASA POWER.
- Analyze temperature, rainfall, humidity, solar radiation, and soil wetness.
- Estimate reference evapotranspiration (ET₀) using the FAO-56 Penman–Monteith method.
- Estimate wheat crop evapotranspiration (ETc) using crop coefficients.
- Simulate water movement and crop-water extraction across 150 soil sublayers.
- Compare 36 combinations of soil texture and initial moisture conditions.
- Visualize crop-water demand, rainfall, soil-water storage, and unmet potential water demand.

## 📍 Study Area

| Parameter | Details |
|---|---|
| Location | Phalia, Punjab, Pakistan |
| Latitude | 32.43° N |
| Longitude | 73.58° E |
| Crop | Wheat |
| Study period | November 23, 2023 – April 20, 2024 |
| Simulation duration | 150 days |

## 🛰️ NASA Data Sources

### NASA POWER

FarmFusion uses climate and soil-wetness variables from the NASA POWER data service.

Source: https://power.larc.nasa.gov/

Variables include:

| Parameter | Description |
|---|---|
| T2M | Mean air temperature |
| T2M_MAX | Maximum air temperature |
| T2M_MIN | Minimum air temperature |
| T2MDEW | Dew-point temperature |
| PRECTOTCORR | Corrected precipitation |
| RH2M | Relative humidity |
| WS10M | Wind speed at 10 metres |
| ALLSKY_SFC_SW_DWN | Surface shortwave downward radiation |
| GWETTOP | Surface soil wetness |
| GWETROOT | Root-zone soil wetness |
| GWETPROF | Profile soil wetness |

## ⚙️ Methodology

FarmFusion follows an integrated climate and soil-water analysis workflow.

1. **Data Collection:** Retrieve daily climate and soil-wetness data from NASA POWER.
2. **Reference Evapotranspiration:** Calculate ET₀ using the FAO-56 Penman–Monteith method.
3. **Crop-Water Demand:** Estimate wheat ETc using reference evapotranspiration and crop growth-stage coefficients.
4. **Root Development:** Represent wheat root growth using an assumed linear root-depth function.
5. **Layered Soil Simulation:** Divide the soil profile into five depth zones and 150 one-centimetre sublayers.
6. **Scenario Analysis:** Simulate 12 soil textures under three hypothetical initial moisture conditions: Wet, Moderate, and Dry.
7. **Numerical Validation:** Check water conservation and crop-water demand accounting across all 36 scenarios.
8. **Visualization:** Compare rainfall, water demand, soil-water storage, and unmet potential demand.

## 📊 Simulation Results

The layered soil-water model was tested across 12 soil textures and three initial moisture conditions, producing 36 scenarios over a 150-day wheat growing season.

### Example: Sandy Loam — Wet Scenario

| Metric | Simulated Result |
|---|---:|
| Initial soil-water storage | 147.30 mm |
| Total rainfall | 193.38 mm |
| Potential crop-water demand (ETc) | 404.39 mm |
| Actual water extracted | 295.86 mm |
| Unmet potential water demand | 108.53 mm |
| Final soil-water storage | 44.82 mm |
| Total drainage | 0.00 mm |

### Numerical Validation

- 36 scenarios completed.
- 5,400 daily simulation records generated.
- Maximum water-balance error: 0.0 mm.
- Maximum crop-water demand accounting error: 0.0 mm.
- All scenarios passed numerical accounting checks.

Simulated unmet potential demand ranged from 0.00 mm to approximately 201.35 mm across the scenarios.

These are outputs of a simplified simulation under assumed initial soil conditions and root-growth parameters, not direct field measurements.

## 📈 Visualizations

FarmFusion generates visual comparisons of:

- `unmet_demand_comparison.png` — Unmet potential crop-water demand across scenarios.
- `water_demand_comparison.png` — Actual extracted water and unmet demand.
- `daily_water_trends.png` — Daily soil-water storage and unmet demand.
- `cumulative_water_comparison.png` — Cumulative rainfall and potential crop-water demand.

## 🧪 Model Limitations

FarmFusion is an experimental research prototype. Its current model has several limitations:

1. Initial soil moisture conditions are hypothetical rather than measured.
2. Soil available-water-capacity values have not been calibrated using local Phalia soil samples.
3. Root growth is represented by a simplified linear function.
4. Water extraction does not use a locally calibrated root-density or hydraulic uptake function.
5. Rainfall infiltration is simulated without explicit runoff or infiltration-rate limitations.
6. Unmet potential water demand is an accounting estimate, not a direct measurement of crop stress.
7. The model has not yet been validated against field measurements.

**Interpretation:** FarmFusion currently supports exploratory agricultural scenario analysis. Its results should not be interpreted as precise irrigation recommendations or crop-yield predictions.

Further development requires local soil measurements, field observations, improved soil-water physics, and independent model validation.

## 🛠️ Technology Stack

- Python
- Streamlit
- Pandas
- NumPy
- Matplotlib
- NASA POWER API
- FAO-56 Penman–Monteith methodology
- Layered soil-water balance simulation

## 💻 Installation and Local Execution

### Requirements

- Python 3.11 or later
- pip
- Internet connection for API-based data retrieval

### 1. Clone the Repository

```bash
git clone https://github.com/ayesha855009-cmd/FarmFusion.git
cd FarmFusion
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

### 3. Activate the Environment

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 4. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### 5. Run FarmFusion

```bash
streamlit run app.py
```

The application will open in your browser at:

`http://localhost:8501`

## 🔬 Optional: Backend Simulation Pipeline

To regenerate the backend calculations and simulation outputs, execute the following scripts from the project root:

```bash
python src/calculate_eto.py
python src/calculate_annual_etc.py
python src/run_layered_water_balance.py
```

Generate visualizations:

```bash
python src/plot_scenario_comparison.py
python src/plot_water_demand_comparison.py
python src/plot_daily_water_trends.py
python src/plot_cumulative_water.py
```

Generated charts and processed datasets are stored in `data/processed/`.

The required input datasets must be available at the paths configured in the respective scripts.

## 📁 Project Structure

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

## 👥 Team

**Project:** FarmFusion

**Challenge:** Field Shift: Adapting Farms with NASA Data

**Team Members:**
- [Add team member name and contribution]
- [Add team member name and contribution]
- [Add team member name and contribution]

## 🌱 Future Development

- Expand agricultural analysis beyond the initial Phalia case study.
- Integrate additional regional soil and agricultural datasets.
- Improve soil-water simulation using field-calibrated parameters.
- Incorporate more crop types and growing seasons.
- Develop more advanced agricultural decision-support capabilities.

---

**FarmFusion — Turning NASA Earth observations into agricultural insights.**

*Developed as an experimental research prototype for the NASA challenge: Field Shift: Adapting Farms with NASA Data.*