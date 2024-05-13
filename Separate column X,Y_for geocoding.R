# Spécifier le chemin du fichier
file_path <- "D:/Users/rabehi/Documents/ACP/Corine Maitte/Carto prévilèges/Saint empire/Géolocalisation privilègesV2.csv"

# Charger les données depuis le fichier CSV
data <- read.csv2(file_path, header = TRUE)
data <- data[,-3]
# Afficher les premières lignes pour vérifier la structure des données
head(data)


# Séparation de la colonne "Lat..Long" en deux colonnes "Lat" et "Long"
coordinates <- strsplit(as.character(data$`Lat..Long`), ",")
coordinates <- t(sapply(coordinates, as.numeric))

# Création de nouvelles colonnes pour "Lat" et "Long"
data$Lat <- coordinates[,1]
data$Long <- coordinates[,2]

# Supprimer la colonne "Lat..Long" originale
data <- data[, -which(names(data) == "Lat..Long")]

# Affichage du nouveau data frame
print(data)

#enregistrer dans un nouveau fichier
write.csv(data, "D:/Users/rabehi/Documents/ACP/Corine Maitte/Carto prévilèges/Saint empire/Géolocalisation privilègesV3.csv")
