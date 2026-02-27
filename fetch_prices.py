import os
import requests
import json

def fetch_and_save_metal_prices(currency):
    # Fetch the key from environment variables
    api_key = os.environ.get("METALS_API_KEY")
    
    if not api_key:
        print("Error: METALS_API_KEY not found in environment.")
        return

    url = f"https://api.metals.dev/v1/latest?api_key={api_key}&currency={currency}&unit=toz"

    # List of specific metals we want to extract
    target_metals = [
        "gold", "silver", "platinum", "palladium",
        "copper", "nickel", "aluminum", "zinc", "lead"
    ]

    try:
        print(f"Fetching data for {currency}...")
        response = requests.get(url, headers={"Accept": "application/json"})
        response.raise_for_status() # Raise error for bad status codes

        data = response.json()

        # 1. Extract only the metals we care about
        filtered_metals = {
            metal: data["metals"].get(metal)
            for metal in target_metals
            if metal in data["metals"]
        }

        # 2. Build the new structure
        transformed_data = {
            "metals": filtered_metals,
            "timestamps": {
                "metal": data.get("timestamps", {}).get("metal", "")
            }
        }

        # 3. Save to file
        filename = f"{currency}.json"
        with open(filename, 'w') as f:
            json.dump(transformed_data, f, indent=2)

        print(f"Successfully saved {filename}")

    except Exception as e:
        print(f"Error processing {currency}: {e}")

if __name__ == "__main__":
    # Process both currencies
    for curr in ["USD", "EUR"]:
        fetch_and_save_metal_prices(curr)
