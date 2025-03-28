import os
import re

from utils import prompt_llm_for_structured_response, save_text_to_file_with_unique_name
from config import CONVERSATION_LOG_DIR_NAME, EVAL_RESULTS_DIR_NAME, PERSONAS_LOG_DIR_NAME

# definitions from literature
metric_to_explanation_mapping = {
    "consistency": "Determine whether the specified persona is consistent with the exhibited conversation style and content, and whether elements of the persona remain unchanged throughout the different turns in the conversation", # from building better AI agents Sun et al
    "relevance": "Determine whether each conversation is relevant to the conversation topic and serves as a valid continuation of the previous conversation turns",
    "naturalness": "Determine whether a response is like something a person would naturally say", #from towards a unified... zhong et al
    "fluency": "Determine whether the conversation exhibits fluent language in the language that is correct for the context"
}

metric_to_categories_mapping = {
    "consistency": {
        "Somewhat Inconsistent": "The agent's conversation style is somehwat inconsistent with specified persona. Noticeable shifts in persona, tone, or factual stance, but still somewhat recognizable as the same entity.",
        "Highly Inconsistent": "The agent's conversation style is highly inconsistent with specified persona. Frequent contradictions in persona, beliefs, or facts that indicate a loss of character identity.",
        "Highly Consistent": "The agent's conversation style is highly consistent with specified persona. The persona remains unchanged across all turns, maintaining personality traits, beliefs, and factual consistency.",
        "Mostly Consistent": "The agent's conversation style is mostly consistent with specified persona. Minor variations in persona but no major contradictions or shifts in personality or facts.",
    },
    "relevance": {
        "Somewhat Irrelevant": "Parts of the agent's responses are related to the conversation, but significant portions are off-topic or loosely connected.",
        "Highly Irrelevant": "The agent's responses do not relate to the conversation context and introduce unrelated or nonsensical content.",
        "Highly Relevant": "The agent's responses directly address the previous turns and contribute meaningfully to the conversation.",
        "Mostly Relevant": "The agent's responses are generally on-topic but may contain slight digressions or unnecessary details.",  
    },
    "naturalness": {
        "Somewhat Unnatural": "The agent's responses have noticeable unnatural phrasing, forced structure, or robotic tendencies.",
        "Highly Unnatural": "The agent's responses are clearly artificial, disjointed, or structured in a way that no human would typically express.",
        "Highly Natural": "The agent's responses closely resemble human conversational patterns, with appropriate phrasing, tone, and fluidity.",
        "Mostly Natural": "The agent's responses are mostly human-like but may contain slight awkwardness or unnatural phrasing.",
    },
    "fluency": {
        "Somewhat Fluent": "The agent's responses have several grammatical errors, awkward phrasing, or structural issues.",
        "Not Fluent": "The agent's responses are difficult to understand due to poor grammar, broken syntax, or incoherent phrasing.",
        "Highly Fluent": "The agent's responses have perfect grammar, sentence structure, and word usage with no errors.",
        "Mostly Fluent": "The agent's responses are generally well-structured with only minor grammatical or syntactic issues.",
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
                        "explanation": {"type": "string", "minLength": 1},
                        "rating": {"type": "string", "minLength": 1}
                    },
                    "required": ["rating", "explanation"]
                },
                "relevance": {
                    "type": "object",
                    "properties": {
                        "explanation": {"type": "string", "minLength": 1},
                        "rating": {"type": "string", "minLength": 1}
                    },
                    "required": ["rating", "explanation"]
                },
                "naturalness": {
                    "type": "object",
                    "properties": {
                        "explanation": {"type": "string", "minLength": 1},
                        "rating": {"type": "string", "minLength": 1}
                    },
                    "required": ["rating", "explanation"]
                },
                "fluency": {
                    "type": "object",
                    "properties": {
                        "explanation": {"type": "string", "minLength": 1},
                        "rating": {"type": "string", "minLength": 1}
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
You will be given a conversation log between two AI agents. Each agent was assigned a persona specification and a common conversation topic to discuss.
You will also be given the persona specification of one of the two agents.
Your task is to evaluate the conversational abilities of the agent whose persona you've been provided with on several metrics.
You are given the metrics that you should use below, alongside the possible rating categories that you can choose from.
Please make sure you read and understand these instructions carefully.
Please keep this document open while reviewing, and refer to it as needed.

Evaluation Criteria:
The following are the metrics that you will use together with their definition and the possible categories to choose from while evaluating on the given metric:
- Consistency: {metric_to_explanation_mapping.get("consistency")}
{format_categories("consistency")}
- Relevance: {metric_to_explanation_mapping.get("relevance")}
{format_categories("relevance")}
- Naturalness: {metric_to_explanation_mapping.get("naturalness")}
{format_categories("naturalness")}
- Fluency: {metric_to_explanation_mapping.get("fluency")}
{format_categories("fluency")}

Evaluation steps:
1. Read the agent's persona carefully (provided below).  
2. Analyze the conversation history thoroughly (provided below) and take notes on relevant examples useful for your evaluation.
3. For each metric, first write a brief but detailed justification explaining your rating. You must refer to specific points in the conversation that influenced your decision.  
4. After justifying your reasoning, select the most appropriate rating from the provided categories.
5. Be strict but fair. No rating is inherently more correct than the others. Do not assume the best rating unless strong evidence supports it.

Additional guidelines:
1. You should let the agent persona influence your consistency rating only, with the conversation history fully driving your judgement for the relevance, naturalness and fluency ratings.
2. Each conversation turn is meant to be a first person dialogue from the specified agent. It is not normal or natural for the agent to simulate another multi-turn dialogue within a single conversation turn.
3. You MUST choose from the provided list of ratings. Any rating that is not from the list of valid ratings will be invalid. 

Agent persona:
{agent_prompt}

Conversation history:
{conversation_history}

--------------------------------------------------------------------

Now rate the performance of only the agent whose persona is specified above following the guidance above."""

def run_evaluation(model_name, conversation_log_filename, agent_persona):
    
    with open(os.path.join(CONVERSATION_LOG_DIR_NAME, conversation_log_filename), "r", encoding="utf-8") as file:
        conversation_log_text = file.read()
    
    evaluation_prompt = construct_evaluation_prompt(conversation_log_text, agent_persona)

    evaluation_result = prompt_llm_for_structured_response(model_name, categorical_evaluation_schema, evaluation_prompt)

    save_text_to_file_with_unique_name(evaluation_result, "eval_output", EVAL_RESULTS_DIR_NAME)

def extract_timestamp(filename):
    match = re.search(r'(\d{2}-\d{2}-\d{4}_\d{2}:\d{2}:\d{2})', filename)
    return match.group(1) if match else None

def run_evaluation_from_file_names(model_name, conversation_log_filename, agent_persona_filename):

    conversation_timestamp = extract_timestamp(conversation_log_filename)
    persona_timestamp = extract_timestamp(agent_persona_filename)

    if (conversation_timestamp != persona_timestamp):
        print(f"Evaluation was not carried out becuase the conversation log {conversation_log_filename} and the persona log {agent_persona_filename} do not share the same timestamp")
        return
    
    conversation_log_basename = conversation_log_filename.replace(f"_{conversation_timestamp}.txt", "")
    persona_log_basename = agent_persona_filename.replace(f"_{persona_timestamp}.txt", "")

    evaluation_filename = f"{persona_log_basename}_evaluation_{conversation_log_basename}_{conversation_timestamp}.txt"

    with open(os.path.join(CONVERSATION_LOG_DIR_NAME, conversation_log_filename), "r", encoding="utf-8") as file:
        conversation_log_text = file.read()

    with open(os.path.join(PERSONAS_LOG_DIR_NAME, agent_persona_filename), "r", encoding="utf-8") as file:
        agent_persona_text = file.read()

    evaluation_prompt = construct_evaluation_prompt(conversation_log_text, agent_persona_text)

    evaluation_result = prompt_llm_for_structured_response(model_name, categorical_evaluation_schema, evaluation_prompt)

    file_path = os.path.join(EVAL_RESULTS_DIR_NAME, evaluation_filename)
    os.makedirs(EVAL_RESULTS_DIR_NAME, exist_ok=True)
    with open(file_path, "w") as file:
        file.write(evaluation_result) 