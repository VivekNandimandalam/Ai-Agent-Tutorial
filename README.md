# AI Agent Tutorial

This project demonstrates how to build a research assistant agent using LangChain, OpenAI, Anthropic, and Google Generative AI models, with a minimal chat-like frontend powered by Streamlit.![Recording 2025-08-11 182600](https://github.com/user-attachments/assets/6bbc5d1c-1866-4b8c-8fa1-c3ba8b2844d9)


## Features

- **Multi-LLM Support:** Easily switch between OpenAI, Anthropic, and Google Gemini models.
- **Tool Integration:** Web search, Wikipedia lookup, and saving research outputs to text files.
- **Structured Output:** Uses Pydantic for clean, structured responses.
- **Streamlit Frontend:** Chat-like UI for interactive research queries.

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/VivekNandimandalam/Ai-Agent-Tutorial.git
cd Ai-Agent-Tutorial
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set Up Environment Variables

Create a `.env` file in the project root and add your API keys:

```
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key
GOOGLE_API_KEY=your_google_key
```


### 4. Run the Streamlit Frontend

```bash
streamlit run app.py
```

## Usage

- Enter your research question in the input box.
- The agent will use web search, Wikipedia, and LLMs to generate a structured summary.
- Results are displayed in a chat-like interface.

## Project Structure

- `main.py` — Backend agent logic and tool setup.
- `tools.py` — Tool definitions for search, Wikipedia, and saving output.
- `app.py` — Streamlit frontend for user interaction.
- `.env` — **(Not tracked)** Store your API keys here.

## Contributing

Feel free to fork and submit pull requests!

## License

MIT License

---
