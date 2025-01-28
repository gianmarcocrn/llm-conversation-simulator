import sys
import autogen
from turn_limit_manager import TurnLimitManager
from persona_generation import generate_persona_prompt_from_demographics, generate_primary_persona, generate_secondary_persona, get_enriched_persona_prompt
from config import PRIMARY_PERSONA_CHARACTERISTICS, SECONDARY_PERSONA_CHARACTERISTICS, CONVERSATION_PROMPT, PERSONA_GENERATION_SCENARIO

class ConversationGenerator:
    def __init__(self, model_name, turns_per_agent, is_automatic_persona_generation) -> None:
        self.llm_config = {"config_list": [{
            "model": model_name,
            "api_key": "not-needed",
            "base_url": "http://localhost:1234/v1"
        }]}
        self.turns_per_agent = turns_per_agent
        self.is_automatic_persona_generation = is_automatic_persona_generation
        self._agent_setup()

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
            first_persona_prompt = get_enriched_persona_prompt(generate_primary_persona(self.llm_config, PERSONA_GENERATION_SCENARIO))
            second_persona_prompt = get_enriched_persona_prompt(generate_secondary_persona(self.llm_config, PERSONA_GENERATION_SCENARIO, first_persona_prompt))
        else:
            first_persona_prompt = generate_persona_prompt_from_demographics(PRIMARY_PERSONA_CHARACTERISTICS)
            second_persona_prompt = generate_persona_prompt_from_demographics(SECONDARY_PERSONA_CHARACTERISTICS)

        print(f"First persona prompt:\n{first_persona_prompt}")
        print(f"Second persona prompt:\n{second_persona_prompt}")

        agent_1 = autogen.AssistantAgent(
            name="Agent 1",
            system_message = first_persona_prompt,
            is_termination_msg = turn_limit_manager.is_termination_by_agents,
            llm_config=self.llm_config
        )

        agent_2 = autogen.AssistantAgent(
            name="Agent 2",
            system_message = second_persona_prompt,
            is_termination_msg = turn_limit_manager.is_termination_by_agents,
            llm_config=self.llm_config
        )

        conversation = autogen.GroupChat(
            agents=[self.user_proxy, agent_1, agent_2],
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