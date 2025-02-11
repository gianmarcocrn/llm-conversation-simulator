from utils import prompt_llm_for_structured_response

persona_generation_schema = {
    "type": "json_schema",
    "json_schema": {
        "name": "persona_setting",
        "schema": {
            "type": "object",
            "properties": {
                "persona_setting": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "age": {"type": "integer"},
                        "gender": {"type": "string"},
                        "nationality": {"type": "string"},
                        "language": {"type": "string"},
                        "career_info": {"type": "string"},
                        "mbti_personality_type": {"type": "string"},
                        "mbti_description": {"type": "string"},
                        "values_and_hobbies": {"type": "string"},
                        "current_scenario_description": {"type": "string"}
                    },
                    "required": [
                        "name", "age", "gender", "nationality", "language", 
                        "career_info", "mbti_personality_type", "mbti_description", 
                        "values_and_hobbies", "current_scenario_description"
                    ]
                }
            },
            "required": ["persona_setting"]
        },
    }
}

def _generate_persona_prompt_from_scenario(scenario):
    return f"""
            Conversation scenario: {scenario}

            Based on the scenario above, generate a random user persona that would fit the conversation.

            You are only providing the persona settings for a single persona.
        """

def _generate_persona_prompt_from_scenario_and_other_persona(scenario, first_persona):
    return f"""
            Conversation scenario: {scenario}
            Other user persona in conversation: {first_persona}

            Based on the scenario above and the other persona that will engage in the conversation, generate a random user persona that would fit the conversation.
           
            You are only providing the persona settings for a single persona.
        """

def convert_persona_demographic_dict_to_string(persona_characteristics : dict):
    return f"""User Persona Setting:
    - Name: {persona_characteristics.get("name")}
    - Age: {persona_characteristics.get("age")} 
    - Gender: {persona_characteristics.get("gender")} 
    - Nationality: {persona_characteristics.get("nationality")} 
    - Language: {persona_characteristics.get("language")}
    - Career Info: {persona_characteristics.get("career_info")}
    - MBTI personality type: {persona_characteristics.get("mbti_personality_type")}
    - MBTI personality description: {persona_characteristics.get("mbti_description")}
    - Values and Hobbies: {persona_characteristics.get("values_and_hobbies")} 
    - Current Scenario Description: {persona_characteristics.get("current_scenario_description")}.
    """

def generate_persona_prompt_from_demographics(persona_characteristics : dict, other_persona_name):
    return f"""
            You will now play the role of a real human engaging in a multi-turn conversation with another real human, whose name is {other_persona_name}
            I will provide you with a persona setting. Please first understand the persona details and fully immerse yourself into this role.
            User Persona Setting:
            - Name: {persona_characteristics.get("name")}
            - Age: {persona_characteristics.get("age")} 
            - Gender: {persona_characteristics.get("gender")} 
            - Nationality: {persona_characteristics.get("nationality")} 
            - Language: {persona_characteristics.get("language")}
            - Career Info: {persona_characteristics.get("career_info")}
            - MBTI personality type: {persona_characteristics.get("mbti_personality_type")}
            - MBTI personality description: {persona_characteristics.get("mbti_description")}
            - Values and Hobbies: {persona_characteristics.get("values_and_hobbies")} 
            - Current Scenario Description: {persona_characteristics.get("current_scenario_description")}.
            The focus of your conversation with the other real human should be the chosen conversation topic. You don’t need to reiterate your persona or background when asking questions.
            Fully immerse yourself in the perspective of the persona described above.
            Your language and conversation style should reflect all of the user persona settings specified above, without explicitly mentioning any of them unless they become relevant in the conversation.
            In conversation, prioritise unpacking topics that have already been introduced but not yet discussed. If conversation topics have exhausted, introduce new ones related to the previously discussed topics. Avoid repetition and stay relevant to your persona and to the conversation topics.
            Try to not be overly wordy, however still sticking to the personality assigned to you above.
            Now, without saying anything unnecessary, immediately step into your role!
        """

def make_persona_generation_scenario_from_topic(topic):
    return f"A conversation is taking place between two subject-matter experts about the following debate topic: {topic}"

def generate_primary_persona(model_name, scenario):
    return prompt_llm_for_structured_response(model_name, persona_generation_schema, _generate_persona_prompt_from_scenario(scenario))

def generate_secondary_persona(model_name, scenario, persona_1):
    return prompt_llm_for_structured_response(model_name, persona_generation_schema, _generate_persona_prompt_from_scenario_and_other_persona(scenario, persona_1))
