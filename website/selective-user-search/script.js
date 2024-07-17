var map = L.map("map").setView([22.326224233602904, 114.09416440034015], 11);

L.tileLayer(
  "https://mapapi.geodata.gov.hk/gs/api/v1.0.0/xyz/basemap/wgs84/{z}/{x}/{y}.png"
).addTo(map);

L.tileLayer(
  "https://mapapi.geodata.gov.hk/gs/api/v1.0.0/xyz/label/hk/en/wgs84/{z}/{x}/{y}.png",
  {
    attribution:
      '<a href="https://api.portal.hkmapservice.gov.hk/disclaimer" target="_blank" class="copyrightDiv">&copy;Map information from Lands Department </a><img src="https://api.hkmapservice.gov.hk/mapapi/landsdlogo.jpg" height=20></img>',
    maxZoom: 18
  }
).addTo(map);

var drawControl = new L.Control.Draw({
  draw: {
    polyline: false,
    polygon: false,
    circle: false,
    marker: false,
    rectangle: true
  }
});
map.addControl(drawControl);

var fetchedData = [];

map.on(L.Draw.Event.CREATED, function (event) {
  var layer = event.layer;
  var bounds = layer.getBounds();
  var bbox = [
    bounds.getWest(),
    bounds.getSouth(),
    bounds.getEast(),
    bounds.getNorth()
  ];
  var id = document.getElementById("id").value;
  var layerName = document.getElementById("layer").value;

  fetchData(bbox, id, layerName);
  map.removeLayer(layer);
});

document.getElementById("fetchBtn").addEventListener("click", function () {
  var id = document.getElementById("id").value;
  var layerName = document.getElementById("layer").value;
  var bounds = map.getBounds();
  var bbox = [
    bounds.getWest(),
    bounds.getSouth(),
    bounds.getEast(),
    bounds.getNorth()
  ];
  fetchData(bbox, id, layerName);
});

function fetchData(bbox, id, layerName) {
  document.getElementById("loading").style.display = "block";

  var apiUrl = `https://api.csdi.gov.hk/apim/dataquery/api/?id=${id}&layer=${layerName}&bbox-crs=WGS84&bbox=${bbox.join(
    ","
  )}&limit=500&offset=0`;

  fetch(apiUrl)
    .then((response) => response.json())
    .then((data) => {
      map.eachLayer(function (layer) {
        if (layer instanceof L.Marker) {
          map.removeLayer(layer);
        }
      });

      fetchedData = data.features;

      if (fetchedData.length === 0) {
        alert("No data found for the selected area.");
        return;
      }

      fetchedData.forEach((feature) => {
        var coordinates = feature.geometry.coordinates;
        var popupContent = "<b>Attributes:</b><br>";

        for (const [key, value] of Object.entries(feature.properties)) {
          popupContent += `${key}: ${value}<br>`;
        }

        var marker = L.marker([coordinates[1], coordinates[0]], {
          icon: L.divIcon({
            className: "marker-icon",
            iconSize: [10, 10]
          })
        }).addTo(map);
        marker.bindPopup(popupContent);
      });

      renderDataTable();

      var group = new L.featureGroup(
        fetchedData.map((feature) => {
          return L.marker([
            feature.geometry.coordinates[1],
            feature.geometry.coordinates[0]
          ]);
        })
      );
      map.fitBounds(group.getBounds());
    })
    .catch((error) => console.error("Error fetching data:", error))
    .finally(() => {
      document.getElementById("loading").style.display = "none";
    });
}

function renderDataTable() {
  var tableContainer = document.getElementById("table-container");

  tableContainer.innerHTML = "";
  var table = document.createElement("table");
  table.classList.add("data-table");
  var headerRow = table.insertRow();
  for (const key in fetchedData[0].properties) {
    var headerCell = document.createElement("th");
    headerCell.textContent = key;
    headerRow.appendChild(headerCell);
  }

  fetchedData.forEach((feature, index) => {
    var row = table.insertRow();
    for (const key in feature.properties) {
      var cell = row.insertCell();
      cell.textContent = feature.properties[key];
    }
    row.addEventListener("click", () => {
      const coordinates = feature.geometry.coordinates;
      map.panTo([coordinates[1], coordinates[0]]);
    });
  });
  tableContainer.appendChild(table);
}

function downloadData() {
  if (fetchedData.length === 0) {
    alert("No data to download.");
    return;
  }

  const keys = [
    "Latitude",
    "Longitude",
    ...Object.keys(fetchedData[0].properties)
  ];

  let csvData = keys.join(",") + "\n"; // Header row with all keys
  fetchedData.forEach(function (feature) {
    const coordinates = feature.geometry.coordinates;
    const values = [
      coordinates[1],
      coordinates[0],
      ...keys.slice(2).map((key) => {
        const value = feature.properties[key] || ""; // Handle missing values
        return `"${value.toString().replace(/"/g, '""')}"`;
      })
    ];
    csvData += values.join(",") + "\n";
  });

  const downloadLink = document.createElement("a");
  downloadLink.setAttribute(
    "href",
    "data:text/csv;charset=utf-8," + encodeURIComponent(csvData)
  );
  downloadLink.setAttribute("download", "filter_data.csv");
  downloadLink.style.display = "none";

  document.body.appendChild(downloadLink);
  downloadLink.click();
  document.body.removeChild(downloadLink);
}