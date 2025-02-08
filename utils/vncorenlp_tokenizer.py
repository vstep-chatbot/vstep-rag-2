from os import path

from py_vncorenlp import VnCoreNLP, download_model
import re

download_model("/app" if path.exists("/.dockerenv") else "./")
vncorenlp = VnCoreNLP(annotators=["wseg"])

__patch_pattern = r"\b[ABC]\s[12]\b"
__patch_list = ["# # #", "# #"]


def word_segment(text) -> str:
    sentences = vncorenlp.word_segment(text)
    sentences = [re.sub(__patch_pattern, lambda x: x.group().replace(" ", ""), sentence) for sentence in sentences]
    for mark in __patch_list:
        replacement = mark.replace(" ", "")
        sentences = [sentence.replace(mark, replacement) for sentence in sentences]

    return "\n".join(sentences)
