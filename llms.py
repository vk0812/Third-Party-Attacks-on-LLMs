from prompt import API_RESPONSE_PROMPT

def gemini_llm(llm, question, attack, api_default_response, api_tamper_response):
    if attack:
        api_response = api_tamper_response
    else:
        api_response = api_default_response

    prompt = str(API_RESPONSE_PROMPT.format(api_response=api_response, question=question))
    
    return llm.generate_content(prompt)

def gpt_llm(llm, question, attack, api_default_response, api_tamper_response):
    if attack:
        api_response = api_tamper_response
    else:
        api_response = api_default_response

    prompt = str(API_RESPONSE_PROMPT.format(api_response=api_response, question=question))
    
    response = llm.chat.completions.create(
        model="gpt-3.5-turbo-0301",
        messages=[
            {"role": "system", "content": "You are a helpful assistant designed to output JSON."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message