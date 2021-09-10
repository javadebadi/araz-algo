from datetime import time
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
import logging

class RegressionTimeStamps():
    def __init__(self, freq):
        self.freq=freq
        self.X = []
        self.y = []
        self.reg = LinearRegression()
    
    def _generate_timestamps(self, timestamps):
        m = len(timestamps)
        diff_list = [0]
        for index in range(m-1):
            dates = pd.date_range(start=timestamps[index], end=timestamps[index+1], freq=self.freq)
            diff_list.append(len(dates)-1)
            
        X = np.array(diff_list).cumsum().reshape((len(diff_list), 1))
        timestamps = pd.date_range(start=timestamps[0], end=timestamps[-1], freq=self.freq)
        return timestamps, X
    
    def fit(self, timestamps: list, y: list):
        assert isinstance(timestamps, list) and isinstance(y, list)
        self.timestamps, self.X = self._generate_timestamps(timestamps)
        self.reg.fit(self.X, y)
        
    def interpolated_df(self, exclude_max=False, col_name='value'):
        if exclude_max is False:
            interploated_index_array = np.arange(self.X.min(), self.X.max()+1)
            timestamps = self.timestamps
        else:
            interploated_index_array = np.arange(self.X.min(), self.X.max())
            timestamps = self.timestamps[:-1]
        m = len(interploated_index_array)
        interploated_index_array = interploated_index_array.reshape((m, 1))
        interpolations = self.reg.predict(interploated_index_array)
        interpolations = interpolations.reshape((1,m)).flatten()
        indexes = list(interploated_index_array.reshape(1,m).flatten())
        self.df = pd.DataFrame(data={col_name: interpolations}, index=timestamps)
        return self.df
    
    def extrapolate(self, till_timestamp, col_name='value'):
        timestamps, X = self._generate_timestamps([self.timestamps[0], till_timestamp])
        yhats = self.reg.predict(np.arange(len(timestamps)).reshape(len(timestamps),1))
        self.df = pd.DataFrame(data={col_name:yhats}, index=timestamps)
        return self.df 
    
    def back_extrapolate(self, from_timestamp, col_name='value'):
        timestamps, X = self._generate_timestamps([from_timestamp, self.timestamps[0]])
        timestamps = timestamps[:-1]
        X = X[:-1]
        if len(timestamps) == 0:
            self.df = None
            return None
        yhats = self.reg.predict(np.arange(len(timestamps)).reshape(len(timestamps),1))
        self.df  = pd.DataFrame(data={col_name:yhats}, index=timestamps)
        return self.df
    
    def df_to_dict(self, col_name):
        if self.df is None:
            return None
        else:
            return self.df[col_name].to_dict()
        




class RegressionTimeStampsTS:
    
    def __init__(self, df, bool_filter_col, objective_col, train_data_size, freq):
        """df must be a pandas dataframe where its index is pandas Timestamps"""
        self.df = df.copy()
        # convert pandas index to pandas datetime object
        self.df.index = pd.to_datetime(df.index)
        # convert the columns that must be bool to a bool
        # (sometimes in reading from database bool are read as integer)
        self.df[bool_filter_col] = self.df[bool_filter_col].astype('bool')
        # set train data size 
        self.train_data_size = train_data_size  
        # a dictionary to 
        self.regression_dict = {}
        # selected df according to bool filter
        self.df_selected = self.df[self.df[bool_filter_col]==True]
        # size of selected df
        self.m = len(self.df_selected)
        # objective col
        self.objective_col = objective_col
        # freq
        self.freq = freq
        
    def fit_interpolate_extraploate(self):
        for index in range(self.train_data_size-1, self.m):
            # get list of timestamps
            timestamps_list = self.df_selected.index[index+1-self.train_data_size:index+1].to_list()
            # find list of objective valuues needed to used as train set y (target)
            ys_list = self.df_selected[self.objective_col].iloc[index+1-self.train_data_size:index+1].to_list()
            reg_ts = RegressionTimeStamps(freq=self.freq)
            reg_ts.fit(timestamps_list, ys_list)
            if index == self.train_data_size-1:
                logging.warning("Started back extraplolate")
                reg_ts.back_extrapolate(from_timestamp=self.df.index.min(), col_name='reg_pred')
                if reg_ts.df is not None:
                    self.regression_dict.update(reg_ts.df_to_dict('reg_pred'))
                logging.warning("Finished back extraplolate")
            if index != self.m -1 :
                reg_ts.interpolated_df(exclude_max=True, col_name='reg_pred')
                self.regression_dict.update(reg_ts.df_to_dict('reg_pred'))
            else:
                reg_ts.extrapolate(till_timestamp=self.df.index.max(), col_name='reg_pred')
                self.regression_dict.update(reg_ts.df_to_dict('reg_pred'))

        # self.df['reg_pred'] = np.array(list(self.regression_dict.values()))
        new_df = pd.DataFrame(
            data = {
                'start_datetime': np.array(list(self.regression_dict.keys())),
                'reg_pred': np.array(list(self.regression_dict.values())),
            }
            )
        # return self.df['reg_pred']
        return new_df
