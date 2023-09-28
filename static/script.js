const MAPBOX_ACCESS_TOKEN = 'pk.eyJ1IjoiY29sZTIxMjEyMTEyMzIzIiwiYSI6ImNsbjNvcmRjZDBocnEycmsyY213NWFoeWEifQ.j7nzi8oH39HQVjRZcwCyWw';
const MAPBOX_MAP_STYLE = 'mapbox://styles/mapbox/streets-v12';


mapboxgl.accessToken = MAPBOX_ACCESS_TOKEN;
var map = new mapboxgl.Map({
    container: 'map',
    style: MAPBOX_MAP_STYLE,
    zoom: 2.5,
    center: [-95, 30]

});
map.getCanvas().style.cursor = 'pointer';
var line_ids = []
var marker_ids = []
packet_info = {} // for links data popup


function load_router_on_map(router_geojson_data)
{
    const marker = document.createElement('div');
    marker.className = 'marker_css';

    var marker_id = new mapboxgl.Marker(marker)
        .setLngLat(router_geojson_data.data.geometry.coordinates)
        .setPopup(
            new mapboxgl.Popup({ offset: 25 })
            .setHTML(
                `<h3>${router_geojson_data.data.properties.name}</h3><p>${router_geojson_data.data.properties.description}</p>`
            )
        )
        .addTo(map);

    marker_ids.push(marker_id);
}

function load_link_on_map(link_geojson_data) 
{
    nickname = link_geojson_data.data.properties.name
    line_ids.push(nickname)
    packet_info[nickname] = `<h3>${nickname}</h3><p>${link_geojson_data.data.properties.description}</p>`
    map.addSource(nickname, link_geojson_data);
    map.addLayer({
        'id': nickname,
        'type': 'line',
        'source': nickname,
        'layout': {
            'line-join': 'round',
            'line-cap': 'round'
        },
        'paint': {
            'line-color': 'rgb(141, 150, 158)',
            'line-width': 3
        }
    })

    // Set a popup for the line
    map.on('click', nickname, function (e) {
        nickname = e.features[0].layer.id;
        new mapboxgl.Popup()
            .setLngLat(e.lngLat)
            .setHTML(packet_info[nickname])
            .addTo(map);
        
    });
}

function remove_links_and_routers_from_map() {
    for (let i = 0; i < line_ids.length; i++) {
        map.removeLayer(line_ids[i])
        map.removeSource(line_ids[i])
    }
    for (let i = 0; i < marker_ids.length; i++) {
        marker_ids[i].remove();
    }

    line_ids = [];
    marker_ids = [];
}









// document.getElementById("traceroute_button").addEventListener("submit", function(event) {
//     event.preventDefault();
//     const inputIP = document.getElementById("destination_url_or_ip").value;
//     traceRoute(inputIP);
// });

