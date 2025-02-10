import sys
import autogen
import json

from turn_limit_manager import TurnLimitManager
from persona_generation import convert_persona_demographic_dict_to_string, generate_persona_prompt_from_demographics, generate_primary_persona, generate_secondary_persona
from config import PRIMARY_PERSONA_CHARACTERISTICS, SECONDARY_PERSONA_CHARACTERISTICS, CONVERSATION_PROMPT, PERSONA_GENERATION_SCENARIO

class ConversationGenerator:
    def __init__(self, model_name, turns_per_agent, is_automatic_persona_generation) -> None:
        self.llm_config = {"config_list": [{
            "model": model_name,
            "api_key": "not-needed",
            "base_url": "http://localhost:1234/v1"
        }]}
        self.model_name = model_name
        self.turns_per_agent = turns_per_agent
        self.is_automatic_persona_generation = is_automatic_persona_generation
        self._agent_setup()
    
    def get_first_persona_setting(self):
        return self.first_persona_setting

    def get_second_persona_setting(self):
        return self.second_persona_setting

    def _agent_setup(self):
        self.user_proxy = autogen.UserProxyAgent(
            name="user proxy",
            code_execution_config={"use_docker": False},
            human_input_mode="NEVER",
            default_auto_reply="Keep the conversation going. Prioritise unpacking topics that have already been introduced but not yet discussed. If conversation topics have exhausted, introduce new ones related to the previously discussed topics. Avoid repetition and stay relevant to your persona and to the conversation topics"
        )

        turn_limit_manager = TurnLimitManager(self.turns_per_agent * 2, self.user_proxy)

        if (self.is_automatic_persona_generation):
            print("Generating Persona Prompts...")

        first_persona_characteristics = json.loads(generate_primary_persona(self.model_name, PERSONA_GENERATION_SCENARIO)).get("persona_setting") if self.is_automatic_persona_generation else PRIMARY_PERSONA_CHARACTERISTICS
        print(f"First persona setting dictionary:\n{first_persona_characteristics}")
        self.first_persona_setting = convert_persona_demographic_dict_to_string(first_persona_characteristics)

        second_persona_characteristics = json.loads(generate_secondary_persona(self.model_name, PERSONA_GENERATION_SCENARIO, self.first_persona_setting)).get("persona_setting") if self.is_automatic_persona_generation else SECONDARY_PERSONA_CHARACTERISTICS
        print(f"Second persona setting:\n{second_persona_characteristics}")
        self.second_persona_setting = convert_persona_demographic_dict_to_string(second_persona_characteristics)

        first_persona_prompt = generate_persona_prompt_from_demographics(first_persona_characteristics, second_persona_characteristics.get("name"))
        second_persona_prompt = generate_persona_prompt_from_demographics(second_persona_characteristics, first_persona_characteristics.get("name"))

        agent_1 = autogen.AssistantAgent(
            name=first_persona_characteristics.get("name"),
            system_message = first_persona_prompt,
            is_termination_msg = turn_limit_manager.is_termination_by_agents,
            llm_config=self.llm_config
        )

        agent_2 = autogen.AssistantAgent(
            name=second_persona_characteristics.get("name"),
            system_message = second_persona_prompt,
            is_termination_msg = turn_limit_manager.is_termination_by_agents,
            llm_config=self.llm_config
        )

        conversation = autogen.GroupChat(
            agents=[self.user_proxy, agent_2, agent_1],
            speaker_selection_method="round_robin",
            messages=[],
            max_round = sys.maxsize
        )

        self.manager = autogen.GroupChatManager(
            groupchat=conversation,
            code_execution_config={"use_docker": False},
            llm_config=self.llm_config
        )


    def initiate_conversation(self):
        self.user_proxy.initiate_chat(
            self.manager,
            message = CONVERSATION_PROMPT,
        )
    
    def generate_conversation_history(self):
        return next(iter(self.user_proxy.chat_messages.values()))