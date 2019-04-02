from elf_kingdom import *

# ***************************     WG"H       ***********************************

# ***************************Global variable************************************

DEBUG = True
DebugSort = True
DebugForSatla = False
mapElvesPerTurns = {}  # the targets of my elf turn before
EnemyElfLoc = {}  # the locations of enemy elf turn before
danger_elves1 = {}  # elves that in was danger turn before
loc_before_disapear = {}  # loc before enemy elf used invisibility
casting_elves = {}  # the elves that casting in this turn
lowest_time = 999  # check the lowest time remaining until the bot time out
dangerous_portal1 = {}  # danger enemy portal this turn
dangerous_elf1 = {}  # danger enemy elf this turn
Elves_invisibility_turns = {}  # expiration_turns for invisibility
if_destroy_fountain = False # if enemy destroy my fountain
ok_to_build_fountain = False # efter we stop build we want to back build  
fountains_loc = []  # my fountain pervious turn
if_enemy_summon_lava = False  #
max_fountains = 0  # max mana fountain we build all the game
alternative_way_for_elf = False  # the alternative way to run from enemy elf
enemy_go_to_my_fountain_naw = False  # enemy want go to my fountain in this turn
enemy_fountain_loc = []  # enemy fountain loc - goof places for build portal
attack = {} # key - elves , value - enemy the elves attack in this turn
sum_my_fountain = 0 # like max_fountain
sum_enemy_fountain = 0  # enemy max fountain
num_enemy_fountain = 0 # count enemy currently mana fountain
num_my_fountain = 0 # count my currently mana fountains
diagonal_line = 0 # save the diagonal of the map
list_fountain=[] # good locatio to build fountain
volcano_life = 0 # the volcano life
good_time_save_mana = False

# ***************************Code************************************

def do_turn(game):
    # ----Settings of the Game----
    global EnemyElfLoc
    global lowest_time
    global debug
    global casting_elves
    global Elves_invisibility_turns
    global dangerous_elf1
    global dangerous_portal1
    global danger_elves1
    global fountains_loc
    global if_enemy_summon_lava
    global max_fountains
    global alternative_way_for_elf
    global enemy_go_to_my_fountain_naw
    global attack
    global sum_my_fountain
    global sum_enemy_fountain
    global num_enemy_fountain
    global num_my_fountain
    global diagonal_line
    global mapElvesPerTurns
    global list_fountain
    global volcano_life
    global good_time_save_mana
    
    # ***************************Introduction************************************
    # 
    good_time_save_mana = False
    # the funny debug
    funnydebug(game, " ")

    # put the boolean values in the global vars
    alternative_way_for_elf = False
    enemy_go_to_my_fountain_naw = True
    if_enemy_destroy_my_fountain(game)
    #if enemy died we dont want that the bot crash
    for k in mapElvesPerTurns.keys():
        if mapElvesPerTurns[k] in game.get_all_enemy_elves() and not mapElvesPerTurns[k].is_alive():
            mapElvesPerTurns[k]=Location(0,0)
    #
    list_fountain=good_locations_for_building_fountain(game)
    
    # save the diagonal of the map
    if game.turn == 1:
        diagonal_line = Location(0, 0).distance(Location(game.rows, game.cols))

    # put values in all the keys for the bot will not crush
    for elf in game.get_all_my_elves():
        attack[elf] = None

    # put the enemy that my living elves attack in this turn
    for elf in game.get_my_living_elves():
        attack[elf] = try_attack(game, elf, True)

    # give the OK to summon lava - if is False we not summing
    if len(game.get_enemy_lava_giants()) > 0 or game.turn > 40:
        if_enemy_summon_lava = True

    # svae the location of the enemy mana fountain - good places for build portal
    for enemy_fountain in game.get_enemy_mana_fountains():
        if enemy_fountain.location not in enemy_fountain_loc and 3 * enemy_fountain.distance(
                game.get_enemy_castle()) < enemy_fountain.distance(game.get_my_castle()):
            enemy_fountain_loc.append(enemy_fountain.location)

    # save the casting elves and save the turns the invisibility will end
    for elf in game.get_all_my_elves():
        casting_elves[elf] = False
        if elf in Elves_invisibility_turns.keys() and Elves_invisibility_turns[elf] > 0:
            Elves_invisibility_turns[elf] -= 1

    # put values in all the keys for the bot will not crush
    for elf in game.get_all_my_elves():
        dangerous_elf1[elf] = None
        dangerous_portal1[elf] = None

    # put the dangerous portal end elf in the value of each elf
    for elf in game.get_my_living_elves():
        dangerous_elf1[elf] = None
        dangerous_portal1[elf] = None
        dangerous_portal1[elf] = dangerous_portal(game, elf)
        dangerous_elf1[elf] = dangerous_elf(game, elf)

    # count my max mana fountain all the game
    for elf in game.get_my_living_elves():
        if elf.currently_building == "ManaFountain" and elf.turns_to_build == 1:
            max_fountains += 1

    # how match the fountain was build
    if num_my_fountain < len(game.get_my_mana_fountains()):
        sum_my_fountain += (len(game.get_my_mana_fountains()) - num_my_fountain)
    if num_enemy_fountain < len(game.get_enemy_mana_fountains()):
        sum_enemy_fountain += (len(game.get_enemy_mana_fountains()) - num_enemy_fountain)

    # the sort debug
    sortdebug(game, "how many times enemy build mana fountain = " + str(sum_enemy_fountain))
    sortdebug(game, "how many times I build mana fountain = " + str(sum_my_fountain))

    # dictionary of each elf and his target in ths turn
    mapElves = {}

    # Divides the mana:
    sortdebug(game, " ")

    # vars for "what to creat"
    priority_portal = need_portal(game, True, mapElves) # num of priority for portal
    priority_fauntain = need_fauntain(game, True, mapElves) # num of priority for mana fountain
    mapElves = SortElves(game, priority_fauntain, priority_portal) # get the elves and his targets
    priority_speed_up = handle_speed_up_spell(game, mapElves, True) # num of priority for speed up
    priority_invisibility = handel_invisibility_spell(game, mapElves, True) # num of priority for invisibility
    # to save the time remaining
    if game.get_my_portals():
        priority_Ice = handle_portalsIce(game, True, 0) # num of priority for ice
        priority_lava = handle_portalsLava(game, True, 0) # num of priority for lava
        priority_tornado = handel_portalsTorndo(game, True, 0, priority_portal) # num of priority for tornado
    else:
        priority_Ice = 100
        priority_lava = 100
        priority_tornado = 100
    # Save Special mana if nead
    sper_mana = 0
    if priority_speed_up != 100:
        sper_mana += game.speed_up_cost
    if priority_invisibility != 100:
        sper_mana += game.invisibility_cost
    if priority_tornado == 1:
        sper_mana += game.tornado_cost
    if priority_fauntain == 0:
        sper_mana += game.mana_fountain_cost
    # regular debug
    debug(game, " ")
    debug(game, "                         *****MANA*****")
    debug(game, " ")

    # Using the mana
    WhatToCreate(game, mapElves, priority_Ice, priority_portal, priority_fauntain, priority_lava, priority_speed_up,priority_invisibility, priority_tornado, [], sper_mana)

    # Sending the elves to their destinations:
    for elf in game.get_my_living_elves():
        if casting_elves[elf] == False:
            if not elf.is_building:
                if need_run(game, elf) is None:
                    if not try_attack(game, elf, False):
                        if elf in mapElves.keys():
                            if when_I_go_to_alternative_way(game, elf, mapElves[elf]) == False:
                                elf.move_to(mapElves[elf])
                            else:
                                elf.move_to(alternative_way(game, elf, mapElves[elf]))
                        else:
                            elf.move_to(game.get_enemy_castle())
                else:
                    mapElvesPerTurns[elf] = elf
                    elf.move_to(run(game, elf, mapElves))

    # put the enemy elves locations in the end of the turn
    for elf in game.get_enemy_living_elves():
        EnemyElfLoc[elf] = elf.location
    
    # put the volcano life
    if game.get_active_volcanoes():
        for enemy in game.get_enemy_living_elves():
            ev = sorted(game.get_active_volcanoes(),key  = lambda e:e.distance(enemy))
            volcano_life = ev[0].current_health
    # my elf that die - his danger equal to None
    for elf in game.get_all_my_elves():
        if not elf.is_alive():
            danger_elves1[elf] = None

    # the time until the bot crushed
    if lowest_time > game.get_time_remaining():
        lowest_time = game.get_time_remaining()

    # Save my mana fountain locations
    for mana_fountains in game.get_my_mana_fountains():
        fountains_loc.append(mana_fountains.location)

    # the count of my and enemy fountain in the end of the turn
    num_my_fountain = len(game.get_my_mana_fountains())
    num_enemy_fountain = len(game.get_enemy_mana_fountains())

    sortdebug(game, "time remaining : " + str(lowest_time))
    
#***************************Mana************************************

def WhatToCreate(game,mapElves,priority_Ice,priority_portal,priority_fauntain,priority_lava,priority_speed_up,priority_invisibility,priority_tornado,without,sper_mana):
    #useful vars
    more_priority = True
    fountain_mana_to_check_more = game.mana_fountain_cost + game.lava_giant_cost
    portal_mana_to_check_more = game.portal_cost + game.lava_giant_cost
    # finish the game:
    if priority_lava == 0 and more_priority:
        debug(game, "finish the game")
        more_priority = handle_portalsLava(game,False,sper_mana)
    # to came enemy castle faster 
    if priority_speed_up == 1 and more_priority:
        debug(game, "Speed up")
        more_priority = handle_speed_up_spell(game,mapElves,False)
    # to hide from enemies 
    if priority_invisibility == 1 and more_priority:
        debug(game, "invisibility")
        more_priority = handel_invisibility_spell(game,mapElves,False)
    # destroy enemy portal before enemy destroy my
    if priority_tornado==1 and more_priority and game.get_my_mana()>=sper_mana:
        debug(game,"need tornado to enemy building")
        more_priority=handel_portalsTorndo(game,False,sper_mana,priority_portal)
    # we loosing
    if priority_Ice == 3 and more_priority and game.get_my_mana() >= sper_mana:
        debug(game, "We loosing - deafence")
        more_priority = handle_portalsIce(game,False,sper_mana)
    # destroy enemy portal before enemy destroy my
    if priority_tornado==0 and more_priority and game.get_my_mana()>=sper_mana:
        debug(game,"need tornado to enemy building")
        more_priority=handel_portalsTorndo(game,False,sper_mana,priority_portal)
    # we need'nt deafence and to come enemy castle - we fight
    if priority_tornado==100 and priority_Ice == 100 and priority_portal == 100 and priority_fauntain == 100 and more_priority and game.get_my_mana() >= sper_mana and if_enemy_summon_lava:
        debug(game, "There is no somnething else so - attack ")
        more_priority = handle_portalsLava(game,False,sper_mana)
    # we need protect portal or elf  
    if (priority_Ice == 1) and more_priority and game.get_my_mana() >= sper_mana:
        debug(game, "Protect portal or elf")
        more_priority = handle_portalsIce(game,False,sper_mana)
    #
    if (priority_portal == 1) and more_priority and "portal" not in without and game.get_my_mana() >= sper_mana:
        debug(game, "Build portal")
        more_priority = need_portal(game,False,mapElves)
        if game.get_my_mana() > portal_mana_to_check_more+sper_mana:
            without.append("portal")
            WhatToCreate(game,mapElves,priority_Ice,priority_portal,priority_fauntain,priority_lava,priority_speed_up,priority_invisibility,priority_tornado,without,game.portal_cost+sper_mana)
    # we need protect portal or elf  
    if (priority_Ice == 1 or priority_Ice == 2) and more_priority and game.get_my_mana() >= sper_mana:
        debug(game, "Protect portal or elf")
        more_priority = handle_portalsIce(game,False,sper_mana)
    # destroy enemy fountain 
    if priority_tornado==2 and more_priority and game.get_my_mana()>=sper_mana:
        debug(game,"need tornado to enemy building")
        more_priority=handel_portalsTorndo(game,False,sper_mana,priority_portal)
    # enemy per turn more my per turn 
    if (priority_fauntain == 1) and more_priority and "mana_fountain" not in without and game.get_my_mana() >= sper_mana:
        debug(game,"want to build mama fauntain")
        more_priority = need_fauntain(game,False,mapElves)
        if game.get_my_mana() > fountain_mana_to_check_more+sper_mana:
            without.append("mana_fountain")
            WhatToCreate(game,mapElves,priority_Ice,priority_portal,priority_fauntain,priority_lava,priority_speed_up,priority_invisibility,priority_tornado,without,game.mana_fountain_cost+sper_mana)
    # build next to fountain
    if (priority_portal == 2 or priority_portal==3) and more_priority and "portal" not in without and game.get_my_mana() >= sper_mana:
        debug(game, "Build portal")
        more_priority = need_portal(game,False,mapElves)
        if game.get_my_mana() > portal_mana_to_check_more+sper_mana:
            without.append("portal")
            WhatToCreate(game,mapElves,priority_Ice,priority_portal,priority_fauntain,priority_lava,priority_speed_up,priority_invisibility,priority_tornado,without,game.portal_cost+sper_mana)
    # same per turn 
    if priority_fauntain == 2 and more_priority and "mana_fountain" not in without and game.get_my_mana() >= sper_mana:
        debug(game,"want to build mama fauntain")
        more_priority = need_fauntain(game,False,mapElves)
        if game.get_my_mana() > fountain_mana_to_check_more+sper_mana:
            without.append("mana_fountain")
            WhatToCreate(game,mapElves,priority_Ice,priority_portal,priority_fauntain,priority_lava,priority_speed_up,priority_invisibility,priority_tornado,without,game.mana_fountain_cost+sper_mana)
    # to save elf from ice
    if priority_lava == 1 and more_priority and game.get_my_mana() >= sper_mana and if_enemy_summon_lava:
        debug(game, "Save elf from ice")
        more_priority = handle_portalsLava(game,False,sper_mana)
    # we need help for good fight or to come neer to enemy  
    if priority_portal != 100 and more_priority and "portal" not in without and game.get_my_mana() >= sper_mana:
        debug(game, "Improve fight or improve attack")
        more_priority = need_portal(game,False,mapElves)
        if game.get_my_mana() > portal_mana_to_check_more+sper_mana:
            without.append("portal")
            WhatToCreate(game,mapElves,priority_Ice,priority_portal,priority_fauntain,priority_lava,priority_speed_up,priority_invisibility,priority_tornado,without,game.portal_cost+sper_mana)
    # increase my mana per turn
    if priority_fauntain == 3 and more_priority and "mana_fountain" not in without and game.get_my_mana() >= sper_mana:
        debug(game,"want to build mama fauntain")
        more_priority = need_fauntain(game,False,mapElves)
        if game.get_my_mana() > fountain_mana_to_check_more+sper_mana:
            without.append("mana_fountain")
            WhatToCreate(game,mapElves,priority_Ice,priority_portal,priority_fauntain,priority_lava,priority_speed_up,priority_invisibility,priority_tornado,without,game.mana_fountain_cost+sper_mana)
    # we can attack  
    if (priority_lava == 2 or priority_lava == 3) and more_priority and game.get_my_mana() >= sper_mana and if_enemy_summon_lava: 
        debug(game, "We can attack")
        more_priority = handle_portalsLava(game,False,sper_mana)
    # sper mana - so attack 
    if more_priority and game.get_my_mana() >= sper_mana and if_enemy_summon_lava: 
        debug(game, "We can attack")
        more_priority = handle_portalsLava(game,False,sper_mana)
    '''
    # sper mana deafence
    if more_priority and game.get_my_mana() >= sper_mana:
        debug(game,"deafence - speshial")
        more_priority = handle_portalsIce(game,False,sper_mana)
       ''' 
       
def need_portal(game,for_check,mapElves):
    enemy_ice_turrgets = sort_enemy_ice(game)
    my_ice_turrgets = sort_my_ice(game)
    optional_locations = list_fountain
    mana_for_portal = 0 
    if game.get_my_mana() < game.portal_cost:
        mana_for_portal = game.portal_cost - game.get_my_mana() 
    myElves = {}
    # check the elves not in the middle fight
    for elf in game.get_my_living_elves():
        if elf in mapElvesPerTurns.keys() and mapElvesPerTurns[elf] in game.get_enemy_mana_fountains() and len(game.get_enemy_mana_fountains()) > len(game.get_my_mana_fountains()):
            myElves[elf] = False
        neerst_enemy = sorted(game.get_enemy_living_elves() + game.get_enemy_ice_trolls(), key = lambda e: elf.in_attack_range(e))
        myElves[elf] = "Yes"
        if casting_elves[elf] == True:
            myElves[elf] = "No"
        if ((spell_casted(game,elf) == "speed up") or (spell_casted(game,elf) == "both of them")) and mapElvesPerTurns[elf] in game.get_enemy_mana_fountains():
            myElves[elf] = "No"
        for enemy in neerst_enemy:
            if myElves[elf] == "Yes":
                if elf in mapElvesPerTurns.keys() and mapElvesPerTurns[elf] in game.get_enemy_living_elves() and mapElvesPerTurns[elf].distance(game.get_my_castle()) < elf.distance(game.get_my_castle()):
                    myElves[elf] = "No"
                elif enemy.type == "IceTroll":
                    if enemy_ice_turrgets[enemy] == elf and (elf.distance(enemy) - enemy.attack_range)/enemy.max_speed <= game.portal_building_duration and not (check_location_for_build_portal(game,elf.location) and (elf.distance(enemy) - enemy.attack_range)/enemy.max_speed +elf.current_health<=game.portal_building_duration):
                        myElves[elf] = "No"
                    elif (spell_casted(game,elf)=="invisibility" or spell_casted(game,elf)=="both of them") and enemy.distance(elf)<enemy.attack_range+elf.max_speed:
                        myElves[elf]="No"
                    elif (spell_casted(game,elf)=="speed up" or spell_casted(game,elf)=="both of them") and elf in mapElvesPerTurns.keys() and mapElvesPerTurns[elf] in game.get_enemy_mana_fountains():
                        myElves[elf]="No"
                    else:
                        myElves[elf] = "Yes"
                else:
                    if (elf.distance(enemy) - enemy.attack_range)/enemy.max_speed <= game.portal_building_duration and enemy.distance(elf)<=EnemyElfLoc[enemy].distance(elf):
                        myElves[elf] = "No"
                    else:
                        myElves[elf] = "Yes"
        if elf.location in optional_locations:
            myElves[elf]="No"
        enemy_portal_to_elf = sorted(game.get_enemy_portals(), key = lambda p: p.distance(elf))
        if enemy_portal_to_elf and enemy_portal_to_elf[0].distance(elf) < game.portal_size + 6*game.tornado_max_speed and game.get_enemy_mana() + game.get_enemy().mana_per_turn *game.portal_building_duration >= game.tornado_cost:
            myElves[elf] = "No"
        enemy_tornado_to_elf = sorted(game.get_enemy_tornadoes(), key = lambda e: e.distance(elf))
        if enemy_tornado_to_elf and enemy_tornado_to_elf[0].current_health - (enemy_tornado_to_elf[0].distance(elf)/game.tornado_max_speed)*game.tornado_suffocation_per_turn > game.portal_building_duration + game.tornado_max_health/6:
            myElves[elf] = "No"
        enemy_portals = []
        for enemy_portal in game.get_enemy_portals():
            my_obj = sorted(game.get_my_portals()+game.get_my_mana_fountains()+[elf], key = lambda e: e.distance(enemy_portal))
            if my_obj and my_obj[0].distance(elf) < game.tornado_max_health/5*game.tornado_max_speed and enemy_portal.currently_summoning == "Tornado":
                myElves[elf] = "No"
    locations=list_fountain
    for elf in game.get_my_living_elves():
        if elf.location in locations or (elf in mapElvesPerTurns.keys() and mapElvesPerTurns[elf] in locations):
            myElves[elf]="No"
    elf_to_enemy_castle = sorted(game.get_my_living_elves(),key = lambda e: e.distance(game.get_enemy_castle()))
    portal_enemy_castle = sorted(game.get_my_portals(),key = lambda p: p.distance(game.get_enemy_castle()))
    enemy_portal_neer_my_castle = sorted(game.get_enemy_portals(),key = lambda p: p.distance(game.get_my_castle()))
    # there isnt enemy elves and enemy elves came befor build neer castle
    if not game.get_enemy_living_elves() and not game.get_enemy_portals() and not (portal_enemy_castle and (portal_enemy_castle[0].distance(game.get_enemy_castle()) - (game.portal_size + game.castle_size) ) < 2*(portal_enemy_castle[0].distance(game.get_my_castle()) - (game.portal_size + game.castle_size) )and (not game.get_enemy_portals() or portal_enemy_castle[0].distance(game.get_enemy_castle()) < enemy_portal_neer_my_castle[0].distance(game.get_my_castle()) ) and game.get_myself().mana_per_turn < game.portal_cost/10):
        for elf in game.get_my_living_elves():
            elf.distance(game.get_enemy_castle()) < elf.distance(game.get_my_castle())
            my_portal_to_enemy_castle=sorted(game.get_my_portals(),key=lambda portal:portal.distance(game.get_enemy_castle()))    
            if my_portal_to_enemy_castle:
                turn_elf_to_enemy_castle = elf.distance(game.get_enemy_castle())/elf.max_speed 
                enemy_revaive = sorted(game.get_all_enemy_elves(), key = lambda e: e.turns_to_revive)
                if enemy_revaive and enemy_revaive[0].turns_to_revive < turn_elf_to_enemy_castle and elf.distance(game.get_enemy_castle()) < my_portal_to_enemy_castle[0].distance(game.get_enemy_castle()) and elf.distance(game.get_enemy_castle()) <= elf.distance(game.get_my_castle()):
                    if my_portal_to_enemy_castle[0].distance(game.get_enemy_castle()) > game.castle_size + game.portal_size + 3*game.elf_max_speed:
                        if for_check:
                            debug(game, "Save mana - build near his castle befur enemy came")
                            return 1
                        if elf.can_build_portal() and myElves[elf] == "Yes":
                            elf.build_portal()
                            debug(game, "Build - build near his castle befur enemy came")
                            return True 
    # build near his castle:
    for elf in game.get_my_living_elves():
        build_in_enemy_castle_loc = game.get_enemy_castle().location.towards(elf.location,game.castle_size+game.portal_size+elf.max_speed/10)
        if elf.distance(game.get_enemy_castle()) < game.castle_size+game.portal_size+elf.max_speed/10:
            build_in_enemy_castle_loc = game.get_enemy_castle().location.towards(game.get_my_castle().location,game.castle_size+game.portal_size+elf.max_speed/10)
        portal_in_loc = False
        for portal in game.get_my_portals():
            if portal.distance(game.get_enemy_castle()) < game.portal_size + game.castle_size + 3*game.elf_max_speed:
                portal_in_loc = True
        if elf in mapElvesPerTurns.keys() and (mapElvesPerTurns[elf] == build_in_enemy_castle_loc or (elf.distance(game.get_enemy_castle())<game.castle_size+game.portal_size+elf.max_speed/10 and not portal_in_loc and mapElvesPerTurns[elf]==game.get_enemy_castle())or mapElvesPerTurns[elf] in enemy_fountain_loc):
            if elf.max_speed==0:
                turn_elf_came=0
            elif mapElvesPerTurns[elf] not in enemy_fountain_loc:
                turn_elf_came = (elf.distance(build_in_enemy_castle_loc)/elf.max_speed)-1
            else:
                turn_elf_came = (elf.distance(mapElvesPerTurns[elf])/elf.max_speed)-1
            if game.get_myself().mana_per_turn == 0:
                turn_to_mana = 0
            else:
                turn_to_mana = mana_for_portal/game.get_myself().mana_per_turn
            if turn_elf_came <= turn_to_mana:
                debug(game, "Save mana - build near his castle")
                if for_check:
                    return 1 
                if elf.can_build_portal() and myElves[elf] == "Yes":
                    elf.build_portal()
                    debug(game, "Build - build near his castle")
                    return True 
    
    # to build in dangerus place
    my_elf_near_enemy_castle = sorted(game.get_my_living_elves(), key = lambda e: e.distance(game.get_enemy_castle()))
    my_portal_to_enemy_castle = sorted(game.get_my_portals(), key = lambda p: p.distance(game.get_enemy_castle()))
    for elf in my_elf_near_enemy_castle:
        enemy_elf_to_elf = sorted(game.get_enemy_living_elves(), key = lambda e: e.distance(elf))
        if 2*elf.distance(game.get_enemy_castle()) < elf.distance(game.get_my_castle()) and ((not (my_portal_to_enemy_castle)) or (elf.distance(game.get_enemy_castle()) < my_portal_to_enemy_castle[0].distance(game.get_enemy_castle()))):
            if elf in mapElvesPerTurns.keys() and mapElvesPerTurns[elf] in game.get_enemy_living_elves() and mapElvesPerTurns[elf] in EnemyElfLoc.keys() and mapElvesPerTurns[elf].distance(game.get_enemy_castle()) < EnemyElfLoc[mapElvesPerTurns[elf]].distance(game.get_enemy_castle()):
                enemy_attackers = 0 
                nearest_enemy = None
                for enemy in game.get_enemy_living_elves() + game.get_enemy_ice_trolls():
                    if enemy.distance(elf) < enemy.attack_range:
                        enemy_attackers +=1
                    if (nearest_enemy == None or enemy.distance(elf) < nearest_enemy.distance(elf)):
                        nearest_enemy = enemy
                if ((nearest_enemy != None and enemy_attackers <= attackers_count(game,nearest_enemy)) or (nearest_enemy == None)) and not (enemy_elf_to_elf and enemy_elf_to_elf[0].distance(elf) < enemy_elf_to_elf[0].attack_range + enemy_elf_to_elf[0].max_speed + game.portal_size):
                    debug(game, "Save - build in dangerus place - 1")
                    if for_check:
                        return 1
                    if elf.current_health > 2 and elf.can_build_portal():
                        elf.build_portal()
                        debug(game, "Build - build in dangerus place - 1")
                        return True
    # to build in very dangerus place:
    elf_to_enemy_castle = sorted(game.get_enemy_living_elves() + game.get_my_living_elves(), key = lambda e: e.distance(game.get_enemy_castle()))
    for elf in my_elf_near_enemy_castle:
        if elf_to_enemy_castle and elf == elf_to_enemy_castle[0] and game.get_enemy_living_elves() and 3*elf.distance(game.get_enemy_castle()) < elf.distance(game.get_my_castle()):
            enemy_elf_to_elf = sorted(game.get_enemy_living_elves(), key = lambda e: e.distance(elf))
            enemy_attackers = 0 
            nearest_enemy = None
            for enemy in game.get_enemy_living_elves() + game.get_enemy_ice_trolls():
                if enemy.distance(elf) < enemy.attack_range:
                    enemy_attackers +=1
            if enemy_attackers <= attackers_count(game,enemy) and elf.current_health > game.portal_building_duration and not (myElves[elf]=="No" and game.get_my_mana()<=game.tornado_cost+game.portal_cost)and not (enemy_elf_to_elf and enemy_elf_to_elf[0].distance(elf) < enemy_elf_to_elf[0].attack_range + enemy_elf_to_elf[0].max_speed + game.portal_size):
                debug(game, "Save - build in dangerus place - 2")
                if for_check:
                    return 1
                if elf.current_health > 2 and elf.can_build_portal():
                    elf.build_portal()
                    debug(game, "Build - build in dangerus place - 2")
                    return True

    # to good fight elf to elf - havent portals 
    for elf in game.get_my_living_elves():
        less_mana = 0
        if game.get_my_mana() < (game.portal_cost):
            less_mana = (game.portal_cost) - game.get_my_mana()
        Enemy = sorted(game.get_enemy_living_elves(), key = lambda enemy: enemy.distance(elf))
        if Enemy:
            if Enemy[0].max_speed==0:
                turn_enemy_came=9999
            else:
                turn_enemy_came = (elf.distance(Enemy[0]) - (Enemy[0].attack_range+1))/(2*Enemy[0].max_speed)
            if game.get_myself().mana_per_turn == 0:
                turn_to_mana = 0
            else:
                turn_to_mana = less_mana/game.get_myself().mana_per_turn
            turn_to_build_and_creat = (game.portal_building_duration + game.ice_troll_summoning_duration) + (turn_to_mana)
            turn_buid = game.portal_building_duration
            if turn_enemy_came <= turn_to_build_and_creat and (turn_enemy_came > turn_buid and (len(game.get_my_portals()) == 0) or (distance_point_from_line(game.get_enemy_castle().location,game.get_my_castle().location,elf.location) > 12*elf.max_speed ) ) and not (spell_casted(game,Enemy[0])=="speed up" and sum_my_fountain==0 ):
                debug(game, "Save mana - good fight")
                if for_check:
                    return 1
                if elf.can_build_portal() and (1.25)*turn_enemy_came <= turn_to_build_and_creat and myElves[elf] == "Yes":
                    debug(game, "Build - good fight")
                    elf.build_portal()
                    return True
    # portal in the front
    portal_enemy_castle = sorted(game.get_my_portals(),key = lambda p: p.distance(game.get_enemy_castle()))
    enemy_portal_neer_my_castle = sorted(game.get_enemy_portals(),key = lambda p: p.distance(game.get_my_castle()))
    # there isnt enemy elves and enemy elves came befor build neer castle
    if not good_time_save_mana and not (portal_enemy_castle and portal_enemy_castle[0].distance(game.get_enemy_castle()) < 2*portal_enemy_castle[0].distance(game.get_my_castle()) and (not game.get_enemy_portals() or portal_enemy_castle[0].distance(game.get_enemy_castle()) < enemy_portal_neer_my_castle[0].distance(game.get_my_castle()) ) and game.get_myself().mana_per_turn < game.portal_cost/10):
        for elf in game.get_my_living_elves():
            elves_to_enemy_castle = sorted(game.get_all_living_elves(), key = lambda e: e.distance(game.get_enemy_castle())) 
            if elves_to_enemy_castle and elves_to_enemy_castle[0] in game.get_my_living_elves() and len(game.get_my_living_elves()) > len(game.get_enemy_living_elves()) and not (spell_casted(game,elf) == "speed up" or spell_casted(game,elf) == "both of them"):
                my_portal_to_enemy_castle = sorted(game.get_my_portals(), key = lambda p: p.distance(game.get_enemy_castle()))
                if ((not my_portal_to_enemy_castle) or (my_portal_to_enemy_castle[0].distance(game.get_enemy_castle()) > elf.distance(game.get_enemy_castle()) + 2*game.portal_size and elf.distance(game.get_enemy_castle()) < elf.distance(game.get_my_castle()) + 3*elf.max_speed) )and not(game.get_my_mana() >= game.mana_fountain_cost+game.portal_cost and check_location_for_build_fountain(game,elf.location)):
                    debug(game, "Save mana - portal in the front ")
                    if for_check:
                        return 1
                    if elf.can_build_portal() and myElves[elf] == "Yes":
                        debug(game, "Build - portal in the front ")
                        elf.build_portal()
                        return True
    # help in deafence 
    my_elves_nearst_to_my_castle = sorted(game.get_my_living_elves(), key = lambda e: e.distance(game.get_my_castle()))
    my_portal_to_my_castle = sorted(game.get_my_portals(), key = lambda e: e.distance(game.get_my_castle()))
    for elf in my_elves_nearst_to_my_castle:
        if (not (my_portal_to_my_castle) or (elf.distance(game.get_my_castle()) < my_portal_to_my_castle[0].distance(game.get_my_castle()))) and elf in mapElvesPerTurns.keys() and mapElvesPerTurns[elf] in game.get_enemy_living_elves() and 3*elf.distance(game.get_my_castle()) < elf.distance(game.get_enemy_castle()) and 3*mapElvesPerTurns[elf].distance(game.get_my_castle()) < mapElvesPerTurns[elf].distance(game.get_enemy_castle()):
            if not (mapElvesPerTurns[elf].current_health < elf.current_health and mapElvesPerTurns[elf].current_health < game.portal_building_duration/2) and elf.current_health > game.portal_building_duration*elf.attack_multiplier:        
                my_creatures_can_attack = sorted(game.get_my_living_elves()+game.get_my_ice_trolls(), key = lambda e: e.distance(mapElvesPerTurns[elf]))
                if ((not my_creatures_can_attack) or (my_creatures_can_attack[0].distance(mapElvesPerTurns[elf])>my_creatures_can_attack[0].attack_range)):
                    if for_check:
                        debug(game," Save - help in deafence")
                        return 1
                    if elf.can_build_portal() and elf.location not in optional_locations :
                        debug(game, "Build - help in deafence")
                        elf.build_portal()
                        return True
    
    # build portal in alternative_way 
    for elf in game.get_my_living_elves():
        my_portal_to_elf = sorted(game.get_my_portals(), key = lambda p: p.distance(elf))
        if not (my_portal_to_elf and my_portal_to_elf[0].distance(elf) < 2*game.portal_size + 5*game.tornado_max_speed):
            if dangerous_portal1[elf]==None and dangerous_elf1[elf]==None and elf in mapElvesPerTurns.keys() and when_I_go_to_alternative_way(game,elf,mapElvesPerTurns[elf]) and (elf.current_health >= game.portal_building_duration) and mapElvesPerTurns[elf] not in game.get_enemy_mana_fountains():
                enemy_elf_to_elf = sorted(game.get_enemy_living_elves(), key = lambda e: e.distance(elf))
                if ((enemy_elf_to_elf and enemy_elf_to_elf[0].distance(elf) < enemy_elf_to_elf[0].attack_range + enemy_elf_to_elf[0].max_speed + game.portal_size) or (not enemy_elf_to_elf)) and myElves[elf] == "Yes":    
                    debug(game, "Save - build portal in alternative_way")
                    if for_check:
                        return 2
                    if elf.can_build_portal():
                        elf.build_portal()
                        debug(game, "Build - build portal in alternative_way")
                        return True
                
    #build a portal next to fountain
    locations1=good_locations_for_portal_for_defend_on_fountain(game)
    for elf1 in game.get_my_living_elves():
        locations1.sort(key=lambda l:l.distance(elf1))
        if locations1 and elf1 in mapElvesPerTurns.keys() and mapElvesPerTurns[elf1]!= None and mapElvesPerTurns[elf1] not in game.get_all_enemy_elves() and mapElvesPerTurns[elf1].distance(locations1[0]) < 2*elf1.max_speed:
            turn_to_came = elf1.distance(mapElvesPerTurns[elf1])/elf1.max_speed
            if game.get_myself().mana_per_turn == 0:
                turn_to_mana = 0
            else:
                turn_to_mana = mana_for_portal/game.get_myself().mana_per_turn
            if turn_to_came <= turn_to_mana+5:
                debug(game, "Save mana - for building a portal next to fountain")
                if for_check:
                    return 2
                if elf1.can_build_portal() and myElves[elf1] == "Yes" and elf1.distance(locations1[0]) < 2*elf1.max_speed:
                    elf1.build_portal()
                    debug(game, "Build - portal next to fountain")
                    return True
                return False
                    
    # to good fight elf to elf 
    for elf in game.get_my_living_elves():
        less_mana = 0
        if game.get_my_mana() < (game.portal_cost+game.ice_troll_cost*0):
            less_mana = (game.portal_cost+game.ice_troll_cost*0) - game.get_my_mana()
        Enemy = sorted(game.get_enemy_living_elves(), key = lambda enemy: enemy.distance(elf))
        if Enemy:
            if Enemy[0].max_speed==0:
                turn_enemy_came==9999999
            else:
                turn_enemy_came = (elf.distance(Enemy[0]) - (Enemy[0].attack_range+1))/(2*Enemy[0].max_speed)
            if game.get_myself().mana_per_turn == 0:
                turn_to_mana = 0
            else:
                turn_to_mana = less_mana/game.get_myself().mana_per_turn
            turn_to_build_and_creat = (game.portal_building_duration + game.ice_troll_summoning_duration) + (turn_to_mana)
            turn_buid = game.portal_building_duration
            my_portal_to_enemy_castle = sorted(game.get_my_portals(), key = lambda p: p.distance(game.get_enemy_castle()))
            need_attack = False
            if my_portal_to_enemy_castle and my_portal_to_enemy_castle[0].distance(game.get_enemy_castle()) < 2*(game.portal_size + game.portal_size + 10) and game.get_my_castle().current_health < game.get_enemy_castle().current_health:
                need_attack = True
            if Enemy[0] in mapElvesPerTurns.values() and Enemy[0] in my_ice_turrgets.values() and Enemy[0].current_health<elf.current_health:
                need_attack=True
            if turn_enemy_came <= turn_to_build_and_creat and turn_enemy_came > turn_buid and not (1.5*Enemy[0].distance(game.get_my_castle()) < elf.distance(game.get_my_castle())) and not need_attack:
                debug(game, "Save mana - good fight")
                if for_check:
                    return 3
                if elf.can_build_portal() and (1.25)*turn_enemy_came <= turn_to_build_and_creat and myElves[elf] == "Yes":
                    debug(game, "Build - good fight")
                    elf.build_portal()
                    return True
                    
    # to destroy his portal:
    if not (game.get_enemy_mana() + game.get_enemy().mana_per_turn *game.portal_building_duration > game.tornado_cost and game.get_my_mana() + game.get_myself().mana_per_turn * game.portal_building_duration < game.portal_cost + game.ice_troll_cost):
        for elf in game.get_my_living_elves():
            my_portal_to_elf = sorted(game.get_my_portals(), key = lambda p: p.distance(elf))
            if not (my_portal_to_elf and my_portal_to_elf[0].distance(elf) < 2*game.portal_size + 4*game.tornado_max_speed):
                my_less_mana = 0
                if game.get_my_mana() < (game.portal_cost):
                    my_less_mana = (game.portal_cost) - game.get_my_mana() 
                enemy_portal_neer_this_elf = sorted(game.get_enemy_portals(),key = lambda p: p.distance(elf))
                if enemy_portal_neer_this_elf:
                    if enemy_portal_neer_this_elf[0].currently_summoning == "IceTroll":
                        turn_to_sum = enemy_portal_neer_this_elf[0].turns_to_summon
                        turn_enemy_came = turn_to_sum + (elf.distance(enemy_portal_neer_this_elf[0]) - (game.ice_troll_attack_range+1))/game.ice_troll_max_speed
                    else:
                        turn_enemy_came = (elf.distance(enemy_portal_neer_this_elf[0])-(2*game.portal_size+1))/elf.max_speed
                    if game.get_myself().mana_per_turn > 0:
                        if game.get_myself().mana_per_turn == 0:
                            turn_to_mana = 0
                        else:
                            turn_to_mana = less_mana/game.get_myself().mana_per_turn
                        turn_to_build_and_creat = (game.portal_building_duration + game.ice_troll_summoning_duration) + (turn_to_mana)
                        turn_buid = game.portal_building_duration
                        if turn_enemy_came <= turn_to_build_and_creat and turn_enemy_came > turn_buid and myElves[elf] == "Yes":
                            debug(game, "Save mana- portal fight")
                            if for_check:
                                return 3
                            if elf.can_build_portal() and myElves[elf] == "Yes":
                                debug(game, "Build - portal fight")
                                elf.build_portal()
                                return True
            
    #to build portal that near to enemy castle than other my portals
    EnemyCastle = game.get_enemy_castle()
    MyCastle = game.get_my_castle()
    my_elf_neer_enemy_castle = sorted(game.get_my_living_elves(), key = lambda e: e.distance(EnemyCastle))
    for elf in my_elf_neer_enemy_castle:
        enemy_portal_neer_my_castle = sorted(game.get_enemy_portals(),key = lambda p: p.distance(MyCastle))
        my_portal_neer_enemy_castle = sorted(game.get_enemy_portals(),key = lambda p: p.distance(EnemyCastle))
        if enemy_portal_neer_my_castle and not my_portal_neer_enemy_castle:
            if elf.distance(EnemyCastle)<elf.distance(MyCastle):
                debug(game, "Save mana - near portal than my portals ")
                if for_check:
                    return 4 
                if elf.can_build_portal() and myElves[elf] == "Yes":
                    elf.build_portal()
                    debug(game, "Build - near portal than my portals ")
                    return True
            if my_portal_neer_enemy_castle:
                if elf.distance(EnemyCastle)<my_portal_neer_enemy_castle[0].distance(EnemyCastle):
                    debug(game, "Save mana - near portal than my portals ")
                    if for_check:
                        return 4 
                    if elf.can_build_portal() and myElves[elf] == "Yes":
                        elf.build_portal()
                        debug(game, "Build - near portal than my portals ")
                        return True
                        
    # to build neerst other portal 
    for elf in my_elf_neer_enemy_castle:
        neer_portal_to_enemy = sorted(game.get_all_portals(), key = lambda p: p.distance(EnemyCastle))
        if neer_portal_to_enemy and elf.distance(EnemyCastle) < neer_portal_to_enemy[0].distance(EnemyCastle) and neer_portal_to_enemy[0].distance(elf) > 2*game.portal_size + 1:
            debug(game, "Save mana - near portal than other ")
            if for_check:
                return 4
            if elf.can_build_portal() and myElves[elf] == "Yes":
                elf.build_portal()
                debug(game, "Build - near portal than other ")
                return True
                
    # to build neer my castle 
    elf_to_my_castle = sorted(game.get_my_living_elves(),key = lambda e: e.distance(game.get_my_castle()), reverse = True)
    portal_my_castle = sorted(game.get_my_portals(),key = lambda p: p.distance(game.get_my_castle()))
    if elf_to_my_castle and ((portal_my_castle and elf_to_my_castle[0].distance(game.get_my_castle()) < portal_my_castle[0].distance(game.get_my_castle())) or (len(portal_my_castle) == 0)):
        count_summing = 0
        for portal in game.get_enemy_portals():
            if portal.currently_summoning == "LavaGiant":
                count_summing +=1
        if not (count_summing == len(game.get_enemy_portals()) and len(game.get_enemy_portals()) > 1 and len(game.get_my_portals())>0) and not(game.can_build_mana_fountain_at(elf_to_my_castle[0].initial_location) and game.turn<2):
            if not (portal_my_castle and portal_my_castle[0].distance(game.get_my_castle())<game.portal_size*2+game.mana_fountain_size*2+game.castle_size+game.elf_max_speed):
                debug(game, "Save mana - near portal than other to my castle")
                if for_check:
                    return 4
                if elf_to_my_castle[0].can_build_portal() and myElves[elf_to_my_castle[0]] == "Yes":
                    elf_to_my_castle[0].build_portal()
                    debug(game, "Build - near portal than other to my castle")
                    return True
    if for_check:
        return 100
    return False

