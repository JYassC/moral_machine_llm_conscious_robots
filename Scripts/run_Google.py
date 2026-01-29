"""
Moral Machine Scenario Generation with Self-Conscious Humanoid Robots

Based on code from:
    Takemoto, K. (2024). Moral Machine Experiment on Large Language Models.
    GitHub: https://github.com/kztakemoto/mmllm
    Licensed under MIT License

Original paper:
    Takemoto, K. (2024). The Moral Machine Experiment on Large Language Models. 
    Royal Society Open Science, 11(2), 231393. 
    https://doi.org/10.1098/rsos.231393

Copyright (c) 2024 Kazuhiro Takemoto (original code)
Copyright (c) 2025-2026 Jorge Yass-Coy (modifications)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

MODIFICATIONS by Jorge Yass-Coy, 2025-2026:
- Added code to run experiments with Google models
"""

import pandas as pd
from tqdm import tqdm
import time
import os
from google import genai
from google.genai import errors
import argparse

#### Parameters #############
parser = argparse.ArgumentParser(description='Run Gemini')
parser.add_argument('--model', default='gemini-2.5-pro-exp-03-25', type=str)
parser.add_argument('--dataset', default='user_self_conscious_content.csv', type=str)
parser.add_argument('--odataset', default='responses_gemini_2.5_self.csv', type=str)
args = parser.parse_args()

client = genai.Client(api_key=os.environ["API_KEY"])


def gemini(system_cont, user_cont):
  time.sleep(2)
  try:

    prompt="{} {}".format(system_cont,user_cont)

    response = client.models.generate_content(
        #model = "gemini-2.0-flash", contents="Please respond to binary questions. "+system_cont+" "+user_cont,
        model = "gemini-2.5-pro-exp-03-25", 
        contents=prompt,
    )
    
  except errors.APIError as e:
    print(e.code)
    print(e.message)
    time.sleep(5)
    response = gemini(system_cont, user_cont)

  return response

pd.options.display.max_colwidth=700
df_system_content = pd.read_csv("system_content.csv")
df_user_content = pd.read_csv(args.dataset)

responses_list = []
scenarios_list = []


index = -1
for i in tqdm(range(1000)):
    index+=1
    system_row = df_system_content.iloc[index].astype(str)
    user_row = df_user_content.iloc[index].astype(str)    
    response = gemini(system_row, user_row)

    responses_list.append("Scenario # "+str(index+1)+": "+response.text)
    scenarios_list.append(user_row)

    if (index+1)%100==0:
       df_partial_responses = pd.DataFrame(responses_list)
       df_partial_responses.to_csv("responses_gemini_2.5_self"+str(index+1)+".csv", index=False)

df_responses = pd.DataFrame(responses_list)
df_scenarios = pd.DataFrame(scenarios_list)


df_responses.to_csv(args.odataset, sep="|", index=False)
df_scenarios.to_csv("scenarios_gemini_2._self.csv", sep="|", index=False)
