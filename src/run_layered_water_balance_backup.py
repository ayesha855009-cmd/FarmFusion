
import pandas as pd
from pathlib import Path


# 1. FIND PROJECT FOLDER

BASE_DIR = Path(__file__).resolve().parent.parent

SOIL_FILE = BASE_DIR / "data" / "processed" / "global_soil_properties.csv"


# 2. LOAD SOIL DATA

soil_data = pd.read_csv(SOIL_FILE)

print("\nFARMFUSION - LAYERED SOIL WATER MODEL")
print("-------------------------------------")

print("Soil types loaded:", len(soil_data))


# 3. DEFINE SOIL LAYERS

layer_definitions = [
    (0.00, 0.15),
    (0.15, 0.30),
    (0.30, 0.60),
    (0.60, 1.00),
    (1.00, 1.50)
]

# 4. WHEAT ROOT GROWTH FUNCTION

def calculate_root_depth(
    days_after_sowing,
    maximum_root_depth,
    season_days=150,
    initial_root_depth=0.15
):

    # Limit crop age to the growing season
    days = max(0, min(days_after_sowing, season_days))

    # Calculate the proportion of root growth completed
    growth_fraction = days / season_days

    # Calculate current root depth
    root_depth = (
        initial_root_depth
        + (maximum_root_depth - initial_root_depth)
        * growth_fraction
    )

    return root_depth


# 4. DEFINE INITIAL MOISTURE SCENARIOS

moisture_scenarios = {
    "Wet":      [0.05, 0.10, 0.15, 0.20, 0.25],
    "Moderate": [0.20, 0.25, 0.30, 0.35, 0.40],
    "Dry":      [0.40, 0.45, 0.50, 0.55, 0.60]
}


# 5. CREATE INITIAL SOIL LAYERS

all_scenarios = []

for _, soil in soil_data.iterrows():

    soil_name = soil["soil_texture"]

    available_water = soil["available_water_mm_per_m"]

    for scenario_name, depletion_fractions in moisture_scenarios.items():

        layers = []

        for i, (top, bottom) in enumerate(layer_definitions):

            thickness = bottom - top

            capacity = available_water * thickness

            depletion_fraction = depletion_fractions[i]

            initial_depletion = capacity * depletion_fraction

            initial_storage = capacity - initial_depletion

            layer = {
                "top": top,
                "bottom": bottom,
                "capacity_mm": capacity,
                "depletion_fraction": depletion_fraction,
                "initial_storage_mm": initial_storage,
                "initial_depletion_mm": initial_depletion
            }

            layers.append(layer)

        all_scenarios.append({
            "soil_texture": soil_name,
            "moisture_scenario": scenario_name,
            "layers": layers
        })


print("\nInitial soil scenarios created:", len(all_scenarios))

# TEST WHEAT ROOT GROWTH

print("\nWHEAT ROOT GROWTH TEST")

for day in [0, 30, 60, 90, 120, 150]:

    depth = calculate_root_depth(
        days_after_sowing=day,
        maximum_root_depth=1.5
    )

    print(
        f"Day {day}:",
        round(depth, 2),
        "m root depth"
    )
# TEST ROOT ACCESS TO SOIL LAYERS

print("\nROOT ACCESS TO SOIL LAYERS")

for day in [0, 30, 60, 90, 120, 150]:

    root_depth = calculate_root_depth(
        days_after_sowing=day,
        maximum_root_depth=1.5
    )

    print(f"\nDay {day} - Root depth: {root_depth:.2f} m")

    for top, bottom in layer_definitions:

        rooted_thickness = max(
            0,
            min(bottom, root_depth) - top
        )

        print(
            f"{top:.2f}-{bottom:.2f} m:",
            round(rooted_thickness, 2),
            "m accessible"
        )

# CONNECT DAILY NASA DATA WITH ROOT GROWTH

CROP_DATA_FILE = (
    BASE_DIR
    / "data"
    / "processed"
    / "phalia_complete_wheat_etc.csv"
)

crop_data = pd.read_csv(CROP_DATA_FILE)

# Convert date column into datetime format
crop_data["date"] = pd.to_datetime(crop_data["date"])

# Select the 150-day wheat growing season
crop_data = crop_data[
    (crop_data["date"] >= "2023-11-23")
    & (crop_data["date"] <= "2024-04-20")
].copy()

