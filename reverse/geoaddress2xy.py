import time
import requests
import pandas as pd
from tqdm import tqdm

def process_geoaddress(geoaddress):
    digits = geoaddress[:10]
    x = int(digits[:5]) + 800000
    y = int(digits[5:]) + 800000
    return x, y

def fetch_api(x, y, delay=0.001):
    url = f"https://geodata.gov.hk/gs/api/v1.0.0/identify?x={x}&y={y}"
    response = requests.get(url)
    time.sleep(delay)
    return response.json()

def process_batch(input_file, delay=0.001):
    results = []

    with open(input_file, 'r') as infile:
        geoaddresses = infile.readlines()

    with tqdm(total=len(geoaddresses), desc="Processing geoaddresses", bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]", colour="green") as pbar:
        for geoaddress in geoaddresses:
            geoaddress = geoaddress.strip()
            x, y = process_geoaddress(geoaddress)
            data = fetch_api(x, y, delay=delay)

            if data['results']:
                address_info = data['results'][0]['addressInfo'][0]
                result = {
                    'geoaddress': geoaddress,
                    'x': x,
                    'y': y,
                    'eaddress': address_info.get('eaddress', ''),
                    'caddress': address_info.get('caddress', ''),
                    'roofLevel': address_info.get('roofLevel', ''),
                    'baseLevel': address_info.get('baseLevel', '')
                }
                results.append(result)

            pbar.update(1)

    df = pd.DataFrame(results)
    return df
