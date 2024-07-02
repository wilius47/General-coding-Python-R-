#it is a random dispersion of points which was superimposed on the same location
library(sf)
#ouvrir le fichier 
A <- st_read("path/file_point.shp")
B <- read.csv("Historical factories.csv")
# visualiser la table d'attribut
A


mapview
# ajouter un champs random (1,2,3,4........ N)
A1 <- cbind(A, "increment"=1:nrow(A))
A1$increment <- A1$increment/10

#Additionner les latitudes / logitudes avec le champs random
A1$latitude <- A1$latitude + A1$increment
A1$longitude <- A1$longitude + A1$increment

# Visualiser les nouvelles colonnes "latitude/longitude"
A1
#exporter sous CSV la nouvelle table d'attribut
write.csv(A1,"~/ACP/Frederic Saly-Giocanty/Données/CSV/A1.csv")