def need_fauntain(game,for_check,mapElves):
    # useful vars
    enemy_ice_turrgets = sort_enemy_ice(game)
    enemy_mana_per_turn = game.get_enemy().mana_per_turn 
    my_mana_per_turn = game.get_myself().mana_per_turn
    my_ice_turrgets = sort_my_ice(game)
    myElves = {}
    global casting_elves
    global ok_to_build_fountain
    global good_time_save_mana
    # check the elves not in the middle fight
    for elf in game.get_my_living_elves():
       
        neerst_enemy = sorted(game.get_enemy_living_elves() + game.get_enemy_ice_trolls(), key = lambda e: elf.in_attack_range(e))
        myElves[elf] = "Yes"
        
        if casting_elves[elf] == True:
            myElves[elf] = "No"
        
        for enemy in neerst_enemy:
            if myElves[elf] == "Yes":
                if enemy.type == "IceTroll":
                    if (enemy_ice_turrgets[enemy] == elf or (enemy_ice_turrgets[enemy].type == "IceTroll" and enemy_ice_turrgets[enemy].current_health < game.mana_fountain_building_duration)) and (elf.distance(enemy) - enemy.attack_range)/enemy.max_speed <= game.mana_fountain_building_duration:
                        myElves[elf] = "No"
                    else:
                        myElves[elf] = "Yes"
                else:
                    if (elf.distance(enemy) - enemy.attack_range)/enemy.max_speed <= game.mana_fountain_building_duration and not (enemy in my_ice_turrgets.values() and enemy.current_health<elf.current_health):
                        myElves[elf] = "No"
                    else:
                        myElves[elf] = "Yes"
        enemy_portals = sorted(game.get_enemy_portals(),key = lambda p: p.distance(elf))
        if enemy_portals:
            my_obj = sorted(game.get_my_portals()+game.get_my_mana_fountains()+[elf],key = lambda e: e.distance(enemy_portals[0]))
            if my_obj and my_obj[0] == elf and my_obj[0].distance(enemy_portals[0])<diagonal_line/3 and sum_my_fountain>0:
                myElves[elf] = "No"
        enemy_portal_to_elf = sorted(game.get_enemy_portals(), key = lambda p: p .distance(elf))
        if enemy_portal_to_elf and enemy_portal_to_elf[0].distance(elf) < game.tornado_max_speed*8:
            saver_portal = False
            for portal in game.get_my_portals():
                if portal.distance(enemy_portal_to_elf[0]) < elf.distance(enemy_portal_to_elf[0]) and portal.distance(elf) < enemy_portal_to_elf[0].distance(elf):
                    saver_portal = True
            if not saver_portal:
                myElves[elf] = "No"
    
    optional_locations = list_fountain
    my_portal_to_enemy_castle = sorted(game.get_my_portals(),key = lambda p: p.distance(game.get_enemy_castle()))
    enemy_portal_to_my_castle = sorted(game.get_enemy_portals(),key = lambda p: p.distance(game.get_my_castle()))
    # the game over :
    if for_check and game.get_enemy_castle().current_health < 20 and my_portal_to_enemy_castle and enemy_portal_to_my_castle:
        if my_portal_to_enemy_castle[0].distance(game.get_enemy_castle()) < enemy_portal_to_my_castle[0].distance(game.get_my_castle()):
            return 100
    if for_check and game.get_enemy_castle().current_health < 20 and my_portal_to_enemy_castle and len(enemy_portal_to_my_castle) == 0:
        return 100
    if for_check and game.turn >= game.max_turns - 50:
        return 100
    if for_check and game.turn >= game.max_turns - 150 and not game.get_enemy_portals() and game.get_my_portals():
        return 100
    #if there is elf near enemy castle and we need portal
    if for_check and enemy_mana_per_turn == my_mana_per_turn + game.mana_fountain_mana_per_turn and (not game.get_enemy_living_elves()):
        for elf in game.get_my_living_elves():
            if (elf.distance(game.get_enemy_castle()) - (game.castle_size+game.lava_giant_attack_range) < 4*game.lava_giant_max_speed):
                my_portal_to_enemy_castle = sorted(game.get_my_portals(), key = lambda e: e.distance(game.get_enemy_castle()))
                if ((not my_portal_to_enemy_castle) or (elf.distance(game.get_enemy_castle()) < my_portal_to_enemy_castle[0].distance(game.get_enemy_castle()))):
                    return 100
                  
    #if enemy leading us -elves
    enemy_elves_life = 0
    my_elves_life = 0
    for enemy in game.get_enemy_living_elves():
        enemy_elves_life +=enemy.current_health
    for my in game.get_my_living_elves():
        my_elves_life +=my.current_health
    if enemy_elves_life >= 2*my_elves_life and len(game.get_enemy_living_elves()) > len(game.get_my_living_elves()) and for_check: 
        return 100
    # a lot of mana to enemy
    for elf in game.get_my_living_elves():
        if game.get_enemy_mana() > 3*game.get_my_mana() and game.get_my_mana() >= game.lava_giant_cost and stay_in_my_plase(game,elf,mapElves):
            if for_check:
                debug(game,"Save - a lot of mana to enemy ")
                return 1
            if elf.can_build_mana_fountain() and check_location_for_build_fountain(game,elf.location):
                debug(game,"Build - a lot of mana to enemy ")
                elf.build_mana_fountain()        
    #if there is good portal we need mana for lava     
    good_portal = None
    for portal in game.get_my_portals():
        loc_to_build_portal = game.get_enemy_castle().location.towards(portal.location,game.castle_size+game.portal_size+game.elf_max_speed/10)
        if portal.distance(loc_to_build_portal) < game.lava_giant_max_speed:
            good_portal = portal
    if for_check and good_portal!= None and not game.get_enemy_living_elves() and not game.get_my_mana_fountains() and not game.get_enemy_mana_fountains() and not (max_fountains > len(game.get_my_mana_fountains()) and game.get_enemy_castle().current_health > game.lava_giant_max_health*3):
        return 100
    # good time to save mana 
    check_if_elf_close_to_initial=False
    for elf in game.get_my_living_elves():
        if elf.distance(elf.initial_location)<elf.max_speed*5:
            check_if_elf_close_to_initial=True
    check_all_elves_far_from_initial_loc=True
    for elf2 in game.get_all_living_elves():
        m_initial_loc_to_elf=sorted(game.get_all_my_elves(),key=lambda e:e.initial_location.distance(elf2))
        e_initial_loc_to_elf=sorted(game.get_all_enemy_elves(),key=lambda e:e.initial_location.distance(elf2))
        if m_initial_loc_to_elf and e_initial_loc_to_elf and m_initial_loc_to_elf[0].initial_location.distance(elf2)<e_initial_loc_to_elf[0].initial_location.distance(elf2) and not (elf2 in game.get_my_living_elves() and elf2.distance(m_initial_loc_to_elf[0].initial_location)<game.elf_max_speed*10):
            check_all_elves_far_from_initial_loc=False
    if not (not if_destroy_fountain and my_mana_per_turn >= 1.5*enemy_mana_per_turn) and ((not game.get_my_living_elves()) or (check_if_elf_close_to_initial)or (len(game.get_my_living_elves())>0 and not game.get_enemy_living_elves()) or (check_all_elves_far_from_initial_loc) ):
        portal_to_enemy = sorted(game.get_my_portals(), key = lambda p: p.distance(game.get_my_castle()))
        if portal_to_enemy and 2*portal_to_enemy[0].distance(game.get_my_castle()) < portal_to_enemy[0].distance(game.get_enemy_castle()) and len(game.get_my_portals()) >= len(game.get_enemy_portals()):
            enemy_portal_to_me = sorted(game.get_enemy_portals(), key = lambda p: p.distance(game.get_my_castle()))
            if ((not enemy_portal_to_me) or  (enemy_portal_to_me[0].distance(game.get_my_castle()) > portal_to_enemy[0].distance(game.get_enemy_castle()))):
                ok_to_build_fountain = True
                if for_check:
                    debug(game, "good time to save mana ")
                    good_time_save_mana = True
                    return 0
    for elf in game.get_my_living_elves():                
        if elf.can_build_mana_fountain() and good_time_save_mana and stay_in_my_plase(game,elf,mapElves) and check_location_for_build_fountain(game,elf.location):
            debug(game,"Build good time")
            elf.build_mana_fountain()
            return True
    #if enemy destroy our fountain 
    if for_check and not ok_to_build_fountain and max_fountains>len(game.get_my_mana_fountains()) and not (sum_enemy_fountain>sum_my_fountain) and not if_it_equal_to_build_mana_fountain(game) :
        return 100
    #??????????
    if for_check and len(game.get_my_mana_fountains()) == len(game.get_enemy_mana_fountains()) and len(game.get_my_mana_fountains()) < max_fountains and (max_fountains>len(game.get_my_mana_fountains())) >1  and not game.get_my_mana_fountains():
        return 100
    # build enemy is weak
    for elf in game.get_my_living_elves():
        if not game.get_enemy_living_elves() and not game.get_enemy_portals() and elf.distance(game.get_my_castle()) <= elf.distance(game.get_enemy_castle()) and stay_in_my_plase(game,elf,mapElves):
            if for_check:
                debug(game,"Save - enemy is weak")
                return 1
            if elf.can_build_mana_fountain() and check_location_for_build_fountain(game,elf.location):
                debug(game,"Build enemy is weak")
                elf.build_mana_fountain()
                return True
    # enemy mana per turn more than my mana per turn
    enemy_fountain_health = 0
    my_fountain_health = 0
    for enemy_mana in game.get_enemy_mana_fountains():
        enemy_fountain_health += enemy_mana.current_health
    for my_mana in game.get_my_mana_fountains():
        my_fountain_health += my_mana.current_health
    for enemy_elf in game.get_enemy_living_elves():
        if enemy_elf.currently_building == "ManaFountain":
            enemy_mana_per_turn += game.mana_fountain_mana_per_turn
    for elf in game.get_my_living_elves():
        if elf.currently_building == "ManaFountain":
            my_mana_per_turn += game.mana_fountain_mana_per_turn
    my_elves_by_distance_to_enemy_castle = sorted(game.get_my_living_elves(), key = lambda e: e.distance(game.get_enemy_castle()), reverse = True)        
    for elf in my_elves_by_distance_to_enemy_castle:
        loc_to_build_portal = game.get_enemy_castle().location.towards(elf.location,game.castle_size+game.portal_size+elf.max_speed/10)
        good_portal = False
        good_build = False
        dis_to_build = game.castle_size + game.portal_size + game.elf_max_speed/10
        if len(game.get_enemy_living_elves()) == 0 and elf.distance(loc_to_build_portal) < 2*elf.max_speed and game.can_build_portal_at(loc_to_build_portal) and game.get_my_mana() > game.portal_cost:
            good_build = True
        for my_portals in game.get_my_portals():
            if (my_portals.distance(loc_to_build_portal) <  5*elf.max_speed):
                good_portal = True
            if not game.get_enemy_portals() and my_portals.distance(game.get_enemy_castle()) < my_portals.distance(game.get_my_castle()) - 3*elf.max_speed and my_mana_per_turn == enemy_mana_per_turn:
                good_portal = True
            if enemy_portal_to_my_castle and 3*(my_portals.distance(game.get_enemy_castle()) - (dis_to_build)) < (enemy_portal_to_my_castle[0].distance(game.get_my_castle()) - (dis_to_build)):
                good_portal = True
        if enemy_mana_per_turn ==  my_mana_per_turn + game.mana_fountain_mana_per_turn and (good_portal):
            if for_check:
                return 100
        if ((enemy_mana_per_turn > my_mana_per_turn) or (len(game.get_my_mana_fountains())==0 and not good_portal and not good_build)) and stay_in_my_plase(game,elf,mapElves):
            #if stay_in_my_plase(game,elf,mapElves):
            if for_check :
                debug(game, "Save mana(loosing) - need fauntain - 1")
                return 1
            if elf.can_build_mana_fountain() and myElves[elf] == "Yes" and check_location_for_build_fountain(game,elf.location):
                elf.build_mana_fountain()
                debug(game,"Build(loosing) - mana fauntain - 1")
                return True
                
    # all ny elves vs enemy elves and we can win
    all_mapElves_enemy_elf = True
    for k in mapElves.keys():
        if k not in game.get_enemy_living_elves():
            all_mapElves_enemy_elf = False
    if for_check and all_mapElves_enemy_elf and my_portal_to_enemy_castle and enemy_portal_to_my_castle:
        if my_portal_to_enemy_castle[0].distance(game.get_enemy_castle()) < enemy_portal_to_my_castle[0].distance(game.get_my_castle()):
            enemy_elf_to_my_castel = sorted(game.get_enemy_living_elves(), key = lambda e: e.distance(game.get_my_castle()))
            if enemy_elf_to_my_castel:
                my_attackers = sorted(game.get_my_living_elves()+game.get_my_ice_trolls(), key = lambda e: e.distance(enemy_elf_to_my_castel[0]))
                if not(my_attackers and enemy_elf_to_my_castel[0].distance(game.get_my_castle()) < my_portal_to_enemy_castle[0].distance(game.get_my_castle()) and my_attackers[0].distance(enemy_elf_to_my_castel[0]) > 2*my_attackers[0].max_speed):
                    return 100
                    
    # 
    for elf in game.get_my_living_elves():
        if (enemy_fountain_health > my_fountain_health):
            #if stay_in_my_plase(game,elf,mapElves):
            if stay_in_my_plase(game,elf,mapElves):
                if for_check :
                    debug(game, "Save mana(loosing) - need fauntain - 2")
                    return 1
                if elf.can_build_mana_fountain() and myElves[elf] == "Yes" and check_location_for_build_fountain(game,elf.location) and elf.distance(game.get_my_castle()) < game.castle_size + game.mana_fountain_size + 3*elf.max_speed and len(game.get_my_living_elves()) > len(game.get_enemy_living_elves()):
                    elf.build_mana_fountain()
                    debug(game,"Build(loosing) - mana fauntain-2")
                    return True 
                               
    # same mana per turn
    good_portal = None
    for portal in game.get_my_portals():
        loc_to_build_portal = game.get_enemy_castle().location.towards(portal.location,game.castle_size+game.portal_size+game.elf_max_speed/10)
        if portal.distance(loc_to_build_portal) < game.lava_giant_max_speed:
            good_portal = portal
    for elf in my_elves_by_distance_to_enemy_castle:
        ok_to_build = True
        my_portals_to_enemy_castle = sorted(game.get_my_portals(),key = lambda p: p.distance(game.get_enemy_castle()))
        if my_portals_to_enemy_castle and my_portals_to_enemy_castle[0].distance(game.get_enemy_castle()) >= elf.distance(game.get_enemy_castle()):
            ok_to_build = False
        if enemy_mana_per_turn == my_mana_per_turn and len(game.get_my_portals()) >= len(game.get_enemy_portals()) and game.get_my_portals() and ok_to_build:
            if stay_in_my_plase(game,elf,mapElves) and not (game.get_enemy_castle().current_health > 1.5*game.get_my_castle().current_health and not game.get_enemy_living_elves()) and not (good_portal != None and not (game.get_enemy_living_elves())):
                if for_check :
                    debug(game, "Save mana(draw) - need fauntain ")
                    return 2
                if elf.can_build_mana_fountain() and myElves[elf] == "Yes" and check_location_for_build_fountain(game,elf.location):
                    elf.build_mana_fountain()
                    debug(game,"Build(draw) - mana fauntain")
                    return True
    for elf in game.get_my_living_elves():
        if ( (if_destroy_fountain and len(game.get_my_mana_fountains()) <= len(game.get_enemy_mana_fountains())) or (game.get_my_mana() >= game.mana_fountain_cost+game.portal_cost) ) and stay_in_my_plase(game,elf,mapElves):
            if for_check :
                debug(game, "Save mana(loosing/draw - enemy destroy mana) - need fauntain ")
                return 2
            if elf.can_build_mana_fountain() and myElves[elf] == "Yes" and check_location_for_build_fountain(game,elf.location):
                elf.build_mana_fountain()
                debug(game, "Build mana(loosing/draw - enemy destroy mana) - need fauntain ")
                return True 
    # build behind portal
    for elf in my_elves_by_distance_to_enemy_castle:
        optional_locations.sort(key = lambda l: l.distance(elf))
        if optional_locations and elf.location.distance(optional_locations[0]) < game.mana_fountain_size + elf.max_speed:
            if for_check :
                debug(game, "Save mana(build behind portal) - need fauntain ")
                return 3
            if elf.can_build_mana_fountain() and myElves[elf] == "Yes" and check_location_for_build_fountain(game,elf.location):
                elf.build_mana_fountain()
                debug(game,"Build(build behind portal) - mana fauntain")
                return True
                
    if for_check:
        return 100 
    return False
    
