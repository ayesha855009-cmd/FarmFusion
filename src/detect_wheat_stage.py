
from datetime import date

# Provisional Phalia test planting date
planting_date = date(2023, 11, 23)

# Test date
test_date = date(2024, 1, 1)

# Approximate FAO reference durations (days)
initial_days = 15
development_days = 30
mid_days = 65
late_days = 40

days_after_sowing = (test_date - planting_date).days

if days_after_sowing < 0:
    stage = "Before planting"

elif days_after_sowing < initial_days:
    stage = "Initial"

elif days_after_sowing < initial_days + development_days:
    stage = "Crop development"

elif days_after_sowing < initial_days + development_days + mid_days:
    stage = "Mid-season"

elif days_after_sowing < (
    initial_days + development_days + mid_days + late_days
):
    stage = "Late-season"

else:
    stage = "Growing season completed"

print("\nFARMFUSION - AUTOMATIC GROWTH STAGE")
print("Crop: Wheat")
print("Planting date:", planting_date)
print("Test date:", test_date)
print("Days after sowing:", days_after_sowing)
print("Detected growth stage:", stage)
