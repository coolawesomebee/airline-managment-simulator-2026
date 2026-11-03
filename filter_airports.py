import pandas as pd
import json

# Fetch live data
airports = pd.read_csv('https://github.io')
runways = pd.read_csv('https://github.io')

# Filter criteria
filtered_runways = runways[(runways['length_ft'] > 5000) & (runways['lighted'] == 1)]
operational_airports = airports[airports['type'].isin(['medium_airport', 'large_airport'])]

# Merge and extract relevant columns
valid_hubs = operational_airports[operational_airports['id'].isin(filtered_runways['airport_ref'])]
output_data = valid_hubs[['name', 'iata_code', 'municipality', 'iso_country']].dropna(subset=['iata_code']).to_dict(orient='records')

# Save to a clean JSON file
with open('hubs.json', 'w') as f:
    json.dump(output_data, f, indent=2)
