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
compteur = 0

if (selectClick !== null) {
    map.addInteraction(selectClick);
    selectClick.on('select', function (e) {
        let feat = e.target.getFeatures().getArray()[0];
        etape.push(feat.get('oaci'))
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
          console.log(etapes)
        }
    });
    }
    }

String.prototype.format = function() {
  a = this;
  for (k in arguments) {
    a = a.replace("{" + k + "}", arguments[k])
  }
  return a
}

function removeEtapes() {
  etapes = []
  console.log(etapes)
  etape = []
  compteur = 0
  document.getElementById("etapes").innerHTML = '<tbody id="etapes" class="tbl-content"></tbody>'
  document.getElementById("liste_vol").innerHTML = ""
  document.getElementById('aide').innerHTML = "Cliquer sur un aérodrome de départ"
 }