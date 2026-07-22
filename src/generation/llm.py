import time
import requests
import logging


logger = logging.getLogger("AeroGrid_LLM")


class LocalLLM:

    def __init__(
        self,
        model="phi3",
        endpoint="http://localhost:11434/api/generate"
    ):
        self.model = model
        self.endpoint = endpoint


    def generate(self, prompt: str) -> str:

        start_time = time.time()

        try:

            response = requests.post(
                self.endpoint,
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False
                },
                timeout=45
            )

            response.raise_for_status()

            output = response.json().get(
                "response",
                "No response generated."
            )

            latency = round(
                time.time() - start_time,
                2
            )

            logger.info(
                f"LLM generation completed in {latency}s"
            )

            return output


        except requests.Timeout:

            logger.error(
                "LLM request timeout"
            )

            return "LLM_TIMEOUT"


        except Exception as e:

            logger.exception(e)

            return "LLM_ERROR"


