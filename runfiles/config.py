# ---------------------------------------------------------------------#
# Configuration file for running the Campbell-Diaz model and optimizer #
#                                                                      #
# Allard de Wit and Deborah Gaso Melgar, Wageningen 2020               #
#----------------------------------------------------------------------#
import sys, os
import yaml

this_dir = os.path.dirname(__file__)
top_dir = os.path.dirname(this_dir)
data_dir = os.path.join(top_dir, "data")


# ------- SETTINGS FOR CAMPBELL-DIAZ MODEL --------
# Weather data

weather_fname = os.path.join(data_dir, "weather_data.xls")


# model parameters
crop_fname = os.path.join(data_dir, "wofost_soybean_parameters.dat")
soil_fname = os.path.join(data_dir, "soil_parameters.dat")

# agromanagement
agromanagement = """

2018:
    campaign_start_date: 2018-06-04
    crop_start_date: 2018-06-04
    crop_end_date: 2018-10-06
2019:
    campaign_start_date: 2019-04-25
    crop_start_date: 2019-04-25
    crop_end_date: 2019-10-10
2020:
    campaign_start_date: 2020-05-06
    crop_start_date: 2020-05-06
    crop_end_date: 2020-10-10
"""
agromanagement = yaml.safe_load(agromanagement)