def handle_portalsIce(game,for_check,sper_mana):
    # useful lists 
    optional_locations = list_fountain
    PortalToEnemyCastle = sorted(game.get_my_portals(), key = lambda portal: portal.distance(game.get_enemy_castle()))
    PortalToMyCastle = sorted(game.get_my_portals(), key = lambda portal: portal.distance(game.get_my_castle()))
    EnemyPortalToMyCastle = sorted(game.get_enemy_portals(), key = lambda portal: portal.distance(game.get_my_castle()))
    # useful Vars
    my_ice_turrgets = sort_my_ice(game)
    enemy_ice_turrgets = sort_enemy_ice(game)
    enemy_tornado_turrgets = sort_enemy_tornado(game)
    TurnsToCreateIce = game.ice_troll_summoning_duration
    InufMana = 0
    if game.get_my_mana() < game.ice_troll_cost:
        InufMana = game.ice_troll_cost - game.get_my_mana()
    LavaLoc = {}
    if game.get_myself().mana_per_turn == 0:
        turn_to_ice = TurnsToCreateIce
    else:
        turn_to_ice = (InufMana/game.get_myself().mana_per_turn) + TurnsToCreateIce
    for lava in game.get_enemy_lava_giants():
        LavaLoc[lava] = lava.location.towards(game.get_my_castle(),(lava.max_speed)*(turn_to_ice))
    
    for elf3 in game.get_my_living_elves():
        if elf3.location in optional_locations:
            if for_check:
                return 100
            return False
            
    #to save the portal from elf
    for portal in PortalToEnemyCastle:
        ice_turgget = False
        EnemynElfNeerPortal = sorted(game.get_enemy_living_elves(), key = lambda enemy: enemy.distance(portal))
        if EnemynElfNeerPortal and spell_casted(game,EnemynElfNeerPortal[0]) != "invisibility" and spell_casted(game,EnemynElfNeerPortal[0]) != "both of them" and not (game.get_my_castle().current_health < game.castle_max_health/5 and game.get_enemy_castle().current_health > 2*game.get_my_castle().current_health and game.get_enemy_portals()): 
            my_portal_to_enemy_elf = sorted(game.get_my_portals(), key = lambda portal: portal.distance(EnemynElfNeerPortal[0]))
            enemy_elf_loc = EnemynElfNeerPortal[0].location.towards(my_portal_to_enemy_elf[0],(game.elf_max_speed)*(turn_to_ice))
            ice_attack_elf = True
            for k in LavaLoc.keys():
                if LavaLoc[k].distance(portal) <= enemy_elf_loc.distance(portal)+3*game.elf_max_speed and k.current_health > game.ice_troll_summoning_duration:
                    ice_attack_elf = False
            for ice in game.get_my_ice_trolls():
                if my_ice_turrgets[ice] == EnemynElfNeerPortal[0] and ice.current_health > 8 and ice not in enemy_ice_turrgets.values():
                    ice_turgget = True
            TurnsOfEnemyElfToMyPortal = 0
            if EnemynElfNeerPortal[0].max_speed != 0:
                TurnsOfEnemyElfToMyPortal = (EnemynElfNeerPortal[0].distance(portal)-EnemynElfNeerPortal[0].attack_range - game.portal_size)/EnemynElfNeerPortal[0].max_speed
            if game.get_myself().mana_per_turn == 0:
                turn_to_ice = 0
            else:
                turn_to_ice = (InufMana/game.get_myself().mana_per_turn)
            TurnsNeedForPerfectDeafence = TurnsToCreateIce+((game.portal_size)/(game.ice_troll_max_speed))+(turn_to_ice)
            if portal == PortalToEnemyCastle[0] and portal.distance(game.get_enemy_castle()) < portal.distance(game.get_my_castle()):
                TurnsNeedForPerfectDeafence += TurnsNeedForPerfectDeafence/2
            enemy_neer_portal = sorted(game.get_enemy_creatures()+game.get_enemy_living_elves() , key = lambda e: e.distance(portal))
            my_ice_to_enemy = [] 
            for ice in game.get_my_ice_trolls():
                if ice.distance(EnemynElfNeerPortal[0]) < game.ice_troll_attack_range + game.ice_troll_max_speed and ice not in enemy_ice_turrgets.values():
                    my_ice_to_enemy.append(ice)
            my_ice_to_portal = sorted(game.get_my_ice_trolls(), key = lambda i: i.distance(portal))
            my_elf_to_enemy = sorted(game.get_my_living_elves(), key = lambda e: e.distance(EnemynElfNeerPortal[0]))
            enemy_not_danger = False
            portal_will_destroy = False
            if EnemynElfNeerPortal[0].in_attack_range(portal) and portal.current_health < game.ice_troll_summoning_duration+1 and attackers_count12(game,EnemynElfNeerPortal[0]) == 0:
                portal_will_destroy = True
            if (EnemynElfNeerPortal[0].distance(portal) -(EnemynElfNeerPortal[0].attack_range + portal.size) )/EnemynElfNeerPortal[0].max_speed + portal.current_health/EnemynElfNeerPortal[0].attack_multiplier < game.ice_troll_summoning_duration + 1 and attackers_count12(game,EnemynElfNeerPortal[0]) == 0:
                portal_will_destroy = True
            enemy_will_die = False
            if EnemynElfNeerPortal[0].current_health < game.ice_troll_summoning_duration:
                for ice in game.get_my_ice_trolls():
                    if my_ice_turrgets[ice] == EnemynElfNeerPortal[0] and ice.distance(EnemynElfNeerPortal[0]) < game.ice_troll_attack_range and enemy_attackers_count(game,ice) <= 1 and ice.current_health > EnemynElfNeerPortal[0].current_health and ice not in enemy_ice_turrgets.values():
                        enemy_will_die = True
            for elf in game.get_my_living_elves():
                if attack[elf] == EnemynElfNeerPortal[0] and elf.current_health >= EnemynElfNeerPortal[0].current_health and EnemynElfNeerPortal[0].current_health <= game.ice_troll_summoning_duration +1 and enemy_attackers_count(game,elf) <=1:
                    enemy_will_die = True
            my_elves_to_portal = sorted(game.get_my_living_elves(),key = lambda e: e.distance(portal))
            my_elf_will_save_the_portal = False
            if my_elves_to_portal and my_elves_to_portal[0].distance(portal) < EnemynElfNeerPortal[0].distance(portal) + my_elves_to_portal[0].max_speed and my_elves_to_portal[0].distance(EnemynElfNeerPortal[0]) < EnemynElfNeerPortal[0].distance(portal) + 2*my_elves_to_portal[0].max_speed and my_elves_to_portal[0].current_health >= EnemynElfNeerPortal[0].current_health:
                my_elf_will_save_the_portal = True
                for enemy_ice in game.get_enemy_ice_trolls():
                    if enemy_ice_turrgets[enemy_ice] == my_elves_to_portal[0] and enemy_ice.distance(my_elves_to_portal[0]) < enemy_ice.attack_range + 5*enemy_ice.max_speed:
                        my_elf_will_save_the_portal = False
            '''
            if my_elf_to_enemy and my_elf_to_enemy[0].in_attack_range(EnemynElfNeerPortal[0]) and my_elf_to_enemy[0].current_health >= EnemynElfNeerPortal[0].current_health and attackers_count(game,EnemynElfNeerPortal[0]) >= enemy_attackers_count(game,my_elf_to_enemy[0]):
                enemy_not_danger = True'''
            if not (if_destroy_fountain and ((spell_casted(game,EnemynElfNeerPortal[0]) == "speed up") or (spell_casted(game,EnemynElfNeerPortal[0]) == "both of them"))) and not (EnemynElfNeerPortal[0].is_building and EnemynElfNeerPortal[0].distance(portal) > game.portal_size + EnemynElfNeerPortal[0].attack_range + 4*EnemynElfNeerPortal[0].distance(portal)) and not not_equal_to_summing(game,portal) and not my_elf_will_save_the_portal and not enemy_will_die and not portal_will_destroy and not enemy_not_danger and not (my_ice_to_portal and my_ice_to_portal[0].distance(portal) < game.ice_troll_attack_range + game.ice_troll_max_speed and 2*portal.distance(game.get_enemy_castle()) < portal.distance(game.get_my_castle())):
                if len(my_ice_to_enemy) < 2 and TurnsOfEnemyElfToMyPortal <= TurnsNeedForPerfectDeafence and portal == my_portal_to_enemy_elf[0] and ice_turgget == False and ice_attack_elf and distance_point_from_line(EnemynElfNeerPortal[0].location, EnemyElfLoc[EnemynElfNeerPortal[0]], portal.location) < (EnemynElfNeerPortal[0].attack_range + EnemynElfNeerPortal[0].max_speed + game.portal_size + 1):
                    if for_check:
                        return 1
                    if not portal.is_summoning and portal.can_summon_ice_troll():
                        debug(game, "Save the portal from elf - summon ice")
                        portal.summon_ice_troll()
                        return True
                    if portal.currently_summoning == "IceTroll":
                        return True
                TurnsNeedForPerfectDeafence = TurnsToCreateIce+((game.portal_size)/(game.ice_troll_max_speed))
                if len(my_ice_to_enemy) < 2 and TurnsOfEnemyElfToMyPortal < TurnsNeedForPerfectDeafence and portal == my_portal_to_enemy_elf[0] and ice_turgget == False and (ice_attack_elf) and not (EnemynElfNeerPortal[0] in EnemyElfLoc.keys() and EnemynElfNeerPortal[0].distance(portal) > EnemyElfLoc[EnemynElfNeerPortal[0]].distance(portal)+EnemynElfNeerPortal[0].max_speed/5):
                    if for_check:
                        return 1
                    if not portal.is_summoning and portal.can_summon_ice_troll():
                        debug(game, "Save the portal from elf that near my portal - summon ice")
                        portal.summon_ice_troll()
                        return True
                    if portal.currently_summoning == "IceTroll":
                        return True

    # save the portal from enemy portal that go revive 
    for portal in game.get_my_portals():
        enemy_initial_to_portal = sorted(game.get_all_enemy_elves(), key = lambda e: e.initial_location.distance(portal))
        for enemy_elf in enemy_initial_to_portal:
            portal_to_enemy_initial = sorted(game.get_my_portals(), key = lambda p: p.distance(enemy_elf.initial_location))
            TurnsNeedForPerfectDeafence = game.ice_troll_summoning_duration + InufMana/game.get_myself().mana_per_turn + 1
            if not not_equal_to_summing(game,portal) and portal_to_enemy_initial[0] == portal and enemy_elf.turns_to_revive < TurnsNeedForPerfectDeafence +game.lava_giant_cost/game.get_myself().mana_per_turn + 1 and enemy_elf.turns_to_revive > 0 and portal.distance(enemy_elf.initial_location) < game.ice_troll_attack_range +game.castle_size +3*game.ice_troll_max_speed:
                if for_check:
                    return 1
                if not portal.is_summoning and portal.can_summon_ice_troll():
                    debug(game, "Save the portal from elf initial location that near my portal - summon ice")
                    portal.summon_ice_troll()
                    return True
                if portal.currently_summoning == "IceTroll":
                    return True
                
    # to save the portal from tornado
    b = False
    for portal in game.get_my_portals():
        turns_perfect_deafence = ((game.portal_size)/(game.ice_troll_max_speed))+(turn_to_ice)
        for enemy_tornado in game.get_enemy_tornadoes():
            turns_tornado_to_portal = (enemy_tornado.distance(portal) - (portal.size + enemy_tornado.attack_range))/enemy_tornado.max_speed
            count_ice_attackers = 0
            for ice in game.get_my_ice_trolls():
                if ice.current_health > 1 and my_ice_turrgets[ice] == enemy_tornado and ice.distance(enemy_tornado) < ice.attack_range+ice.max_speed:
                    count_ice_attackers += 1
            if turns_tornado_to_portal < (enemy_tornado.current_health/enemy_tornado.suffocation_per_turn - (2+count_ice_attackers*4))and turns_perfect_deafence <= turns_tornado_to_portal and enemy_tornado_turrgets[enemy_tornado] == portal:
                if for_check:
                    return 1
                if not portal.is_summoning and portal.can_summon_ice_troll():
                    debug(game, "Save the portal from tornado - summon ice")
                    portal.summon_ice_troll()
                    b = True
                if portal.currently_summoning == "IceTroll":
                    b = True 
    if b:
        return b
                
    # save portal from disapering elf
    b = False
    for portal in game.get_my_portals():
        for enemy_elf in game.get_enemy_living_elves():
            portal_to_enemy = sorted(game.get_my_portals(),key = lambda p: p.distance(enemy_elf))
            if (spell_casted(game,enemy_elf) == "invisibility" or spell_casted(game,enemy_elf) == "both fo them") and enemy_elf in loc_before_disapear.keys() and loc_before_disapear[enemy_elf].distance(portal)<2*enemy_elf.max_speed+enemy_elf.attack_range and loc_before_disapear[enemy_elf].distance(game.get_enemy_castle()) < portal.distance(game.get_enemy_castle()):
                if for_check:
                    return 1
                if not portal.is_summoning and portal.can_summon_ice_troll() and portal == portal_to_enemy[0]:
                    debug(game, "Save the portal from desapirimg elf that near my portal - summon ice")
                    portal.summon_ice_troll()
                    b = True
                if portal.currently_summoning == "IceTroll":
                    b = True
    if b == True:
        return b
        
    # save fountain:
    for portal in game.get_my_portals():
        need_ice = False
        my_fountain = sorted(game.get_my_mana_fountains(), key = lambda m: m.distance(portal))
        if my_fountain and my_fountain[0].distance(portal) < 1500:
            portal_to_fountain = sorted(game.get_my_portals(), key = lambda e: e.distance(my_fountain[0]))
            enemy_elves_to_portal = sorted(game.get_enemy_living_elves(), key = lambda e: e.distance(portal))
            sper_distance = 2
            if len(game.get_enemy_living_elves()) > len(game.get_my_living_elves()):
                sper_distance = 4
            if enemy_elves_to_portal and enemy_elves_to_portal[0].distance(portal) < (2*enemy_elves_to_portal[0].max_speed +enemy_elves_to_portal[0].attack_range)*sper_distance + game.mana_fountain_size and enemy_elves_to_portal[0] and enemy_elves_to_portal in EnemyElfLoc.keys() and EnemyElfLoc[enemy_elves_to_portal[0]].distance(portal) > enemy_elves_to_portal[0].distance(portal) + 2*enemy_elves_to_portal[0].max_speed/3:
                need_ice = True
            if if_destroy_fountain and enemy_elves_to_portal and enemy_elves_to_portal[0] in EnemyElfLoc.keys() and EnemyElfLoc[enemy_elves_to_portal[0]].distance(portal) > enemy_elves_to_portal[0].distance(portal) and ((spell_casted(game,enemy_elves_to_portal[0]) == "speed up" or spell_casted(game,enemy_elves_to_portal[0]) == "both of them") or (enemy_elves_to_portal[0].distance(portal) < enemy_elves_to_portal[0].max_speed*15)):
                need_ice = True
            if enemy_elves_to_portal and ((spell_casted(game,enemy_elves_to_portal[0])== "speed up") or (spell_casted(game,enemy_elves_to_portal[0]) == "both of them")) and enemy_elves_to_portal[0].distance(portal) < (4*enemy_elves_to_portal[0].max_speed +enemy_elves_to_portal[0].attack_range)*sper_distance + game.mana_fountain_size:
                need_ice = True
            if need_ice and portal == portal_to_fountain[0] and not (enemy_elves_to_portal[0].in_attack_range(my_fountain[0]) and enemy_elves_to_portal[0].current_health < enemy_elves_to_portal[0].max_health/2 and enemy_elves_to_portal[0] in mapElvesPerTurns.values()):
                attackers_count = 0
                for ice in game.get_my_ice_trolls():
                    if my_ice_turrgets[ice] == enemy_elves_to_portal[0]:
                        attackers_count +=1
                if for_check and attackers_count < 3:
                    return 1
                if not portal.is_summoning and portal.can_summon_ice_troll() and attackers_count < 3:
                    debug(game, "Save the fountain from elf - summon ice")
                    portal.summon_ice_troll()
                    return True
                if portal.currently_summoning == "IceTroll":
                    return True 
    # save castle from volcano
    ev = []
    closest_enemy_to_my_castle = sorted(game.get_enemy_living_elves(), key =lambda e:e.distance(game.get_my_castle()))
    if game.get_active_volcanoes() and closest_enemy_to_my_castle:
        ev = sorted(game.get_active_volcanoes(),key  = lambda e:e.distance(closest_enemy_to_my_castle[0]))
    if ev and not (game.get_my_living_elves())  and volcano_life > ev[0].current_health and ev[0].damage_by_me < ev[0].damage_by_enemy + ev[0].current_health and ev[0].current_health < ev[0].max_health/2:
            portal_to_my_castle = sorted(game.get_my_portals(), key = lambda p: p.distance(game.get_my_castle()))
            if portal_to_my_castle:
                if for_check:
                    return 1
                if not portal_to_my_castle[0].is_summoning and portal_to_my_castle[0].can_summon_ice_troll():
                    debug(game, "Save my castle for volcano - summon ice")
                    portal_to_my_castle[0].summon_ice_troll()
                    return True
                if portal_to_my_castle[0].currently_summoning == "IceTroll":
                    return True
    # save volcano:
    
    ev = []
    volcano = None
    closest_enemy_to_my_castle = sorted(game.get_enemy_living_elves(), key =lambda e:e.distance(game.get_my_castle()))
    if game.get_active_volcanoes() and closest_enemy_to_my_castle:
        ev = sorted(game.get_active_volcanoes(),key  = lambda e:e.distance(closest_enemy_to_my_castle[0]))
        volcano = ev[0]
    if volcano!= None:
        for enemy in game.get_enemy_living_elves():
            if enemy.distance(volcano) < enemy.attack_range + volcano.size + 3*enemy.max_speed and ((enemy in EnemyElfLoc.keys() and EnemyElfLoc[enemy].distance(volcano) > enemy.distance(volcano) + enemy.max_speed/3) or (EnemyElfLoc[enemy].distance(volcano)  == enemy.distance(volcano) and enemy.in_attack_range(volcano))):
                for portal in game.get_my_portals():
                    if portal.distance(volcano) < portal.size + volcano.size + 3*game.ice_troll_max_speed:
                        if for_check:
                            return 1
                        if not portal.is_summoning and portal.can_summon_ice_troll():
                            debug(game, "Save the volcano from elf - summon ice")
                            portal.summon_ice_troll()
                            return True
                        if portal.currently_summoning == "IceTroll":
                            return True
                    
    # we havnt elves and dangerus elf :
    if not game.get_my_living_elves() and game.get_enemy_living_elves():
        build_dis = game.castle_size + game.portal_size + game.elf_max_speed/10
        enemy_elf_to_my_castel = sorted(game.get_enemy_living_elves(), key = lambda e: e.distance(game.get_my_castle()))
        portal_to_enemy = sorted(game.get_my_portals(),key = lambda p: p.distance(enemy_elf_to_my_castel[0]) + p.distance(game.get_my_castle()))
        if portal_to_enemy and (enemy_elf_to_my_castel[0].distance(game.get_my_castle()) - build_dis)< 2*(enemy_elf_to_my_castel[0].distance(game.get_enemy_castle()) - build_dis):
            enemy_elf_loc = enemy_elf_to_my_castel[0].location.towards(portal_to_enemy[0],(game.elf_max_speed)*(turn_to_ice))
            ice_attack_elf = True
            for k in LavaLoc.keys():
                if LavaLoc[k].distance(portal) <= enemy_elf_loc.distance(portal)+3*game.elf_max_speed and k.current_health > game.ice_troll_summoning_duration:
                    ice_attack_elf = False
                if ice_attack_elf:
                    if for_check:
                        return 1
                    if not portal_to_enemy[0].is_summoning and portal_to_enemy[0].can_summon_ice_troll() and ice_attack_elf:
                        debug(game, "we havnt elves and dangerus elf - summon ice")
                        portal_to_enemy[0].summon_ice_troll()
                        return True
                    if portal_to_enemy[0].currently_summoning == "IceTroll":
                        return True
    
    # to save my elf 
    for portal in game.get_my_portals():
        MyElfsfFromMyPortal = sorted(game.get_my_living_elves(), key = lambda MyElf: MyElf.distance(portal))
        EnemynNeerPortal = sorted(game.get_enemy_living_elves(), key = lambda enemy: enemy.distance(portal))
        enemy_go_my_fountain = False
        not_need_ice = False
        for enemy_elf in game.get_enemy_living_elves():
            fountain_to_enemy_elf = sorted(game.get_my_mana_fountains(), key = lambda m: m.distance(enemy_elf))
            if fountain_to_enemy_elf and enemy_elf in EnemyElfLoc.keys() and (spell_casted(game,enemy_elf) == "speed up" or spell_casted(game,enemy_elf) == "both of them") and enemy_elf.distance(fountain_to_enemy_elf[0]) < EnemyElfLoc[enemy_elf].distance(fountain_to_enemy_elf[0]):
                enemy_go_my_fountain = True
        if not not_equal_to_summing(game,portal) and EnemynNeerPortal and MyElfsfFromMyPortal and not enemy_go_my_fountain and not (EnemynNeerPortal[0].current_health < MyElfsfFromMyPortal[0].current_health and portal.current_health <= 2 and enemy_attackers_count(game,MyElfsfFromMyPortal[0]) <=1):
            turn_enemy_can_attack_my_elf = (EnemynNeerPortal[0].distance(MyElfsfFromMyPortal[0])-EnemynNeerPortal[0].attack_range)/EnemynNeerPortal[0].max_speed
            if game.get_myself().mana_per_turn == 0:
                turn_to_ice = 0
            else:
                turn_to_ice = (InufMana/game.get_myself().mana_per_turn)
            turn_portal_can_save_me = ((MyElfsfFromMyPortal[0].distance(portal))/(game.ice_troll_max_speed))+turn_to_ice
            optional_number = 1
            if len(game.get_enemy_living_elves()) > len(game.get_my_living_elves()):
                optional_number += 0
            if turn_enemy_can_attack_my_elf <= turn_portal_can_save_me and MyElfsfFromMyPortal[0].distance(portal)<5*MyElfsfFromMyPortal[0].max_speed*optional_number:
                PortalToEnemy = sorted(game.get_my_portals(), key = lambda p: p.distance(MyElfsfFromMyPortal[0]))
                enemy_neer_portal = sorted(game.get_enemy_creatures()+game.get_enemy_living_elves() , key = lambda e: e.distance(portal))
                enemy_elf_loc = EnemynElfNeerPortal[0].location.towards(PortalToEnemy[0],(game.elf_max_speed)*(turn_to_ice))
                ice_attack_elf = True
                for k in LavaLoc.keys():
                    if LavaLoc[k].distance(portal) <= enemy_elf_loc.distance(portal)+3*game.elf_max_speed and k.current_health > game.ice_troll_summoning_duration:
                        ice_attack_elf = False
                if enemy_attackers_count(game,MyElfsfFromMyPortal[0]) == 1 and MyElfsfFromMyPortal[0].current_health >= EnemynElfNeerPortal[0].current_health and attack[MyElfsfFromMyPortal[0]] == EnemynElfNeerPortal[0] and MyElfsfFromMyPortal[0].current_health < game.tornado_summoning_duration + 1 and MyElfsfFromMyPortal[0] not in enemy_ice_turrgets.values():
                    not_need_ice = True
                if not_need_ice and portal == PortalToEnemy[0] and (ice_attack_elf) and not (portal.distance(game.get_enemy_castle()) < game.castle_size + game.portal_size +  3*game.elf_max_speed and spell_casted(game,EnemynElfNeerPortal[0]) == "speed up" and max_fountains > len(game.get_my_mana_fountains())):
                    if for_check:
                        return 2
                    if not portal.is_summoning and portal.can_summon_ice_troll():
                        debug(game, "Save my elf from enemy elf - summon ice")
                        portal.summon_ice_troll()
                        return True
                    if portal.currently_summoning == "IceTroll":
                        return True
    # to save my castle 
    attackers = sorted(game.get_enemy_lava_giants()+game.get_enemy_living_elves(), key = lambda e: e.distance(game.get_my_castle()))
    if PortalToMyCastle and attackers:
        portal_for_protect = sorted(game.get_my_portals(), key = lambda p: (p.distance(game.get_my_castle()) + p.distance(attackers[0])))
        MyCastle = game.get_my_castle()
        health_attackers_on_my_castle = 0 
        healt_attackers = 0
        my_ice_attack = False
            
        for lava in game.get_enemy_lava_giants():
            healt_attackers +=lava.current_health
            turn_enemy_attack =  (lava.distance(MyCastle) - (MyCastle.size+lava.attack_range))/lava.max_speed
            optional_turn = 2 
            if turn_enemy_attack <= optional_turn and lava.current_health >= 2:
                health_attackers_on_my_castle +=lava.current_health
                for ice in game.get_my_ice_trolls():
                    if my_ice_turrgets[ice] == lava and ice.current_health > 5:
                        my_ice_attack = True
        
        # I havent elves and enemy elves
        if not game.get_my_living_elves() and game.get_enemy_living_elves():
            danger_enemy = False
            for enemy in game.get_enemy_living_elves():
                if enemy.distance(game.get_my_castle()) < enemy.distance(game.get_enemy_castle()):
                    danger_enemy = True
                if enemy in EnemyElfLoc.keys() and EnemyElfLoc[enemy].distance(game.get_my_castle()) > enemy.distance(game.get_my_castle()):
                    danger_enemy = True
            if danger_enemy:
                portal_near_enemy = None
                portal_distance = 9999
                for portal in game.get_my_portals():
                    enemy_to_portal = sorted(game.get_enemy_living_elves(), key = lambda e: e.distance(portal))
                    if portal.distance(enemy_to_portal[0]) < portal_distance:
                        portal_distance = portal.distance(enemy_to_portal[0])
                        portal_to_enemy = portal
                if portal_to_enemy != None and portal_distance < game.ice_troll_attack_range + game.ice_troll_max_speed*10 and not portal.is_summoning and portal.can_summon_ice_troll():
                    debug(game, "Save my elf from enemy elf - summon ice")
                    portal.summon_ice_troll()
                    return True
                if portal.currently_summoning == "IceTroll":
                    return True
        # Many attackers then protect
        if health_attackers_on_my_castle >= 25 and my_ice_attack == False:
            if for_check:
                return 3
            message = "Save my castle(Many attackers) - summon ice"
            return ice_troll_full_summoning(game,portal_for_protect,sper_mana,message)
        # we loosing
        if game.get_enemy_castle().current_health > 2*game.get_my_castle().current_health and health_attackers_on_my_castle >= 20:
            if for_check:
                return 3
            message = "Save my castle(we loosing) - summon ice"
            return ice_troll_full_summoning(game,portal_for_protect,sper_mana,message)
        # More attacker life than my castle life 
        if healt_attackers > game.get_my_castle().current_health:
            if for_check:
                return 3
            message = "Save my castle(More attacker life than my castle life) - summon ice"
            return ice_troll_full_summoning(game,portal_for_protect,sper_mana,message)
        # speshial - enemy ice troll and sper mana
        portal_to_my_castle = sorted(game.get_my_portals(), key = lambda p:p.distance(game.get_my_castle()))
        if portal_to_my_castle and game.get_enemy_lava_giants() and len(game.get_my_ice_trolls()) < 1:
            if for_check:
                return 100
            if not portal_to_my_castle[0].is_summoning and portal_to_my_castle[0].can_summon_ice_troll():
                debug(game, "Deafence sper mana - summon ice")
                portal_to_my_castle[0].summon_ice_troll()
            if portal_to_my_castle[0].currently_summoning == "IceTroll":
                return True
                
    if for_check:
        return 100
    return False
    
def handle_portalsLava(game,for_check,sper_mana):
    # useful vars 
    TurnsToCreateLava = game.lava_giant_summoning_duration
    InufMana = 0
    if game.get_my_mana() < game.lava_giant_cost:
        InufMana = game.lava_giant_cost - game.get_my_mana()
    PortalToEnemyCastle = sorted(game.get_my_portals(), key = lambda portal: portal.distance(game.get_enemy_castle()))
    EnemyPortalToMyCastle = sorted(game.get_enemy_portals(), key = lambda portal: portal.distance(game.get_my_castle()))
    my_elf_to_enemy_castle = sorted(game.get_my_living_elves() , key = lambda e: e.distance(game.get_enemy_castle()))
    # stop attack wen we need the mana for cameback
    if not game.get_my_living_elves() and ((not PortalToEnemyCastle) or (game.lava_giant_max_health - (game.lava_giant_suffocation_per_turn*(PortalToEnemyCastle[0].distance(game.get_enemy_castle()) - (game.lava_giant_attack_range + game.castle_size))/game.lava_giant_max_speed) < game.get_enemy_castle().max_health/40)) and not (not game.get_enemy_living_elves() and game.get_enemy_lava_giants()):
        if for_check:
            return 100
        return True
    if len(game.get_enemy_living_elves()) > len(game.get_my_living_elves()) and if_enemy_destroy_my_fountain and not game.get_enemy_portals() and game.get_my_mana() < game.mana_fountain_cost + game.lava_giant_cost:
        enemy_by_health = sorted(game.get_enemy_living_elves(), key = lambda e: e.current_health)
        my_by_health = sorted(game.get_my_living_elves(), key = lambda e: e.current_health, reverse = True)
        if ((not my_by_health) or (enemy_by_health and my_by_health[0].current_health < enemy_by_health[0].current_health)): 
            if for_check:
                return 100
            return True
    # we gona win.....
    if PortalToEnemyCastle and not not_equal_to_summing_tornado(game,PortalToEnemyCastle[0]): 
        turns_lava_to_castle = ((PortalToEnemyCastle[0].distance(game.get_enemy_castle()) - (game.castle_size + game.lava_giant_attack_range))/game.lava_giant_max_speed)
        if (game.lava_giant_max_health - turns_lava_to_castle*game.lava_giant_suffocation_per_turn) >= game.get_enemy_castle().current_health + 10:
            if for_check:
                return 0
            else:
                if not PortalToEnemyCastle[0].is_summoning and PortalToEnemyCastle[0].can_summon_lava_giant():
                    debug(game, "we want to finish the game - summon lava giant")
                    PortalToEnemyCastle[0].summon_lava_giant()
                    return True
                if PortalToEnemyCastle[0].currently_summoning == "LavaGiant":
                    return True
    # we have portal very close to enemy castle :                
    if(PortalToEnemyCastle and EnemyPortalToMyCastle and 2*(PortalToEnemyCastle[0].distance(game.get_enemy_castle())- game.lava_giant_attack_range) < (EnemyPortalToMyCastle[0].distance(game.get_my_castle()) - game.lava_giant_attack_range and not not_equal_to_summing(game,PortalToEnemyCastle[0]))) or (len(EnemyPortalToMyCastle)==0 and PortalToEnemyCastle and PortalToEnemyCastle[0].distance(game.get_enemy_castle()) < PortalToEnemyCastle[0].distance(game.get_my_castle()) and not (my_elf_to_enemy_castle and my_elf_to_enemy_castle[0].distance(game.get_enemy_castle()) < PortalToEnemyCastle[0].distance(game.get_enemy_castle()) and PortalToEnemyCastle[0].distance(game.get_enemy_castle()) > game.castle_size + 3*game.portal_size and game.get_enemy_castle().current_health > 30 and game.get_enemy_mana() + game.get_enemy().mana_per_turn*game.lava_giant_summoning_duration >= game.portal_cost and game.get_my_mana() < game.lava_giant_cost + game.tornado_cost)) and not not_equal_to_summing_tornado(game,PortalToEnemyCastle[0]):
        if for_check:
            return 1
        else:
            if not PortalToEnemyCastle[0].is_summoning and PortalToEnemyCastle[0].can_summon_lava_giant() and ((porta_need_over_protect(game,PortalToEnemyCastle[0]) == False) or (game.get_my_mana() >= game.lava_giant_cost + game.ice_troll_cost)):
                debug(game, "We have portal very close to enemy castle - summon lava giant")
                PortalToEnemyCastle[0].summon_lava_giant()
                return True
            if PortalToEnemyCastle[0].currently_summoning == "LavaGiant":
                return True
    # thre isnt enemy elves and my portal neer enemy castle then enemy portal to my castle 
    if len(game.get_enemy_living_elves()) == 0 and PortalToEnemyCastle and not (EnemyPortalToMyCastle and EnemyPortalToMyCastle[0].distance(game.get_my_castle()) < PortalToEnemyCastle[0].distance(game.get_enemy_castle())) and not not_equal_to_summing(game,PortalToEnemyCastle[0]) and not not_equal_to_summing_tornado(game,PortalToEnemyCastle[0]):
        if for_check:
            return 1
        else:
            if not PortalToEnemyCastle[0].is_summoning and PortalToEnemyCastle[0].can_summon_lava_giant():
                debug(game, "Thre isnt enemy elves - summon lava giant")
                PortalToEnemyCastle[0].summon_lava_giant()
                return True
            if PortalToEnemyCastle[0].currently_summoning == "LavaGiant":
                return True
    # to save my elf from enemy ice:
    for portal in game.get_my_portals():
        MyElfsfFromMyPortal = sorted(game.get_my_living_elves(), key = lambda MyElf: MyElf.distance(portal))
        EnemynNeerPortal = sorted(game.get_enemy_ice_trolls(), key = lambda enemy: enemy.distance(portal))
        if EnemynNeerPortal and MyElfsfFromMyPortal and not not_equal_to_summing(game,portal):
            turn_enemy_can_attack_my_elf = (EnemynNeerPortal[0].distance(MyElfsfFromMyPortal[0])-EnemynNeerPortal[0].attack_range)/EnemynNeerPortal[0].max_speed
            if game.get_myself().mana_per_turn == 0:
                turn_to_ice = 0
            else:
                turn_to_ice = (InufMana/game.get_myself().mana_per_turn)
            turn_portal_can_save_me =  TurnsToCreateLava+turn_to_ice
            if turn_enemy_can_attack_my_elf <= turn_portal_can_save_me and (portal.distance(MyElfsfFromMyPortal[0])/game.ice_troll_max_speed+game.ice_troll_summoning_duration) < EnemynNeerPortal[0].current_health:
                PortalToEnemy = sorted(game.get_my_portals(), key = lambda p: p.distance(EnemynNeerPortal[0]))
                distance_enemy_to_enemy_castle = EnemynNeerPortal[0].distance(game.get_enemy_castle())
                distance_portal_to_enemy_castle = PortalToEnemy[0].distance(game.get_enemy_castle())
                if not not_equal_to_summing(game,portal) and portal == PortalToEnemy[0] and distance_enemy_to_enemy_castle < distance_portal_to_enemy_castle and EnemynNeerPortal[0].current_health > game.lava_giant_summoning_duration:
                    if for_check:
                        return 1
                    if not portal.is_summoning and portal.can_summon_lava_giant():
                        debug(game, "Save my elf from enemy ice - summon lava giant")
                        portal.summon_lava_giant()
                        return True
                    if portal.currently_summoning == "LavaGiant":
                        return True
    # check if need the mana for deafence
    enemy_in_dangerous_place = False
    for enemy in game.get_enemy_living_elves():
        if distance_point_from_line(game.get_my_castle().location, game.get_enemy_castle().location, enemy.location) > 15*enemy.max_speed and enemy in mapElvesPerTurns.values():
            for elf in mapElvesPerTurns.keys():
                if mapElvesPerTurns[elf] == enemy and elf.distance(enemy) > game.portal_building_duration*elf.max_speed:
                    enemy_in_dangerous_place = True
    # my portal near enemy castel then enemy portal near my castle - (we can't loss)
    PortalToEnemyCastle = sorted(game.get_my_portals(), key = lambda portal: portal.distance(game.get_enemy_castle()))
    EnemyPortalToMyCastle = sorted(game.get_enemy_portals(), key = lambda portal: portal.distance(game.get_my_castle()))
    b = False 
    if (not enemy_in_dangerous_place and (PortalToEnemyCastle and EnemyPortalToMyCastle and PortalToEnemyCastle[0].distance(game.get_enemy_castle()) < EnemyPortalToMyCastle[0].distance(game.get_my_castle())) and  not not_equal_to_summing(game,PortalToEnemyCastle[0]))or (len(EnemyPortalToMyCastle)==0 and PortalToEnemyCastle) and not not_equal_to_summing(game,PortalToEnemyCastle[0]):
        if for_check:
            return 1
        else:
            for portal in PortalToEnemyCastle:
                if not portal.is_summoning and portal.can_summon_lava_giant() and game.get_my_mana() >= game.lava_giant_cost + game.ice_troll_cost and portal.distance(game.get_enemy_castle()) <= PortalToEnemyCastle[0].distance(game.get_enemy_castle()) + 2*game.ice_troll_max_speed:
                    debug(game, "We can't loos - summon lava giant")
                    portal.summon_lava_giant()
                    b =  True
                if portal.currently_summoning == "LavaGiant":
                    b = True
    if b:
        return b
    # sepshial:
    if not enemy_in_dangerous_place and PortalToEnemyCastle and not not_equal_to_summing(game,PortalToEnemyCastle[0]):
        if for_check:
            return 100
        else:
            if not PortalToEnemyCastle[0].is_summoning and PortalToEnemyCastle[0].can_summon_lava_giant() and game.get_my_mana() >= game.lava_giant_cost + game.ice_troll_cost:
                debug(game, "special event - summon lava giant")
                PortalToEnemyCastle[0].summon_lava_giant()
                return True
            if PortalToEnemyCastle[0].currently_summoning == "LavaGiant":
                return True
    # just attack
    b = False
    if not enemy_in_dangerous_place and PortalToEnemyCastle:
        if for_check:
            return 100
        for portal in PortalToEnemyCastle:
            if ((porta_need_over_protect(game,portal) == False) or (game.get_my_mana() >= game.lava_giant_cost + game.ice_troll_cost)) and not not_equal_to_summing(game,portal):
                if game.get_my_mana() >= game.lava_giant_cost + game.ice_troll_cost:
                    if not portal.is_summoning and portal.can_summon_lava_giant() and game.get_my_mana() - (sper_mana+game.lava_giant_cost) > 0 and portal.distance(game.get_enemy_castle()) < 2*portal.distance(game.get_my_castle()):
                        debug(game, "special event - summon lava giant")
                        portal.summon_lava_giant()
                        b = True
                    elif not portal.is_summoning and portal.can_summon_lava_giant() and game.get_my_mana() - (sper_mana+game.lava_giant_cost + game.mana_fountain_cost) > 0 and game.lava_giant_suffocation_per_turn*(int((portal.distance(game.get_my_castle())-game.lava_giant_attack_range)/game.lava_giant_max_speed)+5/game.lava_giant_attack_multiplier)<=game.lava_giant_max_health:
                        debug(game, "special event (all the attackers portals)- summon lava giant")
                        portal.summon_lava_giant()
                        b = True
                    elif not portal.is_summoning and portal.can_summon_lava_giant() and game.get_my_mana() > sper_mana + (game.mana_fountain_cost + game.portal_cost)/2 + game.lava_giant_cost:
                        debug(game, "special event (all portals)- summon lava giant")
                        portal.summon_lava_giant()
                        b = True
                    if portal.currently_summoning == "LavaGiant":
                        b = True
        return b
    # we can summon 
    if for_check:
        return 100
    return False    
  
