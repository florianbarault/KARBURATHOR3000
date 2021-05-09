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


//let F1 = new ol.Feature({
//    geometry : new ol.geom.Point(ol.proj.fromLonLat([1.09516,49.8787]))
//    type : "Point"
//});
//
//let style1 = new ol.style.Style({
//    image: new ol.style.Icone({
//        color: "black",
//        src: "../static/library/openlayersv6.5.0/examples/data/dot.png",
//        scale: 0.6
//    }),
//})
//
//F1.setStyle(style1);
//
//var vectorLayer = new ol.layer.Vector({
//    source: new ol.source.Vector({
//        features: [F1],
//    }),
//    name : "Villes"
//});
//
//map.addLayer(vectorLayer);