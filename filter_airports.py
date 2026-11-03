import pandas as pd
import json

print("Connecting to database records...")

airports = pd.read_csv('https://davidmegginson.github.io/ourairports-data/airports.csv')
runways = pd.read_csv('https://davidmegginson.github.io/ourairports-data/runways.csv')

print("Filtering runway dimensions and tracking equipment rules...")

filtered_runways = runways[(runways['length_ft'] > 5000) & (runways['lighted'] == 1)]
operational_airports = airports[airports['type'].isin(['medium_airport', 'large_airport'])]

valid_hubs = operational_airports[operational_airports['id'].isin(filtered_runways['airport_ref'])]
output_data = valid_hubs[['name', 'iata_code', 'municipality', 'iso_country']].dropna(subset=['iata_code']).to_dict(orient='records')

print(f"Filter process complete. Extracted {len(output_data)} authorized system nodes.")

with open('hubs.json', 'w') as f:
    json.dump(output_data, f, indent=2)

print("Data saved successfully to hubs.json.")
