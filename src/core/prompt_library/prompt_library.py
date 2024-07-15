from langchain_core.messages import HumanMessage

def chatbot_prompt():
        """
        Creates a prompt template for a friendly conversation between a user and a chatbot.

        This template includes RAG context, chat history, and the user's query.
        Includes rules for rendering tabular data and LaTeX.

        Returns:
            str: The prompt template for the chatbot.
        """
        p_chat ="""
                The following is a friendly conversation between a user and you. You are an expert in the field and any context - text and image summaries you receive, you will reference.\n
                You will be given a mix of text, table and image summaries. Use this information to answer the user question.\n

                Current conversation:\n
                CONTEXT:\n 
                {context}\n
                HISTORY:\n 
                {history}\n
                User-provided question: {query}\n

                STRICTLY follow this list of rules:\n
                1. Render any tabular data in markdown \n
                2. When you encounter latex, ALWAYS surround by $\n

                Expert:"""

        return p_chat

def summarize_text_prompt():
        """
        Creates a prompt template for summarizing text, tables, or formulas for retrieval.

        Designed to optimize text RAG retrieval

        Returns:
            str: The prompt template for summarizing text, tables, or formulas
        """
        p_text ="""You are an assistant tasked with summarizing text, tables, or formulas for retrieval.\n
                These summaries will be embedded and used to retrieve the raw text, table, and formula elements.\n
                Give a concise summary that is well optimized for retrieval. Text, table or formula: {element} """

        return p_text

def summarize_images_prompt(img_base64):
        """
        Creates a HumanMessage object to prompt for summarizing an image for retrieval.

        Designed to optimize image RAG retrieval

        Args: 
            img_base64 (str): The base64 encoded string of the image

        Returns:
            list: A list containing a single HumanMessage object containing the image and prompt            
        """
        prompt = """You are an assistant tasked with summarizing images for retrieval.\n
                These summaries will be embedded and used to retrieve the raw image. If table number is specified make sure to add that to the summary \
                Give a concise, but in-depth summary of the image that is well optimized for retrieval."""

        p_vision = HumanMessage(
                    content=[
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/jpeg;base64,{img_base64}"},
                        },
                    ]
                )

        return [p_vision]
