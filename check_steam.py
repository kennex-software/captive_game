#! python 3
# kennex
# This file is a list of functions required to check and alter steam achievements and stats

def create_steam_achievements_list(gs, steamworks):
    # Required code for Steam Achievements
    """Function pulls Steam Achievements and indexes them
    This function is not used in the program, but this should be executed every time new achievements are made to verify their order.
    """
    achievement_range = steamworks.UserStats.GetNumAchievements()
    for index, achievement in enumerate(range(achievement_range)):
        gs.achievement_list.append(steamworks.UserStats.GetAchievementName(achievement))
    print(gs.achievement_list)

def check_set_achievement(steamworks, achievement_id):
    """Function to check achievement and set it achieved"""
    if not steamworks.UserStats.GetAchievement(achievement_id):
        steamworks.UserStats.SetAchievement(achievement_id)
        steamworks.UserStats.StoreStats()
        print(str(achievement_id) + ' unlocked') # todo comment this out

def check_set_stats(steamworks, stat_id, value_to_add):
    """Function to check achievement and set it achieved"""
    steamworks.UserStats.RequestCurrentStats()
    #print(steamworks.UserStats.GetStatInt(stat_id))
    added_amount = value_to_add + steamworks.UserStats.GetStatInt(stat_id)
    steamworks.UserStats.SetStat(stat_id, added_amount)
    #print(steamworks.UserStats.SetStat(stat_id, added_amount))
    #print(steamworks.UserStats.GetStatInt(stat_id))
    steamworks.UserStats.StoreStats()
    #print('1 added to ' + str(stat_id) + ' stat') # todo comment this out