import pandas as pd
import json
import requests
import io

print("Connecting securely to database records...")

# Use requests to download data safely, bypassing platform verification limits
airports_url = 'https://davidmegginson.github.io/ourairports-data/airports.csv'
runways_url = 'https://davidmegginson.github.io/ourairports-data/runways.csv'

try:
    print("Downloading airports registry...")
    airports_response = requests.get(airports_url, timeout=30).content
    airports = pd.read_csv(io.StringIO(airports_response.decode('utf-8')))

    print("Downloading runways dimensional maps...")
    runways_response = requests.get(runways_url, timeout=30).content
    runways = pd.read_csv(io.StringIO(runways_response.decode('utf-8')))

except Exception as e:
    print(f"Network stream failure: {e}")
    exit(1)

print("Filtering dimensions and active operational layout configurations...")

# Parse configuration rules (Runway > 5,000ft, active lighting, non-closed classes)
filtered_runways = runways[(runways['length_ft'] > 5000) & (runways['lighted'] == 1)]
operational_airports = airports[airports['type'].isin(['medium_airport', 'large_airport'])]

# Filter and structure matching operational entries
valid_hubs = operational_airports[operational_airports['id'].isin(filtered_runways['airport_ref'])]
output_data = valid_hubs[['name', 'iata_code', 'municipality', 'iso_country']].dropna(subset=['iata_code']).to_dict(orient='records')

print(f"Filtering complete. Captured {len(output_data)} corporate system nodes.")

with open('hubs.json', 'w') as f:
    json.dump(output_data, f, indent=2)

print("Process finished successfully. Output written to hubs.json.")
