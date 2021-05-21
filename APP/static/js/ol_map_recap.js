function initMap(coord_map){

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


let style1 = new ol.style.Style({
    image: new ol.style.Icon({
        color: "black",
        src: "../static/library/openlayersv6.5.0/examples/data/dot.png",
        scale: 0.6
    }),
})
let style2 = new ol.style.Style({
    image: new ol.style.Icon({
        color: "red",
        src: "../static/library/openlayersv6.5.0/examples/data/dot.png",
        scale: 0.6
    }),
})


let tab_villes=[];
for (var i = 0; i < coord_map.length; i += 2) {

let lat= parseFloat(coord_map[i][0]);
let lg= parseFloat(coord_map[i][1]);

let F1 = new ol.Feature({
    geometry : new ol.geom.Point(ol.proj.fromLonLat([lg,lat])),
    type : "Point",
    latitude: lat,
    longitude :lg
});

F1.setStyle(style1);
tab_villes.push(F1);
}


let tab_deg=[];
for (var i = 1; i < coord_map.length; i += 2) {

let lat= parseFloat(coord_map[i][0]);
let lg= parseFloat(coord_map[i][1]);

let F2 = new ol.Feature({
    geometry : new ol.geom.Point(ol.proj.fromLonLat([lg,lat])),
    type : "Point",
    latitude: lat,
    longitude :lg
});

F2.setStyle(style2);
tab_deg.push(F2);
}


var vectorLayer = new ol.layer.Vector({
    source: new ol.source.Vector({
        features: tab_villes
    }),
    name : "Villes"

});
var vectorLayer2 = new ol.layer.Vector({
    source: new ol.source.Vector({
        features: tab_deg
    }),
    name : "Villes2"

});


map.addLayer(vectorLayer);
map.addLayer(vectorLayer2);


//let Fligne = new ol.Feature({
//    geometry: new ol.geom.LineString(tab_villes),
//    name: "trajet"
//});
//Fligne.getGeometry().transform('EPSG:4326','EPSG:3857');
//
//let style3 = new ol.style.Style({
//    stroke: new ol.style.Stroke ({
//        color: 'blue',
//        width:2
//    })
//});
//
//var lignes = new ol.layer.Vector({
//    source: new ol.source.Vector({
//        features: [Fligne]
//    }),
//    name : "trajet"
//});
//
//
//map.addLayer(lignes);

}