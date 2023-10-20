import semantic_kernel as sk
from semantic_kernel.connectors.ai.hugging_face import HuggingFaceTextCompletion
from semantic_kernel import PromptTemplateConfig, SemanticFunctionConfig, PromptTemplate
import json

from connectors.custom_connect import CuratedTransformersCompletion

##########################  Static variables and directories  ###########################
CONFIG_DIRECTORY = "/home/rohan/qualitas/nlp/config"
#Custom model config params
PARAMS_DIRECTORY = "/home/rohan/qualitas/nlp/connectors"
#####################################################

params = json.load(open(PARAMS_DIRECTORY + "/params.json"))
prompt_config_dict = json.load(open(CONFIG_DIRECTORY + "/capital_config.json"))


# Kernel initialization
kernel = sk.Kernel()
api_key, org_id = sk.openai_settings_from_dot_env()

hf_model = HuggingFaceTextCompletion("gpt2", task="text-generation")
# kernel.add_text_completion_service("hf_gpt2_text_completion", hf_model)
kernel.add_text_completion_service(
    "gpt2_text_completion",
    CuratedTransformersCompletion(model_name=params["model_name"], device=params["device"]),
)

#Creating the semantic function, ready to be regsitered with the kernel
def create_semantic_function_config(prompt_template, prompt_config_dict, kernel):
    prompt_template_config = PromptTemplateConfig.from_dict(prompt_config_dict)
    prompt_template = sk.PromptTemplate(
        template=prompt_template,
        prompt_config=prompt_template_config,
        template_engine=kernel.prompt_template_engine,
    )
    return SemanticFunctionConfig(prompt_template_config, prompt_template)

#Registering the semantic function with the kernel
gpt2_complete = kernel.register_semantic_function(
    skill_name="GPT2Complete",
    function_name="gpt2_complete",
    function_config=create_semantic_function_config(
        "{{$input}} is the capital city of", prompt_config_dict, kernel
    ),
)

custom_gpt2_complete = kernel.register_semantic_function(
    skill_name="gpt2_text_complete",
    function_name="gpt2_complete",
    function_config=create_semantic_function_config(
        "{{$input}} is the capital city of", config_dict, kernel
    ),
)

response = gpt2_complete("Delhi")
print(response)