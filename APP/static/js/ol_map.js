function initMap(data){

var map = new ol.Map({
        target: 'ol_localisation',
        layers: [
          new ol.layer.Tile({
            source: new ol.source.OSM()
          })
        ],
        view: new ol.View({
          center: ol.proj.fromLonLat([2.4682543369163965, 46.3]),
          zoom: 5.6
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
    nom : "Villes"
});

map.addLayer(vectorLayer);

var selectClick = new ol.interaction.Select({
  condition: ol.events.condition.click,
});

etapes = []
etape = []
coord_etape =[]
compteur = 0

if (selectClick !== null) {
    map.addInteraction(selectClick);
    selectClick.on('select', function (e) {
        let feat = e.target.getFeatures().getArray()[0];
        etape.push(feat.get('oaci'))
        coord_etape.push([feat.get('latitude'), feat.get('longitude')])
        
        if (etape.length == 1){
          document.getElementById('aide').innerHTML = "Cliquer sur l'aérodrome d'arrivé ou d'étape"

        }
        
        if (etape.length == 2) {

          document.getElementById('aide').innerHTML = "Cliquer sur l'aérodrome de dégagement"

        }
        
        if (etape.length == 3){

          
          if (compteur == 0) {
            etapes.push(etape[0])
          }
          
          compteur = compteur +1
          tracerEtape(coord_etape)

          etapes.push(etape[1], etape[2])
          var ligne = document.createElement("tr")
          var col0 = document.createElement("td")
          col0.innerHTML = "<label>{0}</label>".format(compteur.toString(), etape[0].toString(), etape[1].toString(), etape[2].toString())
          ligne.appendChild(col0)
          var col1 = document.createElement("td")
          col1.innerHTML = "<label>{1}</label>".format(compteur.toString(), etape[0].toString(), etape[1].toString(), etape[2].toString())
          ligne.appendChild(col1)
          var col2 = document.createElement("td")
          col2.innerHTML = "<label>{2}</label>".format(compteur.toString(), etape[0].toString(), etape[1].toString(), etape[2].toString())
          ligne.appendChild(col2)
          var col3 = document.createElement("td")
          col3.innerHTML = "<label>{3}</label>".format(compteur.toString(), etape[0].toString(), etape[1].toString(), etape[2].toString())
          ligne.appendChild(col3)

          document.getElementById('etapes').appendChild(ligne)

          document.getElementById("liste_vol").innerHTML = etapes.toString()
          document.getElementById('aide').innerHTML = "Cliquer sur l'aérodrome d'arrivé ou d'étape"


          etape = [etape[1]]
        }
    });
    }

function tracerEtape(coord_map) {
    

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

let coord_villes=[]
let tab_villes=[];
coord_villes.push(coord_map[0])
console.log(coord_map)
for (var i = 1; i < coord_map.length; i= i+2) {
  console.log(coord_map.length)
  console.log(i)

coord_villes.push(coord_map[i]);
let lat= parseFloat(coord_map[i][1]);
let lg= parseFloat(coord_map[i][0]);

let F1 = new ol.Feature({
    geometry : new ol.geom.Point(ol.proj.fromLonLat([lg,lat])),
    type : "Point",
    latitude: lat,
    longitude :lg
});

F1.setStyle(style1);
tab_villes.push(F1);
}
console.log(coord_villes)


let tab_deg=[];
for (var i = 2; i < coord_map.length; i += 2) {

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

coord_villes.map(function (l){
    return l.reverse();
});

let Fligne = new ol.Feature({
    geometry: new ol.geom.LineString(coord_villes),
    name: "trajet"
});
Fligne.getGeometry().transform('EPSG:4326','EPSG:3857');

let style3 = new ol.style.Style({
    stroke: new ol.style.Stroke ({
        color: 'blue',
        width:2
    })
});

var lignes = new ol.layer.Vector({
    source: new ol.source.Vector({
        features: [Fligne]
    }),
    name : "trajet"
});

map.addLayer(lignes);
coord_villes.map(function (l){
  return l.reverse();
});

}


String.prototype.format = function() {
  a = this;
  for (k in arguments) {
    a = a.replace("{" + k + "}", arguments[k])
  }
  return a
}

}