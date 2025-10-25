# Script para visualizar biomas e UCs federais em mapa interativo
import geopandas as gpd
import folium
import mapclassify

# Caminhos dos arquivos
path_biomas = 'asset/lm_bioma_250.shp'
path_ucs = 'asset/limites_ucs_federais_21072025.shp'

# Carregar os dados
gdf_biomas = gpd.read_file(path_biomas)
gdf_ucs = gpd.read_file(path_ucs)

# Verificar colunas
print('Colunas Biomas:', gdf_biomas.columns)
print('Colunas UCs:', gdf_ucs.columns)

# Garantir que ambos estão no mesmo CRS

if gdf_biomas.crs != gdf_ucs.crs:
    gdf_ucs = gdf_ucs.to_crs(gdf_biomas.crs)

# Visualização interativa usando geopandas.explore com backend folium
# Primeiro, plota os biomas como base
m_biomas = gdf_biomas.explore(
    column='Bioma',
    legend=False,
    cmap='Pastel1',
    legend_kwds={"title": "Biomas"},
    legend_loc='topright',
    style_kwds={"fillOpacity": 1, "weight": 1},
    tooltip=['Bioma'],
    tiles='CartoDB positron',
    name='Biomas',
    show=False,
    backend="folium"
)

# Agora adiciona as UCs por GrupoUC
m_ucs = gdf_ucs.explore(
    m=m_biomas,
    column='GrupoUC',
    legend=True,
    legend_kwds={"title": "Grupo UC"},
    legend_loc='bottomright',
    style_kwds={"fillOpacity": 0.5, "weight": 1},
    tooltip=['NomeUC', 'GrupoUC'],
    name='Unidades de Conservação',
    show=True,
    backend="folium"
)

# Adicionar LayerControl manualmente (explore pode não adicionar)
folium.LayerControl(collapsed=False).add_to(m_ucs)

# Salvar o mapa
m_ucs.save('mapa_interativo.html')
print('Mapa salvo como mapa_interativo.html (usando geopandas.explore + folium)')