def handel_portalsTorndo(game,for_check,sper_mana,priority_portal):
    
    sorted_tornadoes=sort_my_tornado(game)
    sorted_enemy_tornadoes=sort_enemy_tornado(game)
    sorted_enemy_ice=sort_enemy_ice(game)
    sorted_my_ice=sort_my_ice(game)
    # enemy portal near me
    d=False
    for portal in game.get_my_portals():
        building_to_portal=sorted(game.get_enemy_mana_fountains()+game.get_enemy_portals(),key=lambda b:b.distance(portal))
        if building_to_portal and not not_equal_to_summing_tornado(game,portal):
            count1=0
            count2=0
            for ice in game.get_enemy_ice_trolls():
                if distance_point_from_line(portal.location,building_to_portal[0].location,ice.location)<ice.attack_range+ice.max_speed and ice.distance(portal)<building_to_portal[0].distance(portal)+200 and ice.distance(building_to_portal[0])<building_to_portal[0].distance(portal)+200 and ice.distance(portal)/(game.tornado_max_speed+game.tornado_max_speed)<ice.current_health:
                    count1+=1
                if ice.distance(building_to_portal[0])<building_to_portal[0].size+ice.attack_range:
                    turn_came_to_ice = (ice.distance(portal)/game.tornado_max_speed)
                    if turn_came_to_ice > ice.current_health/2:
                        count2 +=0
                    else:
                        count2+=(ice.current_health/2-turn_came_to_ice)
            if portal.currently_summoning=="IceTroll":
                count2+=game.ice_troll_max_speed/2
            turn_to_tornado=game.tornado_suffocation_per_turn*((portal.distance(building_to_portal[0])-(game.tornado_attack_range+building_to_portal[0].size))/game.tornado_max_speed)
            if not not_equal_to_summing(game,portal) and (game.tornado_max_health-(1+count2+turn_to_tornado+count1*4*(game.ice_troll_attack_range/game.tornado_max_speed)))>building_to_portal[0].current_health/game.tornado_attack_multiplier:
                portal_to_building=sorted(game.get_my_portals(),key=lambda p:p.distance(building_to_portal[0]))
                if portal_to_building and portal==portal_to_building[0] and building_to_portal[0] in game.get_enemy_portals():
                    check=True
                    for tornado in game.get_my_tornadoes():
                        if sorted_tornadoes[tornado]==building_to_portal[0]:
                            check=False
                    check2=True
                    for elf in game.get_my_living_elves():
                        if elf.currently_building =="Portal" and elf.distance(building_to_portal[0])<portal_to_building[0].distance(building_to_portal[0]):
                            check2=False
                    check3=False
                    for tornado in game.get_enemy_tornadoes():
                        if sorted_enemy_tornadoes[tornado]==portal and  tornado.current_health>(tornado.distance(portal)-(portal.size+tornado.attack_range))/tornado.max_speed+portal.current_health/game.tornado_attack_multiplier:
                            check3=True
                    for enemy_portal in game.get_enemy_portals():
                        if enemy_portal.currently_summoning=="Tornado" and enemy_portal.distance(portal)<diagonal_line/3.5:
                            check3=True
                    check_if_someone_attack=False
                    for elf in game.get_my_living_elves():
                        if attack[elf]==building_to_portal[0]:
                            check_if_someone_attack=True
                    check7=True
                    for k in mapElvesPerTurns.keys():
                        if mapElvesPerTurns[k] == building_to_portal[0] and k not in sorted_enemy_ice.values() and k.distance(building_to_portal[0])<6*game.elf_max_speed+game.portal_size+game.elf_attack_range:
                            check7=False
                    enemy_portal_to_me=sorted(game.get_enemy_portals(),key=lambda p:p.distance(portal))
                    elf_to_portal=sorted(game.get_my_living_elves(),key=lambda e:e.distance(portal))
                    enemy_elf_to_portal=sorted(game.get_enemy_living_elves(),key=lambda e:e.distance(portal))
                    if  check2 and check3 and check7 and not check_if_someone_attack and  enemy_portal_to_me and  enemy_portal_to_me[0].distance(portal)<diagonal_line/3.5 and ((check) or (enemy_elf_to_portal and enemy_elf_to_portal[0].distance(portal)<enemy_elf_to_portal[0].max_speed+enemy_elf_to_portal[0].attack_range)):
                        if for_check :
                            return 0
                        if not portal.is_summoning and portal.can_summon_tornado():
                            debug(game, "there is portal next to me -summon torndo-0")
                            portal.summon_tornado()
                            d=True
                        if portal.currently_summoning == "Tornado":
                            d=True
                    if_dangerous_portal=game.lava_giant_suffocation_per_turn*(int((building_to_portal[0].distance(game.get_my_castle())-game.lava_giant_attack_range-game.castle_size)/game.lava_giant_max_speed)+10/game.lava_giant_attack_multiplier)<=game.lava_giant_max_health 
                    if_portal_far_from_middle=distance_point_from_line(game.get_enemy_castle().location ,game.get_my_castle().location,building_to_portal[0].location)>diagonal_line/7
                    if check and check2 and if_dangerous_portal and if_portal_far_from_middle and not check_if_someone_attack:
                        if for_check :
                            return 0
                        if not portal.is_summoning and portal.can_summon_tornado():
                            debug(game, "there is ahushiling dangerous portal-summon torndo-0")
                            portal.summon_tornado()
                            d=True
                        if portal.currently_summoning == "Tornado":
                            d=True
                    if building_to_portal[0].distance(portal)<diagonal_line/18+game.portal_size*2 and check and check2 and not check_if_someone_attack:
                        if for_check :
                            return 0
                        if not portal.is_summoning and portal.can_summon_tornado():
                            debug(game, "there is ahushiling close portal-summon torndo-0")
                            portal.summon_tornado()
                            d=True
                        if portal.currently_summoning == "Tornado":
                            d=True
    if d:
        return d
    
    #there is enemy portal next to me (very near )- we sommun
    d=False
    for portal in game.get_my_portals():
        enemy_portal_to_portal=sorted(game.get_enemy_portals(),key=lambda p:p.distance(portal))
        if not not_equal_to_summing_tornado(game,portal) and enemy_portal_to_portal and enemy_portal_to_portal[0].distance(portal)<game.portal_size*3+game.tornado_max_speed*game.tornado_summoning_duration+300:
            elf_to_building=sorted(game.get_my_living_elves(),key=lambda e:e.distance(enemy_portal_to_portal[0]))
            portal_to_building=sorted(game.get_my_portals(),key=lambda p:p.distance(enemy_portal_to_portal[0]))
            check=True
            for tornado in game.get_my_tornadoes():
                if sorted_tornadoes[tornado]==enemy_portal_to_portal[0]:
                    check=False
            check_if_someone_attack=False
            for elf in game.get_my_living_elves():
                if attack[elf]==enemy_portal_to_portal[0]:
                    check_if_someone_attack=True
            check7=True
            for k in mapElvesPerTurns.keys():
                if mapElvesPerTurns[k] == enemy_portal_to_portal[0] and k not in sorted_enemy_ice.values() and k.distance(enemy_portal_to_portal[0])<5*game.elf_max_speed+game.portal_size+game.elf_attack_range and attack[k] == None:
                    check7=False
            if check and check7 and not check_if_someone_attack and portal_to_building and portal_to_building[0]==portal :
                portal_summing = False
                for my_portal in game.get_my_portals():
                    if tornado_turget_after_summing(game,my_portal) == enemy_portal_to_portal[0]:
                        portal_summing = True
                if portal_summing:
                    if for_check :
                        return 1
                    if not portal.is_summoning and portal.can_summon_tornado():
                        debug(game, "there is enemy portal next to me -summon torndo-1")
                        portal.summon_tornado()
                        d=True
                    if portal.currently_summoning == "Tornado":
                        d=True
    if d:
        return d
        
    #there is elf that building next to me so we summon tornado            
    for enemy_elf in game.get_enemy_living_elves():
        portal_to_enemy_elf=sorted(game.get_my_portals(),key=lambda p:p.distance(enemy_elf))
        if (enemy_elf.currently_building =="Portal" or (enemy_elf.currently_building =="ManaFountain" and not game.get_enemy_portals())) and enemy_elf.turns_to_build<=game.tornado_summoning_duration and ( (portal_to_enemy_elf and  (portal_to_enemy_elf[0].distance(enemy_elf)<(2*game.portal_size +game.tornado_attack_range + game.tornado_max_speed*game.tornado_max_health/3*game.tornado_suffocation_per_turn)) )or (not game.get_enemy_portals() and not game.get_enemy_ice_trolls() and portal_to_enemy_elf and (portal_to_enemy_elf[0].distance(enemy_elf)-(game.mana_fountain_size+game.tornado_attack_range))/game.tornado_max_speed < (3*game.tornado_max_health/4 )) or (not game.get_enemy_portals() and portal_to_enemy_elf and (portal_to_enemy_elf[0].distance(enemy_elf)-(game.mana_fountain_size+game.tornado_attack_range))/game.tornado_max_speed < (3*game.tornado_max_health/4 - 3 )) ):
            check3=True
            for portal1 in game.get_my_portals():
                if portal1.distance(enemy_elf)<3*game.portal_size and portal1.currently_summoning=="Tornado":
                    check3=False
            other_tornado_attack = False
            for tornado in game.get_my_tornadoes():
                enemy_obj = sorted(game.get_enemy_portals() + game.get_enemy_mana_fountains() + [enemy_elf],key = lambda e: e.distance(tornado))
                if enemy_obj and enemy_obj[0] == enemy_elf and (tornado.distance(enemy_obj[0])-(tornado.attack_range))/tornado.max_speed+game.portal_max_health+enemy_elf.turns_to_build<tornado.current_health:
                    other_tornado_attack = True
            building_to_portal=sorted(game.get_enemy_portals()+game.get_enemy_mana_fountains(),key=lambda b:b.distance(portal_to_enemy_elf[0]))
            enemy_succes_build = True
            for k in attack.keys():
                if attack[k] == enemy_elf and enemy_elf.current_health <= enemy_elf.turns_to_build and enemy_attackers_count(game,k) <= 1:
                    enemy_succes_build = False
            if enemy_succes_build and not other_tornado_attack and not not_equal_to_summing_tornado(game,portal_to_enemy_elf[0]) and check3 and ((not building_to_portal)or (building_to_portal and building_to_portal[0].distance(portal_to_enemy_elf[0])>enemy_elf.distance(portal_to_enemy_elf[0]))):
                if for_check :
                    return 1
                if not portal_to_enemy_elf[0].is_summoning and portal_to_enemy_elf[0].can_summon_tornado():
                    debug(game, "there is enemy elf next to me that build a portal - sommun tornado-1")
                    portal_to_enemy_elf[0].summon_tornado()
                    d=True
                if portal_to_enemy_elf[0].currently_summoning == "Tornado":
                    d=True
    if d:
        return d 
        
    # dangerous portal next to me so sommun tornado
    portal_to_my_castle = sorted(game.get_my_portals() , key = lambda p: p.distance(game.get_my_castle()))
    for portal in portal_to_my_castle:
        building_to_portal=sorted(game.get_enemy_portals()+game.get_enemy_mana_fountains(),key=lambda b:b.distance(portal))
        if building_to_portal and not not_equal_to_summing_tornado(game,portal):
            count1=1
            count2=0
            for ice in game.get_enemy_ice_trolls():
                if distance_point_from_line(portal.location,building_to_portal[0].location,ice.location)<ice.attack_range+ice.max_speed and ice.distance(portal)<building_to_portal[0].distance(portal)+200 and ice.distance(building_to_portal[0])<building_to_portal[0].distance(portal)+200 and ice.distance(portal)/(game.tornado_max_speed+game.tornado_max_speed)<ice.current_health:
                    count1+=1
                if ice.distance(building_to_portal[0])<building_to_portal[0].size+ice.attack_range:
                    turn_came_to_ice = (ice.distance(portal)/game.tornado_max_speed)
                    if turn_came_to_ice > ice.current_health/2:
                        count2 +=0
                    else:
                        count2+=(ice.current_health/2-turn_came_to_ice)
            if portal.currently_summoning=="IceTroll":
                count2+=game.ice_troll_max_speed/2
            turn_to_tornado=game.tornado_suffocation_per_turn*((portal.distance(building_to_portal[0])-(game.tornado_attack_range+building_to_portal[0].size))/game.tornado_max_speed)
            if (game.tornado_max_health-(1+count2 +turn_to_tornado+count1*4*(game.ice_troll_attack_range/game.tornado_max_speed)))>building_to_portal[0].current_health/game.tornado_attack_multiplier:
                portal_to_building=sorted(game.get_my_portals(),key=lambda p:p.distance(building_to_portal[0]))
                if_dangerous_portal=game.lava_giant_suffocation_per_turn*(int((building_to_portal[0].distance(game.get_my_castle())-game.lava_giant_attack_range-game.castle_size)/game.lava_giant_max_speed)+8/game.lava_giant_attack_multiplier)<=game.lava_giant_max_health 
                if (building_to_portal[0] in dangerous_portal1.values() or if_dangerous_portal)and portal_to_building and portal==portal_to_building[0] :
                    elf_to_building=sorted(game.get_my_living_elves(),key=lambda e:e.distance(building_to_portal[0]))
                    check2=True
                    for elf in game.get_my_living_elves():
                        if elf.currently_building=="Portal" and elf.distance(building_to_portal[0])+diagonal_line/20<portal_to_building[0].distance(building_to_portal[0]):
                            check2=False
                    check=True
                    for tornado in game.get_my_tornadoes():
                        if sorted_tornadoes[tornado]==building_to_portal[0]:
                            check=False
                    check7=True
                    for k in mapElvesPerTurns.keys():
                        if mapElvesPerTurns[k] == building_to_portal[0] and k not in sorted_enemy_ice.values() and k.distance(building_to_portal[0])<diagonal_line/8+game.portal_size+game.elf_attack_range:
                            enemy_elf_to_portal=sorted(game.get_enemy_living_elves(),key=lambda e:e.distance(building_to_portal[0]))
                            if not(enemy_elf_to_portal and enemy_elf_to_portal[0].distance(building_to_portal[0])<k.distance(building_to_portal[0])):
                                check7=False
                    check_if_someone_attack=False
                    for elf in game.get_my_living_elves():
                        if attack[elf]==building_to_portal[0]:
                            check_if_someone_attack=True
                    if check2 and check7 and check and not check_if_someone_attack and portal_to_building and portal_to_building[0] == portal :
                        if for_check :
                            return 1
                        if not portal.is_summoning and portal.can_summon_tornado() :
                            debug(game, "there is dangerous enemy building that we can destroy -summon torndo-1")
                            portal.summon_tornado()
                            d=True
                        if portal.currently_summoning == "Tornado":
                            d= True
    if d:
        return d
        
    #there is enemy mana fountain that we can destroy (priority 2)    
    for portal in game.get_my_portals():
        building_to_portal=sorted(game.get_enemy_mana_fountains()+game.get_enemy_portals(),key=lambda b:b.distance(portal))
        if building_to_portal and not not_equal_to_summing_tornado(game,portal):
            count1=0
            count2=0
            for ice in game.get_enemy_ice_trolls():
                if distance_point_from_line(portal.location,building_to_portal[0].location,ice.location)<ice.attack_range+ice.max_speed and ice.distance(portal)<building_to_portal[0].distance(portal)+200 and ice.distance(building_to_portal[0])<building_to_portal[0].distance(portal)+200 and ice.distance(portal)/(game.tornado_max_speed+game.tornado_max_speed)<ice.current_health:
                    count1+=1
                if ice.distance(building_to_portal[0])<building_to_portal[0].size+ice.attack_range:
                    turn_came_to_ice = (ice.distance(portal)/game.tornado_max_speed)
                    if turn_came_to_ice > ice.current_health/2:
                        count2 +=0
                    else:
                        count2+=(ice.current_health/2-turn_came_to_ice)
            if portal.currently_summoning=="IceTroll":
                count2+=game.ice_troll_max_speed/2
            turn_to_tornado=game.tornado_suffocation_per_turn*((portal.distance(building_to_portal[0])-(game.tornado_attack_range+building_to_portal[0].size))/game.tornado_max_speed)
            if (game.tornado_max_health-(1+count2+turn_to_tornado+count1*4*(game.ice_troll_attack_range/game.tornado_max_speed)))>building_to_portal[0].current_health/game.tornado_attack_multiplier  and (portal.distance(building_to_portal[0]) - (game.mana_fountain_size + game.tornado_attack_range))/game.tornado_max_speed < (game.tornado_max_health/3)*game.tornado_suffocation_per_turn:
                portal_to_building=sorted(game.get_my_portals(),key=lambda p:p.distance(building_to_portal[0]))
                if portal_to_building and portal==portal_to_building[0] and building_to_portal[0] in game.get_enemy_mana_fountains():
                    elf_to_building=sorted(game.get_my_living_elves(),key=lambda e:e.distance(building_to_portal[0]))
                    check2=True
                    for elf in game.get_my_living_elves():
                        if elf.currently_building =="Portal" and elf.distance(building_to_portal[0])<portal_to_building[0].distance(building_to_portal[0]):
                            check2=False
                    check=True
                    for tornado in game.get_my_tornadoes():
                        if sorted_tornadoes[tornado]==building_to_portal[0] and tornado.current_health>(tornado.distance(building_to_portal[0])-(building_to_portal[0].size+tornado.attack_range))/tornado.max_speed+building_to_portal[0].current_health/game.tornado_attack_multiplier:
                            check=False
                    check_if_someone_attack=False
                    for elf in game.get_my_living_elves():
                        if attack[elf]==building_to_portal[0]:
                            check_if_someone_attack=True
                    check_if_elf_already_go=False
                    for elf1 in game.get_my_living_elves():
                        if elf1 in mapElvesPerTurns.keys() and mapElvesPerTurns[elf1] == building_to_portal[0] and elf1.distance(mapElvesPerTurns[elf1])<elf1.attack_range+building_to_portal[0].size+diagonal_line/12:
                            check_if_elf_already_go=True
                    if not check_if_elf_already_go and check2 and check and not check_if_someone_attack:
                        if for_check :
                            return 2
                        if not portal.is_summoning and portal.can_summon_tornado() :
                            debug(game, "there is enemy mana fountain that we can destroy (priority 2)- summon torndo ")
                            portal.summon_tornado()
                            d=True
                        if portal.currently_summoning == "Tornado":
                            d= True
    if d:
        return d
        
    for portal in game.get_my_portals():
        building_to_portal=sorted(game.get_enemy_mana_fountains()+game.get_enemy_portals(),key=lambda b:b.distance(portal))
        if building_to_portal and not not_equal_to_summing_tornado(game,portal):
            count1=0
            count2=0
            for ice in game.get_enemy_ice_trolls():
                if distance_point_from_line(portal.location,building_to_portal[0].location,ice.location)<ice.attack_range+ice.max_speed and ice.distance(portal)<building_to_portal[0].distance(portal)+200 and ice.distance(building_to_portal[0])<building_to_portal[0].distance(portal)+200 and ice.distance(portal)/(game.tornado_max_speed+game.tornado_max_speed)<ice.current_health:
                    count1+=1
                if ice.distance(building_to_portal[0])<building_to_portal[0].size+ice.attack_range+ice.max_speed*2:
                    turn_came_to_ice = (ice.distance(portal)/game.tornado_max_speed)
                    if turn_came_to_ice > ice.current_health/2:
                        count2 +=0
                    else:
                        count2+=(ice.current_health/2-turn_came_to_ice)
            if portal.currently_summoning=="IceTroll":
                count2+=game.ice_troll_max_speed/2
            turn_to_tornado=game.tornado_suffocation_per_turn*((portal.distance(building_to_portal[0])-(game.tornado_attack_range+building_to_portal[0].size))/game.tornado_max_speed)
            if (game.tornado_max_health-(3+1+count2+turn_to_tornado+count1*4*(game.ice_troll_attack_range/game.tornado_max_speed)))>(building_to_portal[0].current_health/game.tornado_attack_multiplier):
                portal_to_building=sorted(game.get_my_portals(),key=lambda p:p.distance(building_to_portal[0]))
                if portal_to_building and portal==portal_to_building[0]:
                    check3=True
                    for e in game.get_my_living_elves()+game.get_enemy_living_elves():
                        if e.distance(game.get_enemy_castle())>e.distance(game.get_my_castle()):
                            check3=False
                    if game.get_myself().mana_per_turn<game.get_enemy().mana_per_turn:
                        check3=False
                    PortalToEnemyCastle = sorted(game.get_my_portals(), key = lambda portal: portal.distance(game.get_enemy_castle()))
                    EnemyPortalToMyCastle = sorted(game.get_enemy_portals(), key = lambda portal: portal.distance(game.get_my_castle()))
                    if (PortalToEnemyCastle and EnemyPortalToMyCastle and PortalToEnemyCastle[0].distance(game.get_enemy_castle()) > EnemyPortalToMyCastle[0].distance(game.get_my_castle())) :
                        check3=False
                    elf_to_building=sorted(game.get_my_living_elves(),key=lambda e:e.distance(building_to_portal[0]))
                    check2=True
                    for elf in game.get_my_living_elves():
                        if elf.currently_building=="Portal" and elf.distance(building_to_portal[0])<portal_to_building[0].distance(building_to_portal[0]):
                            check2=False
                    check=True
                    for tornado in game.get_my_tornadoes():
                        if sorted_tornadoes[tornado]==building_to_portal[0] and tornado.current_health>(tornado.distance(building_to_portal[0])-(building_to_portal[0].size+tornado.attack_range))/tornado.max_speed+building_to_portal[0].current_health/game.tornado_attack_multiplier:
                            check=False
                    check_if_someone_attack=False
                    for elf in game.get_my_living_elves():
                        if attack[elf]==building_to_portal[0]:
                            check_if_someone_attack=True
                    if check2 and check and check3 and not check_if_someone_attack and game.get_my_castle().current_health>game.get_enemy_castle().current_health:
                        if for_check :
                            return 2
                        if not portal.is_summoning and portal.can_summon_tornado() :
                            debug(game, "summon like maniake tornado-2")
                            portal.summon_tornado()
                            d=True
                        if portal.currently_summoning == "Tornado":
                            d= True
    if d:
        return d                        
    # destroy enemy mana fountain
    if not game.get_enemy_portals() and game.get_my_portals() and game.get_enemy_mana_fountains() and len(game.get_enemy_mana_fountains()) >= len(game.get_my_mana_fountains()) and not game.get_enemy_ice_trolls():
        my_portal,enemy_fountain,portals_dis = nearest_portals(game)
        check=True
        for tornado in game.get_my_tornadoes():
            if sorted_tornadoes[tornado]==enemy_fountain and tornado.current_health>(tornado.distance(enemy_fountain)-(enemy_fountain.size+tornado.attack_range))/tornado.max_speed+enemy_fountain.current_health/game.tornado_attack_multiplier:
                check=False
        check_if_elf_already_go=False
        for elf1 in game.get_my_living_elves():
            if elf1 in mapElvesPerTurns.keys() and mapElvesPerTurns[elf1] == building_to_portal[0] and elf1.distance(mapElvesPerTurns[elf1])<elf1.attack_range+building_to_portal[0].size+diagonal_line/12:
                check_if_elf_already_go=True
        if not check_if_elf_already_go and not not_equal_to_summing_tornado(game,portal) and enemy_fountain not in attack.values() and (portals_dis/game.tornado_max_speed)*game.tornado_suffocation_per_turn < 2*(game.tornado_max_health)/3 - (enemy_fountain.current_health/game.tornado_attack_multiplier) and check:
            if for_check :
                return 2
            if not my_portal.is_summoning and my_portal.can_summon_tornado() :
                debug(game, "destroy enemy mana fountain - summon Tornado")
                my_portal.summon_tornado()
                return True
            if my_portal.currently_summoning == "Tornado":
                return True
    if for_check:
        return 100
    return False

def nearest_portals(game):
    my_portal = None
    enemy_fountain = None
    portals_dis = None
    for portal in game.get_my_portals():
        enemy_fountain_to_portal = sorted(game.get_enemy_mana_fountains(), key = lambda p: p.distance(portal))
        if enemy_fountain_to_portal and my_portal == None and enemy_fountain == None and portals_dis == None:
            my_portal = portal
            enemy_fountain = enemy_fountain_to_portal[0]
            portals_dis = my_portal.distance(enemy_fountain) - (game.mana_fountain_size + game.tornado_attack_range)
        elif enemy_fountain_to_portal and (enemy_fountain_to_portal[0].distance(portal) - (game.mana_fountain_size + game.tornado_attack_range)) < (portals_dis - (game.tornado_attack_range)):
            my_portal = portal
            enemy_fountain = enemy_fountain_to_portal[0]
            portals_dis = enemy_fountain_to_portal[0].distance(portal)- (game.mana_fountain_size + game.tornado_attack_range)
    return my_portal,enemy_fountain,portals_dis

def tornado_turget_after_summing(game,portal):
    if portal in game.get_my_portals():
        enemy_obj = sorted(game.get_enemy_portals()+game.get_enemy_mana_fountains(), key = lambda obj: obj.distance(portal))
        if enemy_obj:
            return enemy_obj[0]
    if portal in game.get_enemy_portals():
        my_obj = sorted(game.get_my_portals()+game.get_my_mana_fountains(), key = lambda obj: obj.distance(portal))
        if my_obj:
            return my_obj[0]
    return None

def most_portal_for_summing_tornado(game,enemy_obj):
    most_portal = None
    optional_portals_for_summing = []
    for portal in game.get_my_portals():
        obj_to_portal = sorted(game.get_enemy_mana_fountains() + game.get_enemy_portals(), key = lambda obj: obj.distance(portal))
        if obj_to_portal and obj_to_portal[0] == enemy_obj:
            optional_portals_for_summing.append(portal)
    for portal in optional_portals_for_summing:
        if most_portal == None:
            most_portal = portal
        elif portal.distance(enemy_obj) < most_portal.distance(enemy_obj):
            most_portal = portal
    return most_portal
            
def ice_troll_full_summoning(game,portal_for_protect,sper_mana,message):
    b = False
    if not not_equal_to_summing(game,portal_for_protect[0]) and not portal_for_protect[0].is_summoning and portal_for_protect[0].can_summon_ice_troll() and game.get_my_mana() > sper_mana:
        portal_for_protect[0].summon_ice_troll()
        debug(game,message)
        b = True
    if portal_for_protect[0].currently_summoning == "IceTroll":
        b = True    
    return b
    
def stay_in_my_plase(game,elf,mapElves):
    less_mana = game.mana_fountain_cost - game.get_my_mana()
    if game.get_myself().mana_per_turn==0:
        turn_to_get_the_nama=0
    else:
        turn_to_get_the_nama = less_mana/game.get_myself().mana_per_turn
    if less_mana > 0 and elf in mapElves.keys():
        loc = elf.location.towards(mapElves[elf],elf.max_speed*turn_to_get_the_nama)
        if loc.distance(game.get_my_castle()) < loc.distance(game.get_enemy_castle()):
            return True
        return False
    else:
        if elf.location.distance(game.get_my_castle()) < elf.location.distance(game.get_enemy_castle()):
            return True
        return False 
    
def porta_need_over_protect(game,portal):
    my_portal_to_enemy = sorted(game.get_my_portals(),key = lambda p: p.distance(game.get_enemy_castle()))
    if my_portal_to_enemy and portal == my_portal_to_enemy[0] and portal.distance(game.get_enemy_castle()) < game.castle_size + game.elf_attack_range + 5*game.elf_max_speed:
        return True
    return False
    
def check_location_for_build_fountain(game,loc):
    optional_lacations=list_fountain
    check=False
    if loc in optional_lacations:
       return True
    if loc.distance(game.get_my_castle()) < game.mana_fountain_size + game.castle_size + diagonal_line/30:
        return True
    enemy_portal_to_loc=sorted(game.get_enemy_portals(),key=lambda p:p.distance(loc))
    if loc.distance(game.get_my_castle()) < game.mana_fountain_size + game.castle_size + 2*game.elf_max_speed and not game.get_enemy_portals():
        return True
    for my_portal in game.get_my_portals():
        if enemy_portal_to_loc and my_portal.distance(loc)<game.portal_size+game.mana_fountain_size+game.ice_troll_max_speed*3 and distance_point_from_line(my_portal.location,enemy_portal_to_loc[0].location,loc)<game.portal_size+100 and loc.distance(my_portal)<loc.distance(enemy_portal_to_loc[0]) and my_portal.distance(enemy_portal_to_loc[0])<loc.distance(enemy_portal_to_loc[0]):
            check=True
    if (not check and len(game.get_my_mana_fountains())>0)or (game.turn>50 and not check):
        return False
    if len(game.get_enemy_living_elves())+1<len(game.get_my_living_elves()):
        return False
    enemy_to_loc = sorted (game.get_enemy_living_elves(),key=lambda e:e.distance(loc))
    portal_to_loc=sorted(game.get_my_portals(),key=lambda p:p.distance(loc))
    if enemy_to_loc and portal_to_loc and (enemy_to_loc[0].distance(loc)<portal_to_loc[0].distance(loc)+game.ice_troll_summoning_duration*game.elf_max_speed+100 ):
        return False
    if loc.distance(game.get_my_castle()) >loc.distance(game.get_enemy_castle()):
        return False
    for portal in game.get_enemy_portals():
        if portal.distance(loc)<game.portal_size+game.mana_fountain_size+(game.ice_troll_max_speed)*4:
            return False
    return True    
    
def check_location_for_build_portal(game,loc):
    enemy_portal_to_loc = sorted (game.get_enemy_portals(),key=lambda p:p.distance(loc))
    if enemy_portal_to_loc and enemy_portal_to_loc[0].distance(loc)<20*game.ice_troll_max_speed:
        return False
    if game.lava_giant_suffocation_per_turn*(int((loc.distance(game.get_my_castle())-game.lava_giant_attack_range)/game.lava_giant_max_speed)+12/game.lava_giant_attack_multiplier)>=game.lava_giant_max_health :
        return False
    if loc.distance(game.get_my_castle())<loc.distance(game.get_enemy_castle()):
        return False
    return True    

def not_equal_to_summing(game,portal):
    EnemynElfNeerPortal = sorted(game.get_enemy_living_elves() ,key = lambda e: e.distance(portal))
    enemy_tornado = sorted(game.get_enemy_tornadoes() ,key = lambda e: e.distance(portal))
    portal_will_destroy = False
    if EnemynElfNeerPortal and (EnemynElfNeerPortal[0].distance(portal) -(EnemynElfNeerPortal[0].attack_range + portal.size) )/EnemynElfNeerPortal[0].max_speed + portal.current_health/EnemynElfNeerPortal[0].attack_multiplier < game.ice_troll_summoning_duration + 1 and attackers_count12(game,EnemynElfNeerPortal[0]) == 0:
        portal_will_destroy = True
    if enemy_tornado and enemy_tornado[0].distance(portal) <= enemy_tornado[0].attack_range+enemy_tornado[0].max_speed+portal.size:
        portal_will_destroy = True
    enemy_attackers = 0
    for enemy in game.get_enemy_living_elves() + game.get_enemy_tornadoes():
        if enemy in game.get_enemy_living_elves() and enemy.distance(portal) < portal.size + enemy.attack_range + enemy.max_speed:
            enemy_attackers +=1
        if enemy in game.get_enemy_tornadoes() and enemy.distance(portal) < portal.size + enemy.attack_range + 3*enemy.max_speed:
            enemy_attackers +=1
    for enemy in game.get_enemy_living_elves():
        if enemy.distance(portal)<portal.size+enemy.attack_range+enemy.max_speed and enemy not in attack.values() and portal.current_health<portal.max_health/2*enemy.attack_multiplier:
            portal_will_destroy = True
    if enemy_attackers > 1:
        portal_will_destroy = True
    return portal_will_destroy
    
def not_equal_to_summing_tornado(game,portal):
    EnemynElfNeerPortal1 = sorted(game.get_enemy_tornadoes() ,key = lambda e: e.distance(portal))
    portal_will_destroy = False
    if EnemynElfNeerPortal1 and (EnemynElfNeerPortal1[0].distance(portal) -(EnemynElfNeerPortal1[0].attack_range + portal.size) )/EnemynElfNeerPortal1[0].max_speed + portal.current_health/EnemynElfNeerPortal1[0].attack_multiplier < game.tornado_summoning_duration + 1 and (attackers_count12(game,EnemynElfNeerPortal1[0]) - elf_attackers_count(game,EnemynElfNeerPortal1[0])) <= 0 and EnemynElfNeerPortal1[0].current_health >= (EnemynElfNeerPortal1[0].distance(portal) -(EnemynElfNeerPortal1[0].attack_range + portal.size) )/EnemynElfNeerPortal1[0].max_speed + portal.current_health/EnemynElfNeerPortal1[0].attack_multiplier:
        portal_will_destroy = True
    if EnemynElfNeerPortal1 and EnemynElfNeerPortal1[0].distance(portal) < portal.size + 2*game.tornado_max_speed + game.tornado_attack_range and portal.current_health < 3:
        portal_will_destroy = True
    EnemynElfNeerPortal = sorted(game.get_enemy_living_elves() ,key = lambda e: e.distance(portal))
    if EnemynElfNeerPortal and (EnemynElfNeerPortal[0].distance(portal) -(EnemynElfNeerPortal[0].attack_range + portal.size) )/EnemynElfNeerPortal[0].max_speed + portal.current_health/EnemynElfNeerPortal[0].attack_multiplier < game.tornado_summoning_duration + 1 and attackers_count12(game,EnemynElfNeerPortal[0]) <= 0:
        portal_will_destroy = True
    
    return portal_will_destroy
    
def if_it_equal_to_build_mana_fountain(game):
    enemy_elf_turns_to_revive=sorted(game.get_all_enemy_elves(),key=lambda e:e.turns_to_revive)
    if not game.get_enemy_living_elves() or (len(game.get_my_portals())>len(game.get_enemy_portals()) and len(game.get_enemy_living_elves())<len(game.get_my_living_elves())):
        turns_until_enemy_destroy_my_mana=enemy_elf_turns_to_revive[0].turns_to_revive+enemy_elf_turns_to_revive[0].initial_location.distance(game.get_my_castle())/game.elf_max_speed
        if turns_until_enemy_destroy_my_mana>=40:
            return True
    if game.get_enemy_mana() > 2*game.get_my_mana() and game.get_my_mana() > 1.5*game.lava_giant_cost:
        return True
    return False
    
def if_tornado_will_arrive_to_destination(game,tornado,destination):
    if destination in game.get_enemy_portals()+game.get_enemy_mana_fountains():
        turn_to_come=(tornado.distance(destination)-(tornado.attack_range+destination.size))/tornado.max_speed
        sorted_enemy_ice=sort_enemy_ice(game)
        count1=0
        for ice in game.get_enemy_ice_trolls():
            if sorted_enemy_ice[ice]==tornado and distance_point_from_line(tornado.location,destination.location,ice.location)<ice.attack_range+ice.max_speed and ice.distance(tornado)<destination.distance(tornado)+200 and ice.distance(destination)<destination.distance(tornado)+200:
                count1+=1
        if tornado.current_health-(turn_to_come-(2+count1*2*(game.ice_troll_attack_range/tornado.max_speed)))>destination.current_health/tornado.attack_multiplier:
            return True
    return False
    
#***************************Spells************************************

def handel_invisibility_spell(game,mapElves,for_check):
    global casting_elves
    global Elves_invisibility_turns
    sorted_enemy_ice=sort_enemy_ice(game)
    sorted_my_ice = sort_my_ice(game)
    # so many attackers
    for elf in game.get_my_living_elves():
        count_enemy = 0
        count_enemy_elf = 0
        for enemy_ice in game.get_enemy_ice_trolls():
            if enemy_ice.distance(elf) < enemy_ice.attack_range + enemy_ice.max_speed + 1:
                count_enemy +=1
        for enemy_elf in game.get_enemy_living_elves():
            if enemy_elf.distance(elf) < enemy_elf.attack_range + 4*enemy_elf.max_speed + 1:
                count_enemy_elf +=1
        my_elf_to_me = sorted(game.get_my_living_elves(), key = lambda e: e.distance(elf))
        if (count_enemy > 4) or (((len(my_elf_to_me) < 2) or (my_elf_to_me[1].distance(elf) > 6*elf.max_speed)) and count_enemy_elf > 3):        
            if casting_elves[elf] == False and spell_casted(game,elf)!="invisibility" and  spell_casted(game,elf) != "both of them" :
                if for_check:
                    return 1
                if elf.can_cast_invisibility():
                    sortdebug(game, "so many attackers")
                    elf.cast_invisibility()
                    casting_elves[elf]=True
                    Elves_invisibility_turns[elf] = game.invisibility_expiration_turns
                    return True

    #hiding from enemy ice and dangerous elf                
    for elf in game.get_my_living_elves():
        enemy_ice_to_me =sorted(game.get_enemy_ice_trolls(),key=lambda i:i.distance(elf))
        if enemy_ice_to_me and dangerous_elf1[elf]!=None and elf.in_attack_range(dangerous_elf1[elf]) and enemy_ice_to_me[0].distance(elf)<=enemy_ice_to_me[0].attack_range and enemy_ice_to_me[0].current_health>3:
            turn_i_kill = dangerous_elf1[elf].current_health/attackers_count(game,dangerous_elf1[elf])
            turn_enemy_kill = elf.current_health/enemy_attackers_count(game,elf)
            if turn_i_kill>turn_enemy_kill and casting_elves[elf]==False and sorted_enemy_ice[enemy_ice_to_me[0]] == elf:
                if for_check:
                    return 1
                if elf.can_cast_invisibility():
                    sortdebug(game, "hiding from enemy ice and dangerous elf")
                    elf.cast_invisibility()
                    casting_elves[elf]=True
                    Elves_invisibility_turns[elf] = game.invisibility_expiration_turns
                    return True
                    
    # use invisibility for hiding from enemy ice
    for elf in game.get_my_living_elves():
        portal_to_elf = sorted(game.get_enemy_portals(), key = lambda p: p.distance(elf))
        run=need_run(game,elf)
        if not(portal_to_elf and elf.in_attack_range(portal_to_elf[0])):
            if run!=None and run.current_health>5 and (dangerous_elf1[elf]!=None) and casting_elves[elf] == False and (spell_casted(game,elf) != "both of them" and  spell_casted(game,elf) !="invisibility") and run.distance(mapElves[elf]) <= elf.distance(mapElves[elf]) and run.distance(elf) <= mapElves[elf].distance(elf) and mapElves[elf] == dangerous_elf1[elf] and (elf.current_health<=game.elf_max_health/2 or elf.current_health+2<dangerous_elf1[elf].current_health) and elf.current_health >= dangerous_elf1[elf].current_health and not (dangerous_elf1[elf].current_health <= dangerous_elf1[elf].max_health/6 and elf.distance(dangerous_elf1[elf]) > elf.max_speed*7 and dangerous_elf1[elf] in sorted_my_ice.values()):
                if run in game.get_enemy_ice_trolls() and sorted_enemy_ice[run]!=elf:
                    continue
                if for_check:
                    return 1
                if elf.can_cast_invisibility():
                    sortdebug(game, "hiding from enemy ice")
                    elf.cast_invisibility()
                    casting_elves[elf]=True
                    Elves_invisibility_turns[elf] = game.invisibility_expiration_turns
                    return True
    # check if need the mana for deafence
    enemy_in_dangerous_place = False
    for enemy in game.get_enemy_living_elves():
        if distance_point_from_line(game.get_my_castle().location, game.get_enemy_castle().location, enemy.location) > 15*enemy.max_speed and enemy in mapElves.values():
            for elf in mapElves.keys():
                if mapElves[elf] == enemy and elf.distance(enemy) > game.portal_building_duration*elf.max_speed:
                    enemy_in_dangerous_place = True
                    
    # use invisibility for hide from enemies for destroy enemy fountain
    for elf in game.get_my_living_elves():
        if not enemy_in_dangerous_place and spell_casted(game,elf) == None and elf.current_health>1 and mapElves[elf] in game.get_enemy_mana_fountains() and mapElves[elf].distance(elf)<elf.max_speed*10 + elf.attack_range+game.mana_fountain_size and casting_elves[elf]==False and not (elf.distance(mapElves[elf]) <=  mapElves[elf].size + elf.max_speed):
            count_enemies=0
            for ice in game.get_enemy_ice_trolls():
                if sorted_enemy_ice[ice]==elf and ice.distance(elf)<ice.attack_range+ice.max_speed*1.5 and ice.current_health>2:
                    count_enemies+=2
            for enemy_elf in game.get_enemy_living_elves():
                if enemy_elf.distance(elf)<elf.attack_range+elf.max_speed*1.5 and not (enemy_elf in attack.values() and attack[elf] != enemy_elf) and enemy_elf in EnemyElfLoc.keys() and enemy_elf.distance(elf)+elf.max_speed< EnemyElfLoc[enemy_elf].distance(elf):
                    count_enemies+=1
            if count_enemies>1: # and ((elf.distance(mapElves[elf])-(elf.attack_range+game.mana_fountain_size))/elf.max_speed)/2+count_enemies/2+mapElves[elf].current_health>=elf.current_health :
                if for_check:
                    return 1
                if elf.can_cast_invisibility():
                    sortdebug(game, "hide from enemies for destroy enemy fountain")
                    elf.cast_invisibility()
                    casting_elves[elf]=True
                    Elves_invisibility_turns[elf] = game.invisibility_expiration_turns
                    return True
                    
    # to destroy mana fountain and stay in dangerous place
    obj_to_enemy_castle = sorted(game.get_enemy_living_elves() + game.get_enemy_portals() + game.get_my_living_elves(), key = lambda e: e.distance(game.get_enemy_castle()))
    for elf in game.get_my_living_elves():
        need_invisibility = False
        if not enemy_in_dangerous_place and spell_casted(game,elf) == None and mapElves[elf] in game.get_enemy_mana_fountains() and obj_to_enemy_castle and elf == obj_to_enemy_castle[0]  and attack[elf] == mapElves[elf] and not (elf.distance(mapElves[elf]) <=  mapElves[elf].size + elf.max_speed):
            enemy_elf_to_elf = sorted(game.get_enemy_living_elves(), key = lambda e: e.distance(elf))
            if enemy_elf_to_elf and enemy_elf_to_elf[0].distance(elf) <= enemy_elf_to_elf[0].attack_range + 1.5*enemy_elf_to_elf[0].max_speed:
                need_invisibility = True
            for k in sorted_enemy_ice.keys():
                if sorted_enemy_ice[k] == elf and k.distance(elf) < k.attack_range + 1.5*k.max_speed:
                    need_invisibility = True
        if need_invisibility:
            if for_check:
                return 1
            if elf.can_cast_invisibility():
                sortdebug(game, "to destroy mana fountain and stay in dangerous place")
                elf.cast_invisibility()
                casting_elves[elf]=True
                Elves_invisibility_turns[elf] = game.invisibility_expiration_turns
                return True 
   
    if for_check:
        return 100
    return False
    
