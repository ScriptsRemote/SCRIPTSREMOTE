import geopandas as gpd
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import inset_axes, mark_inset

# Caminhos dos arquivos
bioma_fp = 'asset/lm_bioma_250.shp'
ucs_fp = 'asset/limites_ucs_federais_21072025.shp'

# Abrir os GeoDataFrames
gdf_bioma = gpd.read_file(bioma_fp)
gdf_ucs = gpd.read_file(ucs_fp)

# Filtrar apenas o Bioma Cerrado
gdf_cerrado = gdf_bioma[gdf_bioma['Bioma'] == 'Cerrado']

# Garantir que ambos estão no mesmo CRS
gdf_ucs = gdf_ucs.to_crs(gdf_cerrado.crs)

# Selecionar UCs que estão no Bioma Cerrado (interseção espacial)
gdf_ucs_cerrado = gpd.sjoin(gdf_ucs, gdf_cerrado, how='inner', predicate='intersects')

# Plotar
fig, ax = plt.subplots(figsize=(10, 8))
gdf_bioma.plot(ax=ax, color='lightgrey', edgecolor='grey')
gdf_cerrado.plot(ax=ax, color='yellowgreen', edgecolor='green')
gdf_ucs_cerrado.plot(ax=ax, color='none', edgecolor='red', linewidth=1.2)

# Legendas customizadas
import matplotlib.patches as mpatches
legend_patches = [
	mpatches.Patch(facecolor='lightgrey', edgecolor='grey', label='Biomas'),
	mpatches.Patch(facecolor='yellowgreen', edgecolor='green', label='Cerrado'),
	mpatches.Patch(facecolor='none', edgecolor='red', label='UCs no Cerrado', linewidth=1.2)
]
ax.legend(handles=legend_patches, loc='upper right')

ax.set_title('Unidades de Conservação no Bioma Cerrado', fontsize=14)
ax.grid(True)


# Adicionar inset (zoom) no Cerrado inteiro
if not gdf_cerrado.empty:
	minx, miny, maxx, maxy = gdf_cerrado.total_bounds
	# Adiciona um pequeno buffer para o zoom
	dx = (maxx - minx) * 0.05
	dy = (maxy - miny) * 0.05
	minx -= dx
	maxx += dx
	miny -= dy
	maxy += dy
	axins = inset_axes(ax, width="30%", height="30%", loc='lower right', borderpad=2)
	gdf_bioma.plot(ax=axins, color='lightgrey', edgecolor='grey')
	gdf_cerrado.plot(ax=axins, color='yellowgreen', edgecolor='green')
	gdf_ucs_cerrado.plot(ax=axins, color='none', edgecolor='red', linewidth=1.2)
	axins.set_xlim(minx, maxx)
	axins.set_ylim(miny, maxy)
	axins.set_xticks([])
	axins.set_yticks([])
	axins.set_title('Zoom no Cerrado', fontsize=10)
	mark_inset(ax, axins, loc1=2, loc2=4, fc="none", ec="0.5")

# Adicionar latitude e longitude nos eixos do mapa principal
ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')

plt.tight_layout()
plt.savefig('mapa_ucs_cerrado.png', dpi=300, bbox_inches='tight')
plt.show()
