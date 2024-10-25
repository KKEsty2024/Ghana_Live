import csv
import json
from collections import defaultdict

# Load your CSV file
data = []
with open('Total_Sites.csv', 'r', encoding='ISO-8859-1') as file:
    csv_reader = csv.DictReader(file)
    for row in csv_reader:
        data.append(row)

# Prepare a structure to group batteries by site_id
site_dict = defaultdict(lambda: {
    "type": "Feature",
    "geometry": None,
    "properties": {
        "site_name": None,
        "site_id": None,
        "tracker_IMEI": None,
        "installation_status": None,
        "battery_numbers": [],  # Array to hold multiple batteries
        "geofence_distance": None
    }
})

# Populate the site dictionary with data
for site in data:
    if site["Latitude"] and site["Longitude"]:
        site_id = site["Site Number"]
        
        # If the site already exists in site_dict, just append the battery number
        if site_dict[site_id]["geometry"] is None:
            site_dict[site_id]["geometry"] = {
                "type": "Point",
                "coordinates": [float(site["Longitude"]), float(site["Latitude"])]
            }
        
        # Assign basic properties only once per site
        site_dict[site_id]["properties"].update({
            "site_name": site["Site Name"],
            "site_id": site["Site Number"],
            "tracker_IMEI": site["Tracker IMEI"],
            "installation_status": site["Installation Status"],
            "geofence_distance": site["Geofence Meters"]
        })
        
        # Append each battery number to the battery_numbers list
        site_dict[site_id]["properties"]["battery_numbers"].append(site["Serial Number"])

# Convert to GeoJSON format
geojson = {
    "type": "FeatureCollection",
    "features": list(site_dict.values())
}

# Save as a GeoJSON file
with open('map_data.geojson', 'w', encoding='utf-8') as geojson_file:
    json.dump(geojson, geojson_file, indent=4)

print("GeoJSON file with grouped batteries created successfully!")
