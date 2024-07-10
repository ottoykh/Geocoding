# Geocoding 

The package is a proof of concept to adopt different CSDI APIs to enhance the geocoding services in Hong Kong. 

Mainly there are two directions on the Geocoding in Hong Kong, 
(1) Direct, from address string to coordinate (x,y or easting, northing). On the other hand,
(2) Reverse, from coordinate to address string. This package allows different end-use to adopt those APIs with fewer lines of code to reach a codeless API fetching and data interchange for Hong Kong geospatial data. 

## Usage/Examples
Reverse Geocoding with IdentifyAPI
```python
from reverse import geoaddress2xy
input_file = '/content/try.txt'
results = geoaddress2xy.process_batch(input_file)
table = results.to_html(index=True)
display(HTML(table)) 
```

