import csv
import json
import urllib.request

def fetch_and_filter_airports():
    print("Downloading global aviation data from OurAirports...")
    airports_url = "https://github.io"
    runways_url = "https://github.io"
    
    raw_airports_path = "raw_airports.csv"
    raw_runways_path = "raw_runways.csv"
    
    try:
        urllib.request.urlretrieve(airports_url, raw_airports_path)
        urllib.request.urlretrieve(runways_url, raw_runways_path)
    except Exception as e:
        print(f"Error downloading data: {e}")
        return

    # Phase 1: Scan runways.csv to find the longest runway for each airport identifier
    print("Pre-processing runway metrics...")
    airport_runways = {}
    
    with open(raw_runways_path, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            ident = row["airport_ident"].strip().upper()
            try:
                length_ft = float(row["length_ft"]) if row["length_ft"] else 0
            except ValueError:
                length_ft = 0
                
            try:
                # 1 means lighted, 0 means unlighted
                is_lighted = int(row["lighted"]) if row["lighted"] else 0
            except ValueError:
                is_lighted = 0

            # Keep track of the longest runway found for this airport
            if ident not in airport_runways:
                airport_runways[ident] = {"max_length": length_ft, "lighted": is_lighted}
            else:
                if length_ft > airport_runways[ident]["max_length"]:
                    airport_runways[ident]["max_length"] = length_ft
                # If any of the runways at the location have lighting, preserve the flag
                if is_lighted == 1:
                    airport_runways[ident]["lighted"] = 1

    # Phase 2: Process airports.csv and combine with the calculated runway data
    game_airports = {}
    print("Processing and filtering final gameplay dataset...")

    with open(raw_airports_path, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            ident = row["ident"].strip().upper()
            
            # Cross-reference with the runway dictionary
            runway_info = airport_runways.get(ident, {"max_length": 0, "lighted": 0})
            
            # Apply your physical requirements:
            # 1. Long runway threshold (>= 5000ft)
            # 2. Runway must feature lighting systems (== 1)
            # 3. Airport profile must be currently operational (status == "open")
            if (
                runway_info["max_length"] >= 5000 
                and runway_info["lighted"] == 1 
                and row["status"] == "open"
            ):
                # Use IATA if available, fallback to 4-letter identifier if missing
                code_key = row["iata_code"].strip().upper() if row["iata_code"] else ident
                
                game_airports[code_key] = {
                    "ident": ident,
                    "name": row["name"],
                    "municipality": row["municipality"],
                    "country": row["iso_country"],
                    "lat": float(row["latitude_deg"]),
                    "lon": float(row["longitude_deg"]),
                    "type": row["type"],
                    "runway_length": runway_info["max_length"]
                }

    output_json_path = "airports.json"
    with open(output_json_path, "w", encoding="utf-8") as f:
        json.dump(game_airports, f, indent=4)

    print(f"Success! Exported {len(game_airports)} game-ready commercial airports into '{output_json_path}'.")

if __name__ == "__main__":
    fetch_and_filter_airports()
