import os, sqlite3, dill, glob, sys, datetime, multiprocessing, time, json
import pandas as pd
import numpy as np

from collections import OrderedDict


### USER DATA HANDLING ###

# Buckets for the time intervals will be filled and meaned. 
# Empty buckets will result in NaN, texttual values will disappear.
MEANABLE = []

FIRSTABLE = [
    "ACCELEROMETER_DATA", 
    "AMBIENT_TEMPERATURE_DATA", 
    "GRAVITY_DATA", 
    "GYROSCOPE_DATA", 
    "LIGHT_DATA", 
    "LINEAR_ACCELERATION_DATA", 
    "MAGNETIC_FIELD_DATA", 
    "ORIENTATION_DATA", 
    "PRESSURE_DATA", 
    "RELATIVE_HUMIDITY_DATA", 
    "ROTATION_DATA",
    "PING_DATA", 
    "GPS_DATA",
]

# The latest value is used until updated (no NaNs, usable for textual values)
FORWARD_FILLABLE = [
    "AUDIO_DATA", 
    "CDMA_LOCATION_DATA", 
    "CELL_CDMA_DATA", 
    "CELL_DATA_ACTIVITY_DATA", 
    "CELL_GSM_DATA", 
    "CELL_LTE_DATA", 
    "CELL_WCDMA_DATA", 
    "DEVICE_STATE_DATA", 
    "GSM_LOCATION_DATA", 
    "POWER_DATA", 
    "SERVICE_STATE_DATA", 
    "SIGNAL_STRENGTH_DATA", 
    "TCP_PROBE_DATA", 
    "WIFI_DATA",  
    "STEP_COUNTER_DATA", 
    "ACTIVITY_DATA",
    "PREDICTION_DATA",
]

PASS = [
    "CALENDAR_DATA", 
    "WIFI_SCAN_DATA", 
    "AUDIO_DEVICE_DATA", 
    "SIGNIFICANT_MOTION_DATA", 
    "STATIONARY_DETECT_DATA", 
    "TEXT_EVENT_DATA", 
    "STEP_DETECT_DATA", 
]

RESAMPLE = "1S"

def __resample_bluetooth_device_data(data):
    # extract the important columns and add a count column
    addresses = pd.DataFrame(data[["ADDRESS", "NAME"]])
    addresses["COUNT"] = 1

    # create a NAME based pivot (turn names into columns)
    availability = addresses.pivot_table(values="COUNT", columns=["NAME"], index=["DATE"], aggfunc="sum", fill_value=0)
    
    return  availability.resample("20S").sum()

def __resample_wifi_scan_data(data):
    data['DATE_ROUNDED'] = data['DATE'].apply(lambda dt: datetime.datetime(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second))
    aggregated = data.groupby("DATE_ROUNDED").agg({'BSSID':'nunique', 'SSID': 'nunique', 'RSSI': 'mean'})
    return aggregated.resample(RESAMPLE).ffill()
    

CUSTOM = {
    "BLUETOOTH_DEVICE_DATA": __resample_bluetooth_device_data,
    "WIFI_SCAN_DATA": __resample_wifi_scan_data,
}



def _load_db(filepath):
    ''' Load an experiment Database from a given location. '''
    if not os.path.exists(filepath):
        raise Exception("Database does not exists.")
    
    db = sqlite3.connect(filepath)
    tables = {}
    names = db.execute("SELECT name FROM sqlite_master WHERE type='table'")
    for name, in names: 
        if not name.endswith("_DATA"):
            continue
        tables[name] = pd.read_sql_query("select * from " + str(name) + ";", db)
    db.close()

    if len(tables) == 0:
        raise Exception("Database is empty.")

    for name, table in tables.items():
        if "TS" in table:
            table["DATE"] = table.TS.apply(lambda x: datetime.datetime.utcfromtimestamp(x / 1000))
            table.set_index(pd.DatetimeIndex(table["DATE"]), inplace=True)
            table.drop(['TS'], axis=1, inplace=True)
            table.drop(['ID'], axis=1, inplace=True)
    return tables




