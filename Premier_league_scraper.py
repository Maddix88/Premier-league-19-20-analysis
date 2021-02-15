# -*- coding: utf-8 -*-
"""
Created on Mon Sep  7 15:55:14 2020

@author: jimma
"""
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException, \
                                       StaleElementReferenceException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

def premier_league_scraper():
    """Create a function that accesses the players section of the Premier league website,
    scrapes the data for each player from the 2019/2020 season, such as goals and clearances, 
    and stores the data as a DataFrame and saves that Dataframe as a csv file. This was created
    in October 2020 and has not been modified for bugs since."""
    
    #Access the chrome driver that allows the automated navigation of Chrome.
    #Chromedriver must be installed to your computer before you can access it via your directory below 
    PATH = "directory-PATH\chromedriver.exe"
    browser = webdriver.Chrome(PATH)
    
    #access the website below using .get (I accessed "https://www.premierleague.com/players?se=274&cl=-1")
    browser.get("ENTER WEBSITE HERE")

    #Allow time for the page to load
    time.sleep(5)

    #Test for the "Cookies" prompt and get rid of it.
    try:
        browser.find_element_by_css_selector('[role="btn"]').click() 
        print('Cookie removed')
    except NoSuchElementException:
        print('Clicking cookie failed')
        pass
    #remove any adverts that is preventing access to the website
    time.sleep(0.5)
    try:
        browser.find_element_by_class_name('closeBtn').click() 
        print('Advert removed')
    except ElementNotInteractableException:
        print('Advert not present')
        pass

    #scroll to the bottom of the page so all of the player links are loaded
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(20)

    #Locate link to player pages and append to links
    links = []
    try:
        player_names = WebDriverWait(browser, 30).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "playerName")))
    except NoSuchElementException:
        print("Error")
    
    time.sleep(2)
    for name in player_names:
        try:
            links.append(name.get_attribute('href'))
            print(name.get_attribute('href'))
        except StaleElementReferenceException:
            print("ERROR")
            
    #Links list now has a link to each player's personal page

    time.sleep(2) 
