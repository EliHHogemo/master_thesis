import os
import cdsapi
from time import sleep

vars = ["2m_temperature"]

yrs = [str(y) for y in range(2014, 2015)]  # or [1991]
dataset = "reanalysis-era5-single-levels-monthly-means"

request_base = {
    "product_type": "reanalysis",
    #"monthly_statistic": "monthly_mean",
    "time": ["12:00"],
    "data_format": "netcdf",
}

# Prepare full-year month/day lists (strings, zero-padded)
all_months = [f"{m:02d}" for m in range(1, 13)]
all_days = [f"{d:02d}" for d in range(1, 32)]

c = cdsapi.Client()
usr = os.getenv("USER")

for var in vars:
    out_dir = f"/scratch/{usr}/{var}_era5_monthly"
    os.makedirs(out_dir, exist_ok=True)
    for yr in yrs:
        print(f"Downloading {var} for {yr}")
        target = f"{out_dir}/{var}_era5_{yr}.nc"
        if os.path.exists(target):
            print(f"Exists, skipping: {target}")
            continue

        req = dict(request_base)
        req["variable"] = var
        req["year"] = yr
        req["month"] = all_months     # <-- list, not range
        c.retrieve(dataset, req, target)
        sleep(5)