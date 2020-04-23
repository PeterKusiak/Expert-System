import os
import json
from collections import Counter

with open('KES.json', 'r') as fp:
    heroes = json.load(fp)


def get_hero_human_readable(hero_id):
    for hero in heroes:
        if hero['id'] == hero_id:
            return hero['localized_name']
    return 'Unknown hero: %d' % hero_id


class Engine:
    def __init__(self, algorithm):
        self.algorithm = algorithm

    def recommend(self,my_team, their_team,medal_lvl):
        '''Returns a list of (hero, probablility of winning with hero added) recommended to complete my_team.'''
        my_team = list(my_team)
        their_team = list(their_team)
        
        score = 0.0
        medal_val = 0.0

        medal_team = 0.0
        medal_enemy = 0.0
        
        current_hero_names = []
        
        selection = []
        
        score_absolute  = 10

        for hero_id_team in my_team:
            
            hero_data_team = heroes[hero_id_team - 1]
            
            current_hero_names.append(hero_data_team['localized_name'])
            
            lvl_id = 'L'+str(medal_lvl)
            medal_team += hero_data_team['cat_wins'][lvl_id]

            for hero_id_enemy in their_team:
                hero_data_enemy = heroes[hero_id_enemy - 1]
                
                if hero_data_enemy['localized_name'] not in current_hero_names:
                    current_hero_names.append(hero_data_enemy['localized_name'])
                    
                if hero_data_team['localized_name'] in hero_data_enemy['data']['best_vs']:
                    index_of_hero = hero_data_enemy['data']['best_vs'].index(hero_data_team['localized_name'])
                    score = score - hero_data_enemy['data']['best_vs_advantage'][index_of_hero]
    
                if hero_data_team['localized_name'] in hero_data_enemy['data']['worst_vs']:
                    index_of_hero = hero_data_enemy['data']['worst_vs'].index(hero_data_team['localized_name'])
                    score = score + hero_data_enemy['data']['worst_vs_disadvantage'][index_of_hero]
                    
                
        for hero_id_enemy in their_team:
            
            hero_data_enemy = heroes[hero_id_enemy - 1]
            
            lvl_id = 'L'+str(medal_lvl)
            medal_enemy += hero_data_enemy['cat_wins'][lvl_id]
            

            for i in range(len(hero_data_enemy['data']['worst_vs'])):
                if hero_data_enemy['data']['worst_vs'][i] not in current_hero_names:
                    selection.append((hero_data_enemy['data']['worst_vs'][i],int(hero_data_enemy['data']['worst_vs_disadvantage'][i]*100)))
            
            # printing original list 
        #print("The original list is : " + str(selection) )

        # Aggregate values by tuple keys 
        # using Counter() + generator expression 
        res = list(Counter(key for key, num in selection  
                      for idx in range(num)).items()) 
        
        values_only = [y for x,y in res]
        if len(values_only) > 0:
            score_absolute += max(values_only)
        
        selection = [(round(y / (score_absolute), 2),next((name['id'] for name in heroes if name['localized_name'] == x), None)) for x,y in res]
        
        selection = sorted(selection, key=lambda x: x[0], reverse=True)

        # printing result 
        
        if len(my_team) > 0 and len(their_team) > 0:
            medal_team = medal_team / len(my_team)
            medal_enemy = medal_enemy / len(their_team)
        
            medal_val = medal_team * 100 / (medal_team + medal_enemy)
        
            medal_val = ( medal_val + score ) / 100
        else:
            medal_val = 0.0

        
        if len(selection) > 5:
            selection = selection[:5]
        
        return selection,medal_val