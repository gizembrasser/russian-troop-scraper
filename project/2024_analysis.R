library(leaflet)
library(tidyr)
library(dplyr)

data <- read.csv("../data/clean/2024_troepen_EN.csv", header = TRUE)

# Filter out the shoigists "storm-z" unit
cleaned_data <- data %>%
  filter(Militaire.eenheid != 'shoigists "storm-z"')

# Reshape all columns from wide to long format
data_long <- cleaned_data %>%
  pivot_longer(cols = -c(Militaire.eenheid, Totale.beweging..km.), names_to = "Date", values_to = "Coordinates")

# Separate the 'Coordinates' column into 'Latitude' and 'Longitude'
data_long <- data_long %>%
  separate(Coordinates, into = c("Latitude", "Longitude"), sep = ",", convert = TRUE)

# Convert Latitude and Longitude to numeric
data_long$Latitude <- as.numeric(data_long$Latitude)
data_long$Longitude <- as.numeric(data_long$Longitude)

# Filter the data for a specific military unit
unit_name <- '238th Artillery Brigade'
unit_data <- data_long %>%
  filter(Militaire.eenheid == unit_name)

# Create a leaflet map and plot the unit's data on it
leaflet(unit_data) %>%
  addTiles() %>%  # Add default OpenStreetMap tiles
  addCircleMarkers(
    lng = ~Longitude, lat = ~Latitude, 
    popup = ~paste("Military unit:", unit_name, "<br>Date:", Date, "<br>Latitude:", Latitude, "<br>Longitude:", Longitude),
    radius = 5, color = "blue", fillOpacity = 0.7
  ) %>%
  setView(lng = mean(unit_data$Longitude, na.rm = TRUE), lat = mean(unit_data$Latitude, na.rm = TRUE), zoom = 6)  # Center the map