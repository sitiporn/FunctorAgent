# Functor Agent

Ask the report agent questions using information from the configured knowledge base.

## Project Structure

```text
functor_agent/
├── main.py                          # CLI entry point
├── requirements.txt                 # Python dependencies
├── README.md
│   
└── app/
    ├── core/
    │   └── config.py                # Settings from environment / .env
    ├── data/
    │   ├── knowledge_base.txt       # Source policy document
    │   └── chunks.jsonl             # Generated searchable chunks
    ├── ingestion/
    │   ├── chunker.py               # Word-based chunking with overlap
    │   └── document_ingestion.py    # Seed / refresh chunks.jsonl
    ├── agents/
    │   └── report_generator.py      # Retriever + report agents, KB search
    ├── services/
    │   └── agent_service.py         # OpenAI client and agent runner
    └── utils/
        ├── stop_words.py            # Tokens ignored during search
        └── prompt_template/
            ├── retriever_prompt.md
            └── report_generator_prompt.md
```

## Usage Examples

```bash
python main.py "When is business-class airfare allowed for an international trip?"
```
<img width="1071" height="44" alt="image" src="https://github.com/user-attachments/assets/163cd104-c0cb-49aa-98d4-c48639724f0b" />

```bash
python main.py "How many annual leave days do employees receive, and when should they request leave?"
```
<img width="939" height="58" alt="image" src="https://github.com/user-attachments/assets/872ca49d-0689-4223-972a-20ed60c99d79" />


```bash
python main.py "What should an employee do if a company laptop is lost or stolen?"
```
<img width="937" height="43" alt="image" src="https://github.com/user-attachments/assets/20658aa2-76d3-4e75-9adb-3f8d78807281" />
