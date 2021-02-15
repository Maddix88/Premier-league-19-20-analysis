# -*- coding: utf-8 -*-
"""
Created on Wed Nov 11 06:56:50 2020

@author: jimma
"""
import pandas as pd

#import csv file
PATH = "../Data collected\premier_league_player_db.csv"
df = pd.read_csv(PATH)

#only include players that made any appearances during the 2019/2020 season
df2 = df[df["Appearances"] > 0]

#change column names to make them more user friendly
df2 = df2.rename(columns = {"Clean sheets":"Clean_sheets", "Goals conceded":"Goals_conceded",\
                               "Tackle success (%)":"Tackle_success_perc", "Last man tackles":"Last_man_tackles",\
                               "Blocked shots":"Blocked_shots", "Headed clearances":"Headed_clearances",\
                               "Clearances off the line":"Clearances_off_the_line", "Duels won":"Duels_won",\
                               "Duels lost":"Duels_lost", "Successful 50/50s":"Successful_50_50s",\
                               "Aerial battles won":"Aerial_battles_won", "Aerial battles lost":\
                               "Aerial_battles_lost", "Own goals":"Own_goals", "Errors leading to goals":\
                               "Errors_leading_to_goals", "Goals per match": "Goals_per_match", "Headed goals":\
                               "Headed_goals", "Goals with right foot":"Goals_with_right_foot",\
                               "Goals with left foot":"Goals_with_left_foot", "Penalties scored":\
                               "Penalties_scored", "Free-kicks scored":"Freekicks_scored", "Shots on target":\
                               "Shot_on_target", "Shot accuracy":"Shot_accuracy", "Hit the woodwork":\
                               "Hit_the_woodwork", "Big chances missed":"Big_chances_missed", "Yellow cards":\
                               "Yellow_cards", "Red cards": "Red_cards", "Fouls commited":"Fouls_commited",\
                               "Passes per match":"Passes_per_match", "Big chances created":\
                               "Big_chances_created", "Cross accuracy (%)":"Cross_accuracy_perc",\
                               "Through balls":"Through_balls", "Accurate long balls":\
                               "Accurate_long_balls"})

#remove any characters from columns so that columns can be converted to integers
df2["Tackle_success_perc"] = df2.Tackle_success_perc.apply(lambda x: x.replace("%",""))
df2["Shot_accuracy"] = df2.Shot_accuracy.apply(lambda x: x.replace("%",""))
df2["Cross_accuracy_perc"] = df2.Cross_accuracy_perc.apply(lambda x: x.replace("%",""))
df2["Passes"] = df2.Passes.apply(lambda x: x.replace(",",""))

#drop "Unnamed: 0" column
df2 = df2.drop(columns="Unnamed: 0")

#convert columns to integers or floats (avoid converting the first two columns)
for column in df2.columns[2:]:
    df2[column] = pd.to_numeric(df2[column], errors = 'coerce')

print(df2.info())

#save Dataframe as a csv file
df2.to_csv("PL_data_cleaned.csv")
