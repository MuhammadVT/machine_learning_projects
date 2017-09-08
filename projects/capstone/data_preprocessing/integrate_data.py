def add_new_station_id(time_res=15):
	""" adds a new column that remaps the station_id to
	sequential numbers with no gap.
	"""
	import pandas as pd
	import numpy as np

	# read the data
	df_status = pd.read_csv("../data/status_time_res_" + str(time_res) + "min.csv",
							parse_dates=["time"])

	# get the unique station_ids
	station_ids = np.sort(df_status.station_id.unique())

	# map the station_id to new_id
	dct = {station_ids[i] : i+1 for i in range(len(station_ids))}
	
	# add new_id column
	df_status.loc[:, "new_id"] = df_status.station_id.apply(lambda x: dct[x])	

	return df_status

def add_bikes_available_future(df_status, new_id=1, horizon_time=15):
    """Finds available bikes in the next time_res minutes and
    adds it into df_status as a new column.

    Parameters
    ----------
    df_status : pandas.DataFrame
        Status data
    new_id : int
        Number that corresponds to a station_id
    horizon_time : int
        The prediction horizon time in minutes. 

    Returns
    -------
    pandas.DataFrame

    """

    import pandas as pd
    import numpy as np
    import datetime as dt

    # select data for a given new_id
    df_status = df_status.loc[df_status.new_id == new_id]

    # order df_status by time
    df_status = df_status.sort_values(["time"])

    # find available bikes for the next horizon times
    bikes_available_future=[]
    for i in range(df_status.shape[0] - 1): 
        crw = df_status.iloc[i]
        nrw = df_status.iloc[i+1]
        ctm = crw['time']
        ntm = nrw['time']
        ntm_tmp = ctm + dt.timedelta(minutes=horizon_time)
        if ntm == ntm_tmp :
            bikes_available_future.append(nrw["bikes_available"])
        else:
            bikes_available_future.append(np.nan)

    # fill last value with np.nan
    bikes_available_future.append(np.nan)

    # add bikes_available_future column
    df_status.loc[:, "bikes_available_future"] = np.array(bikes_available_future)

    return df_status

def integrate_data(df_status, df_weather,new_id):

    """Integrates different datesets into a single dataframe.
    
    Parameters
    ----------
    df_status : pandas.DataFrame
        Status data
    df_weather : pandas.DataFrame
        Weather data
    new_id : int
        A new station id for which data points are selected.

    Returns
    -------
    pandas.DataFrame
        
    """

    import pandas as pd
    import numpy as np

    # copy status data
    df = df_status.copy()
    
    # drops some columns
    df.drop(["docks_available"], axis=1, inplace=True)

    # add datetime related features from status data
    df.loc[:, "time_of_day"] = df.time.apply(lambda x: x.strftime("%H%M"))
    df.loc[:, "day_of_week"] = df.time.apply(lambda x: x.weekday())
    df.loc[:, "month_of_year"] = df.time.apply(lambda x: x.month)

    def extract_same_day_weather_data(x, df_weather, weather_dates):
        """Extracts weather data for a given date"""
        row_indx = df_weather.index[weather_dates == x.date()]
        return row_indx[0]

    # get all the dates in the weather data
    weather_dates = df_weather.date.apply(lambda x: x.date()).as_matrix()

    # add features from weather data
    features_list = ["mean_temperature_f", "mean_humidity",
                     "mean_visibility_miles", "mean_wind_speed_mph",
                     "precipitation_inches", "events"]
    indices = [extract_same_day_weather_data(x, df_weather, weather_dates) for x in df.time]
    for f in features_list:
        df.loc[:, f] = (df_weather.loc[indices, f]).as_matrix()

    # drop time column
    df.drop(["time"], axis=1, inplace=True)

    # drop NaNs
    df.dropna(axis=0, how="any", inplace=True)

    # change column orders
    cols = list(df)
    cols.remove("bikes_available")
    cols.remove("bikes_available_future")
    cols = cols + ["bikes_available", "bikes_available_future"]
    df = df.loc[:, cols]

    # reindex the index
    df.index = range(df.shape[0])

    return df


def main():

    import pandas as pd
	
    time_res = 15
    new_id = 56

    # add new_id column
    df_status = add_new_station_id(time_res=15)

    # add bikes_available_future column for status data that has a given new_id
    df_status = add_bikes_available_future(df_status, new_id=new_id,
                                           horizon_time=time_res)

    # integrate the data
    df_weather = pd.read_csv("../data/weather_fixed.csv", parse_dates=["date"])
    df = integrate_data(df_status, df_weather,new_id)

    return df

if __name__ == "__main__":
    df = main()

