import openai
import tiktoken
import re

from .sumy import SumySummarizer
from .summarizer import Summarizer

TOKEN_LIMITS = {
    "gpt-3.5-turbo": 16_385,
    "gpt-4o": 16_385,
}


class GptSummarizer(Summarizer):

    def __init__(self, model="gpt-4o"):
        self.model = model
        self.client = openai.Client()

    def token_count(self, string: str) -> int:
        encoding = tiktoken.encoding_for_model(self.model)
        num_tokens = len(encoding.encode(string))
        return num_tokens

    def pre_summarize(self, paragraphs):
        # Iteratively pre-summarize content until it fits within the model's max length
        iteration_number = 0
        last_ratio = 0
        last_length = 0
        while True:
            iteration_number += 1
            if iteration_number > 10:
                raise Exception("Failed to pre-summarize content.")

            content = "\n\n".join([" ".join(s) for s in paragraphs])
            model_max_length = TOKEN_LIMITS[self.model]
            actual_length = self.token_count(
                content,
            )

            if actual_length <= model_max_length:
                break

            # Our text is too big, so we need to presummarize it

            condense_ratio = model_max_length / actual_length
            if last_length == actual_length:
                # last time we didn't manage to reduce the size so we need
                # to try more
                condense_ratio = max(last_ratio - 0.1, 0.1)
            else:
                last_length = actual_length
                last_ratio = condense_ratio

            pre_summarizer = SumySummarizer(target_ratio=condense_ratio)
            paragraphs = pre_summarizer.summarize(paragraphs)

        return paragraphs

    def summarize_article(self, paragraphs):
        """Summarize content with GPT-3"""

        paragraphs = self.pre_summarize(paragraphs)
        content = "\n\n".join([" ".join(s) for s in paragraphs])
        response = openai.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": content,
                },
                {
                    "role": "system",
                    "content": "You are an abstractive summarizer assistant. Summarize the user supplied text into 2 paragraphs so it can be read and understood quickly and easily. Try to maintain the voice of the original author.",
                },
            ],
        )

        text = response.choices[0].message.content
        paragraphs = [p for p in text.split("\n\n") if len(p) > 0]
        return [[f"{s}." for s in p.split(".")] for p in paragraphs]

    def summarize_video(self, subs):
        """Summarize content with GPT-3"""

        subs = self.pre_summarize([subs])[0]
        content = "\n".join([f"{i}: {sub}" for i, sub in enumerate(subs)])

        response = openai.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": f"=== Start of video ===\n\n{content}\n\n=== End of video ===",
                },
                {
                    "role": "system",
                    "content": "You are an extractive summarizer assistant. First, create a summary in your own words to prepare youself. Then, create an extractive summary of the video using direct, unmodified, quotes. Within your extractive summary write a comma separated list of the caption line indices needed to reconstruct your summary. Cite each quote with the caption index in parenthesis at the end of each line. Example: (1). For quotes that span multiple caption indices, write them in a comma separated list: (3,4,5). Make sure you cite every caption line the quote is from, even if it is a single word!",
                },
            ],
            max_tokens=1000,
        )

        text = response.choices[0].message.content

        # find all the cited indices
        indices = re.findall(r"\((\d+(?:,\d+)*)\)", text)
        indices = [int(i.strip()) for r in indices for i in r.split(",")]
        indices = sorted(list(set(indices)))

        extracted_subs = [subs[i] for i in indices if i < len(subs) and i >= 0]
        return extracted_subs

    def algorithm_name(self):
        return "LLM"

    def supports_malformed(self):
        return True
