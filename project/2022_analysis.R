library(leaflet)
library(tidyr)
library(dplyr)

data <- read.csv("../data/clean/2022_troepen_EN.csv", header = TRUE)

# Filter out the shoigists "storm-z" unit
cleaned_data <- data %>%
  filter(Militaire.eenheid != 'shoigists "storm-z"')

head(cleaned_data)

# Get the 10 units that travelled the most
top_units <- cleaned_data %>%
  distinct(Militaire.eenheid) %>%
  slice(1:10) %>%
  pull(Militaire.eenheid)

filtered_data <- cleaned_data %>%
  filter(Militaire.eenheid %in% top_units)

# Reshape all columns from wide to long format
data_long <- filtered_data %>%
  pivot_longer(cols = -c(Militaire.eenheid, Totale.beweging..km.), names_to = "Date", values_to = "Coordinates")

# Separate the 'Coordinates' column into 'Latitude' and 'Longitude'
data_long <- data_long %>%
  separate(Coordinates, into = c("Latitude", "Longitude"), sep = ",", convert = TRUE)

# Convert Latitude and Longitude to numeric
data_long$Latitude <- as.numeric(data_long$Latitude)
data_long$Longitude <- as.numeric(data_long$Longitude)

# Create a color palette with distinct colors for each military unit
colors <- colorFactor(palette = "Set1", domain = data_long$Militaire.eenheid)

# Create a leaflet map and plot data for the 10 military units, each with a unique color
leaflet(data_long) %>%
  addTiles() %>%  # Add default OpenStreetMap tiles
  addCircleMarkers(
    lng = ~Longitude, lat = ~Latitude, 
    popup = ~paste("Military unit:", Militaire.eenheid, "<br>Date:", Date, "<br>Latitude:", Latitude, "<br>Longitude:", Longitude),
    radius = 5, color = ~colors(Militaire.eenheid), fillOpacity = 0.7
  ) %>%
  setView(lng = mean(data_long$Longitude, na.rm = TRUE), lat = mean(data_long$Latitude, na.rm = TRUE), zoom = 6)  # Center the map