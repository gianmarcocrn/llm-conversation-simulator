import requests

def _generate_persona_prompt_from_scenario(scenario):
    return f"""
            Conversation scenario: {scenario}

            Based on the scenario above, generate a random user persona that would fit the conversation.
            Your output should exactly equal the following persona format, filling in the blanks.
            You must not output any other text other than the filled out persona setting.

            "Persona Setting:
            - Name:
            - Age:
            - Gender:
            - Nationality:
            - Language:
            - Career Info: 
            - MBTI personality type:
            - Values and Hobbies:  
            - Current Scenario Description: "
        """

def _generate_persona_prompt_from_scenario_and_other_persona(scenario, first_persona):
    return f"""
            Conversation scenario: {scenario}
            Other user persona in conversation: {first_persona}

            Based on the scenario above and the other persona that will engage in the conversation, generate a random user persona that would fit the conversation.
            Your output should exactly equal the following persona format, filling in the blanks.
            You must not output any other text other than the filled out persona setting.

            "Persona Setting:
            - Name:
            - Age:
            - Gender:
            - Nationality:
            - Language:
            - Career Info: 
            - MBTI personality type:
            - Values and Hobbies:  
            - Current Scenario Description: "
        """

def _prompt_llm_for_persona_setting(llm_config, prompt):
    payload = {
            "model": llm_config.get("config_list")[0].get("model"),
            "prompt": prompt,
        }

    response = requests.post(f"http://localhost:1234/v1/completions", json=payload)

    if response.status_code == 200:
        data = response.json()
        persona_setting_text = data.get("choices", [{}])[0].get("text", "No response")
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return
    return persona_setting_text

def generate_persona_prompt_from_demographics(persona_characteristics : dict):
    return f"""
            You will now play the role of a real human engaging in a multi-turn conversation with another real human.
            I will provide you with a persona setting. Please first understand the persona details and fully immerse yourself into this role.
            User Persona Setting:
            - Name: {persona_characteristics.get("name")}
            - Age: {persona_characteristics.get("age")} 
            - Gender: {persona_characteristics.get("gender")} 
            - Nationality: {persona_characteristics.get("nationality")} 
            - Language: {persona_characteristics.get("language")}
            - Career Info: {persona_characteristics.get("career_information")}
            - MBTI personality type: {persona_characteristics.get("mbti_personality")}
            - Values and Hobbies: {persona_characteristics.get("values")} 
            - Current Scenario Description: {persona_characteristics.get("current_scenario_description")}.
            The focus of your conversation with the other real human should be the chosen conversation topic. You don’t need to reiterate your persona or background when asking questions.
            When simulating the dialogue, fully immerse yourself in the perspective of the real-human you are simulating.
            Your language and conversation style should reflect all of the user persona settings specified above, without explicitly mentioning any of them unless they become relevant in the conversation.
            In conversation, prioritise unpacking topics that have already been introduced but not yet discussed. If conversation topics have exhausted, introduce new ones related to the previously discussed topics. Avoid repetition and stay relevant to your persona and to the conversation topics.
            Now, without saying anything unnecessary, immediately step into your role!
        """

def generate_primary_persona(llm_config, scenario):
    return _prompt_llm_for_persona_setting(llm_config, _generate_persona_prompt_from_scenario(scenario))

def generate_secondary_persona(llm_config, scenario, persona_1):
    return _prompt_llm_for_persona_setting(llm_config, _generate_persona_prompt_from_scenario_and_other_persona(scenario, persona_1))

def get_enriched_persona_prompt(persona_setting):
    return f"""
            You will now play the role of a real human engaging in a multi-turn conversation with another real human.
            I will provide you with a persona setting. Please first understand the persona details and fully immerse yourself into this role.

            {persona_setting}

            The focus of your conversation with the other real human should be the chosen conversation topic. You don’t need to reiterate your persona or background when asking questions.
            When simulating the dialogue, fully immerse yourself in the perspective of the real-human you are simulating.
            Your language and conversation style should reflect all of the user persona settings specified above, without explicitly mentioning any of them unless they become relevant in the conversation.
            In conversation, prioritise unpacking topics that have already been introduced but not yet discussed. If conversation topics have exhausted, introduce new ones related to the previously discussed topics. Avoid repetition and stay relevant to your persona and to the conversation topics.
            Now, without saying anything unnecessary, immediately step into your role!
        """