def handle_speed_up_spell(game,mapElves,for_check):
    global casting_elves
    sorted_my_tornado=sort_my_tornado(game)
    elf_attack = []
    #vs week 3 bot            
    enemy_elves_revive = sorted(game.get_all_enemy_elves(), key = lambda e: e.turns_to_revive)
    for elf in game.get_my_living_elves():
        count_enemy = 0
        for enemy_ice in game.get_enemy_ice_trolls():
            if enemy_ice.distance(elf) < enemy_ice.attack_range + enemy_ice.max_speed + 1:
                count_enemy +=1
        if spell_casted(game,elf)=="invisibility" and casting_elves[elf]==False and spell_casted(game,elf)!="speed up" and  spell_casted(game,elf) != "both of them" and dangerous_portal1[elf] == None and dangerous_elf1[elf] == None and ((not enemy_elves_revive) or (enemy_elves_revive[0].turns_to_revive > elf.distance(game.get_enemy_castle())/elf.max_speed + game.portal_building_duration/2)):
            if for_check:
                return 1
            if elf.can_cast_speed_up():
                elf.cast_speed_up()
                casting_elves[elf]=True
                return True

    #if elf can attack portal or enemy elf
    for elf in game.get_my_living_elves():
        portal_to_elf = sorted(game.get_enemy_portals(), key = lambda p: p.distance(elf))
        enemy_elf_to_elf = sorted(game.get_enemy_living_elves(), key = lambda p: p.distance(elf))
        if portal_to_elf and enemy_elf_to_elf and (elf.in_attack_range(portal_to_elf[0]) or elf.in_attack_range(enemy_elf_to_elf[0])):
            elf_attack.append(elf)
            
    # check if need the mana for deafence
    enemy_in_dangerous_place = False
    for enemy in game.get_enemy_living_elves():
        if distance_point_from_line(game.get_my_castle().location, game.get_enemy_castle().location, enemy.location) > 15*enemy.max_speed and enemy in mapElves.values():
            for elf in mapElves.keys():
                if mapElves[elf] == enemy and elf.distance(enemy) > game.portal_building_duration*elf.max_speed:
                    enemy_in_dangerous_place = True
    # need to speed up to destroy enemy mana fountain
    for elf in game.get_my_living_elves():
        enemy_can_attack = sorted(game.get_enemy_living_elves()+game.get_enemy_ice_trolls(), key = lambda e: e.distance(elf))
        enemy_portal_to_my_elf = sorted(game.get_enemy_portals(),key = lambda p: p.distance(elf))
        if game.get_my_portals() and not enemy_in_dangerous_place and mapElves[elf] in game.get_enemy_mana_fountains() and elf.current_health >= mapElves[elf].current_health and (elf.distance(mapElves[elf]) -(elf.attack_range + game.mana_fountain_size))> 1.5*elf.max_speed*game.speed_up_multiplier and casting_elves[elf]==False and (spell_casted(game,elf) != "both of them" and  spell_casted(game,elf) !="speed up") and ((attack[elf]==None) or (enemy_can_attack and not elf.distance(enemy_can_attack[0]) < enemy_can_attack[0].attack_range + enemy_can_attack[0].max_speed+1)) and( (not game.get_enemy_living_elves()) or (len(game.get_enemy_mana_fountains())>len(game.get_my_mana_fountains()) ) or enemy_go_to_my_fountain_naw ) :
            elves_to_fountain = sorted(game.get_my_living_elves(),key = lambda e: e.distance(mapElves[elf]))
            check3=True
            for tornado in game.get_my_tornadoes():
                if sorted_my_tornado[tornado]==mapElves[elf] and if_tornado_will_arrive_to_destination(game,tornado,mapElves[elf]):
                    check3=False
            check_if_portal_next_to_fountain=False
            for portal in game.get_my_portals():
                building_to_portal=sorted(game.get_enemy_portals()+game.get_enemy_mana_fountains(),key=lambda b:b.distance(portal))
                if building_to_portal[0]==mapElves[elf] and (portal.distance(mapElves[elf])-(game.tornado_attack_range+game.mana_fountain_size))/game.tornado_max_speed+mapElves[elf].current_health+5<game.tornado_max_health:
                    check_if_portal_next_to_fountain=True
            if check3 and not (elves_to_fountain and elves_to_fountain[0].in_attack_range(mapElves[elf])) and elf == elves_to_fountain[0] and not check_if_portal_next_to_fountain:
                if for_check:
                    return 1
                if elf.can_cast_speed_up():
                    sortdebug(game,"speed up to destroy enemy fauntain")
                    elf.cast_speed_up()
                    casting_elves[elf]=True
                    return True
                    
    #finish the game
    for elf in game.get_my_living_elves():
        if finish_the_game(game) and casting_elves[elf]==False and elf.distance(game.get_enemy_castle())>game.elf_max_speed*game.speed_up_multiplier+game.castle_size:
            if (spell_casted(game,elf) != "both of them" and  spell_casted(game,elf) !="speed up"):
                if for_check:
                    return 1
                if elf.can_cast_speed_up():
                    sortdebug(game,"speed up to finish the game")
                    elf.cast_speed_up()
                    casting_elves[elf]=True
                    return True
                    
    # need speed up to chase dangerous elf
    for elf in game.get_my_living_elves():
        portal_to_elf = sorted(game.get_enemy_portals(), key = lambda p: p.distance(elf))
        enemy_can_attack = sorted(game.get_enemy_living_elves()+game.get_enemy_ice_trolls(), key = lambda e: e.distance(elf))
        if dangerous_elf1[elf]!=None and dangerous_elf1[elf].distance(elf)>15*game.elf_max_speed and dangerous_elf1[elf].current_health <= elf.current_health and dangerous_elf1[elf].distance(game.get_my_castle())<10*game.elf_max_speed and casting_elves[elf]==False and (spell_casted(game,elf) != "both of them" and  spell_casted(game,elf) !="speed up") and not elf in elf_attack and (not enemy_can_attack or (enemy_can_attack and not elf.distance(enemy_can_attack[0]) < enemy_can_attack[0].attack_range + enemy_can_attack[0].max_speed+1)) and mapElves[elf] == dangerous_elf1[elf]:
            if for_check:
                return 1
            if elf.can_cast_speed_up():
                sortdebug(game, "speed up to chase dangerous elf")
                elf.cast_speed_up()
                casting_elves[elf]=True
                return True

    # enemy elf very close to my castle and I am far away
    for elf in game.get_my_living_elves():
        if dangerous_elf1[elf] is not None and dangerous_elf1[elf].current_health <= elf.current_health and dangerous_elf1[elf].distance(game.get_my_castle())/dangerous_elf1[elf].max_speed <= elf.distance(dangerous_elf1[elf])/elf.max_speed and casting_elves[elf]==False and spell_casted(game,elf) != "both of them" and  spell_casted(game,elf) !="speed up" and not elf in elf_attack and (not enemy_can_attack  or (enemy_can_attack and not elf.distance(enemy_can_attack[0]) < enemy_can_attack[0].attack_range + enemy_can_attack[0].max_speed)) and mapElves[elf] == dangerous_elf1[elf]:
            if not (dangerous_elf1[elf] in EnemyElfLoc.keys() and dangerous_elf1[elf].distance(game.get_enemy_castle()) < EnemyElfLoc[dangerous_elf1[elf]].distance(game.get_enemy_castle()) and dangerous_elf1[elf].distance(elf) < EnemyElfLoc[dangerous_elf1[elf]].distance(elf)):
                distance_for_build = (game.castle_size + game.portal_size + game.elf_max_speed/10)
                if (dangerous_elf1[elf].distance(game.get_my_castle()) - distance_for_build) < (2*elf.distance(game.get_my_castle()) - distance_for_build):
                    count_enemy = 0 
                    for enemy_ice in game.get_enemy_ice_trolls():
                        if enemy_ice.distance(dangerous_elf1[elf]) < enemy_ice.attack_range + 2*enemy_ice.max_speed:
                            count_enemy +=1
                    if count_enemy == 0 and game.can_build_portal_at(dangerous_elf1[elf].location):
                        if for_check:
                                return 1
                        if elf.can_cast_speed_up():
                            sortdebug(game, "speed up because I am far away")
                            elf.cast_speed_up()
                            casting_elves[elf]=True
                            return True

    # enemy elf with speed up - we need speed up as well
    for elf in game.get_my_living_elves():        
        portal_to_elf = sorted(game.get_enemy_portals(), key = lambda p: p.distance(elf))
        if dangerous_elf1[elf]!=None and dangerous_elf1[elf].current_health <= elf.current_health and (spell_casted(game,dangerous_elf1[elf]) == "both of them" or  spell_casted(game,dangerous_elf1[elf]) =="speed up") and casting_elves[elf]==False and  spell_casted(game,elf) != "both of them" and  spell_casted(game,elf) !="speed up" and not elf in elf_attack and (not enemy_can_attack  or (enemy_can_attack and not elf.distance(enemy_can_attack[0]) < enemy_can_attack[0].attack_range + enemy_can_attack[0].max_speed+1)) and mapElves[elf] == dangerous_elf1[elf]:
            if dangerous_elf1[elf].distance(game.get_my_castle()) - dangerous_elf1[elf].max_speed < elf.distance(game.get_my_castle()):    
                if for_check:
                    return 1
                if elf.can_cast_speed_up():
                    sortdebug(game, "dangerous elf with speed up - we need speed up as well")
                    elf.cast_speed_up()
                    casting_elves[elf]=True
                    return True

    # speed up to destroy dangerous portal
    for elf in game.get_my_living_elves():
        portal_to_elf = sorted(game.get_enemy_portals(), key = lambda p: p.distance(elf))
        if enemy_in_turget(game,mapElves[elf],elf) == False and dangerous_portal1[elf]!=None and casting_elves[elf]==False and dangerous_portal1[elf].distance(game.get_my_castle())<10*game.lava_giant_max_speed and dangerous_portal1[elf].distance(elf)>elf.max_speed*game.speed_up_multiplier*game.speed_up_expiration_turns and spell_casted(game,elf) != "both of them" and  spell_casted(game,elf) !="speed up" and not elf in elf_attack and (not enemy_can_attack or (enemy_can_attack and not elf.in_attack_range(enemy_can_attack[0]))) and mapElves[elf] == dangerous_elf1[elf]:
            if for_check:
                return 1
            if elf.can_cast_speed_up():
                sortdebug(game, "speed up to destroy dangerous portal")
                elf.cast_speed_up()
                casting_elves[elf]=True
                return True
                
    # speed up to kill enemy elf that builds
    for elf in game.get_my_living_elves():
        if casting_elves[elf]==False and spell_casted(game,elf) != "both of them" and spell_casted(game,elf) !="speed up":
            closest_enemy_to_my_elf = sorted(game.get_enemy_living_elves(), key = lambda e: e.distance(elf))
            if closest_enemy_to_my_elf :
                danger_enemy = closest_enemy_to_my_elf[0]
                turns_to_reach_and_kill = (elf.distance(danger_enemy)-elf.attack_range)/(game.elf_max_speed*game.speed_up_multiplier) + danger_enemy.current_health + 1
                turns_to_reach_and_kill_without_speed = (elf.distance(danger_enemy)-elf.attack_range)/(game.elf_max_speed) + danger_enemy.current_health + 1
                if danger_enemy.is_building and danger_enemy.turns_to_build >= turns_to_reach_and_kill and danger_enemy.turns_to_build<turns_to_reach_and_kill_without_speed and closest_enemy_to_my_elf[0]==mapElves[elf]:
                    if for_check:
                        return 1
                    if elf.can_cast_speed_up():
                        sortdebug(game, "speed up to kill that builds")
                        elf.cast_speed_up()
                        casting_elves[elf]=True
                        return True
    if for_check:
        return 100
    return False
    
def enemy_in_turget(game,turget,elf):
    if elf.max_speed == 0:
        turn_to_came = 0
    else:
        turn_to_came = elf.distance(turget)/elf.max_speed*game.speed_up_multiplier
    enemy_will_attack = False
    for enemy in game.get_enemy_living_elves() + game.get_enemy_ice_trolls():
        loc = enemy.location.towards(turget,enemy.max_speed*turn_to_came)
        if loc.distance(turget) < enemy.attack_range+enemy.max_speed:
            enemy_will_attack = True
    return enemy_will_attack
    
def spell_casted(game,elf):
    if len(elf.current_spells)==0:
        return None
    elif len(elf.current_spells)==1:
        if elf.max_speed>game.elf_max_speed:
            return "speed up"
        else:
            return "invisibility"
    else:
        return "both of them"
    
#***************************Sort************************************

