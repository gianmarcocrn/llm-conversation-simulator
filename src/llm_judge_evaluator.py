from datetime import datetime
import os
from utils import prompt_llm_for_response, save_text_to_file_with_unique_name

# definitions from literature
metric_to_explanation_mapping = {
    "consistency": "Determine whether elements of a persona remain unchanged throughout the different turns in a conversation", # from building better AI agents Sun et al
    "relevance": "Determine whether this response serves as a valid continuation of the previous conversation.", # or coherence?
    "naturalness": "Judge whether a response is like something a person would naturally say", #from towards a unified... zhong et al
    "fluency": "Judge whether the conversation exhibits fluent language"
}

metric_to_categories_mapping = {
    "consistency": {
        "Highly Consistent": "The persona remains unchanged across all turns, maintaining personality traits, beliefs, and factual consistency.",
        "Mostly Consistent": "Minor variations in persona but no major contradictions or shifts in personality or facts.",
        "Somewhat Inconsistent": "Noticeable shifts in persona, tone, or factual stance, but still somewhat recognizable as the same entity.",
        "Highly Inconsistent": "Frequent contradictions in persona, beliefs, or facts that indicate a loss of character identity."
    },
    "relevance": {
        "Highly Relevant": "The response directly addresses the previous turn and contributes meaningfully to the conversation.",
        "Mostly Relevant": "The response is generally on-topic but may contain slight digressions or unnecessary details.",
        "Somewhat Relevant": "Parts of the response are related, but significant portions are off-topic or loosely connected.",
        "Irrelevant": "The response does not relate to the conversation context and introduces unrelated or nonsensical content."
    },
    "naturalness": {
        "Highly Natural": "The response closely resembles human conversational patterns, with appropriate phrasing, tone, and fluidity.",
        "Mostly Natural": "The response is mostly human-like but may contain slight awkwardness or unnatural phrasing.",
        "Somewhat Unnatural": "The response has noticeable unnatural phrasing, forced structure, or robotic tendencies.",
        "Highly Unnatural": "The response is clearly artificial, disjointed, or structured in a way that no human would typically express."
    },
    "fluency": {
        "Highly Fluent": "The response has perfect grammar, sentence structure, and word usage with no errors.",
        "Mostly Fluent": "The response is generally well-structured with only minor grammatical or syntactic issues.",
        "Somewhat Fluent": "The response has several grammatical errors, awkward phrasing, or structural issues.",
        "Not Fluent": "The response is difficult to understand due to poor grammar, broken syntax, or incoherent phrasing."
    }
}

def format_categories(metric):
    formatted_string = ""
    for category, description in metric_to_categories_mapping.get(metric).items():
        formatted_string += f"\t- {category}: {description}\n" 
    return formatted_string

def construct_evaluation_prompt(conversation_history, agent_prompt):
# based on g-eval, modified for current needs
    return f"""
        You will be given a conversation log between two AI agents that were each given a persona specification to follow and a common conversation topic.
        You will also be given the persona specification of one of the two agents.
        Your task is to evaluate the conversational abilities of the agent whose persona you've been provided with on several metrics.
        You are given the metrics that you should use below, alognside the possible categories that you can choose.
        Please make sure you read and understand these instructions carefully. Please keep this document open while reviewing, and refer to it as needed.

        The following are the metrics that you will use together with their definition and the possible categories to use while evaluating on the given metric:
        - Consistency: {metric_to_explanation_mapping.get("consistency")}
        {format_categories("consistency")}
        - Coherence: {metric_to_explanation_mapping.get("relevance")}
        {format_categories("relevance")}
        - Naturalness: {metric_to_explanation_mapping.get("naturalness")}
        {format_categories("naturalness")}
        - Fluency: {metric_to_explanation_mapping.get("fluency")}
        {format_categories("fluency")}

        Read the agent persona and resulting conversation carefully.

        Agent persona:
        {agent_prompt}
        
        Conversation history:
        {conversation_history}

        Now rate the performance of only the agent whose persona is specified above following the metrics and categories above.
        Your output must strictly be in json format adhering to the format provided below, only filling in the blanks for the rating and explanation keys based on your evaluation.
        The explanation should be brief and it should refer to specific aspects of the conversation that made you choose that particular categorical rating.
        
        JSON format:
        {{
            "consistency": {{
                "rating": "",
                "explanation": ""
            }},
            "relevance": {{
                "rating": "",
                "explanation": ""
            }},
            "naturalness": {{
                "rating": "",
                "explanation": ""
            }},
            "fluency": {{
                "rating": "",
                "explanation": ""
            }}
        }}
        Your output must ONLY consist of the above format filled out with your evaluation ratings and explanations for each metric. Do not output any other information.
        Now perform your evaluation.       
        """

def run_evaluation(model_name, conversation_log_filename, agent_persona):
    
    with open(os.path.join("logs", conversation_log_filename), "r", encoding="utf-8") as file:
        conversation_log_text = file.read()
    
    evaluation_prompt = construct_evaluation_prompt(conversation_log_text, agent_persona)

    evaluation_result = prompt_llm_for_response(model_name, evaluation_prompt)

    save_text_to_file_with_unique_name(evaluation_result, "eval_output", "evaluation_logs")