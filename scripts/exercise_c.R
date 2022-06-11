# Variable 1: bathrooms
# Variable 2: bedrooms
# Targed variable: price

# New Variable: Anzahl registrierte Wähler

library('DBI')
# TODO: change path to relative from script
con <- dbConnect(RSQLite::SQLite(), "~/Library/CloudStorage/OneDrive-BernerFachhochschule/wdda_gruppenarbeit/python_scripts/project_data.sqlite")

dbListTables(con)

result <- dbGetQuery(con, 'select
    price / 1000 as price,
    bedroom,
    bathroom
from Sale_Announcement
    inner join House H on H.id = Sale_Announcement.house_id
where bedroom > 0 or bathroom > 0')

attach(result)

hist(bathroom)
hist(bedroom)

mean(price)

mean(bedroom)
median(bedroom)

mean(bathroom)
median(bathroom)

table(bedroom)
table(bathroom)

plot(price~bathroom)
abline(lm(price~bathroom, data = result))
plot(price~bedroom)
abline(lm(price~bedroom, data = result))

summary(lm(price~bathroom, data = result))
summary(lm(price~bedroom, data = result))

model_1 <- lm(price~bathroom + bedroom, data = result)
summary(model_1)
