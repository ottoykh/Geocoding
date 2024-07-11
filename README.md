
# Geocoding 

The package is a proof of concept to adopt different CSDI APIs to enhance the geocoding services in Hong Kong. 

Mainly there are two directions on the Geocoding in Hong Kong, 
- Direct, from address string to coordinate (x,y or easting, northing),
- Reverse, from coordinate to address string. 

This package allows different end-use to adopt those APIs with fewer lines of code to reach a codeless API fetching and data interchange for Hong Kong geospatial data. 

> Try out our webapp [geoaddress2xy](https://ottoykh.github.io/Geocoding/website/reverse-geocoding/index.html)  !

## Features
> Most of the feature will be developed in this late-July. 
- Address formatting with NLP (Natural language processing) and segmentation 
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
Reverse geocoding is a process to convert the spatial coordinates into address, it is important for the documentation Due to the coordinates from the map, it is hard to be identified on the ground without surveying and field measurements. So the address is one of the mediums that allows us to describe the geospatial location. Moreover, the Geoaddress has become a more popular and user-friendly way to store spatial coordinates, then with reverse geocoding batch processing can be applied for mass conversion and applications.  

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

#### Direct Geocoding with ALS API (From Address to Spatial Refernce Coodinates)
Direct geocoding is the process of transforming the address to spatial reference coordinates it can enable more in-depth spatial analysis to be applied with the georeferenced address to point-based spatial data. Still some of the challenges on the input format may be different and not in the ALS recognizable input, therefore this package has added a data formatting, cleaning and validation process to enhance the direct geocoding service in Hong Kong.
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
Most of the time, the Chinese addresses are grouped and fused. Therefore, it would be better that we classify the address into segments, format , and reconstruct the address string in the ALS recognizable input. In this step, the NLP can be adopted for the Chinese language strings. 

```python 
from Geocoding.NLP.zhSeg import segment_text_file
# input path directory
file = '/content/sample.txt'

#  Segment text file will return decompose the chinese address into sub-sets
segmented = segment_text_file(file)
display(segmented)
```
Input : 香港薄扶林道５４號地下至２樓

Output : 香港\薄扶林道\５\４\號\地下\至\２\樓




Still Developing ... 

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
- Addresses have no typo and mistake

Process to segment the English Addresses String :
1. Comma based splitting
At most of the time, in the address string the component will be separated by the comma "," then based on this property, we can split the address string into different segments and clusters.

2. Street pattern keyword based segmentation
The street can be identified with the segmented string cluster with keywords and it follows the street number + street name format. This can be classified and segmented by keyword extraction for the street number and name.

3. District extraction
Most of the user input addresses may differ from the Hong Kong 18 district-defined district, then again by the keyword segment. that user-defined area can be matched with the standard of the HK18 district.

4. Regional classification
Last but not least, the whole of Hong Kong has been divided into three major segments, the Hong Kong Island, Kowloon, and New Territories, at the end of the input address segment, we can add the regional classification based on the previous district classification result.


#### Chinese Address segmentation 

Ongoing development 
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