def _resample_db(tables):
    ''' Resamples the rows of a database'''
    resampled = {}
    
    for name, table in tables.items():
        if name in MEANABLE:
            resampled[name] = table.resample(RESAMPLE).mean()
        elif name in FIRSTABLE:
            resampled[name] = table.resample(RESAMPLE).first()
        elif name in FORWARD_FILLABLE:
            resampled[name] = table.drop_duplicates('DATE').resample(RESAMPLE).ffill()
        elif name in CUSTOM:
            resampled[name] = CUSTOM[name](table)
        elif name in PASS:
            pass
        else:
            raise RuntimeError("No resampler defined for '{}'.".format(name))
                
    return resampled

def _merge_resampled_db(tables, name):
    '''Merge all tables in the provided dict'''
    for key, df in tables.items():
        datafield = df.copy(deep=False)
        datafield.columns = [(key + "_" + s) for s in datafield.columns]

        try:
            out_df = pd.merge(out_df, datafield, how='outer', left_index=True, right_index=True)
        except UnboundLocalError:
            out_df = datafield
    
    # as activity data is added also at the app start, we ignore it when dropping nan rows
    mandatory_columns = ["LINEAR_ACCELERATION_DATA_X"]
    out_df.dropna(axis=0, how='all', inplace=True, subset=mandatory_columns)
    
    out_df["NAME"] = name
    
    return out_df

def load_df(path, name):
    '''Load a database as a resampled dataframe.'''
    db = _load_db(path)
    resampled_db = _resample_db(db)
    df = _merge_resampled_db(resampled_db, name)
    
    return df

def __load_df_helper(dbpath):
    folder = os.path.split(dbpath)[0]
    name = folder.split("/")[-1]
    df = None

    try:
        df = load_df(dbpath, name)
    except Exception as e:
        print("Error loading {}: {}".format(dbpath, str(e)))

    return (dbpath, df)
    
def load_folder(folder):
    '''Load all databases from a folder (non-recursive)'''
    filepaths = [os.path.join(folder, filename) for filename in os.listdir(folder)]
    return load_dfs(filepaths)

def load_dfs(filepaths):
    '''Load the dataframes for the databases '''
    print("Loading {} databases in {} threads...".format(len(filepaths), multiprocessing.cpu_count()))
    threadpool = multiprocessing.Pool(multiprocessing.cpu_count())
    databases = dict(threadpool.map(__load_df_helper, filepaths))
    print("... done.")
    
    return databases
    

### Snapshot / Restore mechanism
DILL_FORMAT = "/tmp/seamless_{}_{}.dill"

def save_snapshot(databases, name="default"):
    '''Save a dict of dataframes as a dill file.'''
    filename = DILL_FORMAT.format(name, int(time.time()))
    with open(filename, "wb" ) as dillfile:
        dill.dump(databases, dillfile)
    
    print("Snapshot saved: {}.".format(datetime.date.today()))


def load_snapshot(name="default", timestamp=None):
    '''Load a pickeled dict of dataframes.'''
    if timestamp:
        filename = glob.glob(DILL_FORMAT.format(name, timestamp))
    else:
        all_dills = glob.glob(DILL_FORMAT.format(name, "*"))
        filename = max(all_dills, key=os.path.getctime)
    
    return dill.load(open(filename, "rb" ))


def refresh_load_snapshot(base_path="/seamless-data/", snapname="default"):
    '''Read the latest snapshot, load the missing dbs and save a new snapshot.'''
    folders = [os.path.join(base_path, name) for name in os.listdir(base_path)]
    linked_folders = [path for path in folders if os.path.islink(path)]
    
    try:
        databases = load_snapshot(name=snapname)
    except ValueError:
        databases = {}
    
    db_paths = [os.path.join(folder, fn) 
                 for folder in linked_folders 
                     for fn in os.listdir(folder)]
    new_db_paths = [path for path in db_paths if path not in databases.keys()]

    if len(new_db_paths) > 0:
        new_databases = load_dfs(new_db_paths)
        databases.update(new_databases)
        save_snapshot(databases, name=snapname)
        
    filtered = {k:v for k, v in databases.items() if not v is None}
    
    return filtered




