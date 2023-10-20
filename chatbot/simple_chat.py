import semantic_kernel as sk
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion, OpenAITextCompletion
from semantic_kernel.connectors.ai.hugging_face import HuggingFaceTextCompletion
from semantic_kernel import PromptTemplate, PromptTemplateConfig

import json

#Static variables and directories
SKILL_DIRECTORY = "/home/rohan/qualitas/mircrosoft_sk/semantic-kernel/samples/skills"
CONFIG_DIRECTORY = "/home/rohan/qualitas/nlp/config"

# Kernel initialization
kernel = sk.Kernel()
api_key, org_id = sk.openai_settings_from_dot_env()

# this is the semantic kernel function. It acts as the middleware to user input and the chatbot using the LLM
kernel.add_chat_service("chat-gpt", OpenAIChatCompletion("gpt-3.5-turbo", api_key, org_id))

# MS Semantic Kernel skill import
skill_chat = kernel.import_semantic_skill_from_directory(SKILL_DIRECTORY,"ChatSkill")
get_resp_chat = skill_chat["Chat"]

while True:

    user_input = input("User -> ")

    if(user_input != "text"):
        response = str(get_resp_chat(user_input))

    print("Response -> " + response)
