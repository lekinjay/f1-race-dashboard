import streamlit as st
import fastf1
import numpy as np
import matplotlib.pyplot as plt
import os

st.title("F1 Race Dashboard")
st.write("Compare two drivers across lap time gap, tyre degradation and track evolution.")

cache_dir = r'C:\Users\HomePC\Documents\F1\cache'
os.makedirs(cache_dir, exist_ok=True)
fastf1.Cache.enable_cache(cache_dir)

# Race selector
race_options = {
    '2022 Monaco': (2022, 'Monaco'),
    '2022 Bahrain': (2022, 'Bahrain')
}
race_choice = st.selectbox('Select a race', list(race_options.keys()))
year, race_name = race_options[race_choice]

# Load the session
session = fastf1.get_session(year, race_name, 'R')
session.load()
laps = session.laps

# Cleaning
clean_laps = laps[laps['TrackStatus'] == '1']
clean_laps = clean_laps[clean_laps['IsAccurate']]
clean_laps = clean_laps.dropna(subset=['LapTime'])
clean_laps = clean_laps[clean_laps['PitInTime'].isna() & clean_laps['PitOutTime'].isna()]
clean_laps = clean_laps.copy()
clean_laps['LapTimeSec'] = clean_laps['LapTime'].dt.total_seconds()

# Driver selector
drivers = sorted(clean_laps['Driver'].unique().tolist())
driver1 = st.selectbox('Select Driver 1', drivers, index=drivers.index('VER'))
driver2 = st.selectbox('Select Driver 2', drivers, index=drivers.index('LEC'))

# Stint selector for tyre degradation
stints = sorted(clean_laps['Stint'].dropna().unique().tolist())
stints = [int(s) for s in stints]
selected_stint = st.selectbox('Select stint for tyre degradation', stints)

# Chart 1: Lap-time gap
st.subheader("Chart 1: Lap-time gap")
d1 = clean_laps[clean_laps['Driver'] == driver1]
d2 = clean_laps[clean_laps['Driver'] == driver2]
gap = d1.merge(d2, on='LapNumber', suffixes=('_D1', '_D2'))
gap['Gap'] = gap['LapTimeSec_D1'] - gap['LapTimeSec_D2']

fig1, ax1 = plt.subplots()
ax1.plot(gap['LapNumber'], gap['Gap'], marker='o')
ax1.axhline(0, color='black', linestyle='--')
ax1.set_xlabel('Lap number')
ax1.set_ylabel(f'Gap: {driver1} minus {driver2} (seconds)')
ax1.set_title(f'Lap-time gap: {driver1} vs {driver2}')
st.pyplot(fig1)

# Chart 2: Tyre degradation
st.subheader("Chart 2: Tyre degradation")
fig2, ax2 = plt.subplots()
for driver, color in [(driver1, 'blue'), (driver2, 'red')]:
    d = clean_laps[(clean_laps['Driver'] == driver) & (clean_laps['Stint'] == selected_stint)]
    if len(d) >= 3:
        try:
            slope, intercept = np.polyfit(d['TyreLife'], d['LapTimeSec'], 1)
            ax2.scatter(d['TyreLife'], d['LapTimeSec'], color=color, label=driver)
            ax2.plot(d['TyreLife'], slope * d['TyreLife'] + intercept, color=color)
        except Exception:
            ax2.scatter(d['TyreLife'], d['LapTimeSec'], color=color, label=f'{driver} (no fit)')
ax2.set_xlabel('Tyre age (laps)')
ax2.set_ylabel('Lap time (seconds)')
ax2.set_title('Tyre degradation')
ax2.legend()
st.pyplot(fig2)

# Chart 3: Track evolution
st.subheader("Chart 3: Track evolution")
med = clean_laps.groupby('LapNumber')['LapTimeSec'].median()
fig3, ax3 = plt.subplots()
ax3.plot(med.index, med.values, marker='o')
ax3.set_xlabel('Lap number')
ax3.set_ylabel('Median lap time (seconds)')
ax3.set_title('Track evolution')
st.pyplot(fig3)








