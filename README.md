# RAG-Chatbot

This repository creates a chatbot that utilizes OpenAI's language models. It integrates FastAPI for backend operations and Streamlit for the frontend. The system uses MongoDB to store chat histories and Chroma for vector-based similarity searches, enabling retrieval-augmented generation (RAG) to provide contextually relevant responses.

## Quick Start

### Clone the repository

```sh
git clone <repo_url>
```

### Modify Environment Variables

1. Rename `.env_example` to `.env`.
2. Add your OpenAI key to the `.env` file:

```sh
OPENAI_API_KEY=<your_openai_api_key>
```

### Build and Run with Docker Compose

```sh
docker-compose up --build -d
```

### Alternatively, Run with Make

```sh
make build
```

## Adding Documents

### Prerequisites

To handle PDFs and OCR functionality, ensure you have the following installed:

- [**Poppler**](https://pdf2image.readthedocs.io/en/latest/installation.html)
- [**Tesseract**](https://tesseract-ocr.github.io/tessdoc/Installation.html)

### Placing Documents

Place your documents in the `data/documents` directory.

### Option 1: Using Makefile

   Add your documents and run the preprocessing script with a single command:

   ```sh
   make preprocess
   ```

### Option 2: Manual Installation

1. Install Requirements

   Install the necessary python packages using:

   ```sh
   pip install -r requirements.txt
   ```

2. Add Documents to the Database

   From the base directory (RAG_chatbot), run the preprocessing script:

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