# Calculate days after sowing
sowing_date = pd.Timestamp("2023-11-23")

crop_data["days_after_sowing"] = (
    crop_data["date"] - sowing_date
).dt.days

# Calculate root depth for every day
crop_data["root_depth_m"] = crop_data[
    "days_after_sowing"
].apply(
    lambda day: calculate_root_depth(
        day,
        maximum_root_depth=1.5
    )
)

print("\nDAILY CROP DATA AND ROOT GROWTH")

print("Growing season records:", len(crop_data))

print("\nFirst five records:")

print(
    crop_data[
        ["date", "PRECTOTCORR", "ETc_mm_day",
         "days_after_sowing", "root_depth_m"]
    ].head()
)

print("\nLast five records:")

print(
    crop_data[
        ["date", "PRECTOTCORR", "ETc_mm_day",
         "days_after_sowing", "root_depth_m"]
    ].tail()
)

# 6. DISPLAY ONE EXAMPLE

test_state = next(
    scenario for scenario in all_scenarios
    if scenario["soil_texture"] == "Sandy loam"
    and scenario["moisture_scenario"] == "Wet"
)

print("\nEXAMPLE: SANDY LOAM - WET")

for layer in test_state["layers"]:

    print(
        f'{layer["top"]:.2f}-{layer["bottom"]:.2f} m:',
        round(layer["initial_storage_mm"], 2),
        "mm water"
    )


# 7. MOVE RAINFALL THROUGH SOIL LAYERS

def move_rainfall_through_layers(layers, rainfall_mm):

    updated_layers = [
        layer.copy() for layer in layers
    ]

    remaining_rainfall = rainfall_mm

    for layer in updated_layers:

        available_space = (
            layer["capacity_mm"]
            - layer["initial_storage_mm"]
        )

        water_added = min(
            remaining_rainfall,
            available_space
        )

        layer["initial_storage_mm"] += water_added

        layer["initial_depletion_mm"] -= water_added

        remaining_rainfall -= water_added

        if remaining_rainfall <= 0.000001:
            break

    drainage = remaining_rainfall

    return updated_layers, drainage


# 8. TEST RAINFALL

rainfall_test = 30.0

updated_layers, drainage = move_rainfall_through_layers(
    test_state["layers"],
    rainfall_test
)

storage_before = sum(
    layer["initial_storage_mm"]
    for layer in test_state["layers"]
)

storage_after = sum(
    layer["initial_storage_mm"]
    for layer in updated_layers
)

print("\nRAINFALL TEST")

print("Storage before:", round(storage_before, 2), "mm")
print("Rainfall:", rainfall_test, "mm")
print("Storage after:", round(storage_after, 2), "mm")
print("Drainage:", round(drainage, 2), "mm")


# 9. VALIDATE RAINFALL CONSERVATION

rainfall_error = (
    storage_before
    + rainfall_test
    - storage_after
    - drainage
)

print("\nRAINFALL CONSERVATION ERROR:",
      round(rainfall_error, 6), "mm")

# TEST EXCESS RAINFALL

heavy_rainfall = 40.0

heavy_rain_layers, heavy_drainage = move_rainfall_through_layers(
    test_state["layers"],
    heavy_rainfall
)

heavy_storage = sum(
    layer["initial_storage_mm"]
    for layer in heavy_rain_layers
)

print("\nEXCESS RAINFALL TEST")

print("Initial storage:", round(storage_before, 2), "mm")
print("Rainfall:", heavy_rainfall, "mm")
print("Final storage:", round(heavy_storage, 2), "mm")
print("Drainage:", round(heavy_drainage, 2), "mm")
# 10. CROP WATER EXTRACTION FUNCTION