### LOADING AND HANDLING EXPERIMENT RESULTS ###



EXPERIMENTS = {}


### DATA HANDLING ###

def resample_bufferlevel(data_frame):
    '''Resample bufferlevel given in dataframe to seconds.'''
    new_data_frame = data_frame.set_index('playback_position')
    new_data_frame.index = pd.to_timedelta(new_data_frame.index, unit="s")
    new_data_frame = new_data_frame.resample("S").mean().fillna(method='ffill')
    return new_data_frame

def resample_bufferlevels():
    '''Resample all bufferlevels in global EXPERIMENTS dict'''
    for key in EXPERIMENTS.keys():
        EXPERIMENTS[key]['bufferlevel_resampled'] = resample_bufferlevel(EXPERIMENTS[key]['bufferlevel'])

def load_experiment(path):
    ''' Read single JSON experiment file in path and return it as a dict'''
    with open(path) as json_data:
        tmp_data = json.load(json_data)
        
        return {'adaptations': pd.DataFrame.from_dict(tmp_data["adaptation"]),
                'stallings' : pd.DataFrame.from_dict(tmp_data["stalling"]),
                'bufferlevel': pd.DataFrame.from_dict(tmp_data["bufferlevel"])}

def load_all_experiments(path):
    ''' Read all JSON experiment files in path and return all in a dict'''
    all_experiments = [f for f in os.listdir(path) if os.path.isfile(path + '/' + f) and 'json' in f and f != 'db.json']
    
    for experiment in all_experiments:
        EXPERIMENTS[os.path.splitext(experiment)[0]] = load_experiment(path + '/' + experiment)

    resample_bufferlevels()


### COMPUTATIONS ###

def get_stallings(stallings_df):
    '''Return non-initial stallings in DF'''
    return stallings_df[stallings_df.eventtype != 'initialStalling']

def get_quality_time(adaptations, bufferlevel):
    '''Get playtime time of highest achieved quality'''
    total_play_time = 0
    for name, group in bufferlevel.groupby(['experiment']):
        total_play_time = total_play_time + group.iloc[-1].playback_position
    
    res_dict = {}
    for index, row in adaptations.iterrows():
        if row.time_in_representation == 0:
            continue
        res_dict[row.last_bitrate] = res_dict.get(row.last_bitrate, 0) + row.time_in_representation
        
    for name, group in adaptations.groupby(['experiment']):
        res_dict[group.iloc[-1].bitrate] = total_play_time - (sum(list(res_dict.values()))) + res_dict.get(group.iloc[-1].bitrate, 0)

    return {k: v / total_play_time for k, v in res_dict.items()}

def get_max_quality(q_dict):
    '''Return the highest quality of above computed dict'''
    return max(q_dict.keys())

def stalling_mos(avg_stall, stalling_count):
    '''Compute stalling mos based on "Internet Video Delivery in YouTube: From Traffic Measurements to Quality of Experience"'''
    return 3.5 * np.exp(-(0.15 * avg_stall + 0.19) * stalling_count) + 1.5

def adaptations_mos(time_percent):
    '''Compute adaptations mos based on "ASSESSING EFFECT SIZES OF INFLUENCE FACTORS TOWARDS A QOE MODEL FOR HTTP ADAPTIVE STREAMING"'''
    return 0.003 * np.exp(0.064 * time_percent * 100) + 2.498

def find_run(run, playtimes):
    '''Helper for finding experiment for given run'''
    for test in playtimes:
        if run in test[1]:
            return test[1][run]
        
def find_conf(run, adapts):
    '''Helper for finding configuration for given run'''
    for test in adapts:
        if run in test[1]:
            return test[0]

