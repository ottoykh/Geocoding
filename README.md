
# Geocoding 

The package is a proof of concept to adopt different CSDI APIs to enhance the geocoding services in Hong Kong. 

Mainly there are two directions on the Geocoding in Hong Kong, 
(1) Direct, from address string to coordinate (x,y or easting, northing). On the other hand,
(2) Reverse, from coordinate to address string. This package allows different end-use to adopt those APIs with fewer lines of code to reach a codeless API fetching and data interchange for Hong Kong geospatial data. 




## Installation

Simple Download and Plug in the Package with the following steps
```python
!git clone https://github.com/ottoykh/Geocoding.git
```
```python
cd /content/Geocoding       # Sample from Colab eviornment, for other IDE to find the downloaded directory 
```
## Usage
Reverse Geocoding with IdentifyAPI (From Geoaddress to Address)
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

Direct Geocoding with ALS API (From Address to Spatial Refernce Coodinates)
```python 
from direct import formatter
from Geocoding.direct.clean import clean_data

#input path directory
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

## Roadmap

-  Reverse geocoding with LandsD API (Both Website and Python)
-  Direct geocoding formatting and data clearning 
-  Direct geocoding quality assurence with similary checking 
-  Address typo or incorrect format similary suggestions (toward the ALS intelligence)