def extract_crop_water(layers, etc_mm, root_depth):

    updated_layers = [
        layer.copy() for layer in layers
    ]

    # Calculate how much water roots can access
    for layer in updated_layers:

        layer_thickness = layer["bottom"] - layer["top"]

        rooted_thickness = max(
            0,
            min(layer["bottom"], root_depth) - layer["top"]
        )

        accessible_fraction = rooted_thickness / layer_thickness

        layer["rooted_thickness"] = rooted_thickness

        # Maximum water available to roots in this layer
        layer["root_accessible_water"] = (
            layer["initial_storage_mm"] * accessible_fraction
        )

    remaining_demand = etc_mm

    while remaining_demand > 0.000001:

        active_layers = [
            layer for layer in updated_layers
            if layer["rooted_thickness"] > 0
            and layer["root_accessible_water"] > 0.000001
        ]

        if not active_layers:
            break

        total_weight = sum(
            layer["rooted_thickness"]
            for layer in active_layers
        )

        demand_this_round = remaining_demand

        extracted_this_round = 0

        for layer in active_layers:

            weight = layer["rooted_thickness"] / total_weight

            layer_demand = demand_this_round * weight

            water_extracted = min(
                layer_demand,
                layer["root_accessible_water"]
            )

            layer["initial_storage_mm"] -= water_extracted

            layer["initial_depletion_mm"] += water_extracted

            layer["root_accessible_water"] -= water_extracted

            extracted_this_round += water_extracted

        remaining_demand -= extracted_this_round

        if extracted_this_round < 0.000001:
            break

    return updated_layers, remaining_demand

# 11. TEST CROP WATER EXTRACTION

water_demand = 5.0

root_depth = 0.30

extracted_layers, unmet = extract_crop_water(
    test_state["layers"],
    water_demand,
    root_depth
)

print("\nCROP WATER EXTRACTION TEST")

print("Water demand:", water_demand, "mm")
print("Root depth:", root_depth, "m")
print("Unmet demand:", round(unmet, 2), "mm")
print("\nWATER EXTRACTED FROM EACH LAYER")

for i in range(len(test_state["layers"])):

    before = test_state["layers"][i]["initial_storage_mm"]

    after = extracted_layers[i]["initial_storage_mm"]

    extracted = before - after

    print(
        f'Layer {i + 1}:',
        round(extracted, 2),
        "mm extracted"
    )

# 12. VALIDATE CROP WATER CONSERVATION

storage_before = sum(
    layer["initial_storage_mm"]
    for layer in test_state["layers"]
)

storage_after = sum(
    layer["initial_storage_mm"]
    for layer in extracted_layers
)

water_extracted = storage_before - storage_after

crop_error = (
    storage_before
    - storage_after
    - water_extracted
)

print("\nCROP WATER CONSERVATION")

print("Storage before:", round(storage_before, 2), "mm")
print("Storage after:", round(storage_after, 2), "mm")
print("Water extracted:", round(water_extracted, 2), "mm")
print("Unmet demand:", round(unmet, 2), "mm")
print("Conservation error:", round(crop_error, 6), "mm")
# TEST DEEPER ROOT ACCESS

deep_root_layers, deep_unmet = extract_crop_water(
    test_state["layers"],
    6.0,
    0.45
)

print("\nDEEPER ROOT ACCESS TEST")

print("Root depth: 0.45 m")
print("Water demand: 6.0 mm")

for i in range(len(test_state["layers"])):

    before = test_state["layers"][i]["initial_storage_mm"]

    after = deep_root_layers[i]["initial_storage_mm"]

    print(
        f"Layer {i + 1}:",
        round(before - after, 2),
        "mm extracted"
    )

print("Unmet demand:", round(deep_unmet, 2), "mm")

# TEST LIMITED ROOT-ACCESSIBLE WATER

limited_layers, limited_unmet = extract_crop_water(
    test_state["layers"],
    60.0,
    0.45
)

print("\nLIMITED ROOT-ACCESSIBLE WATER TEST")

print("Root depth: 0.45 m")
print("Crop water demand: 60.0 mm")

for i in range(len(test_state["layers"])):

    before = test_state["layers"][i]["initial_storage_mm"]

    after = limited_layers[i]["initial_storage_mm"]

    print(
        f"Layer {i + 1}:",
        round(before - after, 2),
        "mm extracted"
    )

print("Unmet water demand:", round(limited_unmet, 2), "mm")

# 13. FINAL TEST STATUS

print("\n-------------------------------------")

if abs(rainfall_error) < 0.000001 and abs(crop_error) < 0.000001:

    print("BASIC WATER CONSERVATION TESTS PASSED")

else:

    print("WATER CONSERVATION TEST FAILED")

print("-------------------------------------")
