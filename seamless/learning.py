import multiprocessing
import multiprocessing.dummy
import sklearn, sklearn_pandas
import imblearn
import pandas as pd
import numpy as np
import copy

import seamless.export

### Feature Engineering 
def __engineer_vector_length(df, name):
    '''vector length computation (eucledian norm)'''
    df[name+"_LENGTH"] = np.sqrt(df[name+"_X"].diff().pow(2)
       + df[name+"_Y"].diff().pow(2)
       + df[name+"_Z"].diff().pow(2))

def _engineer_features(df):
    df["PRESSURE_DATA_DIFF"] = df["PRESSURE_DATA_X"].diff()
    df["STEP_COUNTER_DATA_DIFF"] = df["STEP_COUNTER_DATA_X"].diff()
    __engineer_vector_length(df, "ORIENTATION_DATA")
    __engineer_vector_length(df, "ACCELEROMETER_DATA")
    __engineer_vector_length(df, "GRAVITY_DATA")
    __engineer_vector_length(df, "MAGNETIC_FIELD_DATA")
    __engineer_vector_length(df, "GYROSCOPE_DATA")
    __engineer_vector_length(df, "LINEAR_ACCELERATION_DATA")
    __engineer_vector_length(df, "ROTATION_DATA")
    
    df['WIFI_DATA_STATE_AVAIL'] = 0
    df.loc[df['WIFI_DATA_STATE'] == 'COMPLETED', 'WIFI_DATA_STATE_AVAIL'] = 1
    
    df['WIFI_DATA_SPEED_AVAIL'] = 0
    df.loc[df['WIFI_DATA_SPEED'] > 20, 'WIFI_DATA_SPEED_AVAIL'] = 1
    
    df['WIFI_DATA_RSSI_AVAIL'] = 0
    df.loc[df['WIFI_DATA_RSSI'] > -70, 'WIFI_DATA_RSSI_AVAIL'] = 1


def __compute_prediction_window(df, window, column, shift=0):
    df[column+"_INTERVAL_"+str(window)] = df[column].shift(shift).rolling(window).min().shift(-window)
    

def _annotate_wifi_loss(df, target, shift=0):
    parts = target.split("_")
    window = int(parts[-1])
    column = "_".join(parts[:-2])
    
    __compute_prediction_window(df, window, column)
    
rssi_feature_vector = {
    'WIFI_DATA_RSSI': sklearn.preprocessing.StandardScaler(),
}
    
reduced_feature_vector = {
    'PRESSURE_DATA_DIFF': sklearn.preprocessing.StandardScaler(),
    'LINEAR_ACCELERATION_DATA_LENGTH': sklearn.preprocessing.StandardScaler(),
    'STEP_COUNTER_DATA_DIFF': sklearn.preprocessing.StandardScaler(),
    'POWER_DATA_IS_CHARGING': sklearn.preprocessing.StandardScaler(),
    'GRAVITY_DATA_Z': sklearn.preprocessing.StandardScaler(),
#    'WIFI_DATA_FREQUENCY': sklearn.preprocessing.StandardScaler(),
    'WIFI_DATA_SPEED': sklearn.preprocessing.StandardScaler(),
    'WIFI_DATA_RSSI': sklearn.preprocessing.StandardScaler(),
}

