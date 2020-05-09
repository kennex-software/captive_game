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
        #print(str(achievement_id) + ' unlocked') # todo comment this out

def set_escaped_stat(steamworks, stat_id, value_to_add):
    """Function to check achievement and set it achieved"""
    steamworks.UserStats.RequestCurrentStats()
    #print(steamworks.UserStats.GetStatInt(stat_id))


    #print(steamworks.UserStats.SetStat(stat_id, added_amount))
    #print(steamworks.UserStats.GetStatInt(stat_id))
    steamworks.UserStats.StoreStats()
    #print('1 added to ' + str(stat_id) + ' stat') # todo comment this out

def check_set_stats(steamworks, gs, value_to_add_escaped):
    """Function to check achievement and set it achieved"""
    steamworks.UserStats.RequestCurrentStats()
    current_best_time = steamworks.UserStats.GetStatFloat(b'STAT_BEST_TIME')
    current_worst_time = steamworks.UserStats.GetStatFloat(b'STAT_WORST_TIME')
    current_best_clicks = steamworks.UserStats.GetStatInt(b'STAT_BEST_CLICKS')
    escaped_added_amount = value_to_add_escaped + steamworks.UserStats.GetStatInt(b'STAT_TIMES_ESCAPED')
    time_in_minutes = float(round((gs.current_time / 1000) / 60, 2))
    print('Current Time in Minutes: ' + str(time_in_minutes))
    print('Current Best Time in Minutes: ' + str(current_best_time))
    print('Current Worst Time in Minutes: ' + str(current_worst_time))
    print('Current Best Clicks: ' + str(current_best_clicks))

    if current_best_time > time_in_minutes:
        steamworks.UserStats.SetStat(b'STAT_BEST_TIME', time_in_minutes)
    elif current_best_time == 0:
        steamworks.UserStats.SetStat(b'STAT_BEST_TIME', time_in_minutes)

    if current_worst_time < time_in_minutes:
        steamworks.UserStats.SetStat(b'STAT_WORST_TIME', time_in_minutes)

    if gs.game_clicks < current_best_clicks:
        steamworks.UserStats.SetStat(b'STAT_BEST_CLICKS', gs.game_clicks)
    elif current_best_clicks == 0:
        steamworks.UserStats.SetStat(b'STAT_BEST_CLICKS', gs.game_clicks)

    steamworks.UserStats.SetStat(b'STAT_TIMES_ESCAPED', escaped_added_amount)


    steamworks.UserStats.StoreStats()

    current_best_time = steamworks.UserStats.GetStatFloat(b'STAT_BEST_TIME')
    current_worst_time = steamworks.UserStats.GetStatFloat(b'STAT_WORST_TIME')
    current_best_clicks = steamworks.UserStats.GetStatInt(b'STAT_BEST_CLICKS')
    times_escaped = steamworks.UserStats.GetStatInt(b'STAT_TIMES_ESCAPED')
    print('Current Time in Minutes: ' + str(time_in_minutes))
    print('Current Best Time in Minutes: ' + str(current_best_time))
    print('Current Worst Time in Minutes: ' + str(current_worst_time))
    print('Current Best Clicks: ' + str(current_best_clicks))
    print('Times Escaped: ' + str(times_escaped))