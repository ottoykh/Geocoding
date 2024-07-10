import os
import re
from collections import Counter
from tqdm import tqdm
import csv
import re
from collections import Counter

hk_districts = [
    'Central and Western', 'Eastern', 'Southern', 'Wan Chai',
    'Kowloon City', 'Kwun Tong', 'Sham Shui Po', 'Wong Tai Sin', 'Yau Tsim Mong',
    'Kwai Tsing', 'North', 'Sai Kung', 'Sha Tin', 'Tai Po', 'Tsuen Wan',
    'Tuen Mun', 'Yuen Long', 'Islands'
]

hk_district_areas = {
    'Central and Western': ['Central', 'Sheung Wan', 'Sai Ying Pun', 'Kennedy Town', 'Mid-Levels', 'The Peak', 'Admiralty', 'Lower Peak', 'Upper Central', 'Upper Sheung Wan', 'Western District'],
    'Eastern': ['Quarry Bay', 'Chai Wan', 'Shau Kei Wan', 'Sai Wan Ho', 'North Point', 'Fortress Hill', 'Tai Koo Shing', 'Heng Fa Chuen', 'Braemar Hill', 'Aldrich Bay', 'Heng Fa Villa', 'Mount Parker'],
    'Southern': ['Aberdeen', 'Ap Lei Chau', 'Stanley', 'Repulse Bay', 'Wong Chuk Hang', 'Pok Fu Lam', 'Deep Water Bay', 'Tin Wan', 'Cyberport', 'Chi Fu Fa Yuen', 'Wah Fu', 'Tai Tam', 'Shek O', 'Big Wave Bay'],
    'Wan Chai': ['Wan Chai', 'Causeway Bay', 'Happy Valley', 'Tai Hang', 'Jardine’s Lookout', 'Stubbs Road', 'Broadwood Road', 'Bowen Road'],
    'Kowloon City': ['Kowloon City', 'Hung Hom', 'Mong Kok', 'Kowloon Tong', 'To Kwa Wan', 'Ho Man Tin', 'Lok Fu', 'Kowloon Bay', 'Kai Tak', 'Whampoa', 'Hung Hom Bay', 'Ma Tau Wai'],
    'Kwun Tong': ['Kwun Tong', 'Lam Tin', 'Yau Tong', 'Ngau Tau Kok', 'Sau Mau Ping', 'Tiu Keng Leng', 'Lei Yue Mun', 'Kowloon Bay Industrial Area', 'Kwun Tong Industrial Area'],
    'Sham Shui Po': ['Sham Shui Po', 'Cheung Sha Wan', 'Lai Chi Kok', 'Shek Kip Mei', 'Mei Foo', 'Nam Cheong', 'Yau Yat Tsuen', 'So Uk Estate', 'Wah Lai Estate', 'Un Chau Estate'],
    'Wong Tai Sin': ['Wong Tai Sin', 'Diamond Hill', 'Choi Hung', 'Lok Fu', 'Tsz Wan Shan', 'San Po Kong', 'Ngau Chi Wan', 'Wang Tau Hom', 'Chuk Yuen', 'Tung Tau Estate'],
    'Yau Tsim Mong': ['Yau Ma Tei', 'Tsim Sha Tsui', 'Jordan', 'Mong Kok', 'Tai Kok Tsui', 'King’s Park', 'West Kowloon', 'Kowloon Park', 'Cherry Street', 'Langham Place'],
    'Kwai Tsing': ['Kwai Chung', 'Tsing Yi', 'Kwai Fong', 'Kwai Hing', 'Tsing Yi North', 'Tsing Yi South', 'Cheung Hong', 'Cheung Hang', 'Lai King', 'Greenfield Garden', 'Mayfair Gardens', 'Cheung Wang'],
    'North': ['Sheung Shui', 'Fanling', 'Sha Tau Kok', 'Kwu Tung', 'Ta Kwu Ling', 'Lung Yeuk Tau', 'Luk Keng', 'Ping Che', 'Fanling North', 'Shek Wu Hui', 'Wah Ming Estate', 'Ching Ho Estate'],
    'Sai Kung': ['Sai Kung', 'Clear Water Bay', 'Tseung Kwan O', 'Hang Hau', 'Pak Tam Chung', 'Silverstrand', 'Po Lam', 'Fei Ngo Shan', 'Sai Kung Town', 'Kau Sai Chau', 'Pak Sha Wan', 'Marina Cove'],
    'Sha Tin': ['Sha Tin', 'Ma On Shan', 'Fo Tan', 'Tai Wai', 'Hin Keng', 'Wu Kai Sha', 'Shatin City One', 'Jubilee Garden', 'Lek Yuen Estate', 'Wo Che Estate', 'City One', 'Sha Tin Wai', 'Tate’s Cairn', 'Sha Tin Heights'],
    'Tai Po': ['Tai Po', 'Tai Mei Tuk', 'Tai Po Kau', 'Lam Tsuen', 'Plover Cove', 'Hong Lok Yuen', 'Tai Wo Estate', 'Fu Heng Estate', 'Wan Tau Tong', 'Tai Po Industrial Estate', 'Uptown Plaza', 'Greenfield Garden', 'Eightland Gardens'],
    'Tsuen Wan': ['Tsuen Wan', 'Tsing Lung Tau', 'Discovery Park', 'Belvedere Garden', 'Sham Tseng', 'Ma Wan', 'Allway Gardens', 'Tsuen Wan West', 'Tsuen King Circuit', 'Nina Tower', 'Clague Garden Estate'],
    'Tuen Mun': ['Tuen Mun', 'Castle Peak', 'Sam Shing', 'So Kwun Wat', 'Siu Hong', 'Gold Coast', 'Tuen Mun Town Centre', 'San Hui', 'Butterfly Estate', 'Tai Lam', 'Lung Mun Oasis', 'On Ting Estate'],
    'Yuen Long': ['Yuen Long', 'Tin Shui Wai', 'Kam Tin', 'Shui Pin Wai', 'Shap Pat Heung', 'Ping Shan', 'Hung Shui Kiu', 'Fairview Park', 'Yuen Long Town', 'Nam Sang Wai', 'Pat Heung', 'Ha Tsuen'],
    'Islands': ['Lantau Island', 'Cheung Chau', 'Peng Chau', 'Lamma Island', 'Discovery Bay', 'Tung Chung', 'Mui Wo', 'Tai O', 'Ngong Ping', 'Po Lin Monastery', 'Silvermine Bay', 'Pui O', 'Chek Lap Kok', 'Sok Kwu Wan', 'Yung Shue Wan', 'Hei Ling Chau']
}

