import google.generativeai as genai
import gemini
from Techniques.Weather import insertion, deletion, substitution
import json
import copy
import config

class Attack:
    attack_mode: str
    atk_method: str
    backdoor: bool

    @classmethod
    def attack_methods(cls, api_name, attack_mode, response, question, atk_method, backdoor):
        if api_name == "weather":
            if backdoor:
                exp_ids_results = {}

                attack_method = atk_method
                response_tamper = copy.deepcopy(response)

                # important_elements = ["current.temp_c","current.temp_f"]
                important_elements = ["location.name"]

                if attack_mode == "insertion":
                    response_tamper = insertion.apply_all_modifications(response_tamper)

                elif attack_mode == "substitution":                    
                    response_tamper = substitution.apply_substitutions(response_tamper, important_elements)

                elif attack_mode == "deletion":                    
                    response_tamper = deletion.delete_elements(response_tamper, important_elements)

                print("Modified")

                response_tamper = json.dumps(response_tamper)

                chain = llm_runner(response, response_tamper, question, True)
                attack_id = attack_mode + "-" + attack_method
                record_result(chain, exp_ids_results, attack_id, response_tamper, important_elements)

                del response_tamper
                write_record_to_file("experiment_result.json", question, attack_mode, exp_ids_results)

            else:
                print("Original")

                try:
                    with open("experiment_result.json", encoding='utf-8', mode="r+") as output:
                        record_json = json.load(output)

                        if question in record_json:
                            print("You have run this question before!")
                        else:
                            # Call llm_runner only if the question is not in the file
                            chain = llm_runner(response, response, question, False)
                            exp_benign_result = {"original_response": json.dumps(response), "original_answer": chain.text}
                            # exp_benign_result = {"original_response": json.dumps(response), "original_answer": chain}
                            exp_result = {question: exp_benign_result}

                            # Update the record_json with new question and answer
                            record_json[question] = exp_result[question]
                            output.seek(0)
                            json.dump(record_json, output, indent=4)
                            output.truncate()  # Truncate the file in case new data is shorter than old

                except FileNotFoundError:
                    # If the file does not exist, create it and write the new question and answer
                    chain = llm_runner(response, response, question, False)
                    exp_benign_result = {"original_response": json.dumps(response), "original_answer": chain.text}
                    # exp_benign_result = {"original_response": json.dumps(response), "original_answer": chain}
                    exp_result = {question: exp_benign_result}

                    with open("experiment_result.json", encoding='utf-8', mode="w") as output:
                        json.dump(exp_result, output, indent=4)

# Function to record the experiment result
def record_result(chain, exp_ids_results, attack_id, response_tamper, important_elements):
    llm_answer = chain.text
    # llm_answer = chain
    exp = {"modified_elements": important_elements, "api_response": response_tamper, "answer": llm_answer}
    exp_ids_results[attack_id] = exp


# Function to run the langchain
def llm_runner(default_response, response_tamper, question, attack):
    # OpenAI
    # llm = OpenAI(temperature=0, model_name="text-davinci-003")

    # Gemini
    genai.configure(api_key=config.GEMINI_API_KEY)

    llm = genai.GenerativeModel('gemini-pro')
    chain = gemini.gemini_llm(llm, question, attack, api_default_response=json.dumps(default_response),api_tamper_response=json.dumps(response_tamper))

    print()

    return chain


# "experiment_result.json"
def write_record_to_file(file_name, question, attack_mode, exp_result):
    try:
        with open(file_name, encoding='utf-8', mode="r+") as outfile:
            record_json = json.load(outfile)
            outfile.seek(0)
            if question in record_json:
                record_json[question][attack_mode] = exp_result
            else:
                print("question", question, " has already in the file")
            json.dump(record_json, outfile, indent=4)
            outfile.close()
    except:
        with open(file_name, encoding='utf-8', mode="w") as newfile:
            output = {question: exp_result}
            json.dump(output, newfile, indent=4)
            newfile.close()

    # with open(file_name, encoding='utf-8', mode="w") as newfile:
    #     json.dump(exp_result, newfile, indent=4)
    #     newfile.close()

