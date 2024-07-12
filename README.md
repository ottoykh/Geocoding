
# Geocoding 

The package is a proof of concept to adopt different CSDI APIs to enhance the geocoding services in Hong Kong. 

Mainly there are two directions on the Geocoding in Hong Kong, 
- Direct, from address string to coordinate (x,y or easting, northing),
- Reverse, from coordinate to address string. 

This package allows different end-use to adopt those APIs with fewer lines of code to reach a codeless API fetching and data interchange for Hong Kong geospatial data. 

> Try out our webapp [geoaddress2xy](https://ottoykh.github.io/Geocoding/website/reverse-geocoding/index.html).

## Features
> Most of the feature will be developed in this late-July. 
- Address formatting with NLP (Natural language processing)
- Precise Address Lookup Service with Similary Check and Validations
- Batch processing with code-less python package and envrionment

## Installation

Simple Download and Plug in the Package with the following steps
```python
!git clone https://github.com/ottoykh/Geocoding.git
```
```python
cd /content/Geocoding/      # Sample from Colab eviornment, for other IDE to find the downloaded directory 
```
## Usage
#### Reverse Geocoding with IdentifyAPI (From Geoaddress to Address)
Reverse geocoding is a process to convert the spatial coordinates into address, it is important for the documentation Due to the coordinates from the map, it is hard to be identified on the ground without surveying and field measurements. So the address is one of the mediums that allows us to describe the geospatial location. Moreover, the Geoaddress has become a more popular and user-friendly way to store spatial coordinates, then with reverse geocoding batch processing can be applied for mass conversion and applications.  

```python
from reverse import geoaddress2xy

# input path diectory 
input_file = '/content/try.txt'
output_file = '/content/result.csv'

# Code to call and run the package 
results = geoaddress2xy.process_batch(input_file)
results.to_csv(output_file, index=True)
table = results.to_html(index=True)
display(HTML(table)) 
```
For the interactive web-based application, can either use the embeded website method with iframe to do the processing as well as the python coding based method. The following is the sample of the iframe code. 

```python 
%%html
<iframe src="https://ottoykh.github.io/Geocoding/website/reverse-geocoding/index.html" width="100%" height="850"></iframe>
```

#### Direct Geocoding with ALS API (From Address to Spatial Refernce Coodinates)
Direct geocoding is the process of transforming the address to spatial reference coordinates it can enable more in-depth spatial analysis to be applied with the georeferenced address to point-based spatial data. Still some of the challenges on the input format may be different and not in the ALS recognizable input, therefore this package has added a data formatting, cleaning and validation process to enhance the direct geocoding service in Hong Kong.
```python 
from direct import formatter
from Geocoding.direct.clean import clean_data

# input path directory
input_file = "/content/addresses.txt"
output_file = "/content/extracted_address_elements.txt"
unprocessed_file = "/content/unprocessed_addresses.txt"
clean_file = "/content/extracted_address_clean.txt"

# Code to call and run the package 
formatter.process_file(input_file, output_file, unprocessed_file)
formatter.analyze_results(output_file, unprocessed_file)
clean_data(output_file, clean_file)

```

Still Developing ... 


#### NLP (Natural language processing) for Address formatting 
Most of the time, the Chinese addresses are grouped and fused. Therefore, it would be better that we classify the address into segments, format , and reconstruct the address string in the ALS recognizable input. In this step, the NLP can be adopted for the Chinese language strings. 

```python 
from Geocoding.NLP.zhSeg import segment_text_file
# input path directory
input_file = '/content/sample.txt'

#  Segment text file will return decompose the chinese address into segment 
segmented = segment_text_file(input_file)
display(segmented)
```
Those address will be display in a table format, the following are some of the sample of the input and output. 

Input : 香港薄扶林道５４號地下至２樓

Output : 香港\薄扶林道\５４號\地下\至\２樓

```python 
from Geocoding.NLP.zhSeg import segment_address

#  Segment text file will return decompose the chinese address into sub-sets following the order, area, district, sub_district, street name, street number and building 
segmented = segment_address(input_file)
display(segmented)
```
original / area / district / sub_district / street_name / street_number / building

新界將軍澳唐賢街33號Capri地下G01號舖(部份)/ 新界 / 西貢 / 將軍澳 / 唐賢街 / 33號 / 	

```python 
from Geocoding.NLP.zhSeg import address_list
address_list = address_to_list(segmented)
for address in address_list:
    print(address)
```
The segmented address can be regroup into this list for the [GeoSpatialiser](https://tools.csdi.gov.hk/geospatialiser/) or the ALS API to fetch. The follow is some of the print list from the address_list. 

九龍油尖旺大角咀海輝道10號

九龍九龍城紅磡寶其利街121號

新界元朗第 2號

九龍九龍城九龍塘根德道6號
...

#### Keyword based language process for Address formatting with FastAPI 
The following is a trial for writing a new API to format those address with keyword based approches. The idea is clear that the address start with the area, district, sub_district, street, street number and end with the building name, then it would be simple to split those address and reformat it with a function from python and call into a API with FastAPI. A local host and deployed API with python has been tried out. User can run the file from the /NLP/api_trail1.py. 

Step to local host the api
- Install the package 
```python 
pip install fastapi uvicron
```
- Open the /NLP/api_trail1.py file. 
- Go to the terminal and type : 
```python 
uvicron main.app --reload
```
- The API is now running and hosting on local, you can input any address for the address formatting. 
```python 
http://127.0.0.1:8000/area/zh-hk/[input]
```
- Address formatting json will be display as follow
Input address (Chinese):
```
九龍何文田迦密村街9號君逸山一樓
```
Output result (Chinese):  
```json
[{"area":"九龍","district":"九龍城","sub_district":"何文田","street":["迦密村街9號"],"building":"君逸山一樓"}]
```
Input address (English):
```json
No. 2 Tai Wing Avenue,Tai Koo Shing 
```
Output result (English):
```
{
  "street": "No. 2 Tai Wing Avenue",
  "area": "Tai Koo Shing",
  "district": "Eastern",
  "region": "Hong Kong Island"
}
```

For more information : http://127.0.0.1:8000/docs#/ after local hosting. 

Format of the API
```
http://127.0.0.1:8000/area/[lang]/[value]
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `lang` | `string` | **Specific**, Language, for zh-hk = Chinese and en = English|
| `value` | `string` | **Specific**, either Chinese or English string. |
The user input is now avaliable for both Chinese and English with ./area/[input], the input address string will be identifies to redirect to either Chinese or English. 

The API will return the user back in json format, that includes the following information:

Chinese (zh-hk) address format :
```
├── area                
├── district                
├── sub_district            
├── street               
├── building
```
English (en) address format :
```
├── street                 
├── area                
├── district            
├── region               
```
Still developing... 


## API References for Geocoding 
### Address Lookup Service API
```
https://www.als.ogcio.gov.hk/lookup?q==[value]
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `value` | `string` | **Not specific** either Chinese or English, but format matters for the search result |


Sample usage of searching the "government offices"
```
https://www.als.ogcio.gov.hk/lookup?q=government%20offices
```
The Address Lookup Service API will return the user back in xml format, that includes the following information:
```
├── AddressLookupResult
│   ├── RequestAddress
│   │   └── AddressLine
│   ├── SuggestedAddress
│   │   ├── Address
│   │   │   └── PremisesAddress
│   │   │       ├── EngPremisesAddress
│   │   │       │   ├── EngEstate
│   │   │       │   │   └── EstateName
│   │   │       │   ├── EngStreet
│   │   │       │   │   ├── StreetName
│   │   │       │   │   └── BuildingNoFrom
│   │   │       │   ├── EngDistrict
│   │   │       │   │   └── DcDistrict
│   │   │       │   └── Region
│   │   │       ├── ChiPremisesAddress
│   │   │       │   ├── Region
│   │   │       │   ├── ChiDistrict
│   │   │       │   │   └── DcDistrict
│   │   │       │   ├── ChiStreet
│   │   │       │   │   ├── StreetName
│   │   │       │   │   └── BuildingNoFrom
│   │   │       │   └── ChiEstate
│   │   │       │       └── EstateName
│   │   │       ├── GeoAddress
│   │   │       └── GeospatialInformation
│   │   │           ├── Northing
│   │   │           ├── Easting
│   │   │           ├── Latitude
│   │   │           └── Longitude
│   │   └── ValidationInformation
│   │       └── Score
```

### Identify API
```
https://geodata.gov.hk/gs/api/[version]/identify?x=[value]&y=[value]&lang=[value]
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `version` | `string` | **Required**. Current version of the API is v1.0.0 |
| `x` | `integer` | **Required**. The value of x is the Easting coordinate reference the Hong Kong 1980 Grid System. |
| `y` | `integer`  | **Required**. The value of y is the Norhting coordinate reference the Hong Kong 1980 Grid System. |
| `lang` | `string` | **Not specific** can be either be selected by "zh" refers to Chinese or "en" refers to English. |


Sample usage of the Coordinate (835665,817198)
```
https://geodata.gov.hk/gs/api/v1.0.0/identify?x=835665&y=817198&lang=en
```
The Identify API will return the user back in json format, that includes the following information:

```
├── eaddress                   #English address
├── addressType                
├── cname                      #Chinese name
├── otherCname                 #Alterantive Chinese name 
├── rooflevel 
├── bucsuid                    #Geoaddress
├── ename                      #English name 
├── otherEname                 #Alterantive English name 
├── x                          #Easting coordinate from Hong Kong 1980 Grid 
├── nameStatus 
├── y                          #Northing coordinate from Hong Kong 1980 Grid 
├── caddress                   #Chinese address     
├── baselevel 
│   ├── addressInfo 
│   │   ├── eaddress                    #English address
│   │   ├── distance 
│   │   ├── polyGeometry 
│   │   ├── cname                       #Chinese name
│   │   ├── eextrainfoArray 
│   │   ├── photo
│   │   ├── einfor
│   │   ├── eextrainfo 
│   │   │   ├── Frequency Band(s) In Use 
│   │   │   ├── Service Provider 
│   │   │   ├── District 
│   │   ├── caddress                    #Chinese address
│   │   ├── group 
│   │   ├── addressType                
│   │   └── faciType

```

## Idea

#### English Address segmentation 
 
Assumptions:
- The data was split with comma
- Addresses have no typos and mistake

The process to segment the English Addresses String :
1. Comma based splitting
Most of the time, in the address string the component will be separated by the comma "," then based on this property, we can split the address string into different segments and clusters.

2. Street pattern keyword-based segmentation
The street can be identified with the segmented string cluster with keywords and it follows the street number + street name format. This can be classified and segmented by keyword extraction for the street number and name.

3. District extraction
Most of the user input addresses may differ from the Hong Kong 18 district-defined district, then again by the keyword segment. that user-defined area can be matched with the standard of the HK18 district.

4. Regional classification
Last but not least, the whole of Hong Kong has been divided into three major segments, the Hong Kong Island, Kowloon, and New Territories, at the end of the input address segment, we can add the regional classification based on the previous district classification result.


#### Chinese Address segmentation 

Assumptions: 
- The data was grouped together in one unstructured string
- Address has no typo and mistake which generally follows the district + street pattern 
- Districts are inter-related to each other, such as the sub_district can be retrace the district and area 

The process to segment the Chinese Address String : 
1. NLP or keyword-based identification 
Segmenting and identifying those area, district, and sub_district keywords are important, due to those usually can be identifiable with pre-set string arrays. 

2. Street "number" splitting
The street component can be split out with the characteristic of the Chinese street name, the street name and number, and written just next to the district. Then, after the district has been segmented, the street name and number can be spotted with "號" this keyword.

3. Building classification 
The property of the Chinese written address is that the building is just next to the segmented street number, so split the street, and the remaining will be the building. 


## Roadmap

-  Reverse geocoding with LandsD API (Both Website and Python)
-  Direct geocoding formatting and data clearning (English and Chinese)
-  Direct geocoding quality assurence with similary checking 
-  Address typo or incorrect format similary suggestions (toward the ALS intelligence)

## Authors

- [@ottoykh](https://www.github.com/ottoykh) Yu Kai Him Otto 


## Related

Here are some related projects and usage packages. 

Some similar applcations 
- [GeoSpatialiser](https://tools.csdi.gov.hk/geospatialiser/)
- [Hong Kong Address Parser](https://github.com/g0vhk-io/HKAddressParser?tab=readme-ov-file )

NLP (Natural Language Processing) related 
- [jieba “结巴”中文分词：做最好的 Python 中文分词组件](https://github.com/fxsjy/jieba/tree/master?tab=readme-ov-file)

Geocoding related API 
- [CSDI Identify API](https://portal.csdi.gov.hk/csdi-webpage/apidoc/IdentifyAPI)
- [CSDI ALS/ Location Search API](https://portal.csdi.gov.hk/csdi-webpage/apidoc/LocationSearchAPI)

Geocoding reference dataset 
- [CSDI Place Name](https://portal.csdi.gov.hk/geoportal/?lang=en&datasetId=landsd_rcd_1648571595120_89752)
- [CSDI Street Name](https://portal.csdi.gov.hk/geoportal/?lang=en&datasetId=landsd_rcd_1648633077960_97785)
