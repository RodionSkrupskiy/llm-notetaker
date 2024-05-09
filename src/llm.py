from typing import List
from llama_cpp import Llama



class LLM:
    def __init__(self):
        self.llm = Llama(
            model_path="resources/Llama-3-8B-Instruct-Gradient-1048k.Q5_K_M.gguf",  # IQ4_XS
            n_ctx=2048, 
            n_threads=8, # Optimal
            chat_format="llama-3",
            use_mlock=True,
            use_mmap=True # Otherwise - all weights will be fitted in RAM, but with not much speed gain
        )

    def reply(self, message: str, notes: List):

        formatted_notes = ", ".join(notes)

        output = self.llm.create_chat_completion(
            messages=[
                {
                    "role": "system",
                    "content": "You are a highly capable TEXT ANALYSIS AGENT. Your task is to RECEIVE A LARGE TEXT INPUT and FOLLOW the user's SPECIFIC PROCESSING COMMANDS to extract insights, summarize, or perform other NATURAL LANGUAGE PROCESSING TASKS as requested. You need to answer questions using additional information.",
                },
                {
                    "role": "user",
                    "content": f"Please analyze the following text:{formatted_notes}",
                },
                {
                    "role": "assistant",
                    "content": """I have SUCCESSFULLY RECEIVED the provided text. To accurately process this data, I will follow these steps:
 
CHAIN OF THOUGHTS:
1. CAREFULLY READ through the entire text to gain a COMPREHENSIVE UNDERSTANDING of the content, TAKING NOTE of key points, themes, and entities.
2. CONSIDER the SPECIFIC COMMAND or QUESTION provided by the user to determine the most appropriate NLP task to apply (e.g., summarization, sentiment analysis, named entity recognition, topic modeling, question answering, paraphrasing, or translation).
3. BREAK DOWN the selected NLP task into SMALLER, MANAGEABLE SUBTASKS to ensure thorough and accurate processing.
4. APPLY RELEVANT NLP TECHNIQUES and ALGORITHMS to EXTRACT the requested insights from the text, PAYING CLOSE ATTENTION to maintaining the original context and meaning.
5. ORGANIZE and STRUCTURE the extracted information in a CLEAR, CONCISE, and EASILY UNDERSTANDABLE format for the user.
6. REVIEW the final output to ensure it DIRECTLY ADDRESSES the user's SPECIFIC COMMAND or QUESTION and provides ACTIONABLE and INSIGHTFUL results.
 
Please provide your SPECIFIC COMMAND or QUESTION regarding how you would like me to PROCESS or ANALYZE this text.""",
                },
                {"role": "user", "content": message},
            ],
            temperature=0.05,
            top_p=0.9,
            presence_penalty=0.1
        )
        output = output["choices"][0]["message"]["content"]
        output = output.replace("</s>", "")
        return output
