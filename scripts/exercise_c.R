# Variable 1: bathrooms
# Variable 2: bedrooms
# Target variable: price

# Additional Variable for model 2: Number of registered voters

# Import data from SQLite database
# use SQL DBI library
library('DBI')

# create connection
con <- dbConnect(RSQLite::SQLite(), "../project_data.sqlite")

# Model 1)
# run sql query to fetch needed data
# exclude observations, which have 0 bathrooms and 0 bedrooms, since these observations won't help us for our explanation
# Price is displayed in thousands.
result <- dbGetQuery(con, 'select
    price / 1000 as price,
    bedroom,
    bathroom
from Sale_Announcement
    inner join House H on H.id = Sale_Announcement.house_id
where bedroom > 0 or bathroom > 0;')

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

# we want to find out, between which variables do we have the best correlation
cor(result)
# the best / biggest correlation (0.56) is between bath- and bedroom.
# While we want to explain the price over bath- and bedroom, this correlation does not help.
# The only thing we can say with this correlation, is that it seems, the more bedrooms a house have,
# the more bathrooms it needs, which makes sense.
# When it comes to the correlation which we are interested in, the correlation between price and bathroom (0.52)
# seems better / stronger than the correlation between price and bedroom and price (0.26).

# create model and show summary to analyze
model_1 <- lm(price ~ bedroom + bathroom, data = result)
coef(model_1)
# We can now see, how the prediction for the price looks like:
# -886.829 $ + 904.367 $/bathroom * bathroom + -66.371 $/bedroom * bedroom
# The prediction formula makes not really sense like this.
# It predicts, that you get even money back if you buy a house with one bed- and bathroom.

summary(model_1)  # R^2: 0.2703
# From the summary, we learn, that the adjusted R-squared is even higher than the ones from our single regression models.
# It seems, that we have a bit more accurate model than the single regression models.
# With this model, we can explain the prices to 27.03%. This is still not much and not satisfying.
# Standard Error: 2160 $ (in thousands). 95% of the prices lie between ± 2 * 2160


hist(model_1$residuals)
# With the look at the histogram over the residuals, we can say, that the model is not good enough.
# The distribution of the residuals looks strongly right skewed and not in a bell pattern.

qqnorm(model_1$residuals)
qqline(model_1$residuals)
# The residuals curve, 50% - 60% seem to be normal distributed
# lower 20% - 25% underestimate prices, upper 25% overestimate

plot(model_1$residuals~bedroom)
plot(model_1$residuals~bathroom)
# residuals vs. bedroom: variation seems very high between 7 and 12 bedrooms
# residuals vs. bathroom: variation seems to grow with number of bathrooms.
# While the underestimation seems to grow linear, the over estimation has no clear pattern

# Summary Model 1:
# Our analysis shows, that the model is not good enough.
# The histogram over the residuals shows clearly no bell pattern.
# Also, the formula for the partial regression indicates a bad model.
# Overall, the residuals from our model are not satisfying.


# Model 2)
# run the python script 'exercise_c_data_import.py' to import the data needed for model 2
library(reticulate)
use_virtualenv('../venv')
py_run_file('./exercise_c_data_import.py')

# get the data for the second model from the database. Now we should have voters as a variable available
# Voters is displayed in thousands.
result2 <- dbGetQuery(con, 'select
    price / 1000 as price,
    bedroom,
    bathroom,
    total_registered / 1000 as voters
from Sale_Announcement
    inner join House H on H.id = Sale_Announcement.house_id
    inner join County_to_City CtC on CtC.id = H.county_to_city_id
    inner join County C on C.id = CtC.county_id
    inner join Voter V on C.id = V.county_id
where bedroom > 0 or bathroom > 0;')

detach(result)
attach(result2)

plot(price~voters)
abline(lm(price~voters, data = result2))
# In the first sight on the plot price ~ voters, we cannot see any correlation between these two variables
# At this state we can predict, that including voters in our model won't help much for the model's quality

summary(lm(price~voters, data = result2))
# Even thought the benefit for our model is questionable, we can see some interesting things here:
# For example, we have a quite low residual value. We could assume, that the price is quite stable over all counties.
# The interesting thing we learn from the plot above, is that the smaller the county is,
# the smaller the standard deviation is

cor(result2)
# As predict in the first place, we can see that the correlation between price and voters is very low.
# It is even by far the lowest of all variables. It does not seem to have a clear positive impact on the new model.

model_2 <- lm(price ~ bedroom + bathroom + voters, data = result)
coef(model_2)
# Formula for Price prediction:
# -927.613 $ + 900.635 $/bathroom * bathroom + -66.605 $/bedroom * bedroom + 0.024 $/voter * voter

summary(model_2)
# We could improve the models residuals by 0.004%. It is, as predicted, not much.
# Now we can explain the prices to 27.07%
# Standard deviation: Is unchanged since model
hist(model_2$residuals)
# Also, our histogram over the residuals is not improved and still not with a bell pattern.

qqnorm(model_2$residuals)
qqline(model_2$residuals)

plot(model_2$residuals ~ bathroom)
plot(model_2$residuals ~ bedroom)
plot(model_2$residuals ~ voters)
# Also, the rest seems not to have changed much.

# Summary model 2:
# We could improve the model, but not by a significant value. It is still unsatisfying.