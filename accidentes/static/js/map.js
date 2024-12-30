document.addEventListener('DOMContentLoaded', function() {
    var map = L.map('map').setView([39.527588190897795, 2.5073717858419684], 12);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);

    function updateCoordinates(lat, lng) {
        document.getElementById('coordenadas').value = `${lat}, ${lng}`;
    }

    map.on('click', function(e) {
        var lat = e.latlng.lat;
        var lng = e.latlng.lng;
        updateCoordinates(lat, lng);

        L.marker([lat, lng]).addTo(map)
            .bindPopup(`Accidente en ${lat}, ${lng}`)
            .openPopup();
    });

    var accidentForm = document.getElementById('accident-form');
    if (accidentForm) {
        accidentForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            var formData = new FormData(this);
            var data = {};
            formData.forEach((value, key) => { data[key] = value; });

            try {
                let response = await fetch('/api/accidentes', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                });

                let result = await response.json();
                if (result.status === 'success') {
                    alert('Accidente agregado exitosamente');
                    addAccidentToTable(result);
                    addAccidentToMap(result);
                    this.reset();
                } else {
                    alert(result.message || 'Error al agregar accidente');
                }
            } catch (error) {
                console.error('Error:', error);
                alert('Error al procesar la solicitud');
            }
        });
    }

    // Función para agregar un marcador al mapa
function addMarker(lat, lng, accidente) {
    const popupContent = `
        <b>Accidente</b><br>
        Fecha: ${accidente.fecha}<br>
        Hora: ${accidente.hora}<br>
        Ubicación: ${accidente.ubicacion}<br>
        Gravedad: ${accidente.gravedad}<br>
        Tipo de Vehículo: ${accidente.tipo_vehiculos}<br>
        Víctimas: ${accidente.victimas}
    `;
    const marker = L.marker([lat, lng])
        .addTo(markersGroup) // Agregar al grupo de marcadores
        .bindPopup(popupContent);

    console.log("Marcador agregado:", lat, lng, accidente);
}
    async function loadAccidents() {
        try {
            // Realizar la solicitud a la API para obtener los datos
            let response = await fetch('/api/accidentes');
            let data = await response.json();
    
            // Validar que la respuesta sea un array
            if (!Array.isArray(data)) {
                console.error('La respuesta de la API no es un array:', data);
                return;
            }
    
            // Recorrer cada accidente y representarlo en el mapa
            data.forEach(accidente => {
                // Verificar que las coordenadas existan y sean válidas
                if (accidente.coordenadas && Array.isArray(accidente.coordenadas) && accidente.coordenadas.length === 2) {
                    const [lat, lng] = accidente.coordenadas;
                    if (!isNaN(lat) && !isNaN(lng)) {
                        addMarker(lat, lng, accidente);
                    } else {
                        console.error('Coordenadas no válidas:', accidente.coordenadas);
                    }
                } else {
                    console.error('El accidente no tiene coordenadas válidas:', accidente);
                }
            });
    
            // Ajustar la vista del mapa para incluir todos los marcadores
            if (markersGroup.getLayers().length > 0) {
                map.fitBounds(markersGroup.getBounds());
            }
        } catch (error) {
            console.error('Error al cargar los accidentes:', error);
        }
    }
    


    function addAccidentToTable(accidente) {
        var table = document.getElementById('accident-table').getElementsByTagName('tbody')[0];
        var newRow = table.insertRow();
        newRow.innerHTML = `
            <td>${accidente.id}</td>
            <td>${accidente.fecha}</td>
            <td>${accidente.hora}</td>
            <td>${accidente.ubicacion}</td>
            <td>${accidente.gravedad}</td>
            <td>${accidente.tipo_vehiculos}</td>
            <td>${accidente.victimas}</td>
            <td>${accidente.lat}, ${accidente.lng}</td>
        `;
    }

    function addAccidentToMap(accidente) {
        var popupContent = `
            <b>Accidente</b><br>
            Fecha: ${accidente.fecha}<br>
            Hora: ${accidente.hora}<br>
            Ubicación: ${accidente.ubicacion}<br>
            Gravedad: ${accidente.gravedad}<br>
            Tipo de Vehículo: ${accidente.tipo_vehiculos}<br>
            Víctimas: ${accidente.victimas}
        `;
        L.marker([accidente.lat, accidente.lng]).addTo(map).bindPopup(popupContent);
    }
    loadAccidents();
});
