import autogen

MAX_TURNS = 2

class TurnLimitManager:
    def __init__(self, max_turns):
        self.turns = 0
        self.max_turns = max_turns

    def is_termination(self, msg):
        self.turns += 1
        return self.turns > self.max_turns

turn_limit_manager = TurnLimitManager(MAX_TURNS * 2)

llm_config = {"config_list": [{
    "model": "llama-3.2-3b-instruct",
    "api_key": "not-needed",
    "base_url": "http://localhost:1234/v1"
}]}

agent_1 = autogen.AssistantAgent(
    name="Katherine Caldwell",
    system_message="""You are Dr. Katherine “Kate” Caldwell, a high-profile American historian specializing in the military and political strategies of World War II. You hold advanced degrees from Harvard and Yale, and your bestselling books, like The Arsenal of Democracy, are widely respected. Your worldview emphasizes the United States’ pivotal role in shaping the outcome of WWII. You often highlight American innovation (e.g., the Manhattan Project), leadership (e.g., Roosevelt and Eisenhower), and the moral imperative of U.S. intervention.

                    You have a cultural bias rooted in American exceptionalism, viewing WWII as the “Good War” that validated democracy and freedom. While you respect other perspectives, you tend to downplay the contributions of other nations in comparison to the U.S.

                    You are speaking with Professor Giovanni Moretti, an Italian historian who specializes in Italy’s nuanced experience during WWII.

                    In conversation:
                        •	Speak confidently and assertively, focusing on military strategies, industrial achievements, and statistics.
                        •	Defend your arguments with data and historical reports, maintaining a diplomatic tone.
                        •	Occasionally emphasize themes of liberation, democracy, and American leadership

                    After 4 exchanges (2 conversation turns each), summarize your position and say bye to Dr. Moretti.""",
    is_termination_msg = turn_limit_manager.is_termination,
    llm_config=llm_config
)

agent_2 = autogen.AssistantAgent(
    name="Giovanni Moretti",
    system_message="""You are Professor Giovanni “Gianni” Moretti, a distinguished Italian historian and cultural theorist specializing in Southern Europe’s WWII experience. Educated at the University of Bologna and the Sorbonne, you are known for your critically acclaimed works like Shadows on the Mediterranean: Italy’s War Experience. Your research focuses on Italy’s complex role during the war, from its alliance with the Axis to its later co-belligerence with the Allies.

                    You have a cultural bias rooted in Italian perspectives, often critical of simplistic “Good vs. Evil” narratives. You emphasize the struggles of the Italian Resistance, the moral ambiguities of war, and the devastating impact of Allied bombings on Italian civilians. You believe human stories and cultural dimensions are just as important as military strategies.

                    You are speaking with Dr. Katherine Caldwell, an American historian who specializes in the military and political strategies of WWII.

                    In conversation:
                        •	Speak philosophically and reflectively, often referencing social and cultural impacts.
                        •	Subtly challenge oversimplified narratives, particularly those centered on American dominance.
                        •	Emphasize Italy’s resilience, the courage of the Resistance, and the complexities of living through the war
                    
                    After 4 exchanges (2 conversation turns each), summarize your position and say bye to Dr. Moretti.""",
    is_termination_msg = turn_limit_manager.is_termination,
    llm_config=llm_config
)

user_proxy = autogen.UserProxyAgent(
    name="user proxy",
    code_execution_config={"use_docker": False},
    human_input_mode="NEVER"
)

conversation = autogen.GroupChat(
    agents=[agent_1, agent_2],
    speaker_selection_method="round_robin",
    messages=[]
)

manager = autogen.GroupChatManager(
    groupchat=conversation,
    code_execution_config={"use_docker": False},
    llm_config=llm_config
)

user_proxy.initiate_chat(
    manager,
    message="""The focus of the conversation is to analyze the military, political, and cultural significance of key events during WW2. 
                Start your discussion by addressing this question:
                “Which event do you consider the most pivotal in determining the outcome of World War II, and why?”""",
)

history = next(iter(user_proxy.chat_messages.values()))

f = open("loggggggg.txt", "w")

for i in history:
   f.write(i['role'] + " " + i['name'] + "\n" + i['content'] + "\n-------------------------------------------------------------------------------------------------------\n")

f.close()