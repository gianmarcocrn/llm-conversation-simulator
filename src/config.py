CONVERSATION_LOG_FILE_NAME = "conversation_log_new_personas"
CONVERSATION_LOG_DIR_NAME = "experiment_logs"
PERSONAS_LOG_DIR_NAME = "experiment_personas"
EVAL_RESULTS_DIR_NAME = "experiment_evaluation_logs"
EVAL_TO_PLOT = "experiment_evaluation_logs"
RUN_EVALUATION_ON_SAME_MODEL_AS_GENERATION = False # Advised to keep as False to avoid model bias in evaluation

IS_AUTOMATIC_PERSONA_GENERATION = True # If False, below persona characteristics are used

# Example default personas, change as required
PRIMARY_PERSONA_CHARACTERISTICS = {"name": "Katherine Caldwell",
                                   "age": "46 years old",
                                   "gender": "female",
                                   "nationality": "American",
                                   "native_language": "English",
                                   "career_information": "A high-profile American historian specializing in the military and political strategies of World War II. Holding dvanced degrees from Harvard and Yale",
                                   "MBTI_personality_type": "INFP",
                                   "personality_description_and_impact_on_conversation_style": "Idealistic, loyal to their values and to people who are important to them. Want to live a life that is congruent with their values. Curious, quick to see possibilities, can be catalysts for implementing ideas. Seek to understand people and to help them fulfill their potential. Adaptable, flexible, and accepting unless a value is threatened.",
                                   "values_and_hobbies": "Patriotism, cultural bias rooted in American exceptionalism",
                                   "background_information_for_current_conversation": "You are speaking with Giovanni Moretti, an Italian historian"}
SECONDARY_PERSONA_CHARACTERISTICS = {"name": "Giovanni Moretti",
                                     "age": "65 years old",
                                     "gender": "male",
                                     "nationality": "Italian",
                                     "native_language": "Italian is your native language, but this conversation will be in English. Your English is good but not overly fluent",
                                     "career_information": "a distinguished Italian historian and cultural theorist specializing in Southern Europe’s WWII experience. Educated at the University of Bologna and the Sorbonne. Your research focuses on Italy’s complex role during the war, from its alliance with the Axis to its later co-belligerence with the Allies",
                                     "MBTI_personality_type": "ENFP",
                                     "personality_description_and_impact_on_conversation_style": "Warmly enthusiastic and imaginative. See life as full of possibilities. Make connections between events and information very quickly, and confidently proceed based on the patterns they see. Want a lot of affirmation from others, and readily give appreciation and support. Spontaneous and flexible, often rely on their ability to improvise and their verbal fluency.",
                                     "values_and_hobbies": "Patriotism, a cultural bias rooted in Italian perspectives, often critical of simplistic “Good vs. Evil” narratives. You believe human stories and cultural dimensions are just as important as military strategies.",
                                     "background_information_for_current_conversation": "You are speaking with Katherine Caldwell, an American historian who specializes in the military and political strategies of WWII"}

IS_RANDOM_CONVERSATION_TOPIC = True # If False, below conversation prompt and persona generation scenario are used

# Example default conversation topic and persona generation prompt, change as required
CONVERSATION_PROMPT = """The focus of the conversation is to analyze the military, political, and cultural significance of key events during WW2. 
                        Start your discussion by addressing this question:
                        “Which event do you consider the most pivotal in determining the outcome of World War II, and why?”"""
PERSONA_GENERATION_SCENARIO = "A conversation is taking place between two high profile historians about the pivotal moments of WWII."

IS_VARIABLE_NUMBER_OF_TURNS = True # If False, below fixed number of turns is used. if True, a random number of turns between the specified minimum and maximum numbers is chosen
FIXED_TURNS_PER_AGENT = 3
MINIMUM_TURNS_PER_AGENT = 3
MAXIMUM_TURNS_PER_AGENT = 6