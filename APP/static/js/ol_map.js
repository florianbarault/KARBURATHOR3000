function initMap(data){

var map = new ol.Map({
        target: 'ol_localisation',
        layers: [
          new ol.layer.Tile({
            source: new ol.source.OSM()
          })
        ],
        view: new ol.View({
          center: ol.proj.fromLonLat([2.4682543369163965, 46.8643629949555]),
          zoom: 6
        })
      });


let tooltip = document.getElementById('tooltip');
let overlay = new ol.Overlay({
    element : tooltip,
    offset :[10, 0],
    positioning : 'bottomleft'
})

map.addOverlay(overlay);
map.on('pointermove', function(evt){
    displayTooltip(evt, overlay, map);
})

let style1 = new ol.style.Style({
    image: new ol.style.Icon({
        color: "black",
        src: "../static/library/openlayersv6.5.0/examples/data/dot.png",
        scale: 0.6
    }),
})

let tab=[];
for (a in data)
{

let lat= parseFloat(data[a][2]);
let lg= parseFloat(data[a][3]);

let F1 = new ol.Feature({
    geometry : new ol.geom.Point(ol.proj.fromLonLat([lg,lat])),
    type : "Point",
    latitude: lat,
    longitude :lg,
    oaci : data[a][0],
    nom : data[a][1]
});

F1.setStyle(style1);
tab.push(F1);
}

var vectorLayer = new ol.layer.Vector({
    source: new ol.source.Vector({
        features: tab,
    }),
    name : "Villes"
});

map.addLayer(vectorLayer);

var selectClick = new ol.interaction.Select({
  condition: ol.events.condition.click,
});

var liste_etapes = []

if (selectClick !== null) {
    map.addInteraction(selectClick);
    selectClick.on('select', function (e) {
        let feat = e.target.getFeatures().getArray()[0];
        liste_etapes.push([feat.get('latitude'),feat.get('longitude'),feat.get('nom')])
        console.log(liste_etapes)

    });
    }
    }