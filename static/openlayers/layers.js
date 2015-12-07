function layers() {
    
    var source = new ol.source.Vector({
        url: 'data/grid01.json',
        format: new ol.format.GeoJSON()
    });

    var clusterSource = new ol.source.Cluster({
        distance: 40,
        source: source
    });

    var styleCache = {};
    var clusters = new ol.layer.Vector({
        source: clusterSource,
        style: function (feature, resolution) {
            var size = feature.get('features').length;
            var style = styleCache[size];
            if (!style) {
                style = [new ol.style.Style({
                        image: new ol.style.Circle({
                            radius: 10,
                            stroke: new ol.style.Stroke({
                                color: '#fff'
                            }),
                            fill: new ol.style.Fill({
                                color: '#1abc9c'
                            })
                        }),
                        text: new ol.style.Text({
                            text: size.toString(),
                            fill: new ol.style.Fill({
                                color: '#fff'
                            })
                        })
                    })];
                styleCache[size] = style;
            }
            return style;
        }
    });

    var raster = new ol.layer.Tile({
        source: new ol.source.MapQuest({layer: 'sat'})
    });

    var raw = new ol.layer.Vector({
        source: source
    });

    var map = new ol.Map({
        layers: [
            new ol.layer.Tile({
                source: new ol.source.Stamen({
                    layer: 'toner'
                })
            }),
            new ol.layer.Tile({
                source: new ol.source.Stamen({
                    layer: 'terrain-labels'
                })
            }),
            clusters
                    //raster, clusters
        ],
        target: 'map',
        view: new ol.View({
            center: ol.proj.transform(
                    [9.182932, 48.775846], 'EPSG:4326', 'EPSG:3857'),
            zoom: 12
        })
    });
};