def stall_mos():
    '''Preparing and calculating stall MOS'''
    keys = sorted([key for key in EXPERIMENTS.keys()])
    
    stalls_for_key = [(key, EXPERIMENTS[key]['stallings']) for key in keys]
    stalls_within = [(k, get_stallings(df)) for k, df in stalls_for_key]
    grouped_stalls = [(k, df.groupby('experiment')) for k, df in stalls_within]
    avg_duration_per_group = [(k, (len(group), group.duration.mean() / 1000)) for k, group in grouped_stalls]
    mos_per_group = [(k, stalling_mos(l, c)) for k, (l, c) in avg_duration_per_group]
    
    mos_stall_dict = dict(mos_per_group)
    
    for key, value in mos_stall_dict.items():
        mos_stall_dict[key] = [5] * 5 if len(value) == 0 and 'z' not in key else value
        
    return OrderedDict(sorted(mos_stall_dict.items(), key=lambda v: v[0].split("_")[1]))

def adapt_mos():
    '''Preparing and calculating adaptation MOS'''
    keys = sorted([key for key in EXPERIMENTS.keys()])
    
    playtimes = [(key, EXPERIMENTS[key]['bufferlevel'].groupby('experiment').playback_position.last()) for key in keys]
    
    adaptations_dict = [EXPERIMENTS[key]['adaptations'].to_dict() for key in keys]
    representation_times_dict = {}
    
    for run in adaptations_dict:
        for elem, last_rate in run['last_bitrate'].items():
            current_id = run['experiment'][elem]
            spent_time = run['time_in_representation'][elem]
            current_id_bitrates = representation_times_dict.get(current_id, {})
            current_id_bitrates[last_rate] = current_id_bitrates.get(last_rate, 0) + spent_time
            representation_times_dict[current_id] = current_id_bitrates
            
    for run in adaptations_dict:
        last_elem = list(run['last_bitrate'].items())[-1]
        last_elem_id = last_elem[0]
        last_elem_bitrate = last_elem[1]
        current_run = run['experiment'][last_elem_id]
        total_play_time = find_run(current_run, playtimes)
        representation_times_dict[current_run][last_elem_bitrate] = total_play_time - (sum(representation_times_dict[current_run].values()) + representation_times_dict[current_run][last_elem_bitrate])
        
    representation_time_percentage = {}
    for run, qualities in representation_times_dict.items():
        total_play_time = find_run(run, playtimes)
        representation_time_percentage[run] = {k: v / total_play_time for k, v in qualities.items()}
              
    only_max_qualities = {}
    for run, qualities in representation_time_percentage.items():
        only_max_qualities[run] = qualities[get_max_quality(qualities)]
    
    result_dict = {}
    for run, quality in only_max_qualities.items():
        conf = find_conf(run, playtimes)
        result_dict.setdefault(conf, []).append(quality)
    
    mos_dict = {}
    for conf, qs in result_dict.items():
        mos_dict[conf] = list(map(lambda x: adaptations_mos(x), qs))
        
    return OrderedDict(sorted(mos_dict.items(), key=lambda v: v[0].split("_")[1]))

def prepare_mos():
    '''Preparing the combined MOS for plotting'''
    keys = sorted([key for key in EXPERIMENTS.keys()])

    adaptation_dict_boxes = adapt_mos()
    stall_dict_boxes = stall_mos()
    
    combined_mos = OrderedDict()
    for key in keys:
        combined_mos[key] = [((i + j) / 2) for i, j in zip(adaptation_dict_boxes[key], stall_dict_boxes[key])]
        
    combined_mos.update({'z_scen1': [], 'z_scen2': [], 'z_scen3': []})
    
    order = [
        'stock4_scen1', 'mptcp_scen1', 'seamless1_scen1', 'seamless2_scen1', 'z_scen1',
        'stock4_scen2', 'mptcp_scen2', 'seamless1_scen2', 'seamless2_scen2', 'z_scen2',
        'stock4_scen3', 'mptcp_scen3', 'seamless1_scen3', 'seamless2_scen3', 'z_scen3',
        'stock4_scen4', 'mptcp_scen4', 'seamless1_scen4', 'seamless2_scen4'
    ]
    
    return OrderedDict((k, combined_mos[k]) for k in order)