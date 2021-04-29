import MVT from 'ol/format/MVT';
import TileQueue from 'ol/TileQueue';
import VectorTileLayer from 'ol/layer/VectorTile';
import VectorTileSource from 'ol/source/VectorTile';
import stringify from 'json-stringify-safe';
import styleFunction from 'ol-mapbox-style/dist/stylefunction';
import {Projection} from 'ol/proj';
import {inView} from 'ol/layer/Layer';
import {getTilePriority as tilePriorityFunction} from 'ol/TileQueue';

/** @type {any} */
const worker = self;

let frameState, pixelRatio, rendererTransform;
const canvas = new OffscreenCanvas(1, 1);
// OffscreenCanvas does not have a style, so we mock it
canvas.style = {};
const context = canvas.getContext('2d');

const sources = {
  landcover: new VectorTileSource({
    maxZoom: 9,
    format: new MVT(),
    url:
      'https://api.maptiler.com/tiles/landcover/{z}/{x}/{y}.pbf?key=Get your own API key at https://www.maptiler.com/cloud/',
  }),
  contours: new VectorTileSource({
    minZoom: 9,
    maxZoom: 14,
    format: new MVT(),
    url:
      'https://api.maptiler.com/tiles/contours/{z}/{x}/{y}.pbf?key=Get your own API key at https://www.maptiler.com/cloud/',
  }),
  openmaptiles: new VectorTileSource({
    format: new MVT(),
    maxZoom: 14,
    url:
      'https://api.maptiler.com/tiles/v3/{z}/{x}/{y}.pbf?key=Get your own API key at https://www.maptiler.com/cloud/',
  }),
};
const layers = [];

// Font replacement so we do not need to load web fonts in the worker
function getFont(font) {
  return font[0].replace('Noto Sans', 'serif').replace('Roboto', 'sans-serif');
}

function loadStyles() {
  const styleUrl =
    'https://api.maptiler.com/maps/topo/style.json?key=Get your own API key at https://www.maptiler.com/cloud/';

  fetch(styleUrl)
    .then((data) => data.json())
    .then((styleJson) => {
      const buckets = [];
      let currentSource;
      styleJson.layers.forEach((layer) => {
        if (!layer.source) {
          return;
        }
        if (currentSource !== layer.source) {
          currentSource = layer.source;
          buckets.push({
            source: layer.source,
            layers: [],
          });
        }
        buckets[buckets.length - 1].layers.push(layer.id);
      });

      const spriteUrl =
        styleJson.sprite + (pixelRatio > 1 ? '@2x' : '') + '.json';
      const spriteImageUrl =
        styleJson.sprite + (pixelRatio > 1 ? '@2x' : '') + '.png';
      fetch(spriteUrl)
        .then((data) => data.json())
        .then((spriteJson) => {
          buckets.forEach((bucket) => {
            const source = sources[bucket.source];
            if (!source) {
              return;
            }
            const layer = new VectorTileLayer({
              declutter: true,
              source,
              minZoom: source.getTileGrid().getMinZoom(),
            });
            layer.getRenderer().useContainer = function (target, transform) {
              this.containerReused = this.getLayer() !== layers[0];
              this.canvas = canvas;
              this.context = context;
              this.container = {
                firstElementChild: canvas,
              };
              rendererTransform = transform;
            };
            styleFunction(
              layer,
              styleJson,
              bucket.layers,
              undefined,
              spriteJson,
              spriteImageUrl,
              getFont
            );
            layers.push(layer);
          });
          worker.postMessage({action: 'requestRender'});
        });
    });
}

// Minimal map-like functionality for rendering

const tileQueue = new TileQueue(
  (tile, tileSourceKey, tileCenter, tileResolution) =>
    tilePriorityFunction(
      frameState,
      tile,
      tileSourceKey,
      tileCenter,
      tileResolution
    ),
  () => worker.postMessage({action: 'requestRender'})
);

const maxTotalLoading = 8;
const maxNewLoads = 2;

worker.addEventListener('message', (event) => {
  if (event.data.action !== 'render') {
    return;
  }
  frameState = event.data.frameState;
  if (!pixelRatio) {
    pixelRatio = frameState.pixelRatio;
    loadStyles();
  }
  frameState.tileQueue = tileQueue;
  frameState.viewState.projection.__proto__ = Projection.prototype;
  layers.forEach((layer) => {
    if (inView(layer.getLayerState(), frameState.viewState)) {
      const renderer = layer.getRenderer();
      renderer.renderFrame(frameState, canvas);
    }
  });
  layers.forEach((layer) => layer.renderDeclutter(frameState));
  if (tileQueue.getTilesLoading() < maxTotalLoading) {
    tileQueue.reprioritize();
    tileQueue.loadMoreTiles(maxTotalLoading, maxNewLoads);
  }
  const imageData = canvas.transferToImageBitmap();
  worker.postMessage(
    {
      action: 'rendered',
      imageData: imageData,
      transform: rendererTransform,
      frameState: JSON.parse(stringify(frameState)),
    },
    [imageData]
  );
});
