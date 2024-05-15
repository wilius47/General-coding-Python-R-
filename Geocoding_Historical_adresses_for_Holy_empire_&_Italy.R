# Charger les bibliothèques nécessaires
library(rgdal)
library(rgeos)
library(sp)
install.packages("rgdal")
library(rgdal)

# Charger le package sf
library(sf)

# Définir la fonction de géocodage inversé
reverse_geocode <- function(lat, lon) {
  url <- paste0("https://nominatim.openstreetmap.org/reverse?format=json&lat=", lat, "&lon=", lon)
  result <- jsonlite::fromJSON(url)
  return(result$display_name)
}

#Saint Empire
# Géocodage inversé des coordonnées et création de la colonne "address"
data$address <- mapply(reverse_geocode, data$Lat, data$Long)

# Créer un sf object à partir des coordonnées géocodées
spatial_points <- st_as_sf(data, coords = c("Long", "Lat"), crs = 4326)

# Enregistrer le sf object sous forme de shapefile
st_write(spatial_points, "D:/Users/rabehi/Documents/ACP/Corine Maitte/Carto prévilèges/Saint empire/St_empire.shp")


#Italie_piémont
data$grLieO
# Installer les packages nécessaires
install.packages("readxl")
install.packages("dplyr")
install.packages("tidygeocoder")
install.packages("sf")
install.packages("tidyr") 
library(tidyr)
library(readxl)
library(dplyr)
library(tidygeocoder)
library(sf)
#,"grLiAcS", "grLiAcP"
# Lire le fichier Excel
file_path <- "D:/Users/rabehi/Documents/ACP/Corine Maitte/Carto prévilèges/Italie/Piemont/Potable Turin Piémont.xlsx"
sheet_name <- "Graines"  # Nom de la feuille si nécessaire
data <- read_excel(file_path, sheet = sheet_name)


# Créer une adresse complète pour le géocodage
data <- data %>%
  unite("full_address", c("code commune", "code comuni", "grLiAcPo", "grLiAcSu","grLiAcCh" , "grLieO"), sep = ", ", remove = FALSE) %>%
  geocode(address = full_address, method = 'osm')  # Utilise OpenStreetMap pour le géocodage

#Eliminer les valeurs vides (non géocodées)
data_geocoded <- data %>%
  filter(!is.na(lat) & !is.na(long))

# Convertir en objet spatial
data_sf <- st_as_sf(data_geocoded, coords = c("long", "lat"), crs = 4326)  # Coordonnées en WGS84

# Sauvegarder en tant que Shapefile
st_write(data_sf, "D:/Users/rabehi/Documents/ACP/Corine Maitte/Carto prévilèges/Italie/Piemont/Turin_Piémont2.shp")

# Vérification du Shapefile
new_data_sf <- st_read("path/to/save/shapefile.shp")
print(new_data_sf)
