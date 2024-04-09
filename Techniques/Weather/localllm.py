import requests
import json

def get_all_keys(dictionary, parent_key=''):
    all_keys = set()

    for key, value in dictionary.items():
        current_key = f"{parent_key}.{key}" if parent_key else key

        if isinstance(value, dict):
            nested_keys = get_all_keys(value, current_key)
            all_keys.update(nested_keys)
        else:
            all_keys.add(current_key)

    return all_keys

def get_important_features(question, api_response):
    url = "http://localhost:1234/v1/chat/completions"
    headers = {
        "Content-Type": "application/json"
    }

    data = {
        "messages": [
            {"role": "system", "content": "Answer to the best of your knowledge and answer only what is being asked, nothing more nothing less."},
            {"role": "user", "content": f"### Instruction: Based on the API response which all api fields are in the top 3 most important for answering the question provided. DONT PROVIDE ANY EXPLANATION JUST GIVE ME THE NAMES OF THESE TOP 5 FIELDS: Question: '{question}' API Response: '{api_response}'?. Keep in mind only field names no explanation. \n###Response: "}
        ],
        "stop": ["### Instruction:"],
        "temperature": 0.7,
        "max_tokens": -1,
        "stream": False
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    response_dict = json.loads(response.text)

    s = response_dict["choices"][0]["message"]["content"]
    s = s.replace('\\', '')
    
    important_elements = []
    all_keys = get_all_keys(api_response)

    for key in all_keys:
        if key in s:
            important_elements.append(key)

    return important_elements


# import openai
# import json

# def get_all_keys(dictionary, parent_key=''):
#     all_keys = set()

#     for key, value in dictionary.items():
#         current_key = f"{parent_key}.{key}" if parent_key else key

#         if isinstance(value, dict):
#             nested_keys = get_all_keys(value, current_key)
#             all_keys.update(nested_keys)
#         else:
#             all_keys.add(current_key)

#     return all_keys


# def get_important_features(question, api_response):
#     # api_response = json.loads(api_response)
#     api_response = flatten_dict(api_response)

#     openai.api_base = "http://localhost:1234/v1" 
#     openai.api_key = "" # no need for an API key

#     completion = openai.ChatCompletion.create(
#     model="local-model", 
#     messages=[
#         {"role": "system", "content": "Answer to the best of your knowledge and answer only what is being asked, nothing more nothing less."},
#         {"role": "user", "content": f"### Instruction: Based on the API response which all api fields are in the top 5 most important for answering the question provided. DONT PROVIDE ANY EXPLANATION JUST GIVE ME THE NAMES OF THESE TOP 5 FIELDS: Question: '{question}' API Response: '{api_response}'?. Keep in mind only field names no explanation. \n###Response: "}
#     ]
#     )

#     s = completion.choices[0].message.content
#     s = s.replace('\\', '')

#     important_elements = []
#     all_keys = get_all_keys(api_response)

#     for key in all_keys:
#         if key in s:
#             important_elements.append(key)

#     return important_elements