import sys
import time

sys.path.append('..')

from api.logger import logger

import spacy
from summarizer import Summarizer
from summarizer.coreference_handler import CoreferenceHandler
from transformers import pipeline

from api.model import Document, Summary

model = 't5-base'
tokenizer = 't5-base'
framework = 'tf'


def summarize_t5(doc: Document):
    summarizer = pipeline('summarization',
                          model=model,
                          tokenizer=tokenizer,
                          framework=framework)

    # TODO split up document into 512 token chunks

    summary = summarizer(doc.text)
    return Summary(summary=summary[0]['summary_text'], strategy='t5-base')


def summarize_distill(doc: Document, greedyness=.33):
    spacy.load("en_core_web_md")
    corefHandler = CoreferenceHandler(greedyness=greedyness)
    summarizer = Summarizer(sentence_handler=corefHandler)
    result = summarizer(doc.text)
    return Summary(summary=''.join(result), strategy='distillBERT')


def summarize(doc: Document, strategy: str = 'distill'):
    result = None

    logger.info(f"Starting summarization using {strategy} strategy!")

    tic = time.perf_counter()
    if strategy == 't5':
        result = summarize_t5(doc)
    elif strategy == 'distill':
        result = summarize_distill(doc)
    else:
        result = summarize_distill(doc)
    toc = time.perf_counter()

    logger.info(f"Summarized the document using {strategy} strategy in {toc - tic:0.4f} seconds!")

    return result
