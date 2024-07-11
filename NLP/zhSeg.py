import jieba
import jieba.posseg as pseg
import pandas as pd
import sys

jieba.load_userdict("/content/Geocoding/NLP/Street_csdi.txt")
jieba.load_userdict("/content/Geocoding/NLP/Street_data.txt")

def segment_text_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    
    lines = text.splitlines()
    segmented_lines = []
    for line in lines:
        seg_list = jieba.cut(line, cut_all=False)
        segmented_lines.append(list(seg_list))
    
    df = pd.DataFrame(segmented_lines)
    return df
    