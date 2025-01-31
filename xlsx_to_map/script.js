let jsonData = [];
let map;
let hiddenValues = new Set();

document.getElementById('fileInput').addEventListener('change', function(event) {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            const data = new Uint8Array(e.target.result);
            const workbook = XLSX.read(data, { type: 'array' });
            const sheetName = workbook.SheetNames[0];
            const sheet = workbook.Sheets[sheetName];
            jsonData = XLSX.utils.sheet_to_json(sheet, { raw: false, dateNF: 'YYYY-MM-DD' });

            // Convertir fechas
            jsonData.forEach(row => {
                for (const key in row) {
                    if (typeof row[key] === 'number' && XLSX.SSF.is_date_code(row[key])) {
                        row[key] = convertExcelDate(row[key]).toISOString().split('T')[0]; // Formato YYYY-MM-DD
                    }
                }
            });

            // Update row count
            document.getElementById('rowCount').textContent = `Filas introducidas: ${jsonData.length}`;

            populateColorColumnOptions(jsonData);
            initializeMap(jsonData);
            updateMap();
        };
        reader.readAsArrayBuffer(file);
    }
});

document.getElementById('colorColumn').addEventListener('change', function() {
    updateMap();
});

function populateColorColumnOptions(data) {
    const colorColumnSelect = document.getElementById('colorColumn');
    colorColumnSelect.innerHTML = '';

    const columns = Object.keys(data[0]);
    columns.forEach(col => {
        const option = document.createElement('option');
        option.value = col;
        option.textContent = col;
        colorColumnSelect.appendChild(option);
    });
}

function initializeMap(data) {
    const firstCoord = data[0];
    map = L.map('map').setView([firstCoord.coord_y, firstCoord.coord_x], 12);

    const osm = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);

    const gMaps = L.tileLayer.wms("http://www.google.cn/maps/vt?lyrs=s@189&gl=cn&x={x}&y={y}&z={z}", {
        layers: '0',
        format: 'image/png',
        transparent: true,
        attribution: "Google Maps"
    });

    const baseMaps = { "OpenStreetMap": osm, "Google Maps": gMaps };

    L.control.layers(baseMaps).addTo(map);
}

function updateMap() {
    const colorColumn = document.getElementById('colorColumn').value;
    const colors = generateColors(jsonData, colorColumn);
    const counts = countValues(jsonData, colorColumn);

    if (map) {
        map.eachLayer(function(layer) {
            if (layer instanceof L.Circle) {
                map.removeLayer(layer);
            }
        });

        jsonData.forEach(row => {
            if (!hiddenValues.has(row[colorColumn])) {
                const color = colors[row[colorColumn]];
                const popupText = Object.keys(row).map(key => `<tr><th>${key}</th><td>${row[key]}</td></tr>`).join('');
                const circle = L.circle([row.coord_y, row.coord_x], {
                    color: color,
                    fillColor: color,
                    fillOpacity: 0.5,
                    radius: 50,
                    value: row[colorColumn]
                }).addTo(map);

                circle.on('click', function() {
                    const infoTable = document.getElementById('infoTable').getElementsByTagName('tbody')[0];
                    infoTable.innerHTML = popupText;
                });
            }
        });

        updateLegend(colors, counts);
    }
}

function generateColors(data, column) {
    const uniqueValues = [...new Set(data.map(row => row[column]))];
    const colorPalette = generateColorPalette(uniqueValues.length);
    const colors = {};

    uniqueValues.forEach((value, index) => {
        colors[value] = colorPalette[index];
    });

    return colors;
}

function generateColorPalette(size) {
    const colors = [];
    for (let i = 0; i < size; i++) {
        const color = `hsl(${Math.floor(360 * i / size)}, 100%, 50%)`;
        colors.push(color);
    }
    return colors;
}

function countValues(data, column) {
    const counts = {};
    data.forEach(row => {
        const value = row[column];
        if (counts[value]) {
            counts[value]++;
        } else {
            counts[value] = 1;
        }
    });
    return counts;
}

function updateLegend(colors, counts) {
    const legend = document.getElementById('legend');
    legend.innerHTML = '';

    for (const [value, color] of Object.entries(colors)) {
        const count = counts[value];
        const legendItem = document.createElement('div');
        legendItem.className = 'legend-item';

        const colorBox = document.createElement('div');
        colorBox.className = 'legend-color';
        colorBox.style.backgroundColor = color;

        const text = document.createElement('span');
        text.textContent = `${value}: ${count} vectores`;

        // Create a hide/show button
        const toggleButton = document.createElement('button');
        toggleButton.textContent = hiddenValues.has(value) ? 'Mostrar' : 'Ocultar';
        toggleButton.style.marginLeft = '10px';
        toggleButton.onclick = function() {
            toggleValue(value);
        };

        legendItem.appendChild(colorBox);
        legendItem.appendChild(text);
        legendItem.appendChild(toggleButton);
        legend.appendChild(legendItem);
    }
}

function toggleValue(value) {
    if (hiddenValues.has(value)) {
        hiddenValues.delete(value);
    } else {
        hiddenValues.add(value);
    }
    updateMap();
}

function convertExcelDate(excelDate) {
    const date = XLSX.SSF.parse_date_code(excelDate);
    return new Date(Date.UTC(date.y, date.m - 1, date.d));
}