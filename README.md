# Personal History Agent

The goal: build an agent that you can interact with that knows everything that
happened in your life, so you can query, understand, and interact with your
history and past self.

This is similar to rewind.ai ("Your AI assistant that has all the context"), but
meant to be as lightweight as possible, and focused more on your past history
(rather than live monitoring from now+).

## Example prompts / use cases
- What was happening in my life in 2020?
- Describe my relationship with Alec based on our texts.
- Who have I sent the most imsgs to in the last 5 years?
- What is my personality like? How has it changed in the last 10 years?
- Where do you see yourself in 10 years? Am I fulfilling my dreams?

## Data Sources
- Gmail
- iMsg
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
