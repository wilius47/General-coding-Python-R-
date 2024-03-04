from qgis.core import QgsApplication, QgsVectorLayer, QgsRasterLayer, QgsVectorFileWriter, QgsGeometry, QgsMapLayerRegistry
from qgis.analysis import QgsRasterCalculator, QgsRasterCalculatorEntry

# Initialisation de l'application QGIS
QgsApplication.setPrefixPath("/chemin/vers/QGIS", True)
qgs = QgsApplication([], False)
qgs.initQgis()

# Chemins vers les fichiers
chemin_raster_scan = "/chemin/vers/scan.tif"
chemin_shapefile_route = "/chemin/vers/routes.shp"
chemin_shapefile_foret = "/chemin/vers/foret.shp"
chemin_shapefile_agric = "/chemin/vers/agric.shp"
chemin_shapefile_r = "/chemin/vers/shapefile_r.shp"
chemin_shapefile_cercles = "/chemin/vers/cercles.shp"

# Charger le raster "Scan"
raster_scan = QgsRasterLayer(chemin_raster_scan, "Scan")
if not raster_scan.isValid():
    print("Erreur: Impossible de charger le raster.")
else:
    print("Raster chargé avec succès.")

# Filtrer le raster selon la bande rouge > 200
entries = []
red_band_entry = QgsRasterCalculatorEntry()
red_band_entry.ref = 'raster@1'
red_band_entry.raster = raster_scan
red_band_entry.bandNumber = 1
entries.append(red_band_entry)

expression = 'raster@1 > 200'
calc = QgsRasterCalculator(expression, '/chemin/vers/scan_filtre.tif', 'GTiff', raster_scan.extent(), raster_scan.width(), raster_scan.height(), entries)
calc.processCalculation()

# Charger le fichier shapefile "route"
layer_route = QgsVectorLayer(chemin_shapefile_route, "Routes", "ogr")
if not layer_route.isValid():
    print("Erreur: Impossible de charger le shapefile des routes.")
else:
    print("Shapefile des routes chargé avec succès.")

# Créer une zone tampon (10 mètres) autour du shapefile "route"
buffer_distance = 10  # Distance de la zone tampon en mètres
buffer_layer = layer_route.buffer(buffer_distance, -1)

# Enregistrer la zone tampon en tant que shapefile
buffer_shapefile_path = '/chemin/vers/routes_buffer.shp'
QgsVectorFileWriter.writeAsVectorFormat(buffer_layer, buffer_shapefile_path, 'utf-8', layer_route.crs(), 'ESRI Shapefile')

# Charger le fichier shapefile "R"
layer_r = QgsVectorLayer(chemin_shapefile_r, "R", "ogr")
if not layer_r.isValid():
    print("Erreur: Impossible de charger le shapefile R.")
else:
    print("Shapefile R chargé avec succès.")

# Découper le raster filtré sur l'emprise du shapefile "R"
output_raster_r_decoupe = '/chemin/vers/scan_filtre_r_decoupe.tif'
processing.run("gdal:cliprasterbyextent",
               {'INPUT': '/chemin/vers/scan_filtre.tif',
                'PROJWIN': layer_r.extent().asWktPolygon(),
                'OUTPUT': output_raster_r_decoupe})

# Découper le raster filtré sur l'emprise et le contour du shapefile "foret"
output_raster_foret_decoupe = '/chemin/vers/scan_filtre_foret_decoupe.tif'
processing.run("gdal:cliprasterbymasklayer",
               {'INPUT': '/chemin/vers/scan_filtre.tif',
                'MASK': chemin_shapefile_foret,
                'OUTPUT': output_raster_foret_decoupe})

# Découper le raster filtré sur l'emprise et le contour du shapefile "agric"
output_raster_agric_decoupe = '/chemin/vers/scan_filtre_agric_decoupe.tif'
processing.run("gdal:cliprasterbymasklayer",
               {'INPUT': '/chemin/vers/scan_filtre.tif',
                'MASK': chemin_shapefile_agric,
                'OUTPUT': output_raster_agric_decoupe})

# Découper le raster filtré sur l'emprise et le contour du shapefile "cercles"
output_raster_cercles_decoupe = '/chemin/vers/scan_filtre_cercles_decoupe.tif'
processing.run("gdal:cliprasterbymasklayer",
               {'INPUT': '/chemin/vers/scan_filtre.tif',
                'MASK': chemin_shapefile_cercles,
                'OUTPUT': output_raster_cercles_decoupe})

# Fermer l'application QGIS
qgs.exitQgis()
