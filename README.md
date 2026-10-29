# Formula 1 Race Performance & Strategy Dashboard

🔗 **Live Application:** [f1-race-dashboard-mubarak.streamlit.app](https://f1-race-dashboard-mubarak.streamlit.app)

## Overview
Raw lap times in Formula 1 are noisy. Fuel burn, traffic, track evolution and changing weather can all hide how fast a car really is. In this project I built an interactive dashboard using real F1 race data to find pace gaps between drivers, measure how fast tyres wear out, and see how the track changes over a race. I compared two different races: Monaco 2022 and Bahrain 2022.

## Dataset Information
- **Source:** FastF1 API
- **Volume:**
  - Monaco 2022: 1,179 laps × 31 parameters
  - Bahrain 2022: 1,125 laps × 31 parameters
- **Format:** Lap-by-lap race data
- **Key Features:** `Driver`, `LapNumber`, `Compound`, `TyreLife`, `LapTime`, `LapTimeSec`, `Stint`

## What I Did
1. **Cleaning and filtering noise:**
   - Raw race data includes laps that don't show real pace: pit in/out laps, virtual/safety cars, yellow flags, and unusually slow laps.
   - I removed `NaT` (Not a Time) values and took out the in-laps and out-laps, so I was left with clean flying laps.
   - This is how the row counts went down:
     - Monaco: 1,179 → 910 → 844 → 566 flying laps
     - Bahrain: 1,125 → 958 → 858 clean laps
2. **Feature engineering:**
   - I created `LapTimeSec` by converting the raw lap times into seconds as plain numbers, so I could fit trendlines to them.
3. **Analysis:**
   - I compared Monaco, where the race went from wet to dry, against Bahrain, which was dry and steady.
   - I fitted linear trendlines across the dry stints to get the basic wear rate (seconds lost per lap of tyre age).

## Dashboard Features
The Streamlit app lets you pick any two drivers in a race and compare them:
1. **Lap-Time Gap:** A head-to-head comparison of the gap between the two drivers across the whole race.
2. **Tyre Degradation:** How lap times get slower as the tyre ages (`TyreLife`).
3. **Track Evolution:** How the circuit gets faster over the session as rubber builds up on the track.

## Charts



![Lap Time Gap](lap_time_gap.png)





![Tyre Degradation](Tyre_degradation.png)





![Track Evolution](Track_evolution.png)



## What I Found
- **Conditions change what the data means:** In Monaco 2022, the wet and intermediate tyres and the drying track hid the real tyre wear. Lap times got faster even as the tyres aged, because the track was drying out.
- **Dry races show wear clearly:** In Bahrain 2022, which was dry throughout, I could clearly see tyre wear (from heat and mechanical stress) and measure the pace lost per lap.
- **Why it matters for strategy:** Strategists can't rely on raw lap times alone. They need to separate the track getting faster from the tyres wearing out to pick the best time to pit.

## Project Structure
- `FastF1.ipynb`: The full notebook with my data exploration and processing.
- `dashboard.py`: The Streamlit dashboard script.
- `lap_time_gap.png`, `Tyre_degradation.png`, `Track_evolution.png`: Preview images of the charts.

## Tech Stack
- **Language:** Python
- **Data Engineering:** Pandas, NumPy, FastF1 API
- **Visualization:** Matplotlib, Seaborn
- **Deployment:** Streamlit Cloud

## Author
**Mubarak Agboola**  
Mechanical Engineering Student | Machine Learning & Data Analytics
