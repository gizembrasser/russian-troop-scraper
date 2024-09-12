library(leaflet)
library(tidyr)
library(dplyr)

data <- read.csv("../data/merged/2022-2024_troepen.csv", header = TRUE)

# Filter out the shoigists "storm-z" unit
cleaned_data <- data %>%
  filter(Militaire.eenheid != 'shoigists "storm-z"')

# List of ten military units to plot
selected_units <- c(
  "64th Separate Motorized Rifle Brigade", 
  "56th Air Assault Regiment", 
  "Piatnashka Battalion", 
  "155th Separate Brigade of Marines", 
  "200th Separate Motor Rifle Brigade", 
  "488th Motor Rifle Regiment (from the composition of 144 MRD)", 
  "71st Guards Motorized Rifle Regiment", 
  "38th Separate Motorized Rifle Brigade", 
  "810th Naval Infantry Brigade",
  "11th Separate Assault Brigade"
)

# Filter the data to only include the selected military units
filtered_data <- cleaned_data %>%
  filter(Militaire.eenheid %in% selected_units)

# Reshape all columns (except 'Militaire eenheid') from wide to long format
data_long <- filtered_data %>%
  pivot_longer(cols = -Militaire.eenheid, names_to = "Date", values_to = "Coordinates")

# Separate the 'Coordinates' column into 'Latitude' and 'Longitude'
data_long <- data_long %>%
  separate(Coordinates, into = c("Latitude", "Longitude"), sep = ",", convert = TRUE)

# Convert Latitude and Longitude to numeric
data_long$Latitude <- as.numeric(data_long$Latitude)
data_long$Longitude <- as.numeric(data_long$Longitude)

# Get unique military units (in this case, just the selected 10)
unique_units <- unique(data_long$Militaire.eenheid)

# Create a color palette with distinct colors for the selected military units
colors <- colorFactor(palette = "Set1", domain = unique_units)

# Initialize a leaflet map
mymap <- leaflet() %>%
  addTiles()  # Add default OpenStreetMap tiles

# Loop through each selected military unit and add markers to the map
for (unit in unique_units) {
  unit_data <- data_long %>%
    filter(Militaire.eenheid == unit)  # Filter for the specific military unit
  
  # Add markers for the current unit with a unique color
  mymap <- mymap %>%
    addCircleMarkers(
      data = unit_data,
      lng = ~Longitude, lat = ~Latitude,
      popup = ~paste("Military unit:", unit, "<br>Date:", Date, "<br>Latitude:", Latitude, "<br>Longitude:", Longitude),
      radius = 5, color = ~colors(unit), fillOpacity = 0.7,
      group = unit
    )
}

# Center the map around the mean of all points
mymap <- mymap %>%
  setView(lng = mean(data_long$Longitude, na.rm = TRUE), lat = mean(data_long$Latitude, na.rm = TRUE), zoom = 6)

# Display the map
mymap