def SortElves(game,priority_fauntain,priority_portal):
    # Global vars
    global mapElvesPerTurns
    global danger_elves1
    global loc_before_disapear
    global dangerous_elf1
    global dangerous_portal1
    global enemy_go_to_my_fountain_naw

    # The keys - elves, the values - the locations.
    mapElves = {}

    # usful vars
    elves_go_build_fountain = 0
    my_tornado_turrgets = sort_my_tornado(game)

    # lists of good locations to go
    good_places_for_fountain = list_fountain
    good_places_for_portal = good_locations_for_portal_for_defend_on_fountain(game)
    # Vars for convenience:
    MyCastle = game.get_my_castle()
    EnemyCastle = game.get_enemy_castle()
    my_portal_to_enemy_castle = sorted(game.get_my_portals(), key=lambda p: p.distance(EnemyCastle))
    enemy_portal_to_my_castle = sorted(game.get_enemy_portals(),key=lambda portal: portal.distance(game.get_my_castle()))
    optional_dangerus_portals = sorted(game.get_enemy_portals(), key=lambda p: p.distance(game.get_my_castle()))
    optional_dangerus_portals = filter(lambda p: (p.distance(game.get_my_castle()) - (game.lava_giant_attack_range + game.castle_size)) > game.lava_giant_max_health / 3 and p.is_summoning,optional_dangerus_portals)

    # Removes targets of dead elves
    for elf2 in game.get_all_my_elves():
        if not elf2.is_alive():
            mapElvesPerTurns[elf2] = Location(0, 0)

    sortdebug(game, "                         *****SORT*****")

    # Replaces chasing dangerous elves if better
    elves_witout_dangerous = []
    for elf in game.get_my_living_elves():
        if dangerous_elf1[elf] == None:
            elves_witout_dangerous.append(elf)
    for k in dangerous_elf1.keys():
        if dangerous_elf1[k] != None:
            for other_elf in elves_witout_dangerous:
                enemy_fountain_to_me = sorted(game.get_enemy_mana_fountains(), key = lambda e: e.distance(other_elf))
                if other_elf.current_health > k.current_health and other_elf.current_health >= dangerous_elf1[k].current_health and ((other_elf.distance(dangerous_elf1[k]) < k.distance(dangerous_elf1[k])) or (enemy_fountain_to_me and enemy_fountain_to_me[0].distance(k) < other_elf.distance(dangerous_elf1[k]))): 
                    dangerous_elf1[other_elf] = dangerous_elf1[k]
                    dangerous_elf1[k] = None
        if dangerous_elf1[k] != None:
            for other_elf in elves_witout_dangerous:
                if other_elf.distance(game.get_my_castle()) < k.distance(game.get_my_castle()) and other_elf.distance(dangerous_elf1[k]) < k.distance(dangerous_elf1[k]) + 4 * k.max_speed and k.distance(dangerous_elf1[k]) > k.attack_range + 8 * elf.max_speed and (other_elf.current_health > other_elf.max_health / 2 or other_elf.current_health > dangerous_elf1[k].current_health):
                    dangerous_elf1[other_elf] = dangerous_elf1[k]
                    dangerous_elf1[k] = None

    # give the best target to each elf
    for elf in game.get_my_living_elves():
        
        #***************************Introduction************************************
        
        enemy_elf_to_this_elf = sorted(game.get_enemy_living_elves(), key = lambda e: e.distance(elf))
        my_elf_to_this_elf = sorted(game.get_my_living_elves(), key = lambda e: e.distance(elf))
        elf_in_use = False
        dangerous_fountain1=dangerous_fountain(game,elf)
        good_places_for_fountain.sort(key=lambda l:l.distance(elf))
        initial_loc_to_me=sorted(game.get_all_enemy_elves(),key=lambda e:e.initial_location.distance(elf))
        if initial_loc_to_me:
            good_places_for_portal.sort(key=lambda l:l.distance(initial_loc_to_me[0].initial_location))
        sortdebug(game," ")
        sortdebug(game,"                      ***** Elf Id = "+str(elf.id)+" *****")
        sortdebug(game," ")
        sortdebug( game,"Dangerous portal="+str(dangerous_portal1[elf]))
        sortdebug( game,"Dangerous elf="+str(dangerous_elf1[elf]))
        sortdebug( game,"Dangerous fountain="+str(dangerous_fountain1))
        
        #***************************Code************************************ 

        #finish the game            
        if not elf_in_use and finish_the_game(game)==True:
            sortdebug(game, "Going to enemy castle for finishing the game")
            mapElves[elf] = game.get_enemy_castle()
            mapElvesPerTurns[elf] = game.get_enemy_castle()
            elf_in_use = True
            
        #vs week 3 bot 
        if not elf_in_use and len(game.get_enemy_ice_trolls())>40 and len(game.get_all_my_elves())==1:
            sortdebug(game,"Go to enemy castel-1")
            mapElves[elf] = game.get_enemy_castle()
            mapElvesPerTurns[elf] = mapElves[elf]
            elf_in_use = True
        
        #if turn before my target was enemy fountain so this turn it will be too
        check_if_someone_go=False
        enemy_fountain_to_me = sorted(game.get_enemy_mana_fountains(), key = lambda f: f.distance(elf))
        for elf1 in mapElvesPerTurns.keys():
            if elf1!=elf and elf1 in mapElvesPerTurns.keys() and mapElvesPerTurns[elf1] in game.get_enemy_mana_fountains() and (spell_casted(game,elf1)=="speed up" or spell_casted(game,elf1)=="both of them"):
                check_if_someone_go=True
        if game.get_my_portals() and not check_if_someone_go and enemy_fountain_to_me and elf in mapElvesPerTurns.keys() and mapElvesPerTurns[elf] in game.get_enemy_mana_fountains() and not need_elf(game,mapElvesPerTurns,enemy_fountain_to_me[0],elf):
            sortdebug(game,"stay vs fountains")
            mapElves[elf] = enemy_fountain_to_me[0]
            elf_in_use = True
            
        # build mana batter the destroy
        check=True
        enemy_elf_to_this_elf = sorted(game.get_enemy_living_elves(), key = lambda e: e.distance(elf))
        if not elf_in_use and max_fountains > len(game.get_my_mana_fountains()) and good_places_for_fountain and elf.distance(good_places_for_fountain[0]) < 10*elf.max_speed and len(game.get_enemy_mana_fountains()) >= len(game.get_my_mana_fountains()) and game.get_my_mana() + 7*game.get_myself().mana_per_turn >= game.mana_fountain_cost and not need_elf(game,mapElvesPerTurns,good_places_for_fountain[0],elf) and not (enemy_elf_to_this_elf and enemy_elf_to_this_elf[0].distance(elf) < enemy_elf_to_this_elf[0].attack_range + game.mana_fountain_building_duration*enemy_elf_to_this_elf[0].max_speed):
            for elf1 in mapElvesPerTurns.keys():
                if elf1!=elf and mapElvesPerTurns[elf1]!=None and mapElvesPerTurns[elf1] not in game.get_all_enemy_elves() and mapElvesPerTurns[elf1].distance(good_places_for_fountain[0])<game.portal_size+200 and elf1.distance(mapElvesPerTurns[elf1])<elf.distance(good_places_for_fountain[0]):
                    check=False
            if check and game.get_my_mana() >= 1.5*game.mana_fountain_cost*elves_go_build_fountain:
                sortdebug(game,"stay to build mana ")
                mapElves[elf] = good_places_for_fountain[0]
                mapElvesPerTurns[elf] = mapElves[elf]
                elves_go_build_fountain+=1
                elf_in_use = True
            
        #danger elves locations before disapearing
        if elf in danger_elves1.keys()and danger_elves1[elf]!= None and  danger_elves1[elf].location != Location(-50,-50) and danger_elves1[elf].is_alive():
            loc_before_disapear[danger_elves1[elf]]=danger_elves1[elf].location
            
        #go to my castle for defend from invisibility elf
        if not elf_in_use and elf in danger_elves1.keys() and danger_elves1[elf]!=None and (spell_casted(game,danger_elves1[elf])=="invisibility" or spell_casted(game,danger_elves1[elf])=="both of them"):
            if not check_if_there_is_better_elf_for_chase(game,elf) and danger_elves1[elf] in loc_before_disapear.keys() and loc_before_disapear[danger_elves1[elf]].distance(game.get_my_castle())<elf.distance(game.get_my_castle())+1.5*game.invisibility_expiration_turns*danger_elves1[elf].max_speed and not need_elf(game,mapElvesPerTurns,loc_before_disapear[danger_elves1[elf]],elf):
                sortdebug(game, "Going to my castle for defence")
                mapElves[elf] = game.get_my_castle().location.towards(loc_before_disapear[danger_elves1[elf]],game.castle_size + game.portal_size + game.elf_max_speed/10)
                mapElvesPerTurns[elf] = game.get_my_castle()
                elf_in_use = True
        
        #remove enemy elves that are invisibility-location(-50,-50)       
        if dangerous_elf1[elf] != None and (spell_casted(game,dangerous_elf1[elf]) == "invisibility" or spell_casted(game,dangerous_elf1[elf]) == "both of them"):
            dangerous_elf1[elf] = None
            
        """fountain_to_elf=sorted (game.get_enemy_mana_fountains(),key=lambda f:f.distance(elf))
        if if_destroy_fountain and fountain_to_elf :
            sortdebug(game,"go to enemy fountain")
            mapElves[elf] = fountain_to_elf[0]
            mapElvesPerTurns[elf] = mapElves[elf]
            elf_in_use = True"""
        
        # to desroy his castle before he will came 
        if not elf_in_use and elf.in_attack_range(game.get_enemy_castle()) and len(game.get_enemy_creatures()) == 0 and len(game.get_enemy_portals()) == 0:
            enemy_elves_revive = sorted(game.get_all_enemy_elves(), key = lambda e: e.turns_to_revive)
            if enemy_elves_revive and enemy_elves_revive[0].turns_to_revive + game.portal_building_duration >= game.get_enemy_castle().current_health/elf.attack_multiplier:
                sortdebug(game,"Go to enemy castel befor enemy came ")
                mapElves[elf] = game.get_enemy_castle()
                mapElvesPerTurns[elf] = mapElves[elf]
                elf_in_use = True
                
        #go to destroy dangerous fountain vs week2 bots       
        if not elf_in_use and len(game.get_enemy_mana_fountains()) >= len(game.get_my_mana_fountains()) and len(game.get_all_enemy_elves()) > len(game.get_all_my_elves()):
            dangerous_fountain12 = sorted(game.get_enemy_mana_fountains(),key = lambda f: f.distance(elf))
            if not elf_in_use and dangerous_fountain12 and (dangerous_portal1[elf] == None or elf.distance(dangerous_fountain12[0]) < dangerous_portal1[elf].distance(elf)):
                sortdebug(game,"Going to dangerous fountain - vs bot week 2")
                mapElves[elf] = dangerous_fountain12[0]
                mapElvesPerTurns[elf] = mapElves[elf] 
                elf_in_use = True 
        
        #go to destroy the other mana fountain that close to elf
        if not elf_in_use and game.get_enemy_mana_fountains():
            mana_to_me = sorted(game.get_enemy_mana_fountains(), key = lambda f:f.distance(elf))
            if mana_to_me and mana_to_me[0].distance(elf) < (elf.attack_range + game.mana_fountain_size + diagonal_line/7) and not need_elf(game,mapElvesPerTurns,mana_to_me[0],elf):
                sortdebug(game,"go to destroy the other mana fountain that close to elf")
                mapElves[elf] = mana_to_me[0]
                mapElvesPerTurns[elf] = mapElves[elf]
                elf_in_use = True 
                
        # there is a dangerous_portal with very low health
        if not elf_in_use and dangerous_elf1[elf]!=None and dangerous_portal1[elf]!=None and not need_elf(game,mapElvesPerTurns,dangerous_portal1[elf],elf) and dangerous_portal1[elf].current_health<=3 and elf.distance(dangerous_portal1[elf])/elf.max_speed+dangerous_portal1[elf].current_health<=elf.distance(dangerous_elf1[elf])/elf.max_speed+dangerous_elf1[elf].current_health:
            other_elf_attack = False
            for elf1 in game.get_my_living_elves():
                if elf1.in_attack_range(dangerous_portal1[elf]) and elf1 != elf and elf.distance(dangerous_portal1[elf]) > 6*elf.max_speed:
                    other_elf_attack = True
            for tornado in my_tornado_turrgets.keys():
                if my_tornado_turrgets[tornado] == dangerous_portal1[elf] and tornado.current_health>(tornado.distance(dangerous_portal1[elf])-(dangerous_portal1[elf].size+tornado.attack_range))/tornado.max_speed +dangerous_portal1[elf].current_health/game.tornado_attack_multiplier+2:
                    other_elf_attack = True
            if not other_elf_attack:
                sortdebug(game,"Going to dangerous portal - 1")
                mapElves[elf] = dangerous_portal1[elf]
                mapElvesPerTurns[elf] = mapElves[elf]
                elf_in_use = True
                
        #there is dangerous_portal and dangerous_elf:
        if not elf_in_use and dangerous_elf1[elf]!= None  and dangerous_portal1[elf]!=None:
            sum_of_danger_elf = (dangerous_elf1[elf].distance(MyCastle)- (game.castle_size + game.portal_size + 1)) + elf.distance(dangerous_elf1[elf])
            sum_of_danger_portal = (dangerous_portal1[elf].distance(MyCastle) - elf.attack_range) + elf.distance(dangerous_portal1[elf])
            if sum_of_danger_elf < sum_of_danger_portal and not need_elf(game,mapElvesPerTurns,dangerous_elf1[elf],elf) and check_dangerous_elf(game,elf,dangerous_elf1[elf]):
                sortdebug(game, "Going to dangerous elf - 1")
                mapElves[elf] = dangerous_elf1[elf]
                danger_elves1[elf]=dangerous_elf1[elf]
                mapElvesPerTurns[elf] = mapElves[elf] 
                elf_in_use = True
                
        # there is only dangerous_portal
        if not elf_in_use and dangerous_portal1[elf]!=None and not need_elf(game,mapElvesPerTurns,dangerous_portal1[elf],elf):
            other_elf_attack = False
            other_tornado_attack = False
            for elf1 in game.get_my_living_elves():
                if elf1.in_attack_range(dangerous_portal1[elf]) and elf1 != elf and elf.distance(dangerous_portal1[elf]) > 6*elf.max_speed:
                    other_elf_attack = True
            for portal in game.get_my_portals():
                if portal.currently_summoning == "Tornado" and tornado_turget_after_summing(game,portal) == dangerous_portal1[elf] and portal.distance(dangerous_portal1[elf]) < game.tornado_max_speed*15 + game.tornado_attack_range + game.portal_size:
                    other_tornado_attack = True
            if not other_elf_attack and not other_tornado_attack:
                sortdebug(game,"Going to dangerous portal (only portal)")
                mapElves[elf] = dangerous_portal1[elf]
                mapElvesPerTurns[elf] = mapElves[elf]
                elf_in_use = True
                
        if not elf_in_use and when_I_go_to_volcano(game,elf)==1:
            ev = game.get_active_volcanoes()
            ev.sort(key = lambda e:e.distance(elf))
            if ev:
                sortdebug(game,"go to attack volcano")
                mapElves[elf] = ev[0]
                mapElvesPerTurns[elf] = mapElves[elf]
                elf_in_use = True
            
        # there is only dangerous_elf 
        if not elf_in_use and dangerous_elf1[elf]!= None:
            enemy_portal_to_my_castel = sorted(game.get_enemy_portals(), key = lambda p: p.distance(MyCastle))
            if enemy_portal_to_my_castel and enemy_portal_to_my_castel[0].distance(MyCastle) < dangerous_elf1[elf].distance(MyCastle)and not need_elf(game,mapElvesPerTurns,enemy_portal_to_my_castel[0],elf) and enemy_portal_to_my_castel[0].distance(game.get_my_castle()) < 1.5*enemy_portal_to_my_castel[0].distance(game.get_enemy_castle()):
                sortdebug(game, "Going to portal near castle")
                mapElves[elf] = enemy_portal_to_my_castel[0]
                mapElvesPerTurns[elf] = mapElves[elf]
                elf_in_use = True
            elif not need_elf(game,mapElvesPerTurns,dangerous_elf1[elf],elf) and check_dangerous_elf(game,elf,dangerous_elf1[elf]):
                sortdebug(game, "Going to dangerous elf - 2")
                mapElves[elf] = dangerous_elf1[elf]
                danger_elves1[elf]=dangerous_elf1[elf]
                mapElvesPerTurns[elf] = mapElves[elf]
                elf_in_use = True
                
        if not elf_in_use and max_fountains > 0 and not game.get_my_mana_fountains() and game.get_enemy().mana_per_turn >=game.get_myself().mana_per_turn and if_destroy_fountain and not check_if_there_is_better_elf_for_chase(game,elf):
            enemy_fountain_to_me = sorted(game.get_enemy_mana_fountains(), key = lambda f: f.distance(elf))
            if enemy_fountain_to_me and not need_elf(game,mapElvesPerTurns,enemy_fountain_to_me[0],elf) and better_elf_for_destroy_fountain(game,elf,enemy_fountain_to_me[0])==elf and not( elf in mapElvesPerTurns.keys() and mapElvesPerTurns[elf] in good_places_for_fountain):
                sortdebug(game,"destroy mana fountain")
                mapElves[elf] = enemy_fountain_to_me[0]
                mapElvesPerTurns[elf] = mapElves[elf]
                elf_in_use = True
                
        # help to other elf need help vs dangerous_elf 
        enemy_elves_nearst_to_my_castle = sorted(game.get_enemy_living_elves(), key = lambda e: e.distance(game.get_my_castle()))
        if not elf_in_use and enemy_elves_nearst_to_my_castle and need_elf(game,mapElvesPerTurns,enemy_elves_nearst_to_my_castle[0],elf):
            other_elf_need_help = False
            for k in mapElvesPerTurns.keys():
                if mapElvesPerTurns[k] == enemy_elves_nearst_to_my_castle[0] and k != elf:
                    if k.current_health+game.elf_max_health/4 < enemy_elves_nearst_to_my_castle[0].current_health and ((dangerous_elf1[elf]  != None and 2*mapElvesPerTurns[k].distance(elf) < elf.distance(dangerous_elf1[elf])) or dangerous_elf1[elf] == None):
                        other_elf_need_help = True
            if other_elf_need_help:
                sortdebug(game, "Going to dangerous elf to help other elf")
                mapElves[elf] = enemy_elves_nearst_to_my_castle[0]
                mapElvesPerTurns[elf] = elf.location
                elf_in_use = True
                
        #Go to build fountain in good place
        check=True
        if not if_destroy_fountain and not elf_in_use and len(game.get_enemy_mana_fountains()) > len(game.get_my_mana_fountains()) and not game.get_enemy_living_elves(): 
            if game.get_my_mana() >= 1.5*game.mana_fountain_cost*elves_go_build_fountain and (priority_fauntain == 1) and good_places_for_fountain and not need_elf(game,mapElvesPerTurns,good_places_for_fountain[0],elf):
                elf_to_loc=sorted(game.get_my_living_elves(),key=lambda e:e.distance(good_places_for_fountain[0]))
                for elf1 in mapElvesPerTurns.keys():
                    if elf1!=elf and mapElvesPerTurns[elf1]!=None and mapElvesPerTurns[elf1] not in game.get_all_enemy_elves() and mapElvesPerTurns[elf1].distance(good_places_for_fountain[0])<300 and elf1.distance(mapElvesPerTurns[elf1])<elf.distance(good_places_for_fountain[0]):
                        check=False
                if elf_to_loc and elf==elf_to_loc[0] and check and game.get_enemy().mana_per_turn > 2*game.get_myself().mana_per_turn:
                    if not (len(game.get_enemy_living_elves()) > len(game.get_my_living_elves()) and len(game.get_my_mana_fountains()) < max_fountains):    
                        sortdebug(game,"Go to place for building fountain behind portal - priority_fauntain 1")
                        mapElves[elf] = good_places_for_fountain[0]
                        mapElvesPerTurns[elf] = mapElves[elf]
                        elves_go_build_fountain +=1
                        elf_in_use = True
        
        check4=True
        if not elf_in_use and good_places_for_portal:
            fountain_to_elf=sorted(game.get_my_mana_fountains(),key=lambda f:f.distance(elf))
            if fountain_to_elf:
                portal_to_fountain=sorted(game.get_my_portals(),key=lambda p:p.distance(fountain_to_elf[0]))
                if ((not portal_to_fountain) or ((fountain_to_elf[0].distance(portal_to_fountain[0])>game.portal_size*4 and fountain_to_elf[0].distance(portal_to_fountain[0])<fountain_to_elf[0].distance(game.get_enemy_castle()) and fountain_to_elf[0].distance(game.get_enemy_castle())>game.get_enemy_castle().distance(portal_to_fountain[0]) and distance_point_from_line(game.get_enemy_castle().location,fountain_to_elf[0].location,portal_to_fountain[0].location)<game.portal_size+200))):
                    elf_to_fountain=sorted(game.get_my_living_elves(),key=lambda e:e.distance(fountain_to_elf[0]))
                    for elf1 in mapElvesPerTurns.keys():
                        if elf1!=elf and mapElvesPerTurns[elf1]!=None and type(mapElvesPerTurns[elf1])==type(Location(0,0)) and mapElvesPerTurns[elf1].distance(good_places_for_portal[0])<300 and elf1.distance(mapElvesPerTurns[elf1])<elf.distance(good_places_for_portal[0]):
                            check4=False
                    if elf_to_fountain and check4 and elf_to_fountain[0]==elf and elf.distance(fountain_to_elf[0])<game.mana_fountain_size+game.portal_size+game.elf_max_speed*2:
                        sortdebug(game,"Go to place for building portal in front of fountain ")
                        mapElves[elf] = good_places_for_portal[0]
                        mapElvesPerTurns[elf] = mapElves[elf]
                        elf_in_use = True
                        
        """check_all_elves_far_from_initial_loc=True
        for elf2 in game.get_all_living_elves():
            m_initial_loc_to_elf=sorted(game.get_all_my_elves(),key=lambda e:e.initial_location.distance(elf2))
            e_initial_loc_to_elf=sorted(game.get_all_enemy_elves(),key=lambda e:e.initial_location.distance(elf2))
            if m_initial_loc_to_elf and e_initial_loc_to_elf and m_initial_loc_to_elf[0].initial_location.distance(elf2)<e_initial_loc_to_elf[0].initial_location.distance(elf2) and not (elf2 in game.get_my_living_elves() and elf2.distance(m_initial_loc_to_elf[0].initial_location)<game.elf_max_speed*10):
                check_all_elves_far_from_initial_loc=False"""
                
        if not elf_in_use and when_I_go_to_volcano(game,elf) :
            ev = game.get_active_volcanoes()
            ev.sort(key = lambda e:e.distance(elf))
            if ev:
                sortdebug(game,"go to attack volcano")
                mapElves[elf] = ev[0]
                mapElvesPerTurns[elf] = mapElves[elf]
                elf_in_use = True
                        
        #there is more enemy elf than me and i have friendly elf that close to me- we go to friendly elf for help      
        if not elf_in_use and enemy_elf_to_this_elf and len(my_elf_to_this_elf) > 1  and elf in mapElvesPerTurns.keys() and mapElvesPerTurns[elf] not in game.get_enemy_living_elves() and my_elf_to_this_elf[1] in mapElvesPerTurns.keys() and mapElvesPerTurns[my_elf_to_this_elf[1]]!=my_elf_to_this_elf[1]:
            enemy_elf_to_enemy = sorted(game.get_enemy_living_elves(), key = lambda e: e.distance(enemy_elf_to_this_elf[0]))
            enemy_can_kill_me = False
            for enemy in enemy_elf_to_this_elf:
                if enemy.distance(elf) < 8*elf.max_speed and enemy.current_health >= elf.current_health and not((spell_casted(game,elf) == "speed up" or spell_casted(game,elf) == "both of them") and elf in mapElvesPerTurns and mapElvesPerTurns[elf] in game.get_enemy_mana_fountains()):
                    enemy_can_kill_me = True
            if enemy_can_kill_me and elf.distance(my_elf_to_this_elf[1]) > elf.max_speed+1 and my_elf_to_this_elf[1].current_health > enemy_elf_to_this_elf[0].current_health - 1:
                if len(enemy_elf_to_enemy) > 1 and ( enemy_elf_to_enemy[0].distance(enemy_elf_to_enemy[1]) <  elf.attack_range + 8*elf.max_speed or len(game.get_enemy_living_elves())>len(game.get_my_living_elves()) ):
                    sortdebug(game, "Going to my elf for help")
                    mapElves[elf] = my_elf_to_this_elf[1]
                    mapElvesPerTurns[elf] = mapElves[elf]
                    elf_in_use = True
            my_portal_to_me = sorted(game.get_my_portals(), key = lambda p: p.distance(elf))
            enemy_portal_to_me = sorted(game.get_enemy_portals(), key = lambda p: p.distance(elf))
            if enemy_portal_to_me and my_portal_to_me and enemy_portal_to_me[0].distance(elf) < my_portal_to_me[0].distance(elf) and my_portal_to_me[0].distance( enemy_portal_to_me[0])<game.portal_size*2+9*elf.max_speed:
                enemy_elves = 0
                for enemy in game.get_enemy_living_elves():
                    if enemy.distance(enemy_portal_to_me[0]) < 6*enemy.max_speed + game.portal_size and enemy.distance(enemy_portal_to_me[0])<enemy.distance(my_portal_to_me[0]):
                        enemy_elves +=1
                my_elf_to_this_elf = filter(lambda e: e.distance(elf) < 7*e.max_speed, my_elf_to_this_elf)
                if enemy_elves > 1 and len(my_elf_to_this_elf) > 1 and elf.distance(my_elf_to_this_elf[1]) > elf.max_speed+1 and abs(enemy_portal_to_me[0].distance(game.get_my_castle())-my_portal_to_me[0].distance(game.get_my_castle()))>diagonal_line/7:
                    sortdebug(game, "Going to my elf for help - Second ")
                    mapElves[elf] = my_elf_to_this_elf[1]
                    mapElvesPerTurns[elf] = mapElves[elf]
                    elf_in_use = True
        
            
        #destroy enemy fountain
        enemy_fountain_to_me=sorted(game.get_enemy_mana_fountains(),key=lambda f:f.distance(elf))
        enemy_turn_to_revive=sorted(game.get_all_enemy_elves(),key=lambda e:e.turns_to_revive)
        if not elf_in_use and enemy_fountain_to_me and enemy_turn_to_revive and (not game.get_enemy_living_elves() or elf.in_attack_range(enemy_fountain_to_me[0])) and enemy_turn_to_revive[0].turns_to_revive+enemy_turn_to_revive[0].initial_location.distance(enemy_fountain_to_me[0])/game.elf_max_speed>(elf.distance(enemy_fountain_to_me[0])-(game.mana_fountain_size+elf.attack_range))/(elf.max_speed*game.speed_up_multiplier) and len(game.get_my_mana_fountains()) < max_fountains and better_elf_for_destroy_fountain(game,elf,enemy_fountain_to_me[0])==elf:
            sortdebug(game, "Going to fountain - no enemy elves-1")
            mapElves[elf] = enemy_fountain_to_me[0]
            mapElvesPerTurns[elf] = mapElves[elf]
            elf_in_use = True
        if not elf_in_use and enemy_fountain_to_me and not need_elf(game,mapElvesPerTurns,enemy_fountain_to_me[0],elf)  and elf in mapElvesPerTurns.keys() and mapElvesPerTurns[elf]==enemy_fountain_to_me[0] and (elf.distance(enemy_fountain_to_me[0])-(elf.attack_range+enemy_fountain_to_me[0].size))/elf.max_speed<6 and better_elf_for_destroy_fountain(game,elf,enemy_fountain_to_me[0])==elf:
            sortdebug(game, "Going to fountain-2")
            mapElves[elf] = enemy_fountain_to_me[0]
            mapElvesPerTurns[elf] = mapElves[elf]
            elf_in_use = True      
                
        # build in enemy fountain places :
        if not elf_in_use:
            best_enemy_loc = None
            portal_in_loc = False
            for portal in game.get_my_portals():
                if portal.distance(game.get_enemy_castle()) < game.portal_size + game.castle_size + 3*game.elf_max_speed and portal.current_health>1:
                    portal_in_loc = True
            for loc in enemy_fountain_loc:
                if game.can_build_portal_at(loc) and elf.distance(loc) < 6*elf.max_speed:
                    if best_enemy_loc == None:
                        best_enemy_loc = loc
                    elif loc.distance(elf) < best_enemy_loc.distance(elf):
                        best_enemy_loc = loc
            if best_enemy_loc != None and portal_in_loc:
                if game.get_my_mana() + game.get_myself().mana_per_turn <= game.portal_cost:
                    sortdebug(game,"go to enemy castle to wait for fountain")
                    mapElves[elf] = game.get_enemy_castle()
                    mapElvesPerTurns[elf] = mapElves[elf]
                    elf_in_use = True
                elif not need_elf(game,mapElvesPerTurns,best_enemy_loc,elf) :
                    sortdebug(game,"go to enemy fountain place for build portal")
                    mapElves[elf] = best_enemy_loc
                    mapElvesPerTurns[elf] = mapElves[elf]
                    elf_in_use = True
                    
        # all spell and dere isnt dangerous elf or portal - go enemy castle:
        if not elf_in_use and spell_casted(game,elf) == "both of them":
            loc_to_build_portal = game.get_enemy_castle().location.towards(elf.location,game.castle_size+game.portal_size+elf.max_speed/10)
            if not (elf.distance(loc_to_build_portal) < game.portal_size+1 and elf.can_build_portal() == False and game.get_my_mana() >= game.portal_cost) and not (len(game.get_all_my_elves())<len(game.get_all_enemy_elves()) and my_portal_to_enemy_castle and my_portal_to_enemy_castle[0].distance(game.get_enemy_castle()) <game.castle_size+game.portal_size+diagonal_line/7) and game.portal_cost < 2000:
                sortdebug(game,"Go to enemy castel for build a portal")
                mapElves[elf] = loc_to_build_portal
            else:
                sortdebug(game,"Go to enemy castel-2")
                mapElves[elf] = game.get_enemy_castle()
            mapElvesPerTurns[elf] = mapElves[elf]
            elf_in_use = True
            
            
        #there is dangerous elf's initial location vs week1 bot 
        if not elf_in_use:
            for enemy in game.get_all_enemy_elves():
                elf_to_loc=sorted(game.get_my_living_elves(),key=lambda e:e.distance(enemy.initial_location))
                if (enemy.initial_location.distance(game.get_my_castle())-game.portal_size-game.castle_size)<enemy.max_speed*18:
                    if not enemy.is_alive() and enemy.turns_to_revive*elf.max_speed<=elf.distance(enemy.initial_location) and elf_to_loc and elf_to_loc[0]==elf and not need_elf(game,mapElvesPerTurns,enemy.initial_location,elf):
                        sortdebug(game, "Going to dangerous elf- initial location")
                        mapElves[elf] = enemy.initial_location
                        mapElvesPerTurns[elf] = mapElves[elf]
                        elf_in_use = True
                
        # all enemy elf more than my vs week 2 bots 
        if len(game.get_all_enemy_elves()) > len(game.get_all_my_elves()):
            if not elf_in_use and dangerous_fountain1!=None and not need_elf(game,mapElvesPerTurns,dangerous_fountain1,elf) :
                sortdebug(game,"Going to dangerous fountain")
                mapElves[elf] = dangerous_fountain1
                mapElvesPerTurns[elf] = mapElves[elf] 
                elf_in_use = True 
                
        """# help our elf to kill enemy elf
        closest_elf_to_enemy = the_closest_elf_to_enemy_elf(game)
        if not elf_in_use and closest_elf_to_enemy!=None and closest_elf_to_enemy!=elf and closest_elf_to_enemy in mapElvesPerTurns.keys() and mapElvesPerTurns[closest_elf_to_enemy]!=closest_elf_to_enemy:
            closest_enemy_to_my_elf=sorted(game.get_enemy_living_elves(),key=lambda enemy:enemy.distance(closest_elf_to_enemy))
            if closest_enemy_to_my_elf and not closest_enemy_to_my_elf[0] in mapElvesPerTurns.values() and elf.distance(closest_elf_to_enemy)/elf.max_speed<closest_elf_to_enemy.current_health:
                sortdebug(game,"Going to help to my elf")
                mapElves[elf] = closest_enemy_to_my_elf[0]
                mapElvesPerTurns[elf] = mapElves[elf] 
                elf_in_use = True"""
        
        # elf isn't useful
        if elf in mapElves.keys() and (mapElves[elf] in game.get_enemy_living_elves() or mapElves[elf] in game.get_enemy_portals()):
            my_elves_to_turget = sorted(game.get_my_living_elves(), key = lambda e: e.distance(mapElves[elf]))
            if elf.current_health == 1 and mapElves[elf].current_health > 3*elf.current_health and my_elves_to_turget[0] != elf:
                sortdebug(game,"distination has been changed")
                elf_in_use = False
        
        # thre isnt enemy elves - elf have max_speed go to enemy castle
        if not elf_in_use and not game.get_enemy_living_elves() and len(game.get_my_mana_fountains()) >= len(game.get_enemy_mana_fountains()):
            if (spell_casted(game,elf) == "both of them" or spell_casted(game,elf) == "speed up"):
                loc_to_build_portal = game.get_enemy_castle().location.towards(game.get_my_castle().location,game.castle_size+game.portal_size+elf.max_speed/10)
                sortdebug(game,"Go to enemy castel for build a portal - no enemy elves")
                mapElves[elf] = loc_to_build_portal
                mapElvesPerTurns[elf] = mapElves[elf]
                elf_in_use = True
                
        # enemy go to my fountain - me to
        if not elf_in_use:
            enemy_want_destroy_fountain = False
            enemy_fountain_to_me = sorted(game.get_enemy_mana_fountains(), key = lambda e: e.distance(elf))
            if enemy_fountain_to_me:
                for enemy in game.get_enemy_living_elves():
                    if enemy in EnemyElfLoc.keys() and (spell_casted(game,enemy) == "speed up" or spell_casted(game,enemy) == "both of them"):
                        for my_fountain in game.get_my_mana_fountains():
                            if distance_point_from_line(EnemyElfLoc[enemy],enemy.location,my_fountain.location) <= my_fountain.size:
                                enemy_want_destroy_fountain = True
                if enemy_want_destroy_fountain and not need_elf(game,mapElvesPerTurns,enemy_fountain_to_me[0],elf) and enemy_fountain_to_me[0] not in mapElvesPerTurns.values():
                    sortdebug(game,"enemy go to my fountain - me too")
                    mapElves[elf] = enemy_fountain_to_me[0]
                    mapElvesPerTurns[elf] = mapElves[elf]
                    elf_in_use = True
                    enemy_go_to_my_fountain_naw = True
                    
        #go to enemy fountain - havent what to do
        if not elf_in_use and len(game.get_enemy_mana_fountains()) >= len(game.get_my_mana_fountains()) and len(game.get_my_mana_fountains()) > 0:
            enemy_fountain_to_me = sorted(game.get_enemy_mana_fountains(), key = lambda f: f.distance(elf))
            mana_in_values = False
            for mana in game.get_enemy_mana_fountains():
                if mana in mapElvesPerTurns.values():
                    mana_in_values = True
            if enemy_fountain_to_me and not mana_in_values and not need_elf(game,mapElvesPerTurns,enemy_fountain_to_me[0],elf) :
                sortdebug(game,"go to enemy fountain - havent what to do")
                mapElves[elf] = enemy_fountain_to_me[0]
                mapElvesPerTurns[elf] = mapElves[elf]
                elf_in_use = True
                
        # fight vs dangerous elf1 that havent what to to
        if not elf_in_use:
            enemy_to_attack = None
            for elf1 in dangerous_elf1.keys():
                if dangerous_elf1[elf1] != None and dangerous_elf1[elf1].distance(game.get_my_castle()) < elf1.distance(game.get_my_castle()) and elf.distance(dangerous_elf1[elf1])/elf.max_speed < game.portal_building_duration + game.ice_troll_summoning_duration and elf1.current_health<=dangerous_elf1[elf1].current_health:
                    if enemy_to_attack == None or elf1.distance(dangerous_elf1[elf1]) < elf1.distance(enemy_to_attack):
                        if not(len(game.get_my_living_elves()) > len(game.get_enemy_living_elves()) and elf1.current_health >= dangerous_elf1[elf1].current_health):
                            enemy_to_attack = dangerous_elf1[elf1]
            if enemy_to_attack != None:
                sortdebug(game,"Go to dangerous elf - have nothing to do")
                mapElves[elf] = enemy_to_attack
                mapElvesPerTurns[elf] = elf.location
                elf_in_use = True
                
        # mini dangerous portal 
        if not elf_in_use and optional_dangerus_portals:
            optional_enemy_to_attack_portals = []
            for portal in game.get_my_portals():
                for enemy_elf in game.get_enemy_living_elves():
                    if enemy_elf.in_attack_range(portal):
                        optional_enemy_to_attack_portals.append(enemy_elf)
            optional_enemy_to_attack_portals.sort(key=lambda e:e.distance(elf))
            if optional_enemy_to_attack_portals and optional_enemy_to_attack_portals[0].distance(elf) < optional_dangerus_portals[0].distance(elf) and optional_enemy_to_attack_portals[0] not in dangerous_elf1.values() and optional_enemy_to_attack_portals[0].distance(elf) < 4*elf.max_speed + elf.attack_range and optional_enemy_to_attack_portals[0].distance(elf) < 4*elf.max_speed + elf.attack_range:
                sortdebug(game,"Destroy enemy elf that attack my portal")
                mapElves[elf] = optional_enemy_to_attack_portals[0]
                mapElvesPerTurns[elf] = elf.location
                elf_in_use = True 
            else:
                other_elf_attack = False
                other_tornado_attack = False
                for elf1 in game.get_my_living_elves():
                    if elf1.in_attack_range(optional_dangerus_portals[0]) and elf1 != elf and elf.distance(optional_dangerus_portals[0]) > 6*elf.max_speed:
                        other_elf_attack = True
                for tornado in game.get_my_tornadoes():
                    if my_tornado_turrgets[tornado] == optional_dangerus_portals[0]:
                        other_tornado_attack = True
                if not other_elf_attack and not other_tornado_attack:
                    mapElves[elf] = optional_dangerus_portals[0]
                    mapElvesPerTurns[elf] = mapElves[elf]
                    elves_go_build_fountain +=1
                    sortdebug(game,"Destroy enemy portals - mini dangerous")
                    elf_in_use = True 
                
        #Go to build fountain in good place
        check=True
        if not elf_in_use and game.get_my_mana() >= 1.5*game.mana_fountain_cost*elves_go_build_fountain and ((len(game.get_enemy_living_elves()) < len(game.get_my_living_elves())) or (2*elf.distance(game.get_my_castle()) < elf.distance(game.get_enemy_castle()))) and ((priority_fauntain == 1) or (priority_fauntain == 2 and priority_portal != 2 and priority_portal != 1) or (priority_fauntain == 3 and priority_portal == 100)) and good_places_for_fountain and ( (len(game.get_enemy_living_elves())==0 and elf.distance(good_places_for_fountain[0])<5*elf.max_speed) or (game.get_enemy_living_elves() and elf.distance(good_places_for_fountain[0])<diagonal_line/7) )  and game.get_myself().mana_per_turn<=game.get_enemy().mana_per_turn and not need_elf(game,mapElvesPerTurns,good_places_for_fountain[0],elf):
            elf_to_loc=sorted(game.get_my_living_elves(),key=lambda e:e.distance(good_places_for_fountain[0]))
            for elf1 in mapElvesPerTurns.keys():
                if elf1!=elf and mapElvesPerTurns[elf1]!=None and mapElvesPerTurns[elf1] not in game.get_all_enemy_elves() and mapElvesPerTurns[elf1].distance(good_places_for_fountain[0])<300 and elf1.distance(mapElvesPerTurns[elf1])<elf.distance(good_places_for_fountain[0]):
                    check=False
            if elf_to_loc and elf==elf_to_loc[0] and check and game.mana_fountain_cost-game.get_my_mana()<5*game.get_myself().mana_per_turn  :
                sortdebug(game,"Go to place for building fountain behind portal")
                mapElves[elf] = good_places_for_fountain[0]
                mapElvesPerTurns[elf] = mapElves[elf]
                elves_go_build_fountain +=1
                elf_in_use = True
                
        #there is dangerous fountain that we can destroy
        if not elf_in_use and dangerous_fountain1!=None and not need_elf(game,mapElvesPerTurns,dangerous_fountain1,elf) :
            if not(game.get_my_castle().current_health < game.castle_max_health/ 2 and game.get_enemy_castle().current_health >= game.get_my_castle().current_health and enemy_portal_to_my_castle and ((enemy_portal_to_my_castle[0].distance(game.get_my_castle()) - (game.lava_giant_attack_range + game.castle_size) )/game.lava_giant_max_speed)*game.lava_giant_suffocation_per_turn > (game.lava_giant_max_health/10)):
                other_elf_go = False
                for k in mapElvesPerTurns.keys():
                    if mapElvesPerTurns[k] in game.get_enemy_mana_fountains() and ((spell_casted(game,k) == "speed up") or  (spell_casted(game,k) =="both of them")):
                        other_elf_go = True
                if not other_elf_go:
                    sortdebug(game,"Going to dangerous fountain - 1")
                    mapElves[elf] = dangerous_fountain1
                    mapElvesPerTurns[elf] = mapElves[elf] 
                    elf_in_use = True 
            
        # to build near enemy castle
        if not elf_in_use:
            my_tornado_turrgets = sort_my_tornado(game)
            loc_to_build_portal = game.get_enemy_castle().location.towards(elf.location,game.castle_size+game.portal_size+elf.max_speed/10)
            if elf.distance(game.get_enemy_castle()) < game.castle_size+game.portal_size+elf.max_speed/10:
                loc_to_build_portal = game.get_enemy_castle().location.towards(game.get_my_castle().location,game.castle_size+game.portal_size+elf.max_speed/10)
            my_portal_to_enemy_castle=sorted(game.get_my_portals(),key=lambda portal:portal.distance(game.get_enemy_castle()))    
            enemy_portal_to_my_elf=sorted(game.get_enemy_portals(),key=lambda portal:portal.distance(elf))
            enemy_elf_to_elf = sorted(game.get_enemy_living_elves(), key = lambda e: e.distance(elf))
            enemy_fountain_to_elf = sorted(game.get_enemy_mana_fountains(), key = lambda m: m.distance(elf))
            if elf not in mapElves.keys() and not(game.get_my_castle().current_health < game.castle_max_health/ 2 and game.get_enemy_castle().current_health >= game.get_my_castle().current_health and enemy_portal_to_my_castle and ((enemy_portal_to_my_castle[0].distance(game.get_my_castle()) - (game.lava_giant_attack_range + game.castle_size) )/game.lava_giant_max_speed)*game.lava_giant_suffocation_per_turn > (game.lava_giant_max_health/3)):
                if enemy_fountain_to_elf and ((len(game.get_my_living_elves()) > len(game.get_enemy_living_elves())) or (elf.distance(enemy_fountain_to_elf[0]) < elf.attack_range + 5*elf.max_speed + game.mana_fountain_size)):
                    my_health = 0
                    enemy_health = 0
                    for enemy_elf in game.get_enemy_living_elves():
                        enemy_health += enemy_elf.current_health
                    for elf1 in game.get_my_living_elves():
                        my_health += elf1.current_health
                    other_elf_go = False
                    for k in mapElvesPerTurns.keys():
                        if (spell_casted(game,k) == "speed up" or  spell_casted(game,k) == "both of them") and mapElvesPerTurns[k] == enemy_fountain_to_elf[0]:
                            other_elf_go = True
                    if my_health >= enemy_health and elf.distance(game.get_enemy_castle()) < elf.distance(game.get_my_castle()) and better_elf_for_destroy_fountain(game,elf,enemy_fountain_to_me[0])==elf and not other_elf_go:
                        enemy_portal_to_my_castle=sorted(game.get_enemy_portals(),key=lambda portal:portal.distance(game.get_my_castle()))    
                        if my_portal_to_enemy_castle and not enemy_portal_to_my_castle and not need_elf(game,mapElvesPerTurns,enemy_fountain_to_elf[0],elf):
                            sortdebug(game,"Destroy enemy fauntain - 1")
                            mapElves[elf] = enemy_fountain_to_elf[0]
                        if my_portal_to_enemy_castle and enemy_portal_to_my_castle and my_portal_to_enemy_castle[0].distance(game.get_enemy_castle()) < enemy_portal_to_my_castle[0].distance(game.get_my_castle()) and not need_elf(game,mapElvesPerTurns,enemy_fountain_to_elf[0],elf):
                            sortdebug(game,"Destroy enemy fauntain - 2")
                            mapElves[elf] = enemy_fountain_to_elf[0]
            if elf not in mapElves.keys() :
                optional_enemy_to_attack_portals = []
                for enemy_elf in game.get_enemy_living_elves():
                    portal_to_enemy_elf = sorted(game.get_my_portals(), key = lambda p: p.distance(enemy_elf))
                    if portal_to_enemy_elf and enemy_elf.in_attack_range(portal_to_enemy_elf[0]):
                        optional_enemy_to_attack_portals.append(enemy_elf)
                optional_enemy_to_attack_portals.sort(key=lambda e:e.distance(elf))
                for enemy_portal in enemy_portal_to_my_elf: 
                    count1=0
                    for enemy_elf in game.get_enemy_living_elves():
                        if enemy_elf.distance(enemy_portal)<game.portal_size+(game.elf_attack_range)*2 :
                            count1+=1
                    if  count1<2 and not need_elf(game,mapElvesPerTurns,enemy_portal,elf) and elf not in mapElves.keys() and enemy_portal.current_health<game.elf_attack_multiplier*30 and not (len(game.get_all_my_elves())<len(game.get_all_enemy_elves()) and enemy_portal.distance(elf)>20*elf.max_speed):
                        if optional_enemy_to_attack_portals and optional_enemy_to_attack_portals[0].distance(elf) < enemy_portal.distance(elf):
                            sortdebug(game,"Destroy enemy elf that attack my portal")
                            mapElves[elf] = optional_enemy_to_attack_portals[0]
                        else:
                            if (spell_casted(game,elf) == "speed up" or spell_casted(game,elf) == "both of them"):
                                enemy_with_speed = False
                                for enemy in game.get_enemy_living_elves():
                                    if (spell_casted(game,enemy) == "speed up" or spell_casted(game,enemy) == "both of them"):
                                        enemy_with_speed = True
                                enemy_mana_to_elf = sorted(game.get_enemy_mana_fountains(),key = lambda e: e.distance(elf))
                                if enemy_mana_to_elf and enemy_with_speed and enemy_portal.distance(game.get_my_castle()) > 3*enemy_portal.distance(game.get_enemy_castle()):
                                    sortdebug(game,"Destroy enemy mana - mistake speed")
                                    mapElves[elf] = enemy_mana_to_elf[0]
                            '''# save my mana fountain
                            if elf not in mapElves.keys():
                                optional_enemy = None
                                for enemy in game.get_enemy_living_elves():
                                    if enemy.distance(elf) < enemy.attack_range + 4*elf.max_speed and enemy in EnemyElfLoc.keys() and max_fountains > len(game.get_my_mana_fountains()):
                                        my_fountain_to_enemy = sorted(game.get_my_mana_fountains(), key = lambda f: f.distance(enemy))
                                        if my_fountain_to_enemy and my_fountain_to_enemy[0].distance(enemy) < EnemyElfLoc[enemy].distance(my_fountain_to_enemy[0]) and enemy.current_health < elf.current_health:
                                            if optional_enemy is None or enemy.current_health < optional_enemy.current_health:
                                                optional_enemy = enemy
                                if optional_enemy is not None:
                                    sortdebug(game,"go to enemy elf save my mana ")
                                    mapElves[elf] = optional_enemy'''
                            if elf not in mapElves.keys():
                                loc_to_build_fountain = game.get_my_castle().location.towards(elf.location,game.castle_size + game.mana_fountain_size + elf.max_speed/10)
                                if game.can_build_mana_fountain_at(loc_to_build_fountain) and priority_fauntain == 1 and elf.distance(loc_to_build_fountain) < 4*elf.max_speed and game.get_my_mana() + (elf.distance(loc_to_build_fountain)/elf.max_speed)*game.get_myself().mana_per_turn >= game.mana_fountain_cost:
                                    sortdebug(game,"Go to build fountain")
                                    mapElves[elf] = loc_to_build_fountain
                                elif not enemy_portal in my_tornado_turrgets.values():    
                                    other_tornado_attack = False
                                    for portal in game.get_my_portals():
                                        if portal.currently_summoning == "Tornado" and tornado_turget_after_summing(game,portal) == dangerous_portal1[elf] and portal.distance(dangerous_portal1[elf]) < game.tornado_max_speed*15 + game.tornado_attack_range + game.portal_size:
                                            other_tornado_attack = True
                                    if not other_tornado_attack:
                                        sortdebug(game,"Destroy enemy portals")
                                        mapElves[elf] = enemy_portal
                    
            if elf not in mapElves.keys():
                if elf not in mapElves.keys() and not (elf.distance(loc_to_build_portal) < game.portal_size+1 and elf.can_build_portal() == True and game.get_my_mana() >= game.portal_cost) and not (len(game.get_all_my_elves())<len(game.get_all_enemy_elves()) and my_portal_to_enemy_castle and my_portal_to_enemy_castle[0].distance(game.get_enemy_castle()) <game.castle_size+game.portal_size+diagonal_line/7) and game.portal_cost < 2000:
                    portal_in_loc = False
                    for portal in game.get_my_portals():
                        if portal.distance(game.get_enemy_castle()) < game.portal_size + game.castle_size + 3*game.elf_max_speed:
                            portal_in_loc = True
                    if (not portal_in_loc and (game.get_my_mana() >= game.portal_cost - game.get_myself().mana_per_turn) and game.can_build_portal_at(loc_to_build_portal)):
                        enemy_elf_to_elf = sorted(game.get_enemy_living_elves(), key = lambda e: e.distance(elf))
                        if enemy_elf_to_elf and enemy_elf_to_elf[0].distance(elf) < elf.attack_range + 2*elf.max_speed and enemy_elf_to_elf[0] in attack.values():
                            sortdebug(game,"Go to enemy elf that attck my elf ")
                            mapElves[elf] = enemy_elf_to_elf[0]    
                        else:
                            sortdebug(game,"Go to enemy castel for build a portal 1 ")
                            mapElves[elf] = loc_to_build_portal
                    else:
                        enemy_elf_to_elf = sorted(game.get_enemy_living_elves(),key = lambda e: e.distance(elf))
                        if enemy_elf_to_elf and enemy_elf_to_elf[0].distance(elf) < elf.attack_range + 2*elf.max_speed:
                            my_portal_to_enemy_elf = sorted(game.get_my_portals(), key = lambda p: p.distance(enemy_elf_to_elf[0]))
                            if my_portal_to_enemy_elf and my_portal_to_enemy_elf[0].distance(enemy_elf_to_elf[0]) < enemy_elf_to_elf[0].max_speed + enemy_elf_to_elf[0].attack_range + my_portal_to_enemy_elf[0].size and (elf.current_health >= enemy_elf_to_elf[0].current_health or enemy_elf_to_elf[0] in mapElvesPerTurns.values() or portal_in_loc ):
                                sortdebug(game,"Go to enemy elf that attack my portal")
                                mapElves[elf] = enemy_elf_to_elf[0]
                                mapElvesPerTurns[elf] = mapElves[elf]
                        enemy_portal_to_me=sorted(game.get_enemy_portals(),key=lambda p:p.distance(elf))
                        if enemy_portal_to_me and not enemy_portal_to_me[0] in my_tornado_turrgets.values():
                            other_tornado_attack = False
                            for portal in game.get_my_portals():
                                if portal.currently_summoning == "Tornado" and tornado_turget_after_summing(game,portal) == dangerous_portal1[elf] and portal.distance(dangerous_portal1[elf]) < game.tornado_max_speed*15 + game.tornado_attack_range + game.portal_size:
                                    other_tornado_attack = True
                            if not other_tornado_attack:
                                sortdebug(game,"go to enemy portals have nothing to do")
                                mapElves[elf] = enemy_portal_to_me[0]
                                mapElvesPerTurns[elf] = mapElves[elf]
                        if elf not in mapElves.keys():
                            sortdebug(game,"Go to enemy castel-3")
                            mapElves[elf] = game.get_enemy_castle()
                            mapElvesPerTurns[elf] = mapElves[elf]
                            if not portal_in_loc:
                                mapElvesPerTurns[elf] = loc_to_build_portal
                elif elf not in mapElves.keys():
                    enemy_elf_to_elf = sorted(game.get_enemy_living_elves(),key = lambda e: e.distance(elf))
                    if enemy_elf_to_elf and enemy_elf_to_elf[0].distance(elf) < elf.attack_range + 2*elf.max_speed:
                        my_portal_to_enemy_elf = sorted(game.get_my_portals(), key = lambda p: p.distance(enemy_elf_to_elf[0]))
                        if my_portal_to_enemy_elf and my_portal_to_enemy_elf[0].distance(enemy_elf_to_elf[0]) < enemy_elf_to_elf[0].max_speed + enemy_elf_to_elf[0].attack_range + my_portal_to_enemy_elf[0].size and (elf.current_health >= enemy_elf_to_elf[0].current_health or enemy_elf_to_elf[0] in mapElvesPerTurns.values()):
                            sortdebug(game,"Go to enemy elf that attack my portal")
                            mapElves[elf] = enemy_elf_to_elf[0]
                            mapElvesPerTurns[elf] = mapElves[elf]
                    enemy_portal_to_me=sorted(game.get_enemy_portals(),key=lambda p:p.distance(elf))
                    if enemy_portal_to_me :
                        sortdebug(game,"go to enemy portals have nothing to do")
                        mapElves[elf] = enemy_portal_to_me[0]
                        mapElvesPerTurns[elf] = mapElves[elf]
                    if elf not in mapElves.keys():
                        sortdebug(game,"Go to enemy castel-4")
                        mapElves[elf] = game.get_enemy_castle()
                        if not portal_in_loc:
                            mapElvesPerTurns[elf] = loc_to_build_portal
            if mapElves[elf] in game.get_enemy_living_elves():
                mapElvesPerTurns[elf] = elf.location
            else:
                mapElvesPerTurns[elf] = mapElves[elf]
            elf_in_use = True
            
    return mapElves
    
