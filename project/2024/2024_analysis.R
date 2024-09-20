library(dplyr)
library(ggplot2)
library(geosphere)

data <- read.csv("../data/clean/2024_troepen_EN.csv", header = TRUE, stringsAsFactors = FALSE)

# Filter out the shoigists "storm-z" unit
cleaned_data <- data %>%
  filter(Militaire.eenheid != 'shoigists "storm-z"')

# Filter the dataset for units that moved more than 100 km
units_moved_over_100 <- cleaned_data %>%
  filter(Totale.beweging..km. > 100) %>%
  distinct(Militaire.eenheid)

# Count the number of unique units that moved more than 100 km
count_units <- nrow(units_moved_over_100)

print(paste("Number of units that moved more than 100 km:", count_units))
print("Units that moved more than 100 km:")
print(units_moved_over_100$Militaire.eenheid)


# Remove non-date columns ('Militaire.eenheid', 'Totale.beweging..km.', 'Aantal.bewegingen')
non_date_cols <- c('Militaire.eenheid', 'Totale.beweging..km.', 'Aantal.bewegingen')
date_cols <- setdiff(names(cleaned_data), non_date_cols)

# Function to calculate the distance between two coordinates in kilometers
calculate_distance <- function(coord1, coord2) {
  if (is.na(coord1) || is.na(coord2) || coord1 == "" || coord2 == "") {
    return(0)  # No change if coordinates are missing
  }
  
  # Split the coordinates into latitude and longitude
  coord1 <- as.numeric(strsplit(coord1, ",")[[1]])
  coord2 <- as.numeric(strsplit(coord2, ",")[[1]])
  
  # Calculate the distance in kilometers using the Haversine formula
  dist <- distHaversine(c(coord1[2], coord1[1]), c(coord2[2], coord2[1])) / 1000  # Convert meters to kilometers
  
  return(dist)
}

# Function to determine if the location change is greater than 10 km
location_change <- function(coord1, coord2) {
  distance <- calculate_distance(coord1, coord2)
  return(distance > 10)  # Returns TRUE if the distance is greater than 10 km
}

changes_df <- data.frame(Date1 = character(), Date2 = character(), Changes = integer())

# Iterate over consecutive date columns and count location changes greater than 10 km
for (i in 1:(length(date_cols) - 1)) {
  date1 <- date_cols[i]
  date2 <- date_cols[i + 1]
  
  # Compare coordinates between two consecutive dates
  changes <- sum(mapply(location_change, cleaned_data[[date1]], cleaned_data[[date2]]))
  
  # Store the results
  changes_df <- rbind(changes_df, data.frame(Date1 = date1, Date2 = date2, Changes = changes))
}

# Find the two consecutive dates with the most location changes
max_changes <- changes_df %>%
  arrange(desc(Changes)) %>%
  slice(1)

print("The two dates with the most location changes are:")
print(max_changes)


# Plotting the line graph of location changes over time
changes_df$Date2 <- as.Date(gsub("^X", "", changes_df$Date2), format = "%Y.%m.%d")

# Plot the changes between dates
ggplot(changes_df, aes(x = Date2, y = Changes)) +
  geom_line() +
  labs(title = "Aantal Russische troepenverplaatsingen per maand (2024)", x = "", y = "Verplaatsingen (boven 10 km)") +
  scale_x_date(date_labels = "%Y-%m-%d", date_breaks = "1 month") + 
  theme_minimal() +
  theme(axis.text.x = element_text(angle = 90, hjust = 1))


# Correlation between movements and distance
correlation_analysis <- cleaned_data %>%
  summarise(correlation = cor(Totale.beweging..km., Aantal.bewegingen, use = "complete.obs"))

print(correlation_analysis)