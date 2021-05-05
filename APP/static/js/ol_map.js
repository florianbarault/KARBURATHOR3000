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