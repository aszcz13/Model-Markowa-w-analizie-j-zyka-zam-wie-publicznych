import requests
import json
import os
import time
import random
from datetime import datetime, timedelta

DATA_DIR = "data"
RAW_DATA_FILE = os.path.join(DATA_DIR, "raw_tenders.json")
API_URL = "https://ezamowienia.gov.pl/mo-board/api/v1/notice"

def fetch_data_from_api(limit=500):
    print(f"Attempting to fetch {limit} records from API...")
    
    # Calculate date range for the last 3 months to ensure we get enough data
    end_date = datetime.now()
    start_date = end_date - timedelta(days=90)
    
    params = {
        "NoticeType": "ContractNotice",
        "PublicationDateFrom": start_date.strftime("%Y-%m-%d"),
        "PublicationDateTo": end_date.strftime("%Y-%m-%d"),
        "pageSize": 100,
        "pageNo": 1
    }
    
    all_tenders = []
    
    while len(all_tenders) < limit:
        try:
            response = requests.get(API_URL, params=params, timeout=10)
            if response.status_code != 200:
                print(f"API Error: {response.status_code} - {response.text}")
                break
                
            data = response.json()
            if not data:
                print("No data returned.")
                break
                
            # The API structure might be a list or a dict with a list. 
            # Based on typical paging APIs, it might be a list directly or under a key.
            # Let's inspect the first response structure if we were running interactively, 
            # but here we assume a standard list or 'items' key.
            # If data is a list, extend. If dict, look for 'items' or similar.
            
            items = []
            if isinstance(data, list):
                items = data
            elif isinstance(data, dict):
                # Common keys for paginated responses
                for key in ['items', 'data', 'notices', 'list']:
                    if key in data:
                        items = data[key]
                        break
            
            if not items:
                print("Could not find items in response.")
                break
                
            all_tenders.extend(items)
            print(f"Fetched {len(all_tenders)} records so far...")
            
            if len(items) < params['pageSize']:
                break # End of data
                
            params['pageNo'] += 1
            time.sleep(0.5) # Be nice to the API
            
        except Exception as e:
            print(f"Exception during fetching: {e}")
            break
            
    return all_tenders[:limit]

def generate_synthetic_data(count=500):
    print(f"Generating {count} synthetic records...")
    
    types = ["Dostawy", "Usługi", "Roboty budowlane"]
    
    descriptions = {
        "Dostawy": [
            "Dostawa sprzętu komputerowego dla urzędu.",
            "Zakup i dostawa mebli biurowych.",
            "Dostawa paliw płynnych do samochodów służbowych.",
            "Dostawa artykułów biurowych i papierniczych.",
            "Zakup licencji oprogramowania antywirusowego."
        ],
        "Usługi": [
            "Świadczenie usług sprzątania pomieszczeń biurowych.",
            "Usługa ochrony mienia i osób.",
            "Opracowanie dokumentacji projektowej.",
            "Przeprowadzenie szkoleń z zakresu BHP.",
            "Usługi prawne i doradcze."
        ],
        "Roboty budowlane": [
            "Budowa hali sportowej przy szkole podstawowej.",
            "Remont drogi gminnej nr 12345.",
            "Modernizacja oświetlenia ulicznego.",
            "Przebudowa budynku użyteczności publicznej.",
            "Wykonanie termomodernizacji budynku przedszkola."
        ]
    }
    
    data = []
    for i in range(count):
        category = random.choice(types)
        base_desc = random.choice(descriptions[category])
        # Add some random noise/variation
        desc = f"{base_desc} Numer referencyjny: {i}/{random.randint(2023, 2025)}. Termin realizacji: {random.randint(1, 12)} miesięcy."
        
        record = {
            "id": f"syn-{i}",
            "orderType": category, # This might need mapping to API format later
            "description": desc,
            "title": f"Przetarg na {category.lower()} - {i}"
        }
        data.append(record)
        
    return data

def main():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
        
    tenders = fetch_data_from_api(limit=500)
    
    if not tenders:
        print("API fetch failed or returned no data. Switching to synthetic data.")
        tenders = generate_synthetic_data(limit=500)
    else:
        print(f"Successfully fetched {len(tenders)} records from API.")
        
    # Save to file
    with open(RAW_DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(tenders, f, ensure_ascii=False, indent=2)
    
    print(f"Data saved to {RAW_DATA_FILE}")

if __name__ == "__main__":
    main()
