from unstructured.partition.auto import partition
from langchain_core.prompts import ChatPromptTemplate
from unstructured.chunking.title import chunk_by_title
from langchain_openai.chat_models import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from pydantic import BaseModel, ValidationError
from langchain_core.documents import Document
from dotenv import load_dotenv
import toml
import src.core.prompt_library.prompt_library as library
from unstructured.chunking.basic import chunk_elements
from src.core.database.chroma_database import DataBase
import base64
import os

class Document_Chunk(BaseModel):
    """
    Data model for a document chunk

    Attributes: 
        doc_id (str): Unique identifier for the document.
        original (str): Original text content of the chunk.
        summary (str): Summary of the text content
    """
    doc_id : str
    original : str
    summary : str

class Preprocessing:
    def __init__(self):
        """
        Initializes the preprocessing class by loading configuration
        and initializing the database.
        """
        load_dotenv()
        self.config = toml.load("./configs/config.toml")
        db = DataBase()
        self.vectordatabase = db.get_vectorstore()


    def partitioning_step(self, doc_path):
        """
        Partitions a document into chunks based on title.

        Args:
            doc_path (str): Path to the document file. 

        Returns: 
            list: List of the text chunks from the document
        """
        elements = partition(
                filename=doc_path,
                extract_image_block_types=["Image"],
                skip_infer_table_types=[],
                extract_image_block_output_dir= self.config["FILE"]["image_filepath"],
                strategy="hi_res",
            )
        # elements = chunk_by_title(elements,
        #                         max_characters=1000, 
        #                         include_orig_elements=True,
        #                         combine_text_under_n_chars=0,
        #                         overlap=200,
        #                         )

        elements = chunk_elements(
                                elements,
                                overlap=100,
                                max_characters=1000
                                )
        texts = []
        for element in elements:
            section = ""
            for obj in element.metadata.orig_elements:
                if("unstructured.documents.elements.Table" in str(type(obj))):
                    section += str(obj.metadata.text_as_html) + " "
                else:
                    section += str(obj) + " "
            texts.append(section)
        print(texts)
        print(len(texts))
        return texts


    def text_summary(self, texts):
        """
        Summarizes a list of text chunks. 

        Args:
            texts (list): List of text chunks.

        Returns:
            list: List of summaries fro the text chunks.
        """
        llm_prompt = ChatPromptTemplate.from_template(library.summarize_text_prompt())
        model = ChatOpenAI(model=self.config["LLM"]["model"])
        summarize_chain = llm_prompt | model | StrOutputParser()

        text_summaries = summarize_chain.batch(texts, {"max_concurrrency": 5})

        return text_summaries


    def process_doc(self, doc_path, doc_id):
        """
        Processes a document by partitioning, summarizing, and storing it.

        Args:
            doc_path (str): Path to the document file. 
            doc_id (str): Unique identifier for the document.
        """
        errors = []
        doc_chunks = []
        texts = self.partitioning_step(doc_path)
        # text_summaries = self.text_summary(texts)
        text_summaries = texts
        
        for i, (original, summary) in enumerate(zip(texts, text_summaries)):
            try:
                doc_chunk = Document_Chunk(
                    doc_id=doc_id,
                    original=original,
                    summary=summary,
                )
                doc_chunks.append(doc_chunk)
            except ValidationError as e:
                errors.append(e)
        
        doc_list = [Document(page_content=chunk.summary, metadata=chunk.dict()) for chunk in doc_chunks]
        self.vectordatabase.add_documents(doc_list)


    def process_all_docs(self):
        """
        Processes all documents in the configured directory. 
        """
        for filename in os.listdir(self.config["FILE"]["doc_dir"]):
            self.process_doc(os.path.join(self.config["FILE"]["doc_dir"], filename), filename)


    def image_summary(self):
        """
        Summarizes images in the configured image directory.
        """
        chat = ChatOpenAI(model=self.config["LLM"]["model"], max_tokens=1024)

        base64_list = []
        image_summaries = []
        for filename in os.listdir(self.config["FILE"]["image_filepath"]):
            img_path = os.path.join(self.config["FILE"]["image_filepath"], filename)
            with open(img_path, "rb") as image_file:
                img_base64 = (base64.b64encode(image_file.read()).decode('utf-8'))
                msg = chat.invoke(
                    library.summarize_images_prompt(img_base64)
                )
                base64_list.append(img_base64)
                image_summaries.append(msg.content)
