# Personal History Agent

The goal: build an agent that you can interact with that knows everything that
happened in your life, so you can query, understand, and interact with your
history and past self.

NOTE: This is an *extremely* basic prototype. The current code only support imsg
data, and an effective RAG pipeline would require far more customization.

## Quickstart

### 0. Project + API key setup
```bash
echo '{"openai": "YOUR_KEY"}' > keys.json
direnv allow  # set up local variables
pip install -r requirements
```

### 1. Download iMessage data
```bash
mkdir data/
cargo install imessage-exporter
~/.cargo/bin/imessage-exporter -f txt -s 2023-01-01 -o data/
```
For help, see the project [git repo](https://github.com/ReagentX/imessage-exporter/?tab=readme-ov-file).

### 2. Create the vector store
```bash
python create_vector_store.py
```

### 3. Run interactively run queries
```bash
python query.py
```

### Examples
```
$ python query.py
loading index...
> What is my personality like based on my texts?
loading...
Based on your texts, it seems that you are friendly, open-minded, and have a good sense of humor. You handle conversations with kindness and clarity, making sure to communicate your intentions clearly. You also seem to be supportive of others and willing to help out when needed. Overall, your texts reflect a positive and approachable personality.

Enter a query:
> what are some times i've talked about coffee
loading...
You have talked about coffee on Jan 15, 2024, when you mentioned meeting up for lunch or coffee. Additionally, on Jan 24, 2023, you mentioned how pour overs have enabled you to have caffeinated sessions for deep work.

> what is my relationship like with Alec?
loading...
Your relationship with Alec seems to be friendly. You have been discussing plans to hang out, play tennis, and pickleball together. You have also mentioned having dinner with Alec, Courtney, and your parents. Overall, it appears that you have a positive and casual relationship with Alec.
```

## Example prompts / future use cases
- What was happening in my life in 2020?
- Describe my relationship with [person] based on our texts.
- Who have I sent the most imsgs to in the last 5 years?
- What is my personality like? How has it changed in the last 10 years?
- Where do you see yourself in 10 years? Am I fulfilling my dreams?

# Development Notes

This is similar to rewind.ai ("Your AI assistant that has all the context"), but
meant to be as lightweight as possible, and focused more on your past history
(rather than live monitoring from now+).


## Data Sources
- Gmail
- [x] iMsg
- Messenger
- Notion
- txt journal entries
- Music taste (Spotify)
- Location history (google maps)
- Browsing history
- All social media - Facebook/Instagram/LinkedIn history

## Approach
The first challenge is getting access to all your data, but that is pretty easy
via APIs / downloading data archives. But how can you make use of this data and
power an LLM with it?

LLMs are very powerful but just trained over public data. In order to customize
state of the art models to your personal data there are two approaches:
1. Fine-tuning
2. Retrieval-augmented generation (RAG)

### Fine-Tuning
With this approach, you continue training the parameters of the model over your
own data so it *learns* your personal dataset.

However, fine-tuning jobs can take non-trivial time (minutes to hours), can be
costly, and might not be necessary with good prompting.

OpenAI suggests to try other techniques first (prompt engineering, prompt
chaining, function calling, etc.) before fine-tuning.

References:
- [OpenAI Fine Tuning](https://platform.openai.com/docs/guides/fine-tuning/when-to-use-fine-tuning)
- [TogetherAI Fine Tuning](https://docs.together.ai/docs/fine-tuning-cli)

### Retrieval-Augemented Generation (RAG)
The RAG approach is to respond to a query by:
1. retrieving information from data sources
2. add it as context to the query
3. using the LLM to answer the enriched prompt

The beauty here is that you can easy use and swap between any model/agent
provider (i.e. even those that can't be fine-tuned).

There is a tool that is perfect for this sort of use-case:
[LlamaIndex](https://docs.llamaindex.ai/en/stable/)

# Issues
- OpenAI API keys are a MASSIVE PAIN. If you're running into API key errors, generate a new key and hardcode the following:
```
.direnv/python-3.11.5/lib/python3.11/site-packages/llama_index/embeddings/openai.py
in get_embedding() and get_embeddings()

.direnv/python-3.11.5/lib/python3.11/site-packages/llama_index/llms/openai.py
in OpenAI._chat()

Before using `client`:
client.api_key = 'YOUR API KEY'
```
- With default config, the RAG seems to almost always return just 2 context
blobs -- this is extremely limiting, and prevents summarizing over large volumes
of data.
