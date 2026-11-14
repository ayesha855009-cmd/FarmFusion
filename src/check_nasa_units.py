
import requests

url = "https://power.larc.nasa.gov/api/temporal/daily/point"

params = {
    "parameters": (
        "T2M_MAX,T2M_MIN,T2MDEW,WS10M,"
        "ALLSKY_SFC_SW_DWN,PRECTOTCORR"
    ),
    "community": "AG",
    "latitude": 32.43,
    "longitude": 73.58,
    "start": "20231123",
    "end": "20231125",
    "format": "JSON"
}

response = requests.get(url, params=params, timeout=30)
response.raise_for_status()

data = response.json()

print("NASA POWER PARAMETER UNITS\n")

for parameter, details in data["parameters"].items():
    print(parameter, ":", details["units"])
