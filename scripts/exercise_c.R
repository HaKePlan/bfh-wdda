# Variable 1: bathrooms
# Variable 2: bedrooms
# Target variable: price

# New Variable: Anzahl registrierte Wähler

# Import data from SQLite database
# use SQL DBI library
library('DBI')

# create connection
con <- dbConnect(RSQLite::SQLite(), "../project_data.sqlite")

# run sql query to fetch needed data
# exclude observations, which have 0 bathrooms and 0 bedrooms, since this observations wont help us for our explanation
result <- dbGetQuery(con, 'select
    price / 1000 as price,
    bedroom,
    bathroom
from Sale_Announcement
    inner join House H on H.id = Sale_Announcement.house_id
where bedroom > 0 or bathroom > 0')

# attach and show overview for all variables
attach(result)
pairs(result)

# show a plot for each variable with price to understand our correlation
plot(price ~ bathroom)
abline(lm(price ~ bathroom, data = result))
plot(price ~ bedroom)
abline(lm(price ~ bedroom, data = result))

# Show the result for both variables as single regression model with price
summary(lm(price ~ bathroom, data = result))  # R^2: 0.269
summary(lm(price ~ bedroom, data = result))  # R^2: 0.06729
# While looking at the residuals of each, we can understand, that the residuals of price ~ bedroom much better is.

# Model 1)
# we want to find out, between which variables do we have de best correlation
cor(result)
# the best / biggest correlation (0.56) is between bath- and bedroom.
# While we want to explain the price over bath- and bedroom, this correlation does not help.
# The only thing we can say with this correlation, is that it seems, the more bedrooms a house have,
# the more bathrooms it needs, which makes sense.
# When it comes to the correlation which we are interested in, the correlation between price and bathroom (0.52)
# seems to be better / stronger than the correlation between price and bedroom and price (0.26).

# create model and show summary to analyze
model_1 <- lm(price ~ bedroom + bathroom, data = result)
coef(model_1)
# We can now see, how the prediction for the price looks like:
# -886.829 $ + 904.367 $/bathroom * bathroom + -66.371 $/bedroom * bedroom
# The prediction formula makes not really sense like this.
# It predicts, that you get even money back if you buy a house with one bed- and bathroom.

summary(model_1)  # R^2: 0.2703
# From the summary we learn, that the adjusted R-squared is even higher than the ones from our single regression models.
# It seems, that the single regression model price ~ bedroom is the best we have.
# Taking bathroom in our model (multiple regression model) makes it not better


hist(model_1$residuals)
# With the look at the histogram over the residuals, we can say, that the model is not really good.
# The distribution of the residuals looks strongly right skewed and not in a bell pattern.

qqnorm(model_1$residuals)
qqline(model_1$residuals)
# The residuals curve, 50% - 60% seem to be normal distributed
# lower 20% - 25% underestimate prices, upper 25% overestimate

plot(model_1$residuals~bedroom)
plot(model_1$residuals~bathroom)
# residuals vs. bedroom: variation seems to very high between 7 to 12 bedrooms
# residuals vs. bathroom: variation seems to grow with number of bathrooms.
# While the underestimation seems to grow linear, the over estimation hase no clear pattern

# Summary Model 1:
# Our analysis shows, that the model is not really good.
# The histogramm over the residuals shows clearly no bell pattern.
# Also the formula for the partial regression indicates a bad model.
# Overall, it would be better to create two single regression models (price ~ bathroom and price ~ bedroom)
# instead of a multiple regression model. The residuals for both single regression models are better than the
# residuals for the multiple regression model.


# Model 2)
