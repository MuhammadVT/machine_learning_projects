# load the packages
import sqlite3
import pandas as pd
import numpy as np
import datetime as dt
import multiprocessing as mp

def sampler(time_res=15, n_jobs=None, save_to_db=True, input_dbname=None,
            output_dbname="../data/sampled_data.sqlite", 
            input_tablename="status_new", output_tablename=None,
            verbose=False):
    """ This function reduces the size of the status data by
    sampling it at every time_res minutes. The output is stored in a database.

    Parameters
    ----------
    time_res : int
        time resolution in minutes, default to 15 minutes
    n_jobs : int
        The number of jobs to run in parallel. If set to None, 
        then the number of jobs is set to the number of cores.
        Defulat value is -1.
    save_to_db : bool
        If set to true the output will be save into a database,
        else returns a dataframe that holds the output.
    input_dbname : str
        Name of the database where the original data is stored. 
        Default to ../data/database_fixed.sqlite.
    output_dbname : str
        Name of the database where the output is stored.
        Only effective if save_to_db is True.
        Default to ../data/sampled_data.sqlite 
    input_tablename : str or None
        Name of the input table where original status data is stored
    output_tablename : str or None
        Name of the table where the output status data is stored. 
        Only effective if save_to_db is True.
        Default to None in which case the table name will be
        created. 
    verbose : bool

    Return
    ------
    Pandas DataFrame is returned if save_to_db is True else returns 
    None and the output is stored in a database.

    """

    # number of jobs to be run in parallel
    if not n_jobs:
        # get the number of cups
        n_jobs = mp.cpu_count()

    # make db connection
    if input_dbname is None: 
        conn = sqlite3.connect(database=input_dbname,
                               detect_types=sqlite3.PARSE_DECLTYPES)
    cur = conn.cursor()

    # get the total number of data points in status table
    command = "SELECT Count(*) FROM {tb}".format(tb=input_tablename)
    cur.execute(command)
    npnts = cur.fetchone()[0]

    # batch size for each job (process)
    # batch_size = int(np.ceil(1.0 * npnts / n_jobs)) 
    if time_res < 5:
        batch_size = 200  # NOTE: more than this seems to be problematic for time_res < 5
    else:
        batch_size = 1000  # NOTE: more than this seems to be problematic for time_res=5 and above

    # extract data from status table in database.sqlite
    command = "SELECT station_id, bikes_available, docks_available,\
               time FROM {tb}".format(tb="status")
    cur.execute(command)

    # since the data size is large, we split the whole work into iter_num pieces and
    # for each piece we run n_jobs of processes in parallel
    if save_to_db:
        iter_num = int(np.ceil(1.0 * npnts / (n_jobs * batch_size)))
    else:
        iter_num = 1

    for k in range(iter_num):

        # Define an output queue
        output = mp.Queue()

        # send jobs in parallel
        procs = []
        for pos in range(n_jobs):
            batch = cur.fetchmany(batch_size)
            p = mp.Process(target=worker, args = (batch, time_res, pos, output))
            procs.append(p)
            p.start()

        # exit the completed processes
        for p in procs:
            p.join()
     
        # collect the results of each process
        data = [output.get() for p in procs]

        # flatted the list of lists
        data = [x for lst in data for x in lst[1]]

        # sort by time
        data.sort(key=lambda x: x[-1])

        # save the output into a db
        if save_to_db:

            # make db connection
            conn_new = sqlite3.connect(output_dbname)
            cur_new = conn_new.cursor()

            # create a table
            if not output_tablename:
                tbn = "time_res_" + str(time_res) + "min"
            else:
                tbn = output_tablename
            colname_type = "station_id INTEGER, bikes_available INTEGER,\
                            docks_available INTEGER, time TIMESTAMP,\
                            CONSTRAINT status_pk PRIMARY KEY (station_id, time)"
            command = "CREATE TABLE IF NOT EXISTS {tbn} ({colname_type})"\
                      .format(tbn=tbn, colname_type=colname_type)
            cur_new.execute(command)

            # populate the table
            cols = "station_id, bikes_available, docks_available, time"
            command = "INSERT or IGNORE INTO {tbn}({cols}) VALUES (?, ?, ?, ?)"\
                      .format(tbn=tbn, cols=cols)
            for rw in data:
                cur_new.execute(command, rw)
            conn_new.commit()

            if verbose:
                print "commited " + str(len(data)) +  " data points to db"

            # close db connection
            cur_new.close()

        else:
            # convert list into dictionary
            kys = ["station_id", "bikes_available", "docks_available", "time"]
            data = {kys[i]: [x[i] for x in data] for i in range(len(kys)) }

            # Create a dataframe
            df = pd.DataFrame(data=data)
            df.set_index('time')

    # close db connection
    cur.close()

    # return output
    if save_to_db:
        return None
    else:
        return df

def worker(batch, time_res, pos, output):
    """ A worker function that will be fed into the Multiprocessing module
    for parallel computing

    Parameters
    ----------
    batch : List 
        A list of tuples that Holds the outputs of an sqlite query
    time_res : int
        Time resolution in minutes, default to 15 minutes
    pos : int
        order of a process
    outpur : Multiprocessing.Queue object
        Stores the output of multiprocesses 

    Return
    ------
    List
        A list of tuples
    """

    data = []

    # since data size is large we do not fetchall, but, instead,
    # loop through the elements in batch 
    for rw in batch:
        tm_tmp = rw[-1]

        # sample the data at every time_res minutes
        if not tm_tmp.minute % time_res:
            data.append(tuple(list(rw[:-1]) + [tm_tmp]))

    return output.put((pos, data))

# run the code
def main():


    # sample the data
    df = sampler(time_res=15, n_jobs=None, save_to_db=True, input_dbname=None,
                 output_dbname="../data/sampled_data.sqlite", 
                 input_tablename="status_new", output_tablename=None,
                 verbose=True)

    return df


if __name__ == "__main__":
    main()

