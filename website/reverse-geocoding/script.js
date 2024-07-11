var map = L.map("map").setView([22.4, 114.105], 12);
var tileLayer = L.tileLayer(
  "https://mapapi.geodata.gov.hk/gs/api/v1.0.0/xyz/basemap/wgs84/{z}/{x}/{y}.png",
  {
    attribution: ""
  }
).addTo(map);
var labeledLayer = L.tileLayer(
  "https://mapapi.geodata.gov.hk/gs/api/v1.0.0/xyz/label/hk/en/wgs84/{z}/{x}/{y}.png",
  {
    attribution: "&copy; Map information from Lands Department",
    maxZoom: 18
  }
).addTo(map);

var markers = L.markerClusterGroup().addTo(map);

var hk1980Crs =
  "+proj=tmerc +lat_0=22.31213333333334 +lon_0=114.1785555555556 +k=1 +x_0=836694.05 +y_0=819069.8 +ellps=intl +towgs84=-162.619,-276.959,-161.764,0.067753,-2.24365,-1.15883,-1.09425 +units=m +no_defs";
var wgs84Crs = "+proj=longlat +datum=WGS84 +no_defs";

function processGeoaddress(geoaddress) {
  const digits = geoaddress.slice(0, 10);
  const x = parseInt(digits.slice(0, 5)) + 800000;
  const y = parseInt(digits.slice(5)) + 800000;
  return [x, y];
}

async function fetchAPI(x, y) {
  const maxAttempts = 3; // Maximum number of retry attempts
  let attempt = 0;

  while (attempt < maxAttempts) {
    try {
      const url = `https://geodata.gov.hk/gs/api/v1.0.0/identify?x=${x}&y=${y}`;
      const response = await fetch(url);

      if (!response.ok) {
        throw new Error(
          `Failed to fetch data: ${response.status} - ${response.statusText}`
        );
      }

      const data = await response.json();

      if (data.error || data.results.length === 0) {
        throw new Error("API request failed or returned no results");
      }
      return data;
    } catch (error) {
      console.error("Error fetching data:", error);

      await new Promise((resolve) => setTimeout(resolve, 2000));
    }

    attempt++;
  }

  console.error(
    `Exceeded maximum retry attempts (${maxAttempts}). Unable to fetch data.`
  );
  return { error: "Unable to fetch data" };
}

async function processGeoaddresses() {
  const input = document.getElementById("input").value;
  const geoaddresses = input.split("\n").filter((line) => line.trim() !== "");
  const results = [];
  const progressBar = document.getElementById("progress-bar-fill");
  const progressText = document.getElementById("progress-text");
  for (let i = 0; i < geoaddresses.length; i++) {
    const geoaddress = geoaddresses[i].trim();
    const [x, y] = processGeoaddress(geoaddress);
    const data = await fetchAPI(x, y);
    if (data.results && data.results.length > 0) {
      const addressInfo = data.results[0].addressInfo[0];
      const result = {
        geoaddress,
        x,
        y,
        eaddress: addressInfo.eaddress || "",
        caddress: addressInfo.caddress || "",
        roofLevel: addressInfo.roofLevel || "",
        baseLevel: addressInfo.baseLevel || ""
      };
      results.push(result);
      plotMarker(result, i);
      updateResultsTable(result, i);
    }
    const progress = ((i + 1) / geoaddresses.length) * 100;
    progressBar.style.width = `${progress}%`;
    progressText.textContent = `Processing: ${i + 1}/${geoaddresses.length}`;
    await new Promise((resolve) => setTimeout(resolve, 1));
  }
}

function updateResultsTable(result, index) {
  const table = document.getElementById("results");
  if (index === 0) {
    table.innerHTML = "";
    const headers = Object.keys(result);
    const headerRow = table.insertRow();
    headers.forEach((header) => {
      const th = document.createElement("th");
      th.textContent = header;
      headerRow.appendChild(th);
    });
  }
  const row = table.insertRow();
  row.setAttribute("data-index", index);
  Object.values(result).forEach((value) => {
    const cell = row.insertCell();
    cell.textContent = value;
  });
  row.addEventListener("click", function () {
    const marker = markers.getLayers()[this.getAttribute("data-index")];
    map.setView(marker.getLatLng(), 16);
    marker.openPopup();

    window.scrollTo({ top: 0, behavior: "instant" });
  });
}

function plotMarker(result, index) {
  const [lng, lat] = convertToLatLng(result.x, result.y);
  const marker = L.marker([lat, lng]).bindPopup(`
    Geoaddress: ${result.geoaddress}<br>
    English Address: ${result.eaddress}<br>
    Chinese address: ${result.caddress}<br>
    Roof Level: ${result.roofLevel}<br>
    Base Level: ${result.baseLevel}
  `);
  markers.addLayer(marker);
  if (index === 0) {
    map.fitBounds(markers.getBounds());
  }
}

function convertToLatLng(x, y) {
  return proj4(hk1980Crs, wgs84Crs, [x, y]);
}

function exportToCSV() {
  const results = collectResults();
  let csvContent = "data:text/csv;charset=utf-8,";

  csvContent += Object.keys(results[0]).join(",") + "\n";

  results.forEach((result) => {
    let row = Object.values(result).join(",");
    csvContent += row + "\n";
  });

  const encodedUri = encodeURI(csvContent);
  const link = document.createElement("a");
  link.setAttribute("href", encodedUri);
  link.setAttribute("download", "results.csv");
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
}

function exportToExcel() {
  const results = collectResults();
  const worksheet = XLSX.utils.json_to_sheet(results);
  const workbook = XLSX.utils.book_new();
  XLSX.utils.book_append_sheet(workbook, worksheet, "Results");
  XLSX.writeFile(workbook, "results.xlsx");
}

function exportToTxt() {
  const results = collectResults();
  let txtContent = "";

  txtContent += Object.keys(results[0]).join("\t") + "\n";

  // Add rows
  results.forEach((result) => {
    let row = Object.values(result).join("\t");
    txtContent += row + "\n";
  });

  const blob = new Blob([txtContent], { type: "text/plain;charset=utf-8" });
  saveAs(blob, "results.txt");
}

function collectResults() {
  const table = document.getElementById("results");
  const headers = Array.from(table.rows[0].cells).map(
    (cell) => cell.textContent
  );
  const results = [];

  for (let i = 1; i < table.rows.length; i++) {
    const row = table.rows[i];
    const result = {};
    headers.forEach((header, index) => {
      result[header] = row.cells[index].textContent;
    });
    results.push(result);
  }

  return results;
}