def dangerous_portal(game,elf):
    #vs week 2 bots
    if len(game.get_all_my_elves())<len(game.get_all_enemy_elves()):
        return None
    dangerous_portals=[]
    #Portal is dangerous when : It close to much to my castel,It far from the middel,It can destroy my castle by low health lava 
    my_portal_to_enemy_castel=sorted(game.get_my_portals(),key=lambda portal:portal.distance(game.get_enemy_castle()))
    enemy_portal_to_my_castel=sorted(game.get_enemy_portals(),key=lambda portal:portal.distance(game.get_my_castle()))
    for portal in game.get_enemy_portals():
        if portal.max_health<game.elf_attack_multiplier*30:
            if game.get_my_castle().current_health<=4*game.castle_max_health/9 and game.lava_giant_suffocation_per_turn*(int((portal.distance(game.get_my_castle())-game.lava_giant_attack_range)/game.lava_giant_max_speed)+5/game.lava_giant_attack_multiplier)<=game.lava_giant_max_health:
                dangerous_portals.append(portal)
            if game.lava_giant_suffocation_per_turn*(int((portal.distance(game.get_my_castle())-game.lava_giant_attack_range)/game.lava_giant_max_speed)+12/game.lava_giant_attack_multiplier)<=game.lava_giant_max_health :
                dangerous_portals.append(portal)
            if not (portal in dangerous_portals) and distance_point_from_line(game.get_my_castle().location,game.get_enemy_castle().location,portal.location)>=game.cols/6 and game.lava_giant_suffocation_per_turn*(int((portal.distance(game.get_my_castle())-game.lava_giant_attack_range)/game.lava_giant_max_speed)+7/game.lava_giant_attack_multiplier)<=game.lava_giant_max_health:
                dangerous_portals.append(portal)
            count=0
            for enemy in game.get_enemy_living_elves()+game.get_enemy_ice_trolls():
                if distance_point_from_line(portal.location,elf.location,enemy.location)<enemy.attack_range+enemy.max_speed and ((enemy in game.get_enemy_ice_trolls() and elf.distance(enemy)/elf.max_speed<enemy.current_health)or(enemy in game.get_enemy_living_elves() and enemy.current_health>elf.current_health)):
                    count+=1
            if count>3 and portal in dangerous_portals:
                dangerous_portals.remove(portal)
            count1=0
            for enemy_elf in game.get_enemy_living_elves():
                if enemy_elf.distance(portal)<game.portal_size+(game.elf_attack_range)*2 :
                    count1+=1
            count2=0
            for elf in game.get_my_living_elves():
                if elf.distance(portal)<game.portal_size+(game.elf_attack_range)*2 :
                    count2+=1 
            if count1>1 and count2>1 and portal in dangerous_portals and portal.current_health>=game.portal_max_health/2:
                dangerous_portals.remove(portal)
            for p in dangerous_portals :
                for tornado in game.get_my_tornadoes():
                    if p in dangerous_portals and sort_my_tornado(game)[tornado]==p and tornado.distance(p)/tornado.max_speed+p.current_health/game.tornado_attack_multiplier<tornado.current_health:
                          dangerous_portals.remove(p)
    dangerous_portals.sort(key=lambda portal:counter(game,portal,elf))
    for d_portal in dangerous_portals:
        if  not need_elf(game,dangerous_elf1,d_portal,elf) and not elf_that_more_closer_to_portal(game,elf,d_portal):
            return d_portal
    return None
    
def dangerous_elf(game,elf):
    #vs week 2 bots
    if ((len(game.get_all_my_elves())<len(game.get_all_enemy_elves())) or (elf is None)) :
        return None
    enemy_elf_with_a_chaser=[]
    for enemy in  game.get_enemy_living_elves():
        for elf1 in game.get_my_living_elves():
            if elf1 in mapElvesPerTurns.keys() and mapElvesPerTurns[elf1]==enemy and elf1!=elf:
                enemy_elf_with_a_chaser.append(enemy)
    dangerous_elf=[]
    #Elf is dangerous when: She is closer to my castle than me ,She is  far to much from the middel
    my_elf_to_my_castel=[]
    for elf3 in game.get_my_living_elves():
        if ((elf3 not in mapElvesPerTurns.keys()) or (mapElvesPerTurns[elf3] not in game.get_enemy_living_elves())) and not(dangerous_portal1[elf3]!= None and attack[elf3] == dangerous_portal1[elf3]):
            my_elf_to_my_castel.append(elf3)   
    my_elf_to_my_castel.sort(key=lambda elf1:elf1.distance(game.get_my_castle()))
    enemy_elf_to_my_castel=[]
    for enemy in game.get_enemy_living_elves():
        if (enemy not in mapElvesPerTurns.values() or (elf in mapElvesPerTurns.keys() and mapElvesPerTurns[elf] == enemy)) :
            enemy_elf_to_my_castel.append(enemy)   
    enemy_elf_to_my_castel.sort(key=lambda elf1:elf1.distance(game.get_my_castle()))
    
    if my_elf_to_my_castel and enemy_elf_to_my_castel:
        loc = game.get_my_castle()
        if  my_elf_to_my_castel[0].distance(loc)+4*game.elf_max_speed>enemy_elf_to_my_castel[0].distance(loc):
            my_elf_to_enemy_elf=my_elf_to_my_castel
            my_elf_to_enemy_elf.sort(key=lambda elf1:elf1.distance(enemy_elf_to_my_castel[0]))
            if not( enemy_elf_to_my_castel[0] in enemy_elf_with_a_chaser) and my_elf_to_enemy_elf and my_elf_to_enemy_elf[0].distance(elf)<=elf.max_speed*4 and ((not(my_elf_to_my_castel[0].distance(enemy_elf_to_my_castel[0])<5*elf.max_speed and my_elf_to_my_castel[0].distance(game.get_my_castle())<enemy_elf_to_my_castel[0].distance(game.get_my_castle())))or (spell_casted(game,enemy_elf_to_my_castel[0])=="speed up" or spell_casted(game,enemy_elf_to_my_castel[0])=="both of them" )):
                dangerous_elf.append(enemy_elf_to_my_castel[0])
    for enemy in game.get_enemy_living_elves():
        if enemy not in dangerous_elf and (distance_point_from_line(game.get_my_castle().location,game.get_enemy_castle().location,enemy.location)>Location(0,game.cols).distance(Location(game.rows,0))/6 or ( elf in danger_elves1.keys() and danger_elves1[elf]==enemy) or (enemy.distance(game.get_my_castle())<game.castle_size+game.portal_size+diagonal_line/7)):
            dangerous_elf.append(enemy)
        if enemy in danger_elves1.values() and enemy not in dangerous_elf1.values() and enemy in EnemyElfLoc.keys() and (distance_point_from_line(game.get_my_castle().location,game.get_enemy_castle().location,EnemyElfLoc[enemy])>Location(0,game.cols).distance(Location(game.rows,0))/6 or (enemy.distance(game.get_my_castle())<game.castle_size+game.portal_size+diagonal_line/7)):
            dangerous_elf.append(enemy)
    
    my_portal_to_enemy_castel=sorted(game.get_my_portals(),key=lambda portal:portal.distance(game.get_enemy_castle()))
    for enemy_elf in dangerous_elf:
        if enemy_elf.distance(game.get_enemy_castle())<diagonal_line/4 +game.castle_size and not (my_portal_to_enemy_castel and my_portal_to_enemy_castel[0].distance(game.get_enemy_castle())<enemy_elf.distance(game.get_enemy_castle())):# and not (my_elf_to_my_castel and enemy_elf.distance(game.get_my_castle()) < my_elf_to_my_castel[0].distance(game.get_my_castle())):# and (spell_casted(game,enemy_elf)!="speed up" and  spell_casted(game,enemy_elf)!="both of them" ):
            dangerous_elf.remove(enemy_elf)
    for enemy in game.get_enemy_living_elves():
        enemy_fountain_to_elf = sorted(game.get_enemy_mana_fountains(), key = lambda e: e.distance(elf))
        if enemy not in dangerous_elf and (spell_casted(game,enemy)=="speed up" or spell_casted(game,enemy)=="both of them") and game.get_my_mana_fountains():#and not (enemy_fountain_to_elf and enemy_fountain_to_elf[0].distance(elf) < game.mana_fountain_size +elf.attack_range + 3*elf.max_speed):
            dangerous_elf.append(enemy)
    bad_elf = None
    for enemy in dangerous_elf:
        for k in danger_elves1.keys():
            if k.is_alive() and danger_elves1[k] == enemy and k != elf and k.distance(enemy)  < elf.distance(enemy):
                bad_elf = enemy
    dangerous_elf.sort(key=lambda enemy:(enemy.distance(elf)/elf.max_speed)+(enemy.current_health-elf.current_health))
    for enemy in dangerous_elf:
        if enemy!= bad_elf and not need_elf(game,dangerous_elf1,enemy,elf) and (not check_if_there_is_better_elf_for_chase(game,elf) or enemy.current_health<=elf.current_health) and check_if_there_is_better_elf(game,elf,enemy)==False:
            return enemy
    return None
    
def dangerous_fountain(game,elf):
    dangerous_fountains=[]
    for fountain in game.get_enemy_mana_fountains():
        portal_to_fountain=sorted(game.get_enemy_portals(),key=lambda p:p.distance(fountain))
        dangerous_fountains.append(fountain)
        if fountain in dangerous_fountains and ( (game.get_enemy_living_elves() and fountain.distance(elf)>diagonal_line/3.5)or(len(game.get_enemy_living_elves())==0 and fountain.distance(elf)>diagonal_line/2.4)):
            dangerous_fountains.remove(fountain)
            
        for enemy in game.get_enemy_ice_trolls()+game.get_enemy_living_elves():
            if  fountain in dangerous_fountains and ((enemy in game.get_enemy_living_elves() and enemy.current_health>elf.current_health) or enemy.current_health>elf.distance(enemy)/elf.max_speed )and distance_point_from_line(fountain.location,elf.location,enemy.location)<enemy.attack_range+enemy.max_speed*2:
                dangerous_fountains.remove(fountain)
            
        for portal in game.get_enemy_portals():
            if fountain in dangerous_fountains and distance_point_from_line(fountain.location,elf.location,portal.location)<game.portal_size+game.ice_troll_attack_range+game.ice_troll_max_speed:
                dangerous_fountains.remove(fountain)
        #vs destroy bot from week1        
        if fountain.distance(game.get_my_castle())<game.castle_size+game.mana_fountain_size+500:
            dangerous_fountains.append(fountain)
        
        if fountain.max_health>game.elf_attack_multiplier*30:
            dangerous_fountains.remove(fountain)
            
    dangerous_fountains.sort(key=lambda f:f.distance(elf))
    if dangerous_fountains:
        return dangerous_fountains[0]
    return None

def check_dangerous_elf(game,elf,danger_enemy):
    elf_to_danger=sorted(game.get_my_living_elves(),key=lambda e:e.distance(danger_enemy))
    if elf_to_danger and elf_to_danger[0]!= elf and elf_to_danger[0] in mapElvesPerTurns.keys() and mapElvesPerTurns[elf_to_danger[0]]==game.get_my_castle():
        return False
    return True
    
def check_if_there_is_better_elf(game,elf,enemy):
    for elf1 in game.get_my_living_elves():
        if elf1!=elf and elf1.distance(enemy) < elf.distance(enemy) and elf1.current_health>=elf.current_health>=enemy.current_health and dangerous_elf1[elf1] == None and not (dangerous_portal1[elf1]!=None and attack[elf1]==dangerous_portal1[elf1]):
            return True
    return False
    
def need_elf(game, mapElves,destination,elf):
    my_tornado_turrgets = sort_my_tornado(game)
    for k in mapElves.keys():
        if mapElves[k] == destination and k != elf:
            return True
        if mapElves[k] in game.get_enemy_portals() and elf in mapElves.keys() and mapElves[elf] != dangerous_portal1[elf]:
            for tornado in game.get_my_tornadoes():
                if my_tornado_turrgets[tornado] == mapElves[elf]:
                    return True
    return False    
    
def good_locations_for_building_fountain(game):
    limit=limits(game)
    locations=[]
    for portal in game.get_my_portals():
        for y in limit:
            loc=portal.location.towards(y,portal.size+game.mana_fountain_size+1)
            if game.can_build_mana_fountain_at(loc) and loc.distance(game.get_enemy_castle())>loc.distance(game.get_my_castle()) and distance_point_from_line(game.get_enemy_castle().location,portal.location,loc)<game.portal_size and loc.distance(game.get_enemy_castle())>portal.distance(game.get_enemy_castle()):
                locations.append(loc)
    
    return locations

def good_locations_for_portal_for_defend_on_fountain(game):
    limit=limits(game)
    locations=[]
    for fountain in game.get_my_mana_fountains():
        for y in limit:
            loc=fountain.location.towards(y,game.portal_size+game.mana_fountain_size+1)
            if game.can_build_portal_at(loc) and distance_point_from_line(game.get_enemy_castle().location,fountain.location,loc)<300 and loc.distance(game.get_enemy_castle())<fountain.distance(game.get_enemy_castle()):
                locations.append(loc)
    return locations
            
def the_closest_elf_to_enemy_elf(game):
    if game.get_my_living_elves() and game.get_enemy_living_elves():
        elf1=game.get_my_living_elves()[0]
        for elf in game.get_my_living_elves():
            closest_enemy1=sorted(game.get_enemy_living_elves(),key=lambda enemy:enemy.distance(elf))
            closest_enemy2=sorted(game.get_enemy_living_elves(),key=lambda enemy:enemy.distance(elf1))
            if elf.distance(closest_enemy1[0])<=elf1.distance(closest_enemy2[0]):
                elf1=elf
        closest_enemy3=sorted(game.get_enemy_living_elves(),key=lambda enemy:enemy.distance(elf1))
        if closest_enemy3[0].distance(elf1)<game.elf_attack_range+(game.elf_max_speed)*2:
            return elf1
    return None
    
def elf_that_more_closer_to_portal(game,elf1,portal):
    for elf in game.get_my_living_elves():
        if elf1.distance(portal)>elf.distance(portal) and elf!=elf1 and mapElvesPerTurns[elf] not in game.get_enemy_living_elves()+game.get_enemy_portals():
            return True
    return False

def elf_that_more_closer(game,elf,loc):
    for elf1 in game.get_all_my_elves():
        if elf1.is_alive() == False and elf.distance(loc)/elf.max_speed>(elf1.initial_location.distance(loc)/elf1.max_speed)+elf1.turns_to_revive:
            return True 
    return False
    
def check_if_there_is_better_elf_for_chase(game,elf):
    for elf1 in game.get_my_living_elves():
        if elf.distance(elf1)<(elf.max_speed)*10 and elf1.current_health>elf.current_health+1 and (not mapElvesPerTurns[elf1] in game.get_enemy_living_elves()) and dangerous_elf1[elf1] == None:
            return True
    return False
    
def counter(game,portal,elf):
    how_much_lava_can_damage=int(game.lava_giant_suffocation_per_turn*(portal.distance(game.get_my_castle())-game.lava_giant_attack_range/game.lava_giant_max_speed)-game.lava_giant_max_health)
    how_much_turns_its_take_for_elf=int (portal.distance(elf)-elf.attack_range/elf.max_speed)
    return how_much_lava_can_damage+how_much_turns_its_take_for_elf
 
def if_enemy_destroy_my_fountain(game):
    global if_destroy_fountain
    loc_fountain1=[]
    for f in game.get_my_mana_fountains():
        loc_fountain1.append(f.location)
    fountain=[]
    for f in fountains_loc:
        if f not in loc_fountain1:
            fountain.append(f)
    fountain.sort(key=lambda f:f.distance(game.get_my_castle()))
    if fountain and fountain[0].distance(game.get_my_castle())<fountain[0].distance(game.get_enemy_castle()) and game.get_my_portals():
        if_destroy_fountain=True   
        
def better_elf_for_destroy_fountain(game,elf,target):
    best_elf=elf
    for elf1 in game.get_my_living_elves():
        if target.distance(elf1)-diagonal_line/7< target.distance(elf) and sum_distances_point_from_line2(game,elf1,target)+300>sum_distances_point_from_line2(game,best_elf,target):
            best_elf=elf1
    return best_elf

def sum_distances_point_from_line2(game,point1,point2) :       
    sum1=0
    for enemy in game.get_enemy_living_elves()+game.get_enemy_ice_trolls():
        if enemy.distance(point2)<point1.distance(point2):
            sum1+=distance_point_from_line(point1.location,point2.location,enemy.location)
    return sum1
    
def when_I_go_to_volcano(game,elf):
    ev = game.get_active_volcanoes()
    ev.sort(key = lambda e:e.distance(elf))
    volcano = None
    if ev:
        volcano=ev[0]
    if volcano!= None and volcano.is_active():
        if  volcano.damage_by_enemy >volcano.max_health/2 or not game.get_my_portals(): 
            return False
        if len(game.get_my_mana_fountains())> len(game.get_enemy_mana_fountains()) and (elf.distance(volcano)-(volcano.size+elf.attack_range))<diagonal_line/7:
            sortdebug( game,"volcano p=2")
            return True
            
        enemy_elf_to_volcano =sorted(game.get_enemy_living_elves(),key=lambda e:e.distance(volcano))
        if (elf.distance(volcano)-(volcano.size+elf.attack_range))<diagonal_line/7 and  len(game.get_enemy_living_elves())<len(game.get_my_living_elves()) :
            sortdebug( game,"volcano p=2")
            return True 
            
        PortalToEnemyCastle = sorted(game.get_my_portals(), key = lambda portal: portal.distance(game.get_enemy_castle()))
        EnemyPortalToMyCastle = sorted(game.get_enemy_portals(), key = lambda portal: portal.distance(game.get_my_castle()))
        if PortalToEnemyCastle and EnemyPortalToMyCastle and EnemyPortalToMyCastle[0].distance(game.get_my_castle())>PortalToEnemyCastle[0].distance(game.get_enemy_castle())*2 and (elf.distance(volcano)-(volcano.size+elf.attack_range))<diagonal_line/7:
            sortdebug( game,"volcano p=2")
            return True 
            
        if not EnemyPortalToMyCastle and (elf.distance(volcano)-(volcano.size+elf.attack_range))<diagonal_line/5:
            sortdebug( game,"volcano p=2")
            return True 
        if game.get_enemy_castle().current_health<=20 and elf.distance(volcano)-(elf.attack_range+volcano.size)<elf.max_speed*7 and dangerous_elf1[elf] == None and dangerous_portal1[elf]==None:
            sortdebug( game,"volcano p=2")
            return True 
        if game.turn<45 and game.get_my_portals() and len(game.get_my_mana_fountains())>=len(game.get_enemy_mana_fountains()) and elf in mapElvesPerTurns.keys() and mapElvesPerTurns[elf] not in game.get_enemy_mana_fountains() and mapElvesPerTurns[elf] not in dangerous_portal1.values() and mapElvesPerTurns[elf] not in dangerous_elf1.values():
            sortdebug( game,"volcano p=2")
            return True 
        check = True
        for portal in game.get_enemy_portals():
            if distance_point_from_line(volcano.location,game.get_enemy_castle().location,portal.location) < 400:
                check = False
        if elf.distance(volcano)<3*elf.max_speed and len(game.get_my_living_elves()) > len(game.get_enemy_living_elves()) and check and len(game.get_my_portals())>len(game.get_enemy_portals()):
            sortdebug( game,"volcano p=2")
            return True 
        if (elf.distance(volcano)-(volcano.size+elf.attack_range))<diagonal_line/8 <elf.max_speed*10 and volcano.current_health<3*game.elf_attack_multiplier:
            sortdebug( game,"volcano p=1")
            return 1 
            
    return False
    
def finish_the_game(game):
    return False
    b=False
    if game.turn >=700:
        PortalToEnemyCastle = sorted(game.get_my_portals(), key = lambda portal: portal.distance(game.get_enemy_castle()))
        EnemyPortalToMyCastle = sorted(game.get_enemy_portals(), key = lambda portal: portal.distance(game.get_my_castle()))
        if (PortalToEnemyCastle and EnemyPortalToMyCastle and PortalToEnemyCastle[0].distance(game.get_enemy_castle()) < EnemyPortalToMyCastle[0].distance(game.get_my_castle())):
            if len(game.get_enemy_portals())<=len(game.get_my_portals()):
                b=True
        for enemy_elf in game.get_enemy_living_elves():
            if enemy_elf.distance(game.get_enemy_castle())+diagonal_line/12>enemy_elf.distance(game.get_my_castle()):
                b=False
    if game.get_enemy_castle().current_health<game.castle_max_health/10:
        b=True
                
    return b

#***************************Alternative way************************************

def when_I_go_to_alternative_way(game,elf,target):
    global alternative_way_for_elf
    if finish_the_game(game):
        return False
    if (spell_casted(game,elf) == "invisibility" or spell_casted(game,elf) == "both of them") and Elves_invisibility_turns[elf]>2 and target in game.get_enemy_mana_fountains():
        return False
    loc_build_portal = game.get_enemy_castle().location.towards(elf.location,game.castle_size+game.portal_size+elf.max_speed/10)
    if (target == game.get_enemy_castle() or target == loc_build_portal or target in game.get_enemy_portals() or (target in game.get_enemy_living_elves()) or target in game.get_enemy_mana_fountains() or target in game.get_my_living_elves()):
        counter = 0 
        if type(target)==type(Location(0,0)):
            loc1=target
        else:
            loc1=target.location
        optional_number = 1 
        if not game.get_enemy_living_elves():
            optional_number = 3
        for ice in game.get_enemy_ice_trolls():
            if distance_point_from_line(loc1,elf.location,ice.location) < game.ice_troll_attack_range + game.ice_troll_max_speed and ice.distance(target)<elf.distance(target) and ice.distance(elf)<elf.distance(target) and ice.current_health > game.ice_troll_suffocation_per_turn and (ice.distance(elf)<ice.attack_range+2*(elf.max_speed+ice.max_speed))*optional_number:
                counter+=1
        if ((len(game.get_enemy_living_elves()) > len(game.get_my_living_elves())) or (target  in game.get_my_living_elves())):
            for enemy_elf in game.get_enemy_living_elves():
                if distance_point_from_line(loc1,elf.location,enemy_elf.location) < enemy_elf.attack_range + enemy_elf.attack_range and enemy_elf.distance(target)<elf.distance(target) and enemy_elf.distance(elf)<elf.distance(target) and (enemy_elf.distance(elf)<enemy_elf.attack_range+2*(elf.max_speed+enemy_elf.max_speed))*optional_number:
                    counter+=1
                    alternative_way_for_elf = True
        number = 1.5
        if elf in mapElvesPerTurns.keys() and mapElvesPerTurns[elf] in game.get_enemy_mana_fountains() and ((not game.get_enemy_living_elves()) or ((elf.distance(mapElvesPerTurns[elf]) - (elf.attack_range + mapElvesPerTurns[elf].size)) < number*elf.max_speed )) and ((spell_casted(game,elf) == "speed up") or (spell_casted(game,elf) == "both of them")) and (counter == 1 or elf.current_health > elf.max_health/6) and ( elf.distance(mapElvesPerTurns[elf]) - (elf.attack_range+mapElvesPerTurns[elf].size) )/elf.max_speed <= 2:
            return False

        if counter>0:
            return True 
    return False
            
def alternative_way(game,elf,target):
    speed=(elf.max_speed)*((2**0.5)/2)
    speed = int(speed)
    locations=[None,None,None,None,None,None,None,None,None]
    locations[1]=Location(elf.get_location().row-elf.max_speed,elf.get_location().col)
    locations[2]=Location(elf.get_location().row-speed,elf.get_location().col +speed)
    locations[3]=Location(elf.get_location().row,elf.get_location().col+elf.max_speed)
    locations[4]=Location(elf.get_location().row+speed,elf.get_location().col+speed)
    locations[5]=Location(elf.location.row+elf.max_speed,elf.location.col)
    locations[6]=Location(elf.location.row+speed,elf.location.col-speed)
    locations[7]=Location(elf.location.row,elf.location.col-elf.max_speed)
    locations[8]=Location(elf.location.row-speed,elf.location.col-speed)
    for x in range(len(locations)):
        if locations[x]!=None and  (locations[x].distance(target) > elf.distance(target)) and in_map_location1(game,locations[x],0):
           locations[x] = None
       
    best=0
    for index in range(len(locations)):
        if sum_distances_point_from_line(game,locations[index],target,elf)>sum_distances_point_from_line(game,locations[best],target,elf):
            best=index
    if locations[best]!=None:
        sortdebug(game,"                         *****ALTERNATIVE WAY*****")
        sortdebug(game,"which direction Im going to = " + str(best))
        if not locations[best].in_map():
            if locations[best].row<0:
                locations[best] = Location(1,elf.location.col)
            if locations[best].col<0:
                locations[best] = Location(elf.location.row,1)
            if locations[best].row>game.rows:
                locations[best] = Location(game.rows-1,elf.location.col)
            if locations[best].col<game.cols:
                locations[best] = Location(elf.location.row,game.cols-1)
        return locations[best]
    return target
    
def sum_distances_point_from_line(game,loc,target,elf):
    sum1=0
    if loc!=None :
        if target in game.get_enemy_mana_fountains():
            if type(target)==type(Location(0,0)):
                loc1=target
            else:
                loc1=target.location
            for ice in game.get_enemy_ice_trolls():
                if ice.distance(target)<elf.distance(target) and ice.distance(elf)<elf.distance(target) and ice.current_health>1:
                    sum1+=distance_point_from_line(loc,loc1,ice.location)
            sum1+=sum_distances(game,loc,game.get_enemy_ice_trolls())
        else:
            if type(target)==type(Location(0,0)):
                loc1=target
            else:
                loc1=target.location
            for ice in game.get_enemy_ice_trolls():
                if ice.distance(target)<elf.distance(target) and ice.distance(elf)<elf.distance(target) and ice.current_health>1:
                    sum1+=distance_point_from_line(loc,loc1,ice.location)
            if alternative_way_for_elf:
                for enemy_elf in game.get_enemy_living_elves():
                    if enemy_elf.distance(target)<elf.distance(target) and enemy_elf.distance(elf)<elf.distance(target):
                        sum1+=distance_point_from_line(loc,loc1,enemy_elf.location)
    return sum1
    
#***************************Run************************************

def run(game,elv,mapElves):
    speed=(elv.max_speed)*((2**0.5)/2)
    speed = int(speed)
    portals=game.get_my_portals()
    my_portal_from_my_elf=sorted(portals, key = lambda portal: portal.distance(elv))
    locations=[None,None,None,None,None,None,None,None,None]
    locations[1]=Location(elv.get_location().row-elv.max_speed,elv.get_location().col)
    locations[2]=Location(elv.get_location().row-speed,elv.get_location().col +speed)
    locations[3]=Location(elv.get_location().row,elv.get_location().col+elv.max_speed)
    locations[4]=Location(elv.get_location().row+speed,elv.get_location().col+speed)
    locations[5]=Location(elv.location.row+elv.max_speed,elv.location.col)
    locations[6]=Location(elv.location.row+speed,elv.location.col-speed)
    locations[7]=Location(elv.location.row,elv.location.col-elv.max_speed)
    locations[8]=Location(elv.location.row-speed,elv.location.col-speed)
    sort_enemy={}
    sort_enemy=sort_enemy_ice(game)
    if my_portal_from_my_elf:
        where_to_run=my_portal_from_my_elf[0].location
    else:
        where_to_run=game.get_my_castle().location
    sorted_enemy_ice = sort_enemy_ice(game)
    enemies=[]
    for enemy in game.get_enemy_living_elves():
        if (enemy.distance(elv)<=enemy.attack_range+elv.max_speed+enemy.max_speed) and enemy.current_health>elv.current_health:
            enemies.append(enemy)
    for ice in game.get_enemy_ice_trolls():
        if (ice.distance(elv)<=(game.ice_troll_attack_range+game.ice_troll_max_speed+game.elf_max_speed)) and ((sorted_enemy_ice[ice] == elv or sorted_enemy_ice[ice] in game.get_my_living_elves()) or (sorted_enemy_ice[ice].type == "LavaGiant") or (sorted_enemy_ice[ice].type == "IceTroll" and sorted_enemy_ice[ice].current_health < 3)):
            enemies.append(ice)
    for portal in game.get_enemy_portals():
        if portal.distance(elv)<diagonal_line/7:
            enemies.append(portal)
    enemies.append(game.get_enemy_castle())
    for y in range(len(locations)):
        if  y<len(locations) and locations[y] !=None and in_map_location(game,locations[y])==False:
            locations[y]=None
            
    location12=0
    for x in range(len(locations)):
        if locations[x]!=None and sum_distances(game,locations[x],enemies)>sum_distances(game,locations[location12],enemies) :
            location12=x
            
    enemies=sorted(enemies,key=lambda enemy:elv.distance(enemy))
    sortdebug(game,"                         *****RUN*****")
    sortdebug(game," ")
    sortdebug(game,"                      *****Elf Id = "+str(elv.id)+" *****")
    sortdebug(game," ")
    sortdebug(game, "which direction Im going to = " + str(location12))
    location=locations[location12]
    
    if enemies:
        enemy=enemies[0]
        if elv.current_health>2 and enemy.distance(where_to_run)>game.portal_size+game.ice_troll_attack_range*2:
            if my_portal_from_my_elf and almost_in_location(game, where_to_run.row,elv.location.row):
                if elv.distance(where_to_run)<enemy.distance(where_to_run):
                    if enemy.location.col>elv.location.col:
                        location=Location(where_to_run.row,elv.location.col-elv.max_speed)
                        sortdebug(game,"Location has been changed because we close to portal")
                    else:
                        location=Location(where_to_run.row,elv.location.col+elv.max_speed)
                        sortdebug(game,"Location has been changed because we close to portal")
            if  my_portal_from_my_elf and almost_in_location(game, where_to_run.col,elv.location.col):  
                if elv.distance(where_to_run)<enemy.distance(where_to_run):
                    if enemy.location.row>elv.location.row:
                        location=Location(elv.location.row-elv.max_speed,where_to_run.col)
                        sortdebug(game,"Location has been changed because we close to portal")
                    else:
                        location=Location(elv.location.row+elv.max_speed,where_to_run.col)
                        sortdebug(game,"Location has been changed because we close to portal")
    if location!=None:    
            return location
    return mapElves[elv]
    
