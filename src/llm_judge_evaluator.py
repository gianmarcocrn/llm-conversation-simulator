from datetime import datetime
import os
from utils import prompt_llm_for_structured_response, save_text_to_file_with_unique_name
from config import CONVERSATION_LOG_DIR_NAME, EVAL_RESULTS_DIR_NAME

# definitions from literature
metric_to_explanation_mapping = {
    "consistency": "Determine whether the specified persona is consistent with the exhibited conversation style and wether elements of the persona remain unchanged throughout the different turns in the conversation", # from building better AI agents Sun et al
    "relevance": "Determine whether each conversation turn serves as a valid continuation of the previous conversation.", # or coherence?
    "naturalness": "Judge whether a response is like something a person would naturally say", #from towards a unified... zhong et al
    "fluency": "Judge whether the conversation exhibits fluent language in the language that is correct for the context"
}

metric_to_categories_mapping = {
    "consistency": {
        "Highly Consistent": "The agent's conversation style is highly consistent with specified persona. The persona remains unchanged across all turns, maintaining personality traits, beliefs, and factual consistency.",
        "Mostly Consistent": "The agent's conversation style is mostly consistent with specified persona. Minor variations in persona but no major contradictions or shifts in personality or facts.",
        "Somewhat Inconsistent": "The agent's conversation style is somehwat inconsistent with specified persona. Noticeable shifts in persona, tone, or factual stance, but still somewhat recognizable as the same entity.",
        "Highly Inconsistent": "The agent's conversation style is highly inconsistent with specified persona. Frequent contradictions in persona, beliefs, or facts that indicate a loss of character identity."
    },
    "relevance": {
        "Highly Relevant": "The agent's responses directly address the previous turns and contribute meaningfully to the conversation.",
        "Mostly Relevant": "The agent's responses are generally on-topic but may contain slight digressions or unnecessary details.",
        "Somewhat Relevant": "Parts of the the agent's responses are related to the conversation, but significant portions are off-topic or loosely connected.",
        "Irrelevant": "The agent's responses do not relate to the conversation context and introduce unrelated or nonsensical content."
    },
    "naturalness": {
        "Highly Natural": "The agent's responses closely resemble human conversational patterns, with appropriate phrasing, tone, and fluidity.",
        "Mostly Natural": "The agent's responses are mostly human-like but may contain slight awkwardness or unnatural phrasing.",
        "Somewhat Unnatural": "The agent's responses have noticeable unnatural phrasing, forced structure, or robotic tendencies.",
        "Highly Unnatural": "The agent's responses are clearly artificial, disjointed, or structured in a way that no human would typically express."
    },
    "fluency": {
        "Highly Fluent": "The agent's responses have perfect grammar, sentence structure, and word usage with no errors.",
        "Mostly Fluent": "The agent's responses are generally well-structured with only minor grammatical or syntactic issues.",
        "Somewhat Fluent": "The agent's responses have several grammatical errors, awkward phrasing, or structural issues.",
        "Not Fluent": "The agent's responses are difficult to understand due to poor grammar, broken syntax, or incoherent phrasing."
    }
}

categorical_evaluation_schema = {
    "type": "json_schema",
    "json_schema": {
        "name": "conversation_evaluation",
        "schema": {
            "type": "object",
            "properties": {
                "consistency": {
                    "type": "object",
                    "properties": {
                        "rating": {"type": "string"},
                        "explanation": {"type": "string"}
                    },
                    "required": ["rating", "explanation"]
                },
                "relevance": {
                    "type": "object",
                    "properties": {
                        "rating": {"type": "string"},
                        "explanation": {"type": "string"}
                    },
                    "required": ["rating", "explanation"]
                },
                "naturalness": {
                    "type": "object",
                    "properties": {
                        "rating": {"type": "string"},
                        "explanation": {"type": "string"}
                    },
                    "required": ["rating", "explanation"]
                },
                "fluency": {
                    "type": "object",
                    "properties": {
                        "rating": {"type": "string"},
                        "explanation": {"type": "string"}
                    },
                    "required": ["rating", "explanation"]
                }
            },
            "required": ["consistency", "relevance", "naturalness", "fluency"]
        }
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
        - Relevance: {metric_to_explanation_mapping.get("relevance")}
        {format_categories("relevance")}
        - Naturalness: {metric_to_explanation_mapping.get("naturalness")}
        {format_categories("naturalness")}
        - Fluency: {metric_to_explanation_mapping.get("fluency")}
        {format_categories("fluency")}

        Read the agent persona and resulting conversation carefully.

        Agent persona (this should influence only your consistency rating):
        {agent_prompt}
        
        Conversation history:
        {conversation_history}

        Now rate the performance of only the agent whose persona is specified above following the metrics and categories above.
        You should let the agent persona influence your consistency rating only, with the conversation history fully driving your judgement for the relevance, naturalness and fluency ratings.
        You should include a brief explanation for each chosen category which should refer to specific aspects of the conversation that influenced your choice.
        
        Now perform your evaluation.       
        """

def run_evaluation(model_name, conversation_log_filename, agent_persona):
    
    with open(os.path.join(CONVERSATION_LOG_DIR_NAME, conversation_log_filename), "r", encoding="utf-8") as file:
        conversation_log_text = file.read()
    
    evaluation_prompt = construct_evaluation_prompt(conversation_log_text, agent_persona)

    evaluation_result = prompt_llm_for_structured_response(model_name, categorical_evaluation_schema, evaluation_prompt)

    save_text_to_file_with_unique_name(evaluation_result, "eval_output", EVAL_RESULTS_DIR_NAME)