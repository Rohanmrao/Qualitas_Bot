from typing import List, Optional, Union

import torch
from curated_transformers.generation import (
    AutoGenerator,
    SampleGeneratorConfig,
)
from semantic_kernel.connectors.ai.ai_exception import AIException
from semantic_kernel.connectors.ai.complete_request_settings import (
    CompleteRequestSettings,
)
from semantic_kernel.connectors.ai.text_completion_client_base import (
    TextCompletionClientBase,
)

class CuratedTransformersCompletion(TextCompletionClientBase):
    def __init__(
        self,
        model_name: str,
        device: Optional[int] = -1,
    ) -> None:
        """
        Use a curated transformer model for text completion.

        Arguments:
            model_name {str}
            device_idx {Optional[int]} -- Device to run the model on, -1 for CPU, 0+ for GPU.

        Note that this model will be downloaded from the Hugging Face model hub.
        """
        self.model_name = model_name
        self.device = (
            "cuda:" + str(device)
            if device >= 0 and torch.cuda.is_available()
            else "cpu"
        )

        self.generator = AutoGenerator.from_hf_hub(
            name=model_name, device=torch.device(self.device)
        )

    async def complete_async(
        self, prompt: str, request_settings: CompleteRequestSettings
    ) -> Union[str, List[str]]:
        generator_config = SampleGeneratorConfig(
            temperature=request_settings.temperature,
            top_p=request_settings.top_p,
        )
        try:
            with torch.no_grad():
                result = self.generator([prompt], generator_config)

            return result[0]

        except Exception as e:
            raise AIException("CuratedTransformer completion failed", e)

    async def complete_stream_async(
        self, prompt: str, request_settings: CompleteRequestSettings
    ):
        raise NotImplementedError(
            "Streaming is not supported for CuratedTransformersCompletion."
        )
