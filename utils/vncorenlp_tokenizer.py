from os import path

from py_vncorenlp import VnCoreNLP, download_model
import re

download_model("/app" if path.exists("/.dockerenv") else "./")
vncorenlp = VnCoreNLP(annotators=["wseg"])

# Replace A 2 or B 1 with A2 or B1
__patch_pattern = r"\b[ABC]\s[12]\b"

# Replace # # # with ###
__patch_list = ["# # #", "# #"]

# Replace white space before and after the following characters
__front_white_space_separators = r"\s[.,:;!?\)\]\}]"
__back_white_space_separators = r"[\(\[\{]\s"


def word_segment(text) -> str:
    sentences = vncorenlp.word_segment(text)
    sentences = [re.sub(__patch_pattern, lambda x: x.group().replace(" ", ""), sentence) for sentence in sentences]
    
    paragraph = "\n".join(sentences)
    
    for mark in __patch_list:
        replacement = mark.replace(" ", "")
        paragraph = paragraph.replace(mark, replacement)
        
    paragraph = re.sub(__front_white_space_separators, lambda x: x.group().strip(), paragraph)
    
    paragraph = re.sub(__back_white_space_separators, lambda x: x.group().strip(), paragraph)

    return paragraph
