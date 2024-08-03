import pandas

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import LinearRegression

from sklearn import linear_model
from sklearn.preprocessing import PolynomialFeatures

from sklearn.preprocessing import StandardScaler
import numpy

import csv
import helper

df = pandas.read_csv("individual-performances.csv")
df = df.drop(columns = ["firstName", "lastName", "countryName", "place", "competitionId"])
print("Shape:", df.shape)
print("\nFeatures:", df.columns)

df.loc[df.shape[0]] = [14693572,297748,"FRA","1996-02-21","2024-08-11","The XXXIII Olympic Games","FRA",10229534,"2:29:11"]
print("Shape:", df.shape)
print('tail \n', df.tail(3))
seeded_row = df.tail(1).to_dict(orient='records')[0]
print('Seeded row: \n', seeded_row)

originalCountryCodes = df['countryCode'].tolist()
df['countryCode'] = df['countryCode'].astype('category').cat.codes
codedCountryCodes = df['countryCode'].tolist()
countryCodesMap = helper.mergeListsToMap(originalCountryCodes, codedCountryCodes)

originalCompetitions = df['competition'].tolist()
df['competition'] = df['competition'].astype('category').cat.codes
codedCompetitions = df['competition'].tolist()
competitionsMap = helper.mergeListsToMap(originalCompetitions, codedCompetitions)

originalVenueCountries = df['venueCountry'].tolist()
df['venueCountry'] = df['venueCountry'].astype('category').cat.codes
codedVenueCountries = df['venueCountry'].tolist()
venueCountriesMap = helper.mergeListsToMap(originalVenueCountries, codedVenueCountries)

df['birthDate'] = numpy.array([dob for dob in df['birthDate']], dtype='datetime64')
df['birthDate'] = df['birthDate'].values.astype('float64')

df['performanceDate'] = numpy.array([dob for dob in df['performanceDate']], dtype='datetime64')
df['performanceDate'] = df['performanceDate'].values.astype('float64')

racetimes = []
for raceTime in df['timeResult']:
    hours, minutes, seconds = raceTime.split(':')
    racetimes.append(numpy.timedelta64(hours, 'h') + numpy.timedelta64(minutes, 'm') + numpy.timedelta64(seconds, 's'))
df['timeResult'] = racetimes

transformed_seeded_row = df.tail(1)
df.drop(transformed_seeded_row.index, inplace=True)
#print('last 5 values of df\n', df.tail(5))

X = df[df.columns[:-1]]
y = df[df.columns[-1]]

# printing first 5 rows of feature matrix
print("\nFeature matrix:\n", X.head())

# printing first 5 values of response vector
print("\nResponse vector:\n", y[0:5])

'''
X_train, X_test, y_train, y_test = train_test_split(
        X, y, train_size=0.7, random_state=42
    )

print("\nTraining models...\n", "-"*50)

#logistic regression
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

lr = LogisticRegression(random_state = 0)
lr.fit(X_train_scaled, y_train)
print("\nLogistic Regresion Model Accuracy score is: ", lr.score(X_test_scaled, y_test))

#simple linear regression
regr = linear_model.LinearRegression()
regr.fit(X_train, y_train)
print("\nSimple Linear Model Accuracy score is: ", regr.score(X_test, y_test))
'''

#Polynomial Linear Regression
poly = PolynomialFeatures(degree=2, include_bias=False)
poly_features = poly.fit_transform(X)
X_train, X_test, y_train, y_test = train_test_split(
        poly_features, y, train_size=0.9, random_state=42
    )
poly_reg_model = LinearRegression()
poly_reg_model.fit(X_train, y_train)
print("\nPolynomial Model Accuracy score is: ", poly_reg_model.score(X_test, y_test)) # accuracy 0.387


##### Time to predict athlete's performance at the Olympics
f_in = open('individual-performances.csv', mode='r')
csv_reader = csv.DictReader(f_in)

seeded_row.pop('timeResult')
d = seeded_row.copy() #contains performanceDate, competition, venueCountry, eventId
d['performanceDate'] = [numpy.datetime64(d['performanceDate'][0]).astype('float64')]
d['competition'] = competitionsMap[d['competition']]
d['venueCountry'] = venueCountriesMap[d['venueCountry']]
d['eventId'] = [d['eventId']]

predicted_results = {}

for athlete_row in csv_reader:
    d['id'] = [athlete_row['id']]
    d['iaafId'] = [athlete_row['iaafId']]
    d['countryCode'] = countryCodesMap[athlete_row['countryCode']] #43
    d['birthDate'] = [numpy.datetime64(athlete_row['birthDate']).astype('float64')]

    transformed_athlete_df = pandas.DataFrame(data=d)
    transformed_athlete = poly.transform(transformed_athlete_df)[0]
    y_predicted = poly_reg_model.predict([transformed_athlete])
    result_time = helper.transform_data_point_result_time(y_predicted)

    athlete_name_key = '%s, %s (%s)' % (athlete_row['lastName'], athlete_row['firstName'], athlete_row['countryCode'])
    predicted_results[athlete_name_key] = result_time


sorted_prediction_times_list = sorted(predicted_results.items(), key=lambda x:x[1])
sorted_prediction_times = dict(sorted_prediction_times_list)
print('---------- Athlete Predicted Results ----------')
for athlete, predicted_time in sorted_prediction_times.items():
    print('%s: %s' % (athlete.rjust(37), predicted_time))