full_feature_vector = {
    'PRESSURE_DATA_DIFF': sklearn.preprocessing.StandardScaler(),
    'PRESSURE_DATA_X': sklearn.preprocessing.StandardScaler(),
    'LINEAR_ACCELERATION_DATA_X': sklearn.preprocessing.StandardScaler(),
    'LINEAR_ACCELERATION_DATA_Y': sklearn.preprocessing.StandardScaler(),
    'LINEAR_ACCELERATION_DATA_Z': sklearn.preprocessing.StandardScaler(),
    'LINEAR_ACCELERATION_DATA_LENGTH': sklearn.preprocessing.StandardScaler(),
    'STEP_COUNTER_DATA_DIFF': sklearn.preprocessing.StandardScaler(),
    'POWER_DATA_IS_CHARGING': sklearn.preprocessing.StandardScaler(),
    'POWER_DATA_BATTERY_PERCENTAGE': sklearn.preprocessing.StandardScaler(),
    'GRAVITY_DATA_X': sklearn.preprocessing.StandardScaler(),
    'GRAVITY_DATA_Y': sklearn.preprocessing.StandardScaler(),
    'GRAVITY_DATA_Z': sklearn.preprocessing.StandardScaler(),
    'GYROSCOPE_DATA_LENGTH': sklearn.preprocessing.StandardScaler(),
    'MAGNETIC_FIELD_DATA_X': sklearn.preprocessing.StandardScaler(),
    'MAGNETIC_FIELD_DATA_Y': sklearn.preprocessing.StandardScaler(),
    'MAGNETIC_FIELD_DATA_Z': sklearn.preprocessing.StandardScaler(),
    'ORIENTATION_DATA_X': sklearn.preprocessing.StandardScaler(),
    'ORIENTATION_DATA_Y': sklearn.preprocessing.StandardScaler(),
    'ORIENTATION_DATA_Z': sklearn.preprocessing.StandardScaler(),
    'ROTATION_DATA_X': sklearn.preprocessing.StandardScaler(),
    'ROTATION_DATA_Y': sklearn.preprocessing.StandardScaler(),
    'ROTATION_DATA_Z': sklearn.preprocessing.StandardScaler(),
#    'WIFI_DATA_FREQUENCY': sklearn.preprocessing.StandardScaler(),
    'WIFI_DATA_SPEED': sklearn.preprocessing.StandardScaler(),
    'WIFI_DATA_RSSI': sklearn.preprocessing.StandardScaler(),
}


