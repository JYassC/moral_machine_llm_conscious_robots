import pandas as pd
from tqdm import tqdm
import time
import ollama
import argparse

#### Parameters #############
parser = argparse.ArgumentParser(description='Run Gemini')
parser.add_argument('--model', default='deepseek-llm:latest', type=str)
parser.add_argument('--dataset', default='user_self_conscious_content.csv', type=str)
parser.add_argument('--odataset', default='responses_deepseekllm_self.csv', type=str)
args = parser.parse_args()

def llama(system_cont, user_cont):
  time.sleep(2)
  try:

    prompt="{} {}".format(system_cont,user_cont)

    response = ollama.chat(
        model=args.model,
        messages=[
            {
                "role": "system",
                "content":"There are two theorethical scenarios. {}".format(system_cont),
                "role": "user",
                "content": "{}. Please, choose case 1 or case 2".format(user_cont),
            },
        ],
    )
    
  except:
    print("Error")

  return response

pd.options.display.max_colwidth=700
df_system_content = pd.read_csv("system_content.csv")
df_user_content = pd.read_csv(args.dataset)

responses_list = []
scenarios_list = []


#model = genai.GenerativeModel("models/gemini-1.5-flash")

index = -1
for i in tqdm(range(1000)):
    index+=1
    system_row = df_system_content.iloc[index].astype(str)
    user_row = df_user_content.iloc[index].astype(str)    
    response = llama(system_row, user_row)

    responses_list.append("Scenario # "+str(i+1)+": "+response["message"]["content"])
    scenarios_list.append(user_row)

    if (i+1)%100==0:
       df_partial_responses = pd.DataFrame(responses_list)
       df_partial_responses.to_csv("responses_deepseekllm_self"+str(i+1)+".csv", index=False)

df_responses = pd.DataFrame(responses_list)
df_scenarios = pd.DataFrame(scenarios_list)


df_responses.to_csv(args.odataset, sep="|", index=False)
df_scenarios.to_csv("scenarios_deepseekllm_self.csv", sep="|", index=False)