#*************************************ITERATE THROUGH EACH PLAYER LINK AND NAME************************************
    player_db = []
    #player_db will be the list that contains all of the player data as dictionaries
    
    for link in links:
        browser.get(link) #access player's webpage
        time.sleep(1)
        
        #allow removal of advert that may be present
        try:
            browser.find_element_by_class_name('closeBtn').click() 
            print('Advert removed')
        except ElementNotInteractableException:
            print('Advert not present')
            pass
        
        #Access player's name on the player's initial page
        try:
            Name = browser.find_element_by_xpath(\
                           "//div[@class='name t-colour']").text
        except NoSuchElementException:
            Name = " "

        #Access player's club during 2019/2020 season (there may be more than one)
        clubs = []
        for line in browser.find_elements_by_class_name('table'):
            if line.find_element_by_class_name('season').text == "2019/2020":
                clubs.append(line.find_element_by_class_name('long').text)
            else:
                continue
        
        #Access the "Stats" tab to find player's stats for that season
        try:
            stats_tab = WebDriverWait(browser, 30).until(
                EC.element_to_be_clickable((By.XPATH, "//a[@href='stats']")))
            stats_tab.click()
        except NoSuchElementException:
            print("Could not find tab element for " + Name)
            continue
        time.sleep(2)
        
        #Access filter tab to specify league season year (2019/2020)
        try:
            filter_button = WebDriverWait(browser, 30).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-dropdown-current=compSeasons]")))
            filter_button.click()
        except NoSuchElementException:
            print("Could not find element for " + Name)
            continue
        except TimeoutException:
            print("WebDriverWait timed out for " + Name)
            #Webdriver timed out at this point for some players so I have just repeated the request
            browser.get(link) #link to each player's webpage
            time.sleep(1)
            try:
                browser.find_element_by_class_name('closeBtn').click() 
                print('Advert removed')
            except ElementNotInteractableException:
                print('Advert not present')
                pass
        
            #Access player's name
            try:
                Name = browser.find_element_by_xpath(\
                                                     "//div[@class='name t-colour']").text
            except NoSuchElementException:
                Name = " "

            #Access the "Stats" tab
            try:
                stats_tab = WebDriverWait(browser, 30).until(
                    EC.element_to_be_clickable((By.XPATH, "//a[@href='stats']")))
                stats_tab.click()
            except NoSuchElementException:
                print("Could not find element for " + Name)
                continue
        
        #Once tab has been accessed, specify the year required (i.e.2019/2020)
        try:
            season = WebDriverWait(browser, 30).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-option-name="2019/20"]')))
            season.click()
        except NoSuchElementException:
            print("Could not find element for " + Name)
            continue
        except TimeoutException:
            print("WebDriverWait timed out for " + Name)
            continue
        
        time.sleep(2)
        
        #Find player's performance data and save to corresponding variables.
        #Some values aren't available for some of the players
        try:
            appearances = browser.find_element_by_xpath(\
                           "//span[@class='allStatContainer statappearances']").text
        except NoSuchElementException:
            appearances = "No value"
            
        try:
            wins = browser.find_element_by_xpath(\
                           "//span[@class='allStatContainer statwins']").text
        except NoSuchElementException:
            wins = "No value"
            
        try:
            losses = browser.find_element_by_xpath(\
                           "//span[@class='allStatContainer statlosses']").text
        except NoSuchElementException:
            losses = "No value"
            
        try:
            clean_sheets = browser.find_element_by_xpath(\
                           "//span[@class='allStatContainer statclean_sheet']").text
        except NoSuchElementException:
            clean_sheets = "No value"
    
        try:
            goals_conceded = browser.find_element_by_xpath(\
                             "//span[@class='allStatContainer statgoals_conceded']").text
        except NoSuchElementException:
            goals_conceded = "No value"
    
        try:
            tackles = browser.find_element_by_xpath(\
                              "//span[@class='allStatContainer stattotal_tackle']").text
        except NoSuchElementException:
            tackles = "No value"
    
        try:
            tackle_success_perc = browser.find_element_by_xpath(\
                                          "//span[@class='allStatContainer stattackle_success']").text
        except NoSuchElementException:
            tackle_success_perc = "No value"
            
        try:
            last_man_tackles = browser.find_element_by_xpath(\
                                       "//span[@class='allStatContainer statlast_man_tackle']").text
        except NoSuchElementException:
            last_man_tackles = "No value"
        
        try:
            blocked_shots = browser.find_element_by_xpath(\
                                    "//span[@class='allStatContainer statblocked_scoring_att']").text
        except NoSuchElementException:
            blocked_shots = "No value"
            
        try:
            interceptions = browser.find_element_by_xpath(\
                                    "//span[@class='allStatContainer statinterception']").text
        except NoSuchElementException:
            interceptions = "No value"   
        
        try:
            clearances = browser.find_element_by_xpath(\
                                 "//span[@class='allStatContainer stattotal_clearance']").text
        except NoSuchElementException:
            clearances = "No value"
            
        try:
            headed_clearances = browser.find_element_by_xpath(\
                                        "//span[@class='allStatContainer stateffective_head_clearance']").text
        except NoSuchElementException:
            headed_clearances = "No value"
            
        try:
            clearances_off_line = browser.find_element_by_xpath(\
                                        "//span[@class='allStatContainer statclearance_off_line']").text
        except NoSuchElementException:
            clearances_off_line = "No value"
            
        try:
            recoveries = browser.find_element_by_xpath(\
                                        "//span[@class='allStatContainer statball_recovery']").text
        except NoSuchElementException:
            recoveries = "No value"
            
        try:
            duels_won = browser.find_element_by_xpath(\
                                        "//span[@class='allStatContainer statduel_won']").text
        except NoSuchElementException:
            duels_won = "No value"
        
        try:
            duels_lost = browser.find_element_by_xpath(\
                                        "//span[@class='allStatContainer statduel_lost']").text
        except NoSuchElementException:
            duels_lost = "No value"
            
        try:
            successful_50_50s = browser.find_element_by_xpath(\
                                        "//span[@class='allStatContainer statwon_contest']").text
        except NoSuchElementException:
            successful_50_50s = "No value"
            
        try:
            aerial_battles_won = browser.find_element_by_xpath(\
                                        "//span[@class='allStatContainer stataerial_won']").text
        except NoSuchElementException:
            aerial_battles_won = "No value"
            
        try:
            aerial_battles_lost = browser.find_element_by_xpath(\
                                        "//span[@class='allStatContainer stataerial_lost']").text
        except NoSuchElementException:
            aerial_battles_lost = "No value"
            
        try:
            own_goals = browser.find_element_by_xpath(\
                                        "//span[@class='allStatContainer statown_goals']").text
        except NoSuchElementException:
            own_goals = "No value"
        
        try:
            errors_leading_to_goals = browser.find_element_by_xpath(\
                                        "//span[@class='allStatContainer staterror_lead_to_goal']").text
        except NoSuchElementException:
            errors_leading_to_goals = "No value"
            
        try:
            goals = browser.find_element_by_xpath(\
                                        "//span[@class='allStatContainer statgoals']").text
        except NoSuchElementException:
            goals = "No value"
            
        try:
            goals_per_match = browser.find_element_by_xpath(\
                                        "//span[@class='allStatContainer statgoals_per_game']").text
        except NoSuchElementException:
            goals_per_match = "No value"
            
        try:
            headed_goals = browser.find_element_by_xpath(\
                                        "//span[@class='allStatContainer statatt_hd_goal']").text
        except NoSuchElementException:
            headed_goals = "No value"
        
        try:
            goals_with_right_foot = browser.find_element_by_xpath(\
                                        "//span[@class='allStatContainer statatt_rf_goal']").text
        except NoSuchElementException:
            goals_with_right_foot = "No value"
            
        try:
            goals_with_left_foot = browser.find_element_by_xpath(\
                                        "//span[@class='allStatContainer statatt_lf_goal']").text
        except NoSuchElementException:
            goals_with_left_foot = "No value"
            
        try:
            penalties_scored = browser.find_element_by_xpath(\
                                        "//span[@class='allStatContainer statatt_pen_goal']").text
        except NoSuchElementException:
            penalties_scored = "No value"
            
        try:
            freekicks_scored = browser.find_element_by_xpath(\
                                        "//span[@class='allStatContainer statatt_freekick_goal']").text
        except NoSuchElementException:
            freekicks_scored = "No value"
            
        try:
            shots = browser.find_element_by_xpath(\
                                        "//span[@class='allStatContainer stattotal_scoring_att']").text
        except NoSuchElementException:
            shots = "No value"
            
        try:
            shots_on_target = browser.find_element_by_xpath(\
                                        "//span[@class='allStatContainer statontarget_scoring_att']").text
        except NoSuchElementException:
            shots_on_target = "No value"
            
        try:
            shot_accuracy = browser.find_element_by_xpath(\
                                        "//span[@class='allStatContainer statshot_accuracy']").text
        except NoSuchElementException:
            shot_accuracy = "No value"
            
        try:
            hit_woodwork = browser.find_element_by_xpath(\
                                        "//span[@class='allStatContainer stathit_woodwork']").text
        except NoSuchElementException:
            hit_woodwork = "No value"
            
        try:
            big_chances_missed = browser.find_element_by_xpath(\
                                        "//span[@class='allStatContainer statbig_chance_missed']").text
        except NoSuchElementException:
            big_chances_missed = "No value"
            
        try:
            yellow_cards = browser.find_element_by_xpath(\
                                        "//span[@class='allStatContainer statyellow_card']").text
        except NoSuchElementException:
            yellow_cards = "No value"
            
        try:
            red_cards = browser.find_element_by_xpath(\
                                        "//span[@class='allStatContainer statred_card']").text
        except NoSuchElementException:
            red_cards = "No value"
            
        try:
            fouls = browser.find_element_by_xpath(\
                                        "//span[@class='allStatContainer statfouls']").text
        except NoSuchElementException:
            fouls = "No value"
            
        try:
            offsides = browser.find_element_by_xpath(\
                                        "//span[@class='allStatContainer stattotal_offside']").text
        except NoSuchElementException:
            offsides = "No value"
            
        try:
            assists = browser.find_element_by_xpath(\
                                        "//span[@class='allStatContainer statgoal_assist']").text
        except NoSuchElementException:
            assists = "No value"
            
        try:
            passes = browser.find_element_by_xpath(\
                                        "//span[@class='allStatContainer stattotal_pass']").text
        except NoSuchElementException:
            passes = "No value"
            
        try:
            passes_per_match = browser.find_element_by_xpath(\
                                        "//span[@class='allStatContainer stattotal_pass_per_game']").text
        except NoSuchElementException:
            passes_per_match = "No value"
            
        try:
            big_chances_created = browser.find_element_by_xpath(\
                                        "//span[@class='allStatContainer statbig_chance_created']").text
        except NoSuchElementException:
            big_chances_created = "No value"
            
        try:
            crosses = browser.find_element_by_xpath(\
                                        "//span[@class='allStatContainer stattotal_cross']").text
        except NoSuchElementException:
            crosses = "No value"
            
        try:
            cross_accuracy = browser.find_element_by_xpath(\
                                        "//span[@class='allStatContainer statcross_accuracy']").text
        except NoSuchElementException:
            cross_accuracy = "No value"
            
        try:
            through_balls = browser.find_element_by_xpath(\
                                        "//span[@class='allStatContainer stattotal_through_ball']").text
        except NoSuchElementException:
            through_balls = "No value"  
            
        try:
            accurate_long_balls = browser.find_element_by_xpath(\
                                        "//span[@class='allStatContainer stataccurate_long_balls']").text
        except NoSuchElementException:
            accurate_long_balls = "No value"
        
        #confirm that performance data has been obtained for that player...
        print("Obtained data for " + Name)
    
        #append player's data onto the player_db list
        player_db.append({"Name": Name,
                          "club": clubs,
                         "Appearances": appearances,
                         "Wins": wins,
                         "Losses": losses,
                         "Clean sheets": clean_sheets,
                         "Goals conceded": goals_conceded,
                         "Tackles": tackles,
                         "Tackle success (%)": tackle_success_perc,
                         "Last man tackles": last_man_tackles,
                         "Blocked shots": blocked_shots,
                         "Interceptions": interceptions,
                         "Clearances": clearances,
                         "Headed clearances": headed_clearances,
                         "Clearances off the line": clearances_off_line,
                         "Recoveries": recoveries,
                         "Duels won": duels_won,
                         "Duels lost": duels_lost,
                         "Successful 50/50s": successful_50_50s,
                         "Aerial battles won": aerial_battles_won,
                         "Aerial battles lost": aerial_battles_lost,
                         "Own goals": own_goals,
                         "Errors leading to goals": errors_leading_to_goals,
                         "Goals": goals,
                         "Goals per match": goals_per_match,
                         "Headed goals": headed_goals,
                         "Goals with right foot": goals_with_right_foot,
                         "Goals with left foot": goals_with_left_foot,
                         "Penalties scored": penalties_scored,
                         "Free-kicks scored": freekicks_scored,
                         "Shots": shots,
                         "Shots on target": shots_on_target,
                         "Shot accuracy": shot_accuracy,
                         "Hit the woodwork": hit_woodwork,
                         "Big chances missed": big_chances_missed,
                         "Yellow cards": yellow_cards,
                         "Red cards": red_cards,
                         "Fouls commited": fouls,
                         "Offsides": offsides,
                         "Assists": assists,
                         "Passes": passes,
                         "Passes per match": passes_per_match,
                         "Big chances created": big_chances_created,
                         "Crosses": crosses,
                         "Cross accuracy (%)": cross_accuracy,
                         "Through balls": through_balls,
                         "Accurate long balls": accurate_long_balls})
        time.sleep(1)
    #return the player_db list as a Dataframe. 
    #player_db should now contain performance data from every player during the 2019/2020 season
    return pd.DataFrame(player_db) 

#save function to a variable and save that variable as a csv file, ready to start the cleaning process
df = premier_league_scraper()
print(df.head())
df.to_csv("premier_league_player_db.csv")
    

    

    


    



