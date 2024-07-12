from fastapi import FastAPI
from typing import List, Dict, Union
from urllib.parse import unquote

app = FastAPI()

areas = {
    '香港': {
        '中西區': ['堅尼地城', '石塘咀', '西營盤', '上環', '中環', '金鐘', '半山', '山頂'],
        '灣仔': ['灣仔', '銅鑼灣', '跑馬地', '大坑', '掃桿埔', '渣甸山'],
        '東區': ['天后', '寶馬山', '北角', '鰂魚涌', '西灣河', '筲箕灣', '柴灣', '小西灣'],
        '南區': ['薄扶林', '香港仔', '鴨脷洲', '黃竹坑', '壽臣山', '淺水灣', '舂磡角', '赤柱', '大潭', '石澳']
    },
    '九龍': {
        '油尖旺': ['尖沙咀', '油麻地', '西九龍', '京士柏', '旺角', '大角咀'],
        '深水埗': ['美孚', '荔枝角', '長沙灣', '深水埗', '石硤尾', '又一村', '大窩坪', '昂船洲'],
        '九龍城': ['紅磡', '土瓜灣', '馬頭角', '馬頭圍', '啟德', '九龍城', '何文田', '九龍塘', '筆架山'],
        '黃大仙': ['新蒲崗', '黃大仙', '東頭', '橫頭磡', '樂富', '鑽石山', '慈雲山', '牛池灣'],
        '觀塘': ['坪石', '九龍灣', '牛頭角', '佐敦谷', '觀塘', '秀茂坪', '藍田', '油塘', '鯉魚門']
    },
    '新界': {
        '葵青': ['葵涌', '青衣'],
        '荃灣': ['荃灣', '梨木樹', '汀九', '深井', '青龍頭', '馬灣', '欣澳'],
        '屯門': ['大欖涌', '掃管笏', '屯門', '藍地'],
        '元朗': ['洪水橋', '廈村', '流浮山', '天水圍', '元朗', '新田', '落馬洲', '錦田', '石崗', '八鄉'],
        '北區': ['粉嶺', '聯和墟', '上水', '石湖墟', '沙頭角', '鹿頸', '烏蛟騰'],
        '大埔': ['大埔墟', '大埔', '大埔滘', '大尾篤', '船灣', '樟木頭', '企嶺下'],
        '沙田': ['大圍', '沙田', '火炭', '馬料水', '烏溪沙', '馬鞍山'],
        '西貢': ['清水灣', '西貢', '大網仔', '將軍澳', '坑口', '調景嶺', '馬游塘'],
        '離島': ['長洲', '坪洲', '大嶼山', '東涌', '南丫島']
    }
}

def segment_input(input_str: str) -> List[Dict[str, Union[str, List[str]]]]:
    decoded_input = unquote(input_str)  # Decode URL-encoded input string

    results = []

    # Assuming areas is a predefined dictionary containing areas, districts, and sub-districts
    for area, districts in areas.items():
        for district, sub_districts in districts.items():
            for sub_district in sub_districts:
                if sub_district in decoded_input:
                    # Remove the found sub_district from the input string
                    building_street = decoded_input.replace(sub_district, '').strip()

                    # Remove area, district, and sub_district prefixes if present
                    for prefix in [area, district, sub_district]:
                        if building_street.startswith(prefix):
                            building_street = building_street[len(prefix):].strip()

                    # Split into street and building details
                    if '號' in building_street:
                        street, building_details = building_street.split('號', 1)
                        street += '號'
                    else:
                        street = building_street.strip() + '號'
                        building_details = ''

                    # Append the parsed address components to results
                    results.append({
                        'area': area,
                        'district': district,
                        'sub_district': sub_district,
                        'street': [street],
                        'building': building_details.strip()
                    })

                    return results

    # If no specific match is found, treat the remaining input as a general address
    if decoded_input.strip():
        building_street = decoded_input.strip()

        if '號' in building_street:
            street, building_details = building_street.split('號', 1)
            street += '號'
        else:
            street = building_street.strip() + '號'
            building_details = ''

        results.append({
            'area': '',
            'district': '',
            'sub_district': '',
            'street': [street],
            'building': building_details.strip()
        })

    return results

@app.get("/area/zh-hk/{input_str}")
def segment_address(input_str: str):
    return segment_input(input_str)
