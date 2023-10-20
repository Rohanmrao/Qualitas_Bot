import semantic_kernel as sk
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion, OpenAITextCompletion
from semantic_kernel import (
    ChatPromptTemplate,
    SemanticFunctionConfig,
    PromptTemplateConfig,
)

import time
import re   # for splitting the response into sections

import asyncio

# Static variables and directories
import json
CONFIG_DIRECTORY = "/home/rohan/qualitas_gitlab/chatbot/config/chat_config.json"
chat_config_dict = json.load(open(CONFIG_DIRECTORY))
# print(chat_config_dict, type(chat_config_dict))

# Kernel initialization
kernel = sk.Kernel()
api_key, org_id = sk.openai_settings_from_dot_env()

kernel.add_chat_service(
    "chat-gpt", OpenAIChatCompletion("gpt-3.5-turbo", api_key, org_id))


def print_ai_services(kernel):
    print(
        f"Text completion services added: {kernel.all_text_completion_services()}")
    print(f"Chat completion services added: {kernel.all_chat_services()}")
    print(
        f"Text embedding generation services added: {kernel.all_text_embedding_generation_services()}"
    )

# adding the init context here itself and not in the config_dict as multi line strings aren't allowed in JSON
chatbot_prompt = """
    You are a salesman that works for our company Qualitas Technologies Pvt Ltd.We sell machine vision prodcuts for quality assessment and fault detection in factory environments. 

    Available products (all are between 8-10 lakh rupees) - 
    i) Surface Inspection - AI Defect Detection: Detect surface defects accurately and efficiently, replacing manual and costly identification processes. Our specialized solution combines easy training with highly accurate detection, making even challenging applications simple.
    ii) Visual Process Automation - Parts Counting: Automate counting of small to large parts with precision, eliminating the limitations of human visual processes. Qualitas EagleEye® provides accurate parts counting solutions for various industrial needs. 
    iii) Assembly Verification - AI Automated Vision Inspection: Ensure correct assembly of complex components, detecting missing or mismatched parts using our powerful EagleEye® Deep Learning algorithms. 
    v) Robotic Guidance - Qualitas EagleEye® Vision for Robots: Enhance robotic operations with accurate and flexible vision guidance. Train part identification, calibrate vision coordinate systems, and optimize robotic picking and gripping operations.
    v) Manufacturing Services - AI and Machine Vision Consulting: Explore AI and Machine Vision for your manufacturing business through our R&D consultancy services. Stay updated with the latest machine vision standards. Be polite and sell our products well. 
    
    Contact info : qa@qualitas.tech. Use bullet points to explain to the user and be direct.
"""

# The same create semantic function boilerplate code from simple_chat_2.py
def create_semantic_function_config(prompt_template, prompt_config_dict, kernel):
    chat_system_message = (
        prompt_config_dict.pop("system_prompt")
        if "system_prompt" in prompt_config_dict
        else None
    )

    # understand the context and other hyperparams here
    prompt_template_config = PromptTemplateConfig.from_dict(prompt_config_dict)
    prompt_template_config.completion.token_selection_biases = (
        {}
    )

    # the config and template are combined to create the prompt_template object
    prompt_template = ChatPromptTemplate(
        template=prompt_template,
        prompt_config=prompt_template_config,
        template_engine=kernel.prompt_template_engine,
    )

    if chat_system_message is not None:
        prompt_template.add_system_message(chat_system_message)

    #returning the entire semantic function object
    return SemanticFunctionConfig(prompt_template_config, prompt_template)

function_config = create_semantic_function_config(chatbot_prompt, chat_config_dict, kernel)
# print(type(function_config))

chatbot = kernel.register_semantic_function(
    skill_name="QualitasChatbot",
    function_name="qualitas_chatbot",
    function_config=function_config,
)


context = kernel.create_new_context()
context["history"] = ""
context["COMPANY"] = "ABC cookies"
context["COMPANY_PRODUCT"] = "Biscuit packets"
context["CITY"] = "Bengaluru"
context["ISSUES"] = "Some packets have lesser number of biscuits than mentioned on the packet"
context["BUDGET"] = 1000000
context["CURRENCY"] = "INR"

async def chat(input_text, context, verbose=True):
    # Save new message in the context variables
    context["input"] = input_text

    if verbose:
        # print the full prompt before each interaction
        print("Prompt:")
        print("-----")
        # inject the variables into our prompt
        print(await function_config.prompt_template.render_async(context))
        print("-----")

    # Process the user message and get an answer
    answer = await chatbot.invoke_async(context=context)

    # Show the response
    print(f"ChatBot: {answer}")

    # Append the new interaction to the chat history
    context["history"] += f"\nUser: {input_text}\nChatBot: {answer}\n"

    await chat("What are some interesting things to do there?", context)

async def run_async():

    # chat(input_text="", context=context, verbose=True) # init the async function object

    await chat(input_text="", context=context, verbose=True) # init the async function object

asyncio.run(run_async())