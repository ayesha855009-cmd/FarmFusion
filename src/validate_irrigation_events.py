
import pandas as pd

scenarios = pd.read_csv(
    "data/processed/soil_water_balance_scenarios.csv"
)

events = pd.read_csv(
    "data/processed/irrigation_events.csv"
)

# Group events by all three scenario dimensions
check = events.groupby(
    [
        "soil_texture",
        "maximum_root_depth_m",
        "initial_depletion_fraction"
    ]
).agg(
    calculated_events=("irrigation_amount_mm", "count"),
    calculated_irrigation_mm=("irrigation_amount_mm", "sum")
).reset_index()

# Match each event group to its scenario
comparison = scenarios.merge(
    check,
    on=[
        "soil_texture",
        "maximum_root_depth_m",
        "initial_depletion_fraction"
    ],
    how="left"
)

comparison["calculated_events"] = (
    comparison["calculated_events"].fillna(0)
)

comparison["calculated_irrigation_mm"] = (
    comparison["calculated_irrigation_mm"].fillna(0)
)

# Validate event counts
comparison["event_count_match"] = (
    comparison["irrigation_events"]
    == comparison["calculated_events"]
)

# Validate irrigation totals, allowing for rounding
comparison["irrigation_amount_match"] = (
    (
        comparison["net_irrigation_mm"]
        - comparison["calculated_irrigation_mm"]
    ).abs() < 0.02
)

print("FARMFUSION - IRRIGATION DATA VALIDATION")

print(
    "\nEvent count matches:",
    comparison["event_count_match"].all()
)

print(
    "Irrigation amount matches:",
    comparison["irrigation_amount_match"].all()
)

print(
    "\nFailed scenarios:"
)

print(
    comparison[
        ~(
            comparison["event_count_match"]
            & comparison["irrigation_amount_match"]
        )
    ].to_string(index=False)
)
