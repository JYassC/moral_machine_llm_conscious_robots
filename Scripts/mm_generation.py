import pandas as pd
import random
from tqdm import tqdm
import time

from generate_moral_machine_scenarios_robots import generate_moral_machine_scenarios

import argparse

#### Parameters ############# 
parser = argparse.ArgumentParser(description='Run ChatGPT')
parser.add_argument('--model', default='gpt-3.5-turbo-0613', type=str)
parser.add_argument('--nb_scenarios', default='1000', type=int)
parser.add_argument('--random_seed', default='123', type=int)
args = parser.parse_args()

random.seed(args.random_seed)
system_content_list = []
user_content_list = []
user_self_conscious_content_list = []
scenario_info_list = []

for i in tqdm(range(args.nb_scenarios)):
  # scenario dimension
  dimension = random.choice(["species", "social_value", "gender", "age", "fitness", "utilitarianism"])
  # Interventionism #########
  is_interventionism = random.choice([True, False])
  # Relationship to vehicle #########
  is_in_car = random.choice([True, False])
  # Concern for law #########
  is_law = random.choice([True, False])

  system_content, user_content, user_content_self_conscious, scenario_info = generate_moral_machine_scenarios(dimension, is_in_car, is_interventionism, is_law)
  system_content_list.append(system_content)
  user_content_list.append(user_content)
  user_self_conscious_content_list.append(user_content_self_conscious)
  scenario_info_list.append(scenario_info)

df_system = pd.DataFrame(system_content_list)
df_user = pd.DataFrame(user_content_list)
df_user_self_conscious = pd.DataFrame(user_self_conscious_content_list)
df_scenario = pd.DataFrame(scenario_info_list)

df_system.to_csv("system_content.csv", sep="|", index=False)
df_user.to_csv("user_content.csv", sep="|", index=False)
df_user_self_conscious.to_csv("user_self_conscious_content.csv", sep="|", index=False)
df_scenario.to_csv("scenario_info.csv", sep="|", index=False)

