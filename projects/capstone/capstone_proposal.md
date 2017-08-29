
# Machine Learning Engineer Nanodegree
## Capstone Proposal
Maimaitirebike Maimaiti  
August 26, 2017

## Proposal
### Domain Background
Concerns about global climate change, energy security, and unstable fuel prices have caused many decision makers and policy experts worldwide to closely examine the need for more sustainable transportation strategies. Bike-sharing system, the shared use of a bicycle fleet, is one mobility strategy that could help address many of these concerns [[1]](http://tsrc.berkeley.edu/sites/default/files/Bikesharing%20in%20Europe,%20the%20Americas,%20and%20Asia%20-%20Shaheen.pdf). Although the 1st generation of bike-sharing programs began in Amsterdam in 1965, bike-sharing has received increasing attention in recent years with initiatives to increase cycle usage, improve the first mile/last mile connection to other modes of transit, and lessen the environmental impacts of our transport activities. Especially, the development of better methods of tracking bikes with improved technology gave birth to the rapid expansion of bike-sharing programs throughout Europe and now most other continents during this decade [[2]](http://scholarcommons.usf.edu/jpt/vol12/iss4/3/). 

In 2013, Bay Area Bike Share ([also known as Ford GoBike](https://www.fordgobike.com/)) was introduced as a pilot program for the Bay Area region, with 700 bikes and 70 stations across San Francisco and San Jose. Similar to car sharing, "bicycle sharing" in Bay Area is a membership-based system for short-term bicycle rental. Members can check out a bicycle from a network of automated stations, ride to the station nearest their destination, and leave the bicycle safely locked for someone else to use. While traditional bike rentals are loaned out for half-day or longer, bike sharing is designed for short, quick trips. Stations connect users to transit, businesses and other destinations, often providing the "last-mile connection." To reflect system design, pricing is set to discourage trips longer than 30 minutes. Users can take an unlimited number of 30-minute trips during their membership period; however, any individual trip over 30 minutes will incur an additional fee [[3]](http://www.bayareabikeshare.com/faq#BikeShare101).

A crutial part of successfully operating such a BBS is the redistribution of bikes. Since the count of bikes in each station, each of which has a finite number of docks, fluctuates, redistribution operation must be performed periodically to make the bike-sharing service more efficient and environmentally friendly. However, staff moving bikes from areas of high supply/low demand to areas of low supply/high demand is time consuming, expensive, and polluting [[1]](http://scholarcommons.usf.edu/jpt/vol12/iss4/3/). Thererfore, predicting the number of available bikes in each station over time is one of the key tasks to making this operation more efficient. 

The modeling of bike availability using various features like time, weather, built environment, transportation infrastructure, etc., is an area of significant research interest. [Froehlich et al. (2009)](https://www.ijcai.org/Proceedings/09/Papers/238.pdf) used four predictive models to predict the number of available bikes at each station: last value, historical mean, historical trend, and a Bayesian network. [Kaltenbrunner et al. (2010)](http://www.sciencedirect.com/science/article/pii/S1574119210000568) adopted an Autoregressive Moving Average (ARMA) model and [Yoon et al. (2012)](http://ieeexplore.ieee.org/document/6341407/) proposed a modified Autoregressive Integrated Moving Average (ARIMA) model considering spatial interaction and temporal factors. In a recent study, [Ashqar et al. (2017)](http://ieeexplore.ieee.org/abstract/document/8005700/) used Random Forest (RF) and (Least-Squares Boosting) LSBoost models to predict future bike availability at a given station. In this project we explore a neural network solution for predicting future bike availability.

### Problem Statement
The goal of this project is to predict the number of available bikes at a bike share station using various predictors. Specifically, we will treat the number of available bikes at station _i_ in the future as the predictor, which is denoted by Yi(_t_ + _dt_), where Y is the number of available bikes, _i_ (_i_ = 1,2,...,70.) is the station number, _dt_ is the prediction horizen time. In this project, _dt_=15 minutes will be considered. That means, the prediction would be for the next 15 minutes.  The predictors that will be considered are the available bikes at station _i_ at time _t_ (current time), the month-of-the-year, day-of-the-week, time-of-day, and various weather conditions, like temperature, humidity, visibility, wind speed, precipitation, and events in a day (i.e., rainy, foggy, or sunny). Since the response variable Y takes interger values from 0 to 27, both regression and classification models can be considered. However, the focus of this project will be on using neural network to predict Y by taking a regression approach.

### Datasets and Inputs
For this problem we use the dateset provided by [Bay Area Bike Share (also known as Ford GoBike)](http://www.bayareabikeshare.com/open-data) for August 2013 to August 2015. This data is provided according to the [Ford GoBike Data License Agreement](https://assets.fordgobike.com/data-license-agreement.html). They make regular open data releases, plus maintain a real-time API.

#### The Dataset:
There are four different data files (_status_, _station_, _trip_, _weather_) in this dataset, each of which will be used at different level to solve the problem. The _status_ data provides features like current bike availability and time information. The response variable Y will aslo be taken from this dataset by shifting it by _dt_. The various features in _station_ and _trip_ data will be considered if they are useful in making prediction. Weather related features in _weather_ data will be used as predictors after removing redundant features. A breif description of the data is as follows:
##### _status_ data

_station_id_: station ID number (use "station.csv" to find corresponding station information)

_bikes_available_: number of available bikes

_docks_available_: number of available docks

_time_: date and time, PST

##### _station_ data

_station_id_: station ID number (corresponds to "station_id" in "status.csv")

_name_: name of station

_lat_: latitude

_long_: longitude

_dockcount_: number of total docks at station

_landmark_: city (San Francisco, Redwood City, Palo Alto, Mountain View, San Jose)

_installation_: original date that station was installed.

##### _trip_ data
Each trip is anonymized and includes:

_Trip ID_: numeric ID of bike trip

_Duration_: time of trip in seconds  (trips <1 min and >24 hours are excluded)

_Start Date_: start date of trip with date and time, in PST

_Start Station_: station name of start station

_Start Terminal_: numeric reference for start station

_End Date_: end date of trip with date and time, in PST

_End Station_: station name for end station

_End Terminal_: numeric reference for end station

_Bike #_: ID of bike used

_Subscription Type_: Subscriber = annual or 30-day member; Customer = 24-hour or 3-day member

_Zip Code_: Home zip code of subscriber (customers can choose to manually enter zip at kiosk however data is unreliable)

##### _weather_ data
Daily weather information per service area, provided from Weather Underground in PST. Weather is listed from north to south (San Francisco, Redwood City, Palo Alto, Mountain View, San Jose). The futures included in this data are:
'date', 'max_temperature_f', 'mean_temperature_f', 'min_temperature_f', 'max_dew_point_f', 'mean_dew_point_f', 'min_dew_point_f', 'max_humidity', 'mean_humidity', 'min_humidity', 'max_sea_level_pressure_inches', 'mean_sea_level_pressure_inches', 'min_sea_level_pressure_inches',
'max_visibility_miles', 'mean_visibility_miles', 'min_visibility_miles', 'max_wind_Speed_mph', 'mean_wind_speed_mph', 'max_gust_speed_mph', 'precipitation_inches', 'cloud_cover', 'events', 'wind_dir_degrees', 'zip_code'

*Note:*        

_Precipitation_In_:         "numeric, in form x.xx but alpha ""T""= trace when amount less than .01 inch"        

_Cloud_Cover_:         "scale of 0-8, 0=clear"        

_Zip_: 94107=San Francisco, 94063=Redwood City, 94301=Palo Alto, 94041=Mountain View, 95113= San Jose"


### Solution Statement
A neural network approach will be explored to predict the future bike availability Y based on features X which includes current bike availability, datetime information, and various weather parameters, etc. Y would be treated as a continues variable, and therefore, the neural network model would be used for regression. Various number of layers and different number of neurons per layer will be explored and the best model will be selected based on mean absolute error. Then the final results will be evaluated by comparing its mean absolute error with that reported by [Ashqar et al.](http://ieeexplore.ieee.org/abstract/document/8005700/). 

### Benchmark Model
In a recent paper, [Ashqar et al. (2017)](http://ieeexplore.ieee.org/abstract/document/8005700/) used Random Forest and Least-Squares Boosting algorithms to predict the bike availability in a given station and used mean squared error (MAE) as an evaluation metric. The average MAE results they obtained for RF and LSBoost are 0.37 bikes/station and 0.58 bikes/station. In this project these two values will be taken as Benchmark.

### Evaluation Metrics

Since this is a regression problem, mean absolute error and mean squared error are good options for model evaluation. A recent study [[5]](http://ieeexplore.ieee.org/abstract/document/8005700/), whose results are taken as Benchmark in this project, used MAE as evaluation metric. In this project, mean squred error (MSE) will also be used as an evalluation metric in addition to MAE.

### Project Design
The workflow for reaching the solution for the stated problem can be divided into the following steps: 
#### Data Preprocessing
The four files in this dataset are in csv format and are well structured. However, there are missing values and incorrect entries, which issues need to be addressed first.

The status.csv file size in this dataset is 1.9 GB and it contains about 72 million data points. It is difficult to work with such a large dataset using an ordinary computer. One approach to reduce the _status_ data to managable size is through downsampling. For example, we can downsample the original data (1-min resolution) to 15-min resolution. However, the effect of this downsampling needs to be examined to make sure that the dowwsamled data still represents the original population. 

Feature selection is also necessary for this problem because some features in the dataset could be redundant. For example, features like 'max_temperature_f', 'mean_temperature_f', and 'min_temperature_f' can be highly correlated such that one of them may be sufficient for prediction. 

For the ease of building a model, it is better to pull all the predictors and the reponse variables in a single dataframe. This requies joining the data from the four different files and put them together into a single table. Once data is joined together, categorical features need to be transformed into numerical features before feeding them into a model. One-hot encoding can be used for this purpose. Then, data will be splitted into training and test datasets. The training dataset will be used for training a model and the test data for evaluating the trained model performance.

#### Model Building and Evaluation
Neural network model will be explored to reach a solution to this problem. Since the problem is converted into a regression problem by treating the future bike availability as a continues variable, the last layer of the model will have only one neuron without any activation function. The first layer will have the same number of neurons as the number of encoded-features, excluding the bias. The best model will be searched by exploring different number of hidden layers and various number of neurons in each hidden layer. Model selection will be based on mean absolute error. The final model will be compared with the results reported by [Ashqar et al.](http://ieeexplore.ieee.org/abstract/document/8005700/) where RF and LSBoost models have been used.


