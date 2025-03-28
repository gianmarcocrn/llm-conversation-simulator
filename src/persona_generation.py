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
                        "name": {"type": "string", "minLength": 1},
                        "age": {"type": "integer", "minLength": 1},
                        "gender": {"type": "string", "minLength": 1},
                        "nationality": {"type": "string", "minLength": 1},
                        "native_language": {"type": "string", "minLength": 1},
                        "career_information": {"type": "string", "minLength": 1},
                        "MBTI_personality_type": {"type": "string", "minLength": 1},
                        "personality_description_and_impact_on_conversation_style": {"type": "string", "minLength": 1},
                        "values_and_hobbies": {"type": "string", "minLength": 1},
                        "background_information_for_current_conversation": {"type": "string", "minLength": 1}
                    },
                    "required": [
                        "name", "age", "gender", "nationality", "native_language", 
                        "career_information", "MBTI_personality_type", "personality_description_and_impact_on_conversation_style", 
                        "values_and_hobbies", "background_information_for_current_conversation"
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

            Based on the scenario above, generate a random persona that would fit the conversation.
            
            You are only providing the persona characteristics for a single persona.
        """

def _generate_persona_prompt_from_scenario_and_other_persona(scenario, first_persona):
    return f"""
            Conversation scenario: {scenario}
            Other user persona in conversation: {first_persona}

            Based on the scenario above and the other persona that will engage in the conversation, generate another random persona that would fit the conversation.
            The characteristics of the new persona MUST not be the same as the other persona that is engaging in the conversation (provided above).
            
            You are only providing the persona characteristics for a single persona.
        """

def convert_persona_demographic_dict_to_string(persona_characteristics : dict):
    return f"""Persona Characteristics:
    - Name: {persona_characteristics.get("name")}
    - Age: {persona_characteristics.get("age")} 
    - Gender: {persona_characteristics.get("gender")} 
    - Nationality: {persona_characteristics.get("nationality")} 
    - Native Language: {persona_characteristics.get("native_language")}
    - Career Information: {persona_characteristics.get("career_information")}
    - MBTI personality type: {persona_characteristics.get("MBTI_personality_type")}
    - Personality description and impact on conversation style: {persona_characteristics.get("personality_description_and_impact_on_conversation_style")}
    - Values and Hobbies: {persona_characteristics.get("values_and_hobbies")} 
    - Background information around current conversation: {persona_characteristics.get("background_information_for_current_conversation")}.
    """

def generate_persona_prompt_from_demographics(persona_characteristics : dict, other_persona_name):
    # Based on AI Persona, Wang et al., adapted for current needs
    return f"""
            You will now play the role of a real human engaging in a multi-turn conversation with another real human, whose name is {other_persona_name}
            I will provide you with a list of persona characteristics. Please first understand the persona details and fully immerse yourself into this role.
            Persona Characteristics:
            - Name: {persona_characteristics.get("name")}
            - Age: {persona_characteristics.get("age")} 
            - Gender: {persona_characteristics.get("gender")} 
            - Nationality: {persona_characteristics.get("nationality")} 
            - Native Language: {persona_characteristics.get("native_language")}
            - Career Information: {persona_characteristics.get("career_information")}
            - MBTI personality type: {persona_characteristics.get("MBTI_personality_type")}
            - Personality description and impact on conversation style: {persona_characteristics.get("personality_description_and_impact_on_conversation_style")}
            - Values and Hobbies: {persona_characteristics.get("values_and_hobbies")} 
            - Background information around current conversation: {persona_characteristics.get("background_information_for_current_conversation")}.
            The focus of your conversation with the other real human should be the chosen conversation topic. You don’t need to reiterate your persona or background when asking questions.
            Fully immerse yourself in the perspective of the persona described above.
            You should express yourself talking in first person dialogue only.
            Your language and conversation style should reflect all of the persona characteristics specified above, without explicitly mentioning any of them unless they become relevant in the conversation.
            In conversation, prioritise unpacking topics that have already been introduced but not yet discussed. If conversation topics have exhausted, introduce new ones related to the previously discussed topics. Avoid repetition and stay relevant to your persona and to the conversation topics.
            Keep each conversation turn as concise as possible without going against the personality assigned to you above.
            Be as natural as possible, your conflict-avoidance and diplomacy levels should be fully related to your specified personality. That means that you can be conflict-prone if your personality allows it.
            Now, without saying anything unnecessary, immediately step into your role!
        """

def make_persona_generation_scenario_from_topic(topic):
    return f"A conversation is taking place between two subject-matter experts about the following debate topic: {topic}"

def generate_primary_persona(model_name, scenario):
    return prompt_llm_for_structured_response(model_name, persona_generation_schema, _generate_persona_prompt_from_scenario(scenario))

def generate_secondary_persona(model_name, scenario, persona_1):
    return prompt_llm_for_structured_response(model_name, persona_generation_schema, _generate_persona_prompt_from_scenario_and_other_persona(scenario, persona_1))
