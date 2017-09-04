import pdb
def read_data_from_db(stm, etm, station_id=None, time_res="1"):
    """ reads data (time resolution set by rime_res) from an sqlite3 db
    for a period of time (set by stm and etm) for a given station_id.
    
    Parameters
    ----------
    stm : datetime.datetime
        The start time
    etm : datetime.datetime
        The end time
    station_id : int, default to None
        The station id. If set to None, data fro all the stations will be read.
    time_res : str
        Time resolution.
        
    Returns
    -------
    pandas.DataFrame
    """

    import sqlite3
    import pandas as pd
    
    # construct db name and table name
    db_name = "../data/sampled_data.sqlite"
    table_name = "time_res_" + str(time_res) + "min"

    # make db connection
    conn = sqlite3.connect(database=db_name)

    if station_id is not None:
        # check whehter the user provided station_id actually exists
        command = "SELECT DISTINCT station_id from {tb}".format(tb=table_name)
        ids = conn.cursor().execute(command).fetchall()
        valid_id = station_id in [x[0] for x in ids]

    # if station_id is None then return data for all the stations
    if station_id is None:
        sql = "SELECT * FROM {tb} WHERE "
        sql = sql + "DATETIME(time) BETWEEN '{stm}' and '{etm}'"
        sql = sql.format(tb=table_name, stm=stm, etm=etm)
    
    # if station_id is not None then return data if station_id is valid
    else:
        if valid_id:
            sql = "SELECT * FROM {tb} WHERE station_id={station_id} AND "
            sql = sql + "(DATETIME(time) BETWEEN '{stm}' and '{etm}')"
            sql = sql.format(tb=table_name, station_id=station_id, stm=stm, etm=etm)
        else:
            print("invalid station_id, please choose a correct one. Returning None....")
            return None

    # get the data we want in a pandas DataFrame format
    df = pd.read_sql(sql, conn, index_col=None, coerce_float=True, params=None,
                  parse_dates=["time"], columns=None, chunksize=None)
    
    return df

def test():
    import datetime as dt 
    stm = dt.datetime(2013, 9, 1)
    etm = dt.datetime(2013, 10, 1)
    df = read_data_from_db(stm, etm, station_id=2, time_res="15")
    
    return df

if __name__ == "__main__":
    df = test()
