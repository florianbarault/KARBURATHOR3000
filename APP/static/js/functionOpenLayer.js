function move_marker(marker, line, stepMarker)
{
    var features=marker.getSource().getFeatures();
    var featureToUpdate=features[0];

    var step = 0;
    var key = setInterval( function() { // la fonction suivante s'execute toutes les 70ms
    if (step < stepMarker)
    {
        step++;
        let coord = line.getCoordinateAt(step/stepMarker); // retourne les coordonnées géographiques sur un point de la trajectoire
        let newPoint=new ol.geom.Point(ol.proj.fromLonLat(coord)); // formatage des coordonnées géographiques
        featureToUpdate.setGeometry(newPoint); // deplacement du marker
    } else {
        clearInterval(key); // fin du déplacement
        }

    }, 70);
}




function displayTooltip(evt, overlay, map) {

    var pixel = evt.pixel;
    var feature = map.forEachFeatureAtPixel(pixel, function(feature) {
        return feature;
    });
    tooltip.style.display = feature ? '' : 'none';
    if (feature && feature.get('nom')) {  //uniquement pour les marker de type Point
        overlay.setPosition(evt.coordinate);
        tooltip.innerHTML = feature.get('nom'); //Affichage de la description du marker
    }
}
