// 1. Parâmetros iniciais
var ano = 2023;

// 2. Paleta MapBiomas
var Palettes = require('users/mapbiomas/modules:Palettes.js');
var palette = Palettes.get('classification9');
var vis = {min: 0, max: 69, palette: palette};

// 3. Definir ROI (Porto Alegre)
var roi = ee.Geometry.Rectangle([-51.32, -30.20, -51.03, -29.91]);
Map.centerObject(roi, 11);
Map.addLayer(roi, {color: 'red'}, 'ROI - Porto Alegre');

// 4. Carregar imagem MapBiomas e selecionar banda do ano
var mapbiomas = ee.Image('projects/mapbiomas-public/assets/brazil/lulc/collection9/mapbiomas_collection90_integration_v1');
var uso = mapbiomas.select('classification_' + ano).clip(roi);
Map.addLayer(uso, vis, 'MapBiomas ' + ano);

// 5. Lista de cores seguindo a ordem crescente dos códigos
var coresOrdenadas = [
  '#1f8d49', // 3 - Formação Florestal
  '#7a5900', // 9 - Silvicultura
  '#519799', // 11 - Campo Alagado / Pantanoso
  '#d6bc74', // 12 - Formação Campestre
  '#ffefc3', // 21 - Mosaico de Usos
  '#d4271e', // 24 - Área Urbanizada
  '#db4d4f', // 25 - Outras Áreas Não Vegetadas
  '#2532e4', // 33 - Rio, Lago e Oceano
  '#f5b3c8', // 39 - Soja
  '#c71585', // 40 - Arroz
  '#f54ca9', // 41 - Outras Lavouras Temporárias
  '#02d659', // 49 - Restinga Arbórea
  '#ad5100'  // 50 - Restinga Herbácea
]; 

// 6. Gráfico com cores aplicadas
var chart = ui.Chart.image.byClass({
  image: ee.Image.pixelArea().addBands(uso),
  classBand: 'classification_' + ano,
  region: roi,
  reducer: ee.Reducer.sum(),
  scale: 30,
  classLabels: null,
  xLabels: null
})
.setChartType('BarChart')
.setOptions({
  title: 'Área por classe - Porto Alegre (' + ano + ')',
  hAxis: {title: 'Classe (código MapBiomas)'},
  vAxis: {title: 'Área (m²)'},
  legend: {position: 'none'},
  colors: coresOrdenadas
});

print(chart);