### Object Oriented Learning Implementation
class Learner:
    def __init__(self, target="WIFI_DATA_RSSI_AVAIL_INTERVAL_15"):
        self.codename = None
        
        ## need to be set before calling 'prepare'
        self.mappings = rssi_feature_vector
        self.obs_window = 60
        
        self.target = target
        self.prediction = target + "_PREDICTION"
        self.probability = target + "_PROBABILITY"
        
        # remove all rows where no wifi is available
        self.filter_targets = ["WIFI_DATA_STATE_AVAIL"]
        self.filter_func    = lambda df: df[df["WIFI_DATA_STATE_AVAIL"] == 1]
        
        ## need to be set before calling 'train'
        self.classifier = None
        self.sampler = None
        
    def _gen_mapper(self):
        '''create a list of tuples for the DataFrameMapper for the moving window.'''
        window_mappings = [(self.target, None)] # keep the target untouched
        for k in self.mappings.keys():
            for i in reversed(range(self.obs_window)):
                name = "{}_{}".format(k, i)
                window_mappings.append(([name], self.mappings[k]))
            
        self._mapper = sklearn_pandas.DataFrameMapper(window_mappings)

    def _prepare_df(self, tup):
        '''Select columns; create the moving window and drop NaN rows.'''
        (path, df) = tup
        _engineer_features(df)
        _annotate_wifi_loss(df, self.target)
        
        df_moving = df[[self.target] + self.filter_targets].copy()
        
        for k in self.mappings.keys():
            try:
                for i in reversed(range(self.obs_window)):
                    name = "{}_{}".format(k, i)
                    # shift the column forward to have old values available
                    df_moving[name] = df[k].shift(i)
            except KeyError as e:
                print("{} is missing {}.".format(path, k))
                return None
                
        df_filtered = self.filter_func(df_moving)

        df_filtered = df_filtered.drop(columns=self.filter_targets)
        df_filtered = df_filtered.dropna(axis=0, how='any')
        
        return df_filtered
    
    def prepare(self, databases):
        '''hand over a dataset and prepare it for training and testing'''
        threadpool = multiprocessing.dummy.Pool(multiprocessing.cpu_count()) 

        train = pd.concat(threadpool.map(self._prepare_df, databases.items()))
        
        # create mapper only if none is present
        if not hasattr(self, '_mapper'):
            self._gen_mapper()
            self._mapper.fit(train)

        train_trans = self._mapper.transform(train)
        self.__X_train, self.__X_test, self.__y_train, self.__y_test = sklearn.model_selection.train_test_split(train_trans[:, 1:], train_trans[:, 0], test_size=0.3, random_state=1)
        
        if self.sampler:
            self.__X_resampled, self.__y_resampled = self.sampler.fit_sample(self.__X_train, self.__y_train)
        else:
            self.__X_resampled, self.__y_resampled = self.__X_train, self.__y_train

    
    def split_prepare(self, databases, name=""):
        '''split datasets by a name and prepare them for training and testing'''
        threadpool = multiprocessing.dummy.Pool(multiprocessing.cpu_count()) 
        
        train_dfs = [(k, v) for k, v in databases.items() if name not in k]
        test_dfs  = [(k, v) for k, v in databases.items() if name in k]
        train = pd.concat(threadpool.map(self._prepare_df, train_dfs))
        test = pd.concat(threadpool.map(self._prepare_df, test_dfs))
        
        self._gen_mapper()
        self._mapper.fit(train)
        train_trans = self._mapper.transform(train)
        test_trans = self._mapper.transform(test)

        self.__X_train, self.__y_train = train_trans[:, 1:], train_trans[:, 0]
        self.__X_test, self.__y_test = test_trans[:, 1:], test_trans[:, 0]
        
        if self.sampler:
            self.__X_resampled, self.__y_resampled = self.sampler.fit_sample(self.__X_train, self.__y_train)
        else:
            self.__X_resampled, self.__y_resampled = self.__X_train, self.__y_train
        

    def train(self):
        '''learns a classifier using the prepared datafields'''
        self.classifier.fit(self.__X_resampled, self.__y_resampled)
    
    
    def test(self):
        '''test a trained classifier using the prepared datafields'''
        predictions = self.classifier.predict(self.__X_test)
        report = sklearn.metrics.classification_report(self.__y_test, predictions)
        print(report)

    
    def run_classifier(self, test_df):
        '''test a classifier and add predictions to datafield'''
        test = self._prepare_df(test_df)
        test_trans  = self._mapper.transform(test)

        y_test, X_test = test_trans[:, 0], test_trans[:, 1:]
        
        predictions = self.classifier.predict(X_test)
        probability = self.classifier.predict_proba(X_test)

        # copy back to the pandas dataset (to have matching timestamps)
        test[self.prediction] = predictions
        test_df[self.prediction] = test[self.prediction]
        
        test[self.probability] = probability[:,1]
        test_df[self.probability] = test[self.probability]
    
    
    def get_precision_recall_fscore_support(self, df):
        '''return the printable classification report for the predictions'''
        report_df = df.dropna(axis=0, how='any', subset=[self.target, self.prediction])
        return sklearn.metrics.precision_recall_fscore_support(report_df[self.target], report_df[self.prediction], average="micro")

    
    def get_classification_report(self, df):
        '''return the printable classification report for the predictions'''
        report_df = df.dropna(axis=0, how='any', subset=[self.target, self.prediction])
        return sklearn.metrics.classification_report(report_df[self.target], report_df[self.prediction])

    
    def plot_df(self, df, ax1_extras=[], ax2_extras=[], ax1=None):
        '''plot the actual and the predicted values'''
        # ax1 =  df["PING_DATA_RTT"].plot(alpha=0.2, color="blue", linestyle="", marker=".", ax=ax1)
        ax1 = df["WIFI_DATA_RSSI"].plot(alpha=0.2, color="orange", ax=ax1)

        ax2 = ax1.twinx()
        df[self.target].plot(ax=ax2, color="purple", alpha=0.2)
        
        if self.prediction in df:
            df[self.prediction].plot(ax=ax2, color="black", alpha=0.5)
        if self.probability in df:
            df[self.probability].plot(ax=ax2, color="red", alpha=0.5)
            
        for extra in ax1_extras:
            if extra == "WIFI_DATA_RSSI": continue
            df[extra].plot(ax=ax1, alpha=0.2)            
        for extra in ax2_extras:
            df[extra].plot(ax=ax2, alpha=0.2)
        
        ax1.legend(loc='upper left')
        ax2.legend(loc='lower left')
        
        return ax1
    
    def fork_train_export(self, codename, classifier):
        learner = copy.copy(self)
        learner.codename = codename
        learner.classifier = classifier
    
        print("Training {}...".format(codename))
        learner.train()
        learner.test()
        
        seamless.export.export_learner(learner)
        
        return learner
    