def need_run(game, elf):
    # stop run - the game over a few more turns
    if (spell_casted(game, elf) == "speed up" or spell_casted(game,elf) == "both of them") and elf in mapElvesPerTurns.keys() and mapElvesPerTurns[elf] == game.get_enemy_castle() and finish_the_game(game) and elf.distance(game.get_enemy_castle()) > game.castle_size / 2:
        return None
    if finish_the_game(game) and elf.distance(game.get_enemy_castle()) <= game.castle_size / 2:
        return None
    # stop run if elf with speel and go to enemy fountain
    if (spell_casted(game, elf) == "speed up" or spell_casted(game,elf) == "both of them") and elf in mapElvesPerTurns.keys() and mapElvesPerTurns[elf] in game.get_enemy_mana_fountains():
        return None
    # need destroy fountain and elf close and can destroy
    if mapElvesPerTurns[elf] in game.get_enemy_mana_fountains() and elf.current_health >= mapElvesPerTurns[elf].current_health and elf.distance(mapElvesPerTurns[elf]) < (elf.attack_range + game.mana_fountain_size + 3*elf.max_speed):
        return None
    # stop run if the elf really close to enemy fountain
    if len(game.get_enemy_mana_fountains()) > len(game.get_my_mana_fountains()):
        enemy_fountain_to_elf = sorted(game.get_enemy_mana_fountains(), key=lambda e: e.distance(elf))
        if enemy_fountain_to_elf and enemy_fountain_to_elf[0].distance(elf) - (elf.attack_range + game.mana_fountain_size) < 4 * elf.max_speed and elf.current_health > elf.max_health / 6:
            return None
    my_ice_turrgets = sort_my_ice(game)
    # the function get None
    if elf == None:
        return None
    # the heatth of the elf so low better to die
    if elf.current_health == 1:
        print "aaaaaaaaaaaaaaaaaaaaaaaaaaa"
        return None
    loc_to_build_portal = game.get_enemy_castle().location.towards(elf.location,game.castle_size + game.portal_size + elf.max_speed / 10)
    # elf with all the spells and in good place to build portal
    if spell_casted(game, elf) == "both of them" and elf in mapElvesPerTurns.keys() and (mapElvesPerTurns[elf] == game.get_enemy_castle() or mapElvesPerTurns[elf] == loc_to_build_portal):
        return None
    # elf in the middle to attack mana fountain
    if attack[elf] in game.get_enemy_mana_fountains():  # and (how_many_enemies_can_attack_me(game,elf))*(fountain_to_elf[0].current_health-1) <= elf.current_health:
        return None
    sorted_my_ice = sort_my_ice(game)
    sorted_enemy_ice = sort_enemy_ice(game)
    # running from elf with more life than me:
    portalneerelf = sorted(game.get_enemy_portals(), key=lambda p: p.distance(elf))
    my_portal_near_elf = sorted(game.get_my_portals(), key=lambda p: p.distance(elf))
    danger_elves = [enemy_elf for enemy_elf in game.get_enemy_living_elves() if (enemy_elf.current_health > elf.current_health) and (portalneerelf) and (elf.distance(portalneerelf[0]) < 600) and enemy_elf.distance(elf) < 2 * (elf.max_speed) + elf.attack_range and (attack[elf] == None) and not (my_portal_near_elf and ( (game.get_my_mana() >= game.ice_troll_cost) or (my_portal_near_elf[0].is_summoning) ) and my_portal_near_elf[0].current_health / enemy_elf.attack_multiplier < game.ice_troll_summoning_duration and my_portal_near_elf[0].distance(enemy_elf) < 2 * enemy_elf.max_speed + enemy_elf.attack_range +my_portal_near_elf[0].size)]
    
    danger_ice = [ice
    for ice in game.get_enemy_ice_trolls()
    if (ice.distance(elf) <= (game.ice_troll_attack_range + game.ice_troll_max_speed + game.elf_max_speed)) and ((sorted_enemy_ice[ice] == elf or sorted_enemy_ice[ice] in game.get_my_living_elves()) or
    (sorted_enemy_ice[ice].type == "LavaGiant") or
    (sorted_enemy_ice[ice].type == "IceTroll" and sorted_enemy_ice[ice].current_health < 3)) 
    and not (dangerous_elf1[elf] != None and dangerous_elf1[elf].distance(game.get_my_castle()) < elf.distance(game.get_my_castle()) and elf.current_health > dangerous_elf1[elf].current_health + dangerous_elf1[elf].max_health / 6 and spell_casted(game, elf) == "speed up")]
    
    danger_portals = [portal for portal in game.get_enemy_portals() if
    portal.currently_summoning == "IceTroll" and elf.distance(
    portal) < elf.attack_range + 2 * elf.max_speed + portal.size and len(
    game.get_enemy_living_elves()) > len(game.get_my_living_elves()) and not (
    dangerous_elf1[elf] != None and dangerous_elf1[elf].distance(game.get_my_castle()) < elf.distance(game.get_my_castle()) and elf.current_health > dangerous_elf1[elf].current_health + dangerous_elf1[elf].max_health / 6 and elf.distance(dangerous_elf1[elf]) < elf.attack_range + elf.max_speed)]
    enemy_elf_optional = sorted(game.get_enemy_living_elves(), key=lambda e: e.distance(elf))
    enemy_elf_optional.sort(key=lambda e: e.distance(elf) < 2 * elf.max_speed + elf.attack_range)
    enemy_elf_to_this_elf = sorted(game.get_enemy_living_elves(), key=lambda e: e.distance(elf))
    enemy_portal_to_this_elf = sorted(game.get_enemy_portals(), key=lambda p: p.distance(elf))
    dangerus = sorted(danger_ice, key=lambda d: d.distance(elf))

    '''
    enemy_mana_to_elf = sorted(game.get_enemy_mana_fountains(), key = lambda e: e.distance(elf))
    if enemy_mana_to_elf and elf in mapElvesPerTurns and mapElvesPerTurns[elf] in game.get_enemy_mana_fountains() and len(game.get_my_mana_fountains()) <= len(game.get_enemy_mana_fountains()) and elf.in_attack_range(enemy_mana_to_elf[0]) and elf.current_health > enemy_mana_to_elf[0].current_health:
        return None'''

    # we can go to ice for help :
    for elf1 in game.get_my_living_elves():
        enemy_elf_to_this_elf = sorted(game.get_enemy_living_elves(), key=lambda e: e.distance(elf1))
        if enemy_elf_to_this_elf and enemy_elf_to_this_elf[0].distance(elf1) < enemy_elf_to_this_elf[0].attack_range + 2 * elf1.max_speed and elf1.distance(elf) < elf.max_speed*5 and enemy_elf_to_this_elf[0].current_health > elf1.current_health:
            elf_in_ice_target = False
            for k in my_ice_turrgets.keys():
                if my_ice_turrgets[k] == enemy_elf_to_this_elf[0] and k.current_health > 8 and k.distance(elf1) < 2 * k.max_speed:
                    elf_in_ice_target = True
            if elf_in_ice_target and attack[elf1] not in game.get_enemy_living_elves():
                danger_elves.append(enemy_elf_to_this_elf[0])
    # if enemy_portal_to_this_elf and elf.in_attack_range(enemy_portal_to_this_elf[0]) and len(game.get_my_mana_fountains()) >= len(game.get_enemy_mana_fountains()) and len(game.get_my_portals()) > len(game.get_enemy_portals()) and elf in mapElvesPerTurns.keys() and mapElvesPerTurns[elf] in game.get_enemy_portals():
    #   pass
    
    # elf attack portal and he will succeed to finish
    if enemy_portal_to_this_elf and attack[elf] == enemy_portal_to_this_elf[0] and (how_many_enemies_can_attack_me(game, elf)) * (enemy_portal_to_this_elf[0].current_health - 1) <= elf.current_health:# and elf in mapElvesPerTurns.keys() and mapElvesPerTurns[elf] in game.get_enemy_portals():
        return None
    die_enemy = []
    for enemy_elf in game.get_all_enemy_elves():
        if not enemy_elf.is_alive():
            die_enemy.append(enemy_elf)
    die_enemy.sort(key=lambda e: e.turns_to_revive)

    # elf with invisibility and not close to enemy and the turn until the spell is over more than 2
    if (spell_casted(game, elf) == "invisibility") and not (dangerus and dangerus[0].distance(elf) < dangerus[0].attack_range + dangerus[0].max_speed and elf in Elves_invisibility_turns.keys() and Elves_invisibility_turns[elf] < 2):
        return None

    # elf target is mana fountain and he have speed spell
    enemy_ice_to_elf = sorted(game.get_enemy_ice_trolls(), key=lambda i: i.distance(elf))
    if spell_casted(game, elf) == "speed up" and elf.current_health > 1 and elf in mapElvesPerTurns.keys() and mapElvesPerTurns[elf] in game.get_enemy_mana_fountains():  # enemy_ice_to_elf and elf.distance(mapElvesPerTurns[elf])-enemy_ice_to_elf[0].distance(elf) > game.ice_troll_attack_range+game.ice_troll_max_speed:
        return None

    # I have ice vs enemy elves that in my range - I run , the ice will fight
    if danger_elves:
        for ice in game.get_my_ice_trolls():
            if sorted_my_ice[ice] == danger_elves[0] and ice.distance(danger_elves[0]) < ice.attack_range + ice.max_speed:
                return danger_elves[0]

    # my attackers more enemy attackers so the elf will not hurt
    counter_enemy = 0
    counter_me = 0
    enemy_elves_neer_elf = sorted(game.get_enemy_living_elves(), key=lambda e: e.distance(elf))
    if enemy_elves_neer_elf and elf.distance(enemy_elves_neer_elf[0]) < elf.attack_range + elf.max_speed:
        for enemy in game.get_my_ice_trolls():
            if enemy.distance(elf) <= enemy.attack_range and enemy.current_health > 2 and sort_my_ice(game)[enemy] not in game.get_enemy_lava_giants():
                counter_me += 1
        for ice in game.get_enemy_ice_trolls():
            if ice.distance(elf) < ice.attack_range + elf.max_speed and ice.current_health > 2 and sorted_enemy_ice[ice] not in game.get_my_lava_giants():
                counter_enemy += 1
        if counter_me > counter_enemy:
            return None
    # if elf run the enemy elf will can attack my elf
    colsest_enemy_elf = sorted(game.get_enemy_living_elves(), key=lambda e1: e1.distance(elf))
    if colsest_enemy_elf and colsest_enemy_elf[0].distance(elf) <= elf.attack_range:
        return None
    # run from summing portal:
    if danger_portals:
        return danger_portals[0]
    # run from ice:
    if danger_ice and not (elf.current_health <= game.elf_max_health / 6 and len(game.get_my_living_elves()) > len(game.get_enemy_living_elves()) and len(game.get_my_portals()) >= len(game.get_enemy_portals()) and game.get_myself().mana_per_turn > game.get_enemy().mana_per_turn):
        return danger_ice[0]
    # run from elf:
    if danger_elves:
        return danger_elves[0]
    return None
        
def sum_distances(game,location,enemies):
    sum1=0
    if location!= None:
        for enemy in enemies :
            if enemy !=None:
                sum1+=enemy.distance(location)
    return sum1
        
#***************************Attack************************************
        
def try_attack(game,elf,for_check):
    enemy_ice_turrgets = sort_my_ice(game)
    if finish_the_game(game):
        if elf.distance(game.get_enemy_castle())<game.castle_size/2:
            if for_check:
                return game.get_enemy_castle()
            elf.attack(game.get_enemy_castle())
            sortdebug(game,"                      *****ATTACK*****")
            sortdebug(game," ")
            sortdebug(game,"                      *****Elf Id = "+str(elf.id)+" *****")
            sortdebug(game," ")
            sortdebug(game,"Attack :"+ str(game.get_enemy_castle()))
            return True
        else:
            if for_check:
                return None
            return False
            
    # attack enemy lava:
    enemy_to_elf = sorted(game.get_enemy_ice_trolls(), key = lambda i: i.distance(elf))
    if (spell_casted(game,elf)=="invisibility" or spell_casted(game,elf)=="both of them") and enemy_to_elf and elf.distance(enemy_to_elf[0]) < game.ice_troll_max_speed+game.ice_troll_attack_range:
        if for_check:
            return None 
        return False
    if ((elf in mapElvesPerTurns.keys() and mapElvesPerTurns[elf] not in game.get_enemy_portals()) or (elf not in mapElvesPerTurns.keys())) and (game.get_my_castle().current_health < 20 or (game.get_myself().mana_per_turn == 0 and game.get_my_mana() == 0 and dangerous_fountain(game,elf) == None)):
        for lava in game.get_enemy_lava_giants():
            if elf.in_attack_range(lava):
                if for_check:
                    return lava
                elf.attack(lava)
                sortdebug(game,"                      *****ATTACK*****")
                sortdebug(game," ")
                sortdebug(game,"                      *****Elf Id = "+str(elf.id)+" *****")
                sortdebug(game," ")
                sortdebug(game,"Attack "+ str(lava))
                return True 
                '''
    portal_to_attack = None
    for portal in game.get_enemy_portals():
        if elf_attackers_count(game,portal) >= portal.current_health:
            if portal_to_attack == None:
                portal_to_attack = portal
            elif portal.current_health > portal_to_attack.current_health:
                portal_to_attack = portal
    if portal_to_attack != None:
        sortdebug(game, " attack speshial portal")
        elf.attack(portal_to_attack)
        return True
    '''
    if elf in mapElvesPerTurns.keys() and mapElvesPerTurns[elf] and mapElvesPerTurns[elf] in game.get_enemy_mana_fountains() and (spell_casted(game,elf)=="invisibility" or spell_casted(game,elf)=="both of them"):
        if for_check:
            return None 
        return False
    # special event we attack elf before fountain 
    if enemy_attackers_count(game,elf) == 1 and elf not in enemy_ice_turrgets.values():
        enemy_elf_to_this_elf = sorted(game.get_enemy_living_elves(), key = lambda e: e.distance(elf))
        if enemy_elf_to_this_elf and elf.in_attack_range(enemy_elf_to_this_elf[0]) and ((elf.current_health > 3*enemy_elf_to_this_elf[0].current_health) or (not game.get_enemy_portals() and not game.get_enemy_ice_trolls() and elf.current_health>enemy_elf_to_this_elf[0].current_health)):
            if for_check:
                return enemy_elf_to_this_elf[0]
            elf.attack(enemy_elf_to_this_elf[0])
            sortdebug(game,"                      *****ATTACK(elf before fauntain)*****")
            sortdebug(game," ")
            sortdebug(game,"                      *****Elf Id = "+str(elf.id)+" *****")
            sortdebug(game," ")
            sortdebug(game,"Attack "+ str(enemy_elf_to_this_elf[0]))
            return True
    # attack fauntain
    optinal_fountain = [enemy_fountain  for enemy_fountain  in game.get_enemy_mana_fountains() if elf.in_attack_range(enemy_fountain)]
    optinal_fountain.sort(key = lambda f: f.current_health)
    if optinal_fountain:
        if for_check:
            return optinal_fountain[0]
        elf.attack(optinal_fountain[0])
        sortdebug(game,"                      *****ATTACK*****")
        sortdebug(game," ")
        sortdebug(game,"                      *****Elf Id = "+str(elf.id)+" *****")
        sortdebug(game," ")
        sortdebug(game,"Attack "+ str(optinal_fountain[0]))
        return True
    if elf in mapElvesPerTurns.keys() and mapElvesPerTurns[elf] and mapElvesPerTurns[elf] in game.get_enemy_mana_fountains():
        other_go_to_my_turget = False
        for k in mapElvesPerTurns.keys():
            if k in game.get_my_living_elves() and mapElvesPerTurns[k] == mapElvesPerTurns[elf] and elf!= k and k.distance(mapElvesPerTurns[elf]) < elf.distance(mapElvesPerTurns[elf]):
                other_go_to_my_turget = True
        if not other_go_to_my_turget:
            if for_check:
                return None 
            return False
    # attack enemy elf:
    if elf in mapElvesPerTurns.keys() and mapElvesPerTurns[elf] and mapElvesPerTurns[elf] in game.get_enemy_mana_fountains() and (spell_casted(game,elf)=="speed up" or spell_casted(game,elf)=="both of them"):
        if for_check:
            return None 
        return False
    optinal_enemy_elves = [enemy_elf for enemy_elf in game.get_enemy_living_elves() if elf.in_attack_range(enemy_elf)]
    enemy_ice_to_elf = sorted(game.get_enemy_ice_trolls(), key = lambda i: i.distance(elf))
    optinal_enemy_elves.sort(key = lambda e: e.current_health)
    if optinal_enemy_elves:
        best_turrget = optinal_enemy_elves[0]
        '''
        if dangerous_elf1[elf]!= None and dangerous_elf1[elf]!=optinal_enemy_elves[0]:
            return False
            '''
        for enemy_elf in optinal_enemy_elves:
            if attackers_count(game,enemy_elf) > attackers_count(game,best_turrget):
                best_turrget = enemy_elf
            elif attackers_count(game,enemy_elf) == attackers_count(game,best_turrget) and enemy_elf.current_health < best_turrget.current_health:
                best_turrget = enemy_elf
        # The most attacked enemy
        if attackers_count(game,best_turrget) > 1:
            if for_check:
                return best_turrget
            elf.attack(best_turrget)
            sortdebug(game,"                      *****ATTACK*****")
            sortdebug(game," ")
            sortdebug(game,"                      *****Elf Id = "+str(elf.id)+" *****")
            sortdebug(game," ")
            sortdebug(game,"Attack "+ str(best_turrget))
            return True
        # if only this elf can attack 
        elif attackers_count(game,best_turrget) == 1:
            # look for an enemy with the least life:
            for enemy_elf in optinal_enemy_elves:
                if enemy_elf.current_health < best_turrget.current_health:
                    best_turrget = enemy_elf
            if for_check:
                return best_turrget
            elf.attack(best_turrget)
            sortdebug(game,"                      *****ATTACK*****")
            sortdebug(game," ")
            sortdebug(game,"                      *****Elf Id = "+str(elf.id)+" *****")
            sortdebug(game," ")
            sortdebug(game,"Attack "+ str(best_turrget))
            return True
    # attack volcano
    optinal_v = [v for v in game.get_active_volcanoes() if elf.in_attack_range(v)]
    optinal_v.sort(key = lambda e:e.distance(elf))
    if optinal_v and elf.in_attack_range(optinal_v[0]) and elf in mapElvesPerTurns.keys() and mapElvesPerTurns[elf] in optinal_v and (spell_casted(game,elf) != "speed up" and spell_casted(game,elf) != "both of them" and  spell_casted(game,elf) != "invisibility"):
        if for_check:
            return optinal_v[0]
        elf.attack(optinal_v[0])
        sortdebug(game,"attack volcano")
        return True
    # attack enemy tornado:
    enemy_tornado_turrgets = sort_enemy_tornado(game)
    optinal_tornado = [tornado for tornado in game.get_enemy_tornadoes() if elf.in_attack_range(tornado) and tornado in enemy_tornado_turrgets.keys() and tornado.suffocation_per_turn*((tornado.distance(enemy_tornado_turrgets[tornado]) - (tornado.attack_range + enemy_tornado_turrgets[tornado].size))/tornado.max_speed) < tornado.current_health]
    if optinal_tornado and dangerous_elf1[elf] == None and dangerous_portal1[elf] == None and elf in mapElvesPerTurns.keys() and enemy_tornado_turrgets[tornado] in game.get_my_mana_fountains():
        if for_check:
            return optinal_tornado[0]
        elf.attack(optinal_tornado[0])
        sortdebug(game,"attack enemy tornado")
        return True
    # attack portal:
    enemy_portal_to_elf = sorted(game.get_enemy_portals(), key = lambda p: p.distance(elf))
    enemy_to_elf = sorted(game.get_enemy_ice_trolls(), key = lambda i: i.distance(elf))
    if spell_casted(game,elf)!=None and enemy_to_elf and elf.in_attack_range(enemy_to_elf[0]):
        if for_check:
            return None 
        return False
    if elf in mapElvesPerTurns.keys() and mapElvesPerTurns[elf] in game.get_my_portals():
        if for_check:
            return None 
        return False
    enemy_mana_to_elf = sorted(game.get_enemy_mana_fountains(), key = lambda e: e.distance(elf))
    if elf in mapElvesPerTurns.keys() and mapElvesPerTurns[elf] in game.get_enemy_living_elves() and mapElvesPerTurns[elf].distance(game.get_my_castle()) < elf.distance(game.get_my_castle()) and dangerous_elf1[elf]!=None and enemy_portal_to_elf and enemy_portal_to_elf[0].distance(game.get_my_castle()) < game.get_my_castle().distance(game.get_enemy_castle())/3 and not (enemy_mana_to_elf and elf.in_attack_range(enemy_mana_to_elf[0])):
        if for_check:
            return None 
        return False
    optinal_portal = [enemy_portal for enemy_portal in game.get_enemy_portals() if elf.in_attack_range(enemy_portal) and enemy_portal.max_health<game.elf_attack_multiplier*30]
    optinal_portal.sort(key = lambda p: p.current_health)
    if elf in mapElvesPerTurns.keys() and mapElvesPerTurns[elf] in game.get_enemy_mana_fountains() and elf.distance(mapElvesPerTurns[elf]) < game.mana_fountain_size + elf.attack_range + 4*elf.max_speed:
        optinal_portal = []
    if elf in mapElvesPerTurns.keys() and mapElvesPerTurns[elf] in game.get_enemy_mana_fountains():
        optinal_portal = []
    if (spell_casted(game,elf)=="invisibility" or spell_casted(game,elf)=="both of them"):
        optinal_portal = []
    if optinal_portal:
        sorted_tornado=sort_my_tornado(game)
        for tornado in game.get_my_tornadoes():
            if sorted_tornado[tornado]==optinal_portal[0] and tornado.current_health>(tornado.distance(optinal_portal[0])-(optinal_portal[0].size+tornado.attack_range))/tornado.max_speed +optinal_portal[0].current_health/game.tornado_attack_multiplier+2:
                if optinal_portal[0] != dangerous_portal1[elf] and (tornado.distance(optinal_portal[0])-(tornado.attack_range))/tornado.max_speed<=5:
                    if for_check:
                        return None 
                    return False
                if not game.get_enemy_living_elves() and optinal_portal[0] != dangerous_portal1[elf] and (tornado.distance(optinal_portal[0])-(tornado.attack_range))/tornado.max_speed<=tornado.current_health-8:
                    if for_check:
                        return None 
                    return False
        if (elf in mapElvesPerTurns.keys() and mapElvesPerTurns[elf]!=optinal_portal[0] )and dangerous_elf1[elf]!=None and optinal_portal[0].current_health>optinal_portal[0].max_health/2:
            if for_check:
                return None 
            return False
        count1=0
        for enemy_elf in game.get_enemy_living_elves():
            if enemy_elf.distance(optinal_portal[0])<game.portal_size+(game.elf_attack_range)*2 and elf.current_health-3<enemy_elf.current_health:
                count1+=1
        count2=0
        for my_elf in game.get_my_living_elves():
            if my_elf.distance(optinal_portal[0])<game.portal_size+(game.elf_attack_range)*2:
                count2+=1
        if count1>1 and count2>1:
            if for_check:
                return None 
            return False
        best_turrget = optinal_portal[0]
        for enemy_portal in optinal_portal:
            if elf_attackers_count(game,enemy_portal) > elf_attackers_count(game,best_turrget):
                best_turrget = enemy_portal
            elif elf_attackers_count(game,enemy_portal) == elf_attackers_count(game,best_turrget) and enemy_portal.current_health < best_turrget.current_health:
                best_turrget = enemy_portal
            # The most attacked enemy
            if elf_attackers_count(game,best_turrget) > 1:
                if for_check:
                    return best_turrget
                elf.attack(best_turrget)
                sortdebug(game,"                      *****ATTACK*****")
                sortdebug(game," ")
                sortdebug(game,"                      *****Elf Id = "+str(elf.id)+" *****")
                sortdebug(game," ")
                sortdebug(game,"Attack "+ str(best_turrget))
                return True
            # if only this elf can attack 
            elif elf_attackers_count(game,best_turrget) == 1:
                # look for an enemy with the least life:
                for enemy_portal in optinal_portal:
                    if enemy_portal.current_health < best_turrget.current_health:
                        best_turrget = enemy_portal
                if for_check:
                    return best_turrget
                elf.attack(best_turrget)
                sortdebug(game,"                      *****ATTACK*****")
                sortdebug(game," ")
                sortdebug(game,"                      *****Elf Id = "+str(elf.id)+" *****")
                sortdebug(game," ")
                sortdebug(game,"Attack "+ str(best_turrget))
                return True
    # attack enemy castle:
    if elf.in_attack_range(game.get_enemy_castle()) and mapElvesPerTurns[elf] == game.get_enemy_castle():
        if for_check:
            return game.get_enemy_castle()
        elf.attack(game.get_enemy_castle())
        sortdebug(game,"                      *****ATTACK*****")
        sortdebug(game," ")
        sortdebug(game,"                      *****Elf Id = "+str(elf.id)+" *****")
        sortdebug(game," ")
        sortdebug(game,"Attack :"+ str(game.get_enemy_castle()))
        return True
    # attack enemy ice:
    if spell_casted(game,elf)=="invisibility" or spell_casted(game,elf)=="speed up" or spell_casted(game,elf)=="both of them":
        if for_check:
            return None 
        return False
    if elf in mapElvesPerTurns.keys() and mapElvesPerTurns[elf] in game.get_enemy_living_elves():
        if for_check:
            return None 
        return False
    if  elf in mapElvesPerTurns.keys() and mapElvesPerTurns[elf] in game.get_enemy_mana_fountains():
        if for_check:
            return None 
        return False
    optinal_enemy_ice = [enemy_ice for enemy_ice in game.get_enemy_ice_trolls() if elf.in_attack_range(enemy_ice)]
    optinal_enemy_ice.sort(key = lambda i: i.current_health)
    if optinal_enemy_ice:
        best_turrget = optinal_enemy_ice[0]
        for enemy_ice in optinal_enemy_ice:
            if attackers_count(game,enemy_ice) > attackers_count(game,best_turrget) and enemy_ice.current_health > game.ice_troll_suffocation_per_turn:
                best_turrget = enemy_ice
            elif attackers_count(game,enemy_ice) == attackers_count(game,best_turrget) and enemy_ice.current_health < best_turrget.current_health and enemy_ice.current_health > game.ice_troll_suffocation_per_turn:
                best_turrget = enemy_ice
        # The most attacked enemy
        if attackers_count(game,best_turrget) > 1:
            if for_check:
                return best_turrget
            elf.attack(best_turrget)
            sortdebug(game,"                      *****ATTACK*****")
            sortdebug(game," ")
            sortdebug(game,"                      *****Elf Id = "+str(elf.id)+" *****")
            sortdebug(game," ")
            sortdebug(game,"Attack "+ str(best_turrget))
            return True
        # if only this elf can attack 
        elif attackers_count(game,best_turrget) == 1:
            # look for an enemy with the least life:
            for enemy_ice in optinal_enemy_ice:
                if enemy_ice.current_health < best_turrget.current_health and enemy_ice.current_health > game.ice_troll_suffocation_per_turn:
                    best_turrget = enemy_ice
            if for_check:
                return best_turrget
            elf.attack(best_turrget)
            sortdebug(game,"                      *****ATTACK*****")
            sortdebug(game," ")
            sortdebug(game,"                      *****Elf Id = "+str(elf.id)+" *****")
            sortdebug(game," ")
            sortdebug(game,"Attack "+ str(best_turrget))
            return True
    if for_check:
        return None
    return False

#***************************Other************************************

def sort_enemy_ice(game):
    all_creatures = game.get_my_living_elves() + game.get_my_creatures()
    enemy_ice_turrgets = {}
    if all_creatures:
        for enemy_ice in game.get_enemy_ice_trolls():
            creature_closest_to_the_enemy = sorted(all_creatures, key = lambda creature: creature.distance(enemy_ice))
            cresture_with_same_distance = -1
            for creature in creature_closest_to_the_enemy:
                if creature.distance(enemy_ice) == creature_closest_to_the_enemy[0].distance(enemy_ice):
                    cresture_with_same_distance += 1
            enemy_ice_turrgets[enemy_ice] = creature_closest_to_the_enemy[0]
            for x in range(1,cresture_with_same_distance+1):
                if creature_closest_to_the_enemy[x] in game.get_my_ice_trolls() and enemy_ice_turrgets[enemy_ice] in game.get_my_living_elves():
                    enemy_ice_turrgets[enemy_ice] = creature_closest_to_the_enemy[x]
                if (creature_closest_to_the_enemy[x] in game.get_my_lava_giants()) and (enemy_ice_turrgets[enemy_ice] in game.get_my_living_elves() or enemy_ice_turrgets[enemy_ice] in game.get_my_ice_trolls()):
                    enemy_ice_turrgets[enemy_ice] = creature_closest_to_the_enemy[x]
                if (creature_closest_to_the_enemy[x] in game.get_my_tornadoes()) and (enemy_ice_turrgets[enemy_ice] in game.get_my_living_elves() or enemy_ice_turrgets[enemy_ice] in game.get_my_ice_trolls() or enemy_ice_turrgets[enemy_ice] in game.get_my_lava_giants()):
                    enemy_ice_turrgets[enemy_ice] = creature_closest_to_the_enemy[x]
    return enemy_ice_turrgets 

def sort_my_ice(game):
    all_creatures = game.get_enemy_living_elves() + game.get_enemy_creatures()
    my_ice_turrgets = {}
    if all_creatures:
        for my_ice in game.get_my_ice_trolls():
            creature_closest_to_the_my = sorted(all_creatures, key = lambda creature: creature.distance(my_ice))
            cresture_with_same_distance = -1
            for creature in creature_closest_to_the_my:
                if creature.distance(my_ice) == creature_closest_to_the_my[0].distance(my_ice):
                    cresture_with_same_distance += 1
            my_ice_turrgets[my_ice] = creature_closest_to_the_my[0]
            for x in range(1,cresture_with_same_distance+1):
                if creature_closest_to_the_my[x] in game.get_enemy_ice_trolls() and my_ice_turrgets[my_ice] in game.get_enemy_living_elves():
                    my_ice_turrgets[my_ice] = creature_closest_to_the_my[x]
                if (creature_closest_to_the_my[x] in game.get_enemy_lava_giants()) and (my_ice_turrgets[my_ice] in game.get_enemy_living_elves() or my_ice_turrgets[my_ice] in game.get_enemy_ice_trolls()):
                    my_ice_turrgets[my_ice] = creature_closest_to_the_my[x]
                if (creature_closest_to_the_my[x] in game.get_enemy_tornadoes()) and (my_ice_turrgets[my_ice] in game.get_enemy_living_elves() or my_ice_turrgets[my_ice] in game.get_enemy_ice_trolls() or my_ice_turrgets[my_ice] in game.get_enemy_lava_giants()):
                    my_ice_turrgets[my_ice] = creature_closest_to_the_my[x]
    return my_ice_turrgets 

def sort_enemy_tornado(game):
    all_buildings = game.get_my_portals() + game.get_my_mana_fountains()
    enemy_tornado_turrgets = {}
    if all_buildings:
        for enemy_tornado in game.get_enemy_tornadoes():
            building_closest_to_the_enemy = sorted(all_buildings, key = lambda building: building.distance(enemy_tornado))
            enemy_tornado_turrgets[enemy_tornado] = building_closest_to_the_enemy[0]
    return enemy_tornado_turrgets

def sort_my_tornado(game):
    all_buildings = game.get_enemy_portals() + game.get_enemy_mana_fountains()
    my_tornado_turrgets = {}
    if all_buildings:
        for my_tornado in game.get_my_tornadoes():
            building_closest_to_me = sorted(all_buildings, key = lambda building: building.distance(my_tornado))
            my_tornado_turrgets[my_tornado] = building_closest_to_me[0]
    return my_tornado_turrgets

def limits(game):
    limit=[]
    for x in xrange(0,game.cols,600):
        limit.append(Location(0,x))
        limit.append(Location(game.rows,x))
    for y in xrange(0,game.rows,600):
        limit.append(Location(y,0))
        limit.append(Location(y,game.cols))
    return limit
    
def distance_point_from_line(location1,location2,point):
    xloc1=location1.col
    xloc2=location2.col
    yloc1=location1.row
    yloc2=location2.row
    if xloc2-xloc1!=0:
        m=float(yloc2-yloc1)/float(xloc2-xloc1)
        B=yloc1-(m*xloc1)
        xp=point.col 
        yp=point.row
        dist=abs((m*xp-yp+B)/((m*m +1)**0.5))
        return int (dist)
    else:
        return abs(point.col-xloc1)

def how_many_enemies_can_attack_me(game,item):
    count = 0
    if item in game.get_my_living_elves()+game.get_my_ice_trolls():
        for enemy in game.get_enemy_ice_trolls()+game.get_enemy_living_elves():
            if item.distance(enemy)<=enemy.attack_range:
                count +=1
        return count
    else:
        for enemy in game.get_enemy_living_elves():
            if enemy.in_attack_range(item):
                count +=1
        return count

def almost_in_location(game,num1,num2):
    if abs(num1-num2)<=2*(game.elf_max_speed):
        return True
    return False

def in_map_location(game,location):
    if location.row>=game.rows-400 or location.col>=game.cols-400 or location.row<=400 or location.col<=400:
        return False
    return True
    
def in_map_location1(game,location,num):
    if location.row>=game.rows-num or location.col>=game.cols-num or location.row<=num or location.col<=num:
        return False
    return True
    
def in_map_location_invisibility(game,location):
    if location.row>=game.rows-game.rows/15 or location.col>=game.cols-game.cols/15 or location.row<=game.rows/15 or location.col<=game.cols/15:
        return False
    return True
    
def attackers_count12(game,enemy):
    count = 0
    for elf in game.get_my_living_elves():
        if elf.in_attack_range(enemy):
            count +=1
    for ice in game.get_my_ice_trolls(): 
        enemy_ice_neer_my_ice = sorted(game.get_enemy_ice_trolls(), key = lambda i: i.distance(ice))
        if ice.distance(enemy)<game.ice_troll_attack_range and ((not enemy_ice_neer_my_ice) or ice.distance(enemy)<ice.distance(enemy_ice_neer_my_ice[0])):
            count +=1
        elif ice.distance(enemy)<game.ice_troll_attack_range and enemy_ice_neer_my_ice and enemy_ice_neer_my_ice[0] == enemy:
           count +=1
    return count
    
def attackers_count(game,enemy):
    count = 0
    for elf in game.get_my_living_elves():
        if elf.in_attack_range(enemy):
            count +=1
    for ice in game.get_my_ice_trolls(): 
        enemy_ice_neer_my_ice = sorted(game.get_enemy_ice_trolls(), key = lambda i: i.distance(ice))
        if ice.distance(enemy)<game.ice_troll_attack_range and ((not enemy_ice_neer_my_ice) or ice.distance(enemy)<ice.distance(enemy_ice_neer_my_ice[0])):
            count +=1
        elif ice.distance(enemy)<game.ice_troll_attack_range and enemy_ice_neer_my_ice and enemy_ice_neer_my_ice[0] == enemy:
           count +=1
    return count

def elf_attackers_count(game,enemy):
    count = 0
    for elf in game.get_my_living_elves():
        if elf.in_attack_range(enemy):
            count +=1
    return count 
    
def enemy_attackers_count(game,my):
    count = 0
    for elf in game.get_enemy_living_elves():
        if elf.in_attack_range(my):
            count +=1
    for ice in game.get_enemy_ice_trolls(): 
        my_ice_neer_enemy_ice = sorted(game.get_my_ice_trolls(), key = lambda i: i.distance(ice))
        if ice.distance(my)<game.ice_troll_attack_range and ((not my_ice_neer_enemy_ice) or ice.distance(my)<ice.distance(my_ice_neer_enemy_ice[0])):
            count +=1
        elif ice.distance(my)<game.ice_troll_attack_range and my_ice_neer_enemy_ice and my_ice_neer_enemy_ice[0] == my:
           count +=1
    return count

#***************************Debug************************************

def debug(game, message):
	if DEBUG:
		game.debug(message)
		
def sortdebug(game,message):
    if DebugSort:
        game.debug(message)
        
def funnydebug(game,massage):
    if DebugForSatla:
        jokes = ["Why dont they play poker in the jungle? Too many cheetahs.",
        "What did the blanket say as it fell off the bed? Oh sheet! ",
        "Why shouldnt you write with a broken pencil? Because its pointless!",
        "What happens when the number is dialed on the phone: 001 Answer: Police arrive in reverse",
        "Once there was 2 Chinese, now there are many",
        "What did the shoelace say to the shoe? Be in touch!!!!!!!!!!!!!!!!!!!!!",
        "Mother told me to follow my dreams, So I went back to bed ...",
        "One vegetarian man went and went went ... Boom corn schnitzel",
        "Roses are Red, Violets are blue Unexpected { on line 32(credit Itay from discord) " ,
        "How do you make an elf escape? Answer: Screaming on the screen (credit zadom from discord)"]
        game.debug("Credits : Shilo , Amit , Shoham :")
        game.debug("Itay the TURTLE --> WE F*CKING LOVE YOU")
        if game.turn < 10 : 
            game.debug("We want to thank God for the ideas - thank God")
            game.debug("aylon from yizhak ben tzvi 1- you are so gever, we love you!!")
            game.debug("hilarious jokes in : " + str(10 - game.turn))
            
        else: 
            game.debug(jokes[game.turn%10])
        if game.get_enemy_castle().current_health < 2:
            game.debug("Its nothing personal kiddo... try again in the next time ")
        
