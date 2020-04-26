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

def check_set_achievement(steamworks, achievement_id):
    """Function to check achievement and set it achieved"""
    if not steamworks.UserStats.GetAchievement(achievement_id):
        steamworks.UserStats.SetAchievement(achievement_id)
        steamworks.UserStats.StoreStats()
        print(str(achievement_id) + ' unlocked') # todo comment this out