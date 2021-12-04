# -*- coding: utf-8 -*-
# Copyright (c) 2020 Wageningen-UR
# Deborah Gaso Melgar and Allard de Wit, June 2020

import sys, os
this_dir = os.getcwd()
up_dir = os.path.dirname(this_dir)
if not up_dir in sys.path:
    sys.path.append(up_dir)
    
import datetime as dt
import yaml
import pandas as pd
import numpy as np
import matplotlib
#matplotlib.style.use("ggplot")
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.gridspec as gridspec

from pcse.fileinput import ExcelWeatherDataProvider, PCSEFileReader
from pcse.base import ParameterProvider
from campbell_diaz.model import CampbellDiazModel
#from runfiles import config
from runfiles import config


from matplotlib import rc
rc('mathtext', default='regular')

def make_agromanagement(year):
    
    start_dates = dict()

#Nebraska

    start_dates[2018] = dict(campaign_start_date=dt.date(2018,6,4),
                     crop_start_date=dt.date(2018,6,4),
                     crop_end_date=dt.date(2018,10, 20))
    start_dates[2019] = dict(campaign_start_date=dt.date(2019,4,25),
                         crop_start_date=dt.date(2019,4,25),
                         crop_end_date=dt.date(2019, 10, 1))
    start_dates[2020] = dict(campaign_start_date=dt.date(2020, 4,20),
                         crop_start_date=dt.date(2020,4,20),
                         crop_end_date=dt.date(2020, 10, 10))

    campaign_dates = start_dates[year]
    agromanagement = """
    - {campaign_start_date}:
        CropCalendar:
            crop_name: Soybean 
            variety_name: Soybean 
            crop_start_date: {crop_start_date}
            crop_start_type: sowing
            crop_end_date: {crop_end_date}
            crop_end_type: harvest
            max_duration: 300
        TimedEvents:
        StateEvents:
        """
    agro = yaml.safe_load(agromanagement.format(**campaign_dates))
    return agro

def main():
    
    agro=make_agromanagement(2019)

    weather_data = ExcelWeatherDataProvider(config.weather_fname)

    cropd = PCSEFileReader(config.crop_fname)
    soild = PCSEFileReader(config.soil_fname)
    params = ParameterProvider(cropdata=cropd, soildata=soild,sitedata={})
#    params.set_override(varname='WUE', value=0.5,check=True)

    model = CampbellDiazModel(params, weather_data, agro)
    model.run_till_terminate()
    output=model.get_output()
    
    df = pd.DataFrame(model.get_output()).set_index("day")
#
#    # Plot results
    # fig, axes = plt.subplots(nrows=3, ncols=4, figsize=(8,8))
    # for key, axis in zip(df.columns, axes.flatten()):
    #     df[key].plot(ax=axis, title=key)
    # fig.autofmt_xdate()
#    fig.savefig(os.path.join(this_dir, "output", "Campbell_soybean.png"))
#
#    csv_fname = os.path.join(this_dir, "output", "Campbell_soybean.csv")
#    df.to_csv(csv_fname, header=True)
#    
#    #Plot with field data
#    obs=pd.read_csv('C:\\Users\\gaso001\\Thesis\\deborah_phd\\data\\field\\2014.csv')
#    
#    obs.index = pd.to_datetime(obs.day)
#    combined = obs.join(df, how="right", rsuffix="_sim")
#
#    fig, axes = plt.subplots(figsize=(8,8))
#    axes.plot_date(combined.index,combined.LAI, "or",label="Observed LAI")
#    axes.plot_date(combined.index,combined.LAI_sim, "-b",label="Simulated LAI")
#    axes.set_ylim(0,12)
#    axes.tick_params(axis='both', which='major', labelsize=18)
#    plt.xticks(rotation=45, ha='right',fontsize=14)
#    fig.suptitle("LAI [ m-2 m-2]", fontsize=20)
#    axes.set_ylabel("LAI [ m-2 m-2]", fontsize=20)
#    fig.legend()
#    
#    time = combined.index
#    data1= combined.LAI_sim
#    data2 = combined.TDM_sim*10000
#    data3 = combined.LAI*0.85
#    data4 = combined.TDM
#    data5 = combined.YIELD
#    data6 = combined.YIELD_sim*10000
#    
#    fig = plt.figure()
#    ax = fig.add_subplot(111)
#    
#    lns1 = ax.plot(time, data2, '-b', label = 'TDMsim')
#    lns4 = ax.plot(time, data4, 'ob', label = 'TDMobs')
#    lns6 = ax.plot(time, data6, '-r', label = 'YIELDsim')
#    lns5 = ax.plot(time, data5, 'or', label = 'YIELDobs')
#    plt.yticks(fontsize=14)   
#    plt.xticks(rotation=45, ha='right',fontsize=14)
#    ax2 = ax.twinx()
#    lns2 = ax2.plot(time, data3, 'og', label = 'LAIobs')
#    lns3 = ax2.plot(time, data1, '-g', label = 'LAIsim')
#    
#    
#    # added these three lines
#    lns = lns3+lns1+lns6+lns2+lns4+lns5
#    labs = [l.get_label() for l in lns]
#    ax.legend(lns, labs, bbox_to_anchor=(0.32, 0.5), loc='lower right', ncol=1,borderaxespad=1)
#    
#    #fig.legend()
#    
#    ax.grid()
#    ax.set_xlabel("Date",fontsize=14)
#    ax.set_ylabel(r"TDM and Yield (kg.ha⁻¹)",fontsize=14)
#    ax2.set_ylabel(r"LAI ($m^2$.$m^2$)",fontsize=14)
#    plt.yticks(fontsize=14)   
#    ax2.set_ylim(0, 10)
#    ax.set_ylim(0,15000)
#    fig.suptitle("2020", fontsize=18)
#    plt.show()
        

    #"LAI","FI","YIELD","TDM","W_Stress","TWC","Ta","PT","TPREC","CWDv","CWDr"
    
    
    return model,output


if __name__ == "__main__":
    model,output=main()
    
 