def extract_address_elements(messy_address):
    address_parts = [part.strip() for part in messy_address.split(',')]

    street_info = None
    area = None
    district = None
    region = None

    street_pattern = re.compile(r'''
        (?P<street_number>\d+\s*\/?\s*[A-Za-z]*)?\s*
        (?P<street_name>
            (?:[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\s+
            (Street|Road|Avenue|Lane|Path|Terrace|Drive|Place|Mansion|Boulevard|Court|Square|Garden|Estate))
        )|
        (?P<complex_name>
            (?:[A-Z][a-z]+\s*)+
            (Building|Tower|Block|Phase|Wing|Centre|Complex|Plaza|Arcade|Garden|Estate)
        )
    ''', re.IGNORECASE | re.VERBOSE)

    for part in address_parts:
        match = street_pattern.search(part.lower())
        if match:
            street_info = part
            continue

        for d, areas in hk_district_areas.items():
            if d.lower() in part.lower():
                district = d
                break
            for a in areas:
                if a.lower() in part.lower():
                    area = a
                    district = d
                    break
            if district:
                break

        if 'new territories' in part.lower():
            region = 'New Territories'
        elif 'kowloon' in part.lower():
            region = 'Kowloon'
        elif 'hong kong' in part.lower():
            region = 'Hong Kong Island'

    return street_info, area, district, region

def process_file(input_file, output_file, unprocessed_file):
    with open(input_file, 'r', encoding='utf-8') as infile, \
         open(output_file, 'w', encoding='utf-8', newline='') as outfile, \
         open(unprocessed_file, 'w', encoding='utf-8') as unprocessed_outfile:

        csv_writer = csv.writer(outfile)
        csv_writer.writerow(["Street Info", "Area", "District", "Region"])

        for line in tqdm(infile, desc="Processing addresses"):
            messy_address = line.strip()
            if messy_address:
                street_info, area, district, region = extract_address_elements(messy_address)
                if all([street_info, district, region]):
                    csv_writer.writerow([street_info, area or 'N/A', district, region])
                else:
                    unprocessed_outfile.write(messy_address + '\n')

def analyze_results(output_file, unprocessed_file):
    processed_addresses = 0
    district_counter = Counter()
    region_counter = Counter()

    with open(output_file, 'r', encoding='utf-8') as f:
        csv_reader = csv.reader(f)
        next(csv_reader)
        for row in csv_reader:
            processed_addresses += 1
            _, _, district, region = row
            district_counter[district] += 1
            region_counter[region] += 1

    with open(unprocessed_file, 'r', encoding='utf-8') as f:
        unprocessed_addresses = sum(1 for _ in f)

    total_addresses = processed_addresses + unprocessed_addresses

    print(f"Total addresses: {total_addresses}")
    print(f"Processed addresses: {processed_addresses} ({processed_addresses / total_addresses:.2%})")
    print(f"Unprocessed addresses: {unprocessed_addresses} ({unprocessed_addresses / total_addresses:.2%})")

def clean_data(input_file_path, output_file_path):
    """
    Cleans the data in the input file and saves the cleaned data to the output file.
    
    Args:
        input_file_path (str): The path to the input file.
        output_file_path (str): The path to the output file.
    """
    try:
        with open(input_file_path, 'r') as file:
            lines = file.readlines()
    except FileNotFoundError:
        print(f"Error: {input_file_path} not found.")
        return

    cleaned_lines = [line.replace("N/A,", "") for line in lines]

    try:
        with open(output_file_path, 'w') as file:
            file.writelines(cleaned_lines)
    except IOError:
        print(f"Error: Unable to write to {output_file_path}.")
        return

    print(f"Cleaned data has been saved to {output_file_path}")