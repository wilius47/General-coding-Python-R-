require(jsonlite)
require(dplyr)

urls <- c(
  'https://api-subvention-asso-prod.osc-secnum-fr1.scalingo.io/open-data/subventions/etablissement/40232029500023',
  'https://api-subvention-asso-prod.osc-secnum-fr1.scalingo.io/open-data/subventions/etablissement/44827436500015',
  'https://api-subvention-asso-prod.osc-secnum-fr1.scalingo.io/open-data/subventions/etablissement/51112577500011',
  'https://api-subvention-asso-prod.osc-secnum-fr1.scalingo.io/open-data/subventions/etablissement/49990111400011',
  'https://api-subvention-asso-prod.osc-secnum-fr1.scalingo.io/open-data/subventions/etablissement/40203621400011',
  'https://api-subvention-asso-prod.osc-secnum-fr1.scalingo.io/open-data/subventions/etablissement/78109164000024'
)

data_out=NULL
for(i in seq(1,length(urls))){
  # lire les infos
  tmp=jsonlite::fromJSON(urls[i])
  # ajouter à la suite /!\ créera de nouvelles colonnes si nécessaires
  data_out=bind_rows(data_out,tmp)
}