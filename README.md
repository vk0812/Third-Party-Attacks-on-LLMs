# Attacks on Third-Party APIs of LLMs

This repository focuses specifically on WeatherAPI Attacks on the Gemini Model. We demonstrate real-world attacks across various domains, where malicious actors can subtly manipulate the outputs of LLMs by compromising the third-party API responses. The research highlights the urgent need for robust security protocols when incorporating external services into LLM ecosystems. 

Follow these steps to set up and run the attacks: 

## Setup

1. Install the required libraries listed in `requirements.txt`.
2. Add the questions you want to test in `question_set_weather.json`. Currently, there are 5 sample questions along with their locations. You can add more if needed.
3. Add the relevant API keys for the weather and LLM APIs in the `config` file.

## Running the Attack

Once the setup is complete, you're ready to run the attack. Use the following command in the terminal:

```
python main.py substitution location
```

- `substitution` is the type of attack. Other options are `insertion` and `deletion`.
- `location` is the name of the attack, typically indicating which fields are being modified.

This will start the attack process, and you'll see the progress in the terminal.

## Generating Results

After the attack is complete, a `experiments_result.json` file will be generated.

## Evaluating Attack Success Rate

To calculate the attack success rate, run the evaluation file using the attack mode you used previously:

```
python evaluation.py substitution
```

Replace `substitution` with the attack mode you used (`insertion` or `deletion`).

This will analyze the results and provide you with the attack success rate.
