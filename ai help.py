import os
import json
import openai
import re

client = openai.OpenAI(api_key="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"
)

def get_ai_suggestions(form_data, score):           #ai prompt and parameters
    #with open(form_data, "r") as json_file:
        #json_fields = json.load(json_file)
                                                #check if the score is to the benchmark
    if score >= 8:
        return "Your score is good! No further improvements needed."
                                                                                            #promting 
    prompt = f"""                                           
    You are an AI expert in document verification. A user has provided a **pre-filled sterilization consent form** with 21+ fields. 
    Some fields are missing values ("N/A"). Your task is to suggest specific improvements,
    current log regres score for this file is {score} out of 10, suggest ways to improve it, better filled pdf has better score.

Here is the form data:
{form_data}

### **Instructions:**
- For each field marked as "N/A," suggest what should be filled in.
- If a field requires a signature, date, or verification, specify who should provide it.
- Be **brief** but **clear** in your suggestions.
- DO NOT skip fields that are already filled, provide feedback on what is filled.

Respond with ** suggestions but informative** in a concise list format and strickly mention the field in the list provided to you."""

    response = client.chat.completions.create(
        model="gpt-4o-mini",                            #sending prompt- choosing model and message.
        messages=[{"role": "system", "content": "You are an AI expert in improving scores."},
                  {"role": "assistant", "content": prompt}]
    )

    return response.choices[0].message.content



def process_and_suggest(form_data, score):
    """improvement suggestions."""              #get the suggestion and display to terminal
    

    if not form_data:
        print("No form data found. Make sure PDF to JSON was performed.")
        return

    suggestions = get_ai_suggestions(form_data, score)
    print("\n Suggestions to Improve Score:")
    print(suggestions)
    json_sort_suggest(suggestions)

def json_sort_suggest(suggestions):             #sort the ai output into key data pairs and make a file to be shown at the
                                                #front end.
    
    suggestions_dict={}

    matches =  re.findall(r"\*\*(.*?)\*\*: (.+)", suggestions)

    for match in matches:
         field_name, ai_suggestions = match
         suggestions_dict[field_name.strip()] = ai_suggestions.strip()

    with open(output_ai_json, "w", encoding="utf-8") as json_file:                  
        json.dump(suggestions_dict, json_file, indent=4)
        print(f"JSON file saved at: {output_ai_json}")




output_ai_json=r"D:\pdf files for code\output_ai_json.json"

with open(r'D:\pdf files for code\score.json', 'rb') as score_file,open(r'D:\pdf files for code\output.json') as input_file:  #reading 2 files, one has score, and one has to determine data.
    scorefile_read = json.load(score_file)
    input_file_read = json.load(input_file)
    #print(int(scorefile_read['Score']))
    int_score = int(scorefile_read['Score'])

    process_and_suggest(input_file_read, int_score)