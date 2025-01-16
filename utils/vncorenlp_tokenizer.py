from os import path

from py_vncorenlp import VnCoreNLP, download_model

download_model("/app" if path.exists("/.dockerenv") else "./")
vncorenlp = VnCoreNLP(annotators=["wseg"])


def word_segment(text) -> str:
    sentences = vncorenlp.word_segment(text)
    return " ".join(sentences)
