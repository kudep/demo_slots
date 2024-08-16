## Description

### Restaurant booking bot

Restaurant booking bot built on `DFF`. Uses streamlit as an interface.
This bot was created to demonstrate the use of slots

As models for extraction of slots were taken [NER](https://huggingface.co/Davlan/distilbert-base-multilingual-cased-ner-hrl) and [Open Assistant](https://huggingface.co/OpenAssistant/oasst-sft-4-pythia-12b-epoch-3.5) models

In this example, 3 slots are added: restaurant location, restaurant name and person name. New slots can be easily added, the main limitation is the model. NER model is limited by known tags, for Open Assistant model it is important to choose the right prompt.

### Run with Docker & Docker-Compose environment

In order for the bot to work, set the Hugging Face token via .env

Build the bot:
```commandline
docker-compose build
```

Running in background
```commandline
docker-compose up -d
```

Then website will be accessible via http://0.0.0.0:8501.
