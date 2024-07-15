# RAG-Chatbot
This repository creates a chatbot that utilizes OpenAI's language models. It integrates FastAPI for backend operations and Streamlit for the frontend. The system uses MongoDB to store chat histories and Chroma for vector-based similarity searches, enabling retrieval-augmented generation (RAG) to provide contextually relevant responses.

## Quick Start

### Clone the repository:

```sh
git clone <repo_url>
```

### Modify Environment Variables:

1. Rename `.env_example` to `.env`.
2. Add your OpenAI key to the `.env` file:

```sh
OPENAI_API_KEY=<your_openai_api_key>
```

### Build and Run with Docker Compose:

```sh
docker-compose up --build
```

## Adding Documents:

### Install Requirements:

To install the necessary Python packages, run:

```sh
pip install -r requirements.txt
```

Additionally, you need to install Poppler and Tesseract for handling PDFs and OCR functionality:

- [**Poppler**](https://pdf2image.readthedocs.io/en/latest/installation.html)
- [**Tesseract**](https://tesseract-ocr.github.io/tessdoc/Installation.html)

Place your documents in the `data/documents` directory.\
To add documents to the Chroma database, run `preprocess.py` from the base directory (`RAG_chatbot`):

```sh
python preprocess.py
```

## Components

- **MongoDB**: Used to store chat histories and facilitate history retrieval.
- **ChromaDB**: Serves as the vector database for similarity searches.
- **Streamlit**: Used as the front-end interface.
- **FastAPI**: Used as the back-end server.

## Future Functionality

- Addition of images into ChromaDB.
- Comprehensive testing.
- Adding document ingestion capabilities to the front-end.
