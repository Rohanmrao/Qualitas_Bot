import semantic_kernel as sk
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion, OpenAITextCompletion
from semantic_kernel.connectors.ai.hugging_face import HuggingFaceTextCompletion
from semantic_kernel import PromptTemplate, PromptTemplateConfig

import json

#Static variables and directories
SKILL_DIRECTORY_SK = "/home/rohan/qualitas/mircrosoft_sk/semantic-kernel/samples/skills"


#Static variables and directories
SKILL_DIRECTORY = "/home/rohan/qualitas/mircrosoft_sk/semantic-kernel/samples/skills"
CONFIG_DIRECTORY = "/home/rohan/qualitas/nlp/config"

# Kernel initialization
kernel = sk.Kernel()
api_key, org_id = sk.openai_settings_from_dot_env()

kernel.add_chat_service("chat-gpt", OpenAIChatCompletion("gpt-3.5-turbo", api_key, org_id))
myPlugin = kernel.import_semantic_skill_from_directory("MyPluginsDirectory","AllPlugins")
context = kernel.create_new_context()

context["history"] = ""
context["COMPANY"] = "ABC cookies"
context["COMPANY_PRODUCT"] = "Biscuit packets"
context["CITY"] = "Bengaluru"
context["ISSUES"] = "Some packets have lesser number of biscuits than mentioned on the packet"
context["BUDGET"] = 1000000
context["CURRENCY"] = "INR"

Formulate_Function = myPlugin["FormulatePlugin"]

while True:

    user_input = input("User -> ")

    if(user_input != "text"):
        response = str(Formulate_Function(user_input))

    print("Response -> " + response)
