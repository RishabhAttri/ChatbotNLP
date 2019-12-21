# -*- coding: utf-8 -*-
"""
Created on Sat Dec 21 19:03:22 2019

@author: Rishabh
"""

import numpy as np
import tensorflow as tf
import re 
import time 

# Importing the dataset
lines = open ("movie_lines.txt", encoding = "utf-8", errors = "ignore").read().split('\n' )
conversations = open ("movie_conversations.txt", encoding = "utf-8", errors = "ignore").read().split('\n' )

# Creating a mapping between lines and its id
id2line = {}
for line in lines:
    _line = line.split(" +++$+++ ")
    if len(_line) == 5:
        id2line[_line[0]] = _line[-1]

# Creating a list of only conversation_ids
conversation_ids = []
for convo in conversations:
    _convo = convo.split(" +++$+++ ")[-1][1:-1].replace("'","").replace(" ","")
    conversation_ids.append(_convo.split(","))

# Create a question and answer list
questions = []
answers = []
for convo in conversation_ids:
    for i in range(len(convo)-1):
        questions.append(id2line[convo[i]])
        answers.append(id2line[convo[i+1]])

# Clean the text 
def clean_text(text):
    text = text.lower()
    text = re.sub(r"i'm", "i am", text)
    text = re.sub(r"he's", "he is", text)
    text = re.sub(r"she's", "she is", text)
    text = re.sub(r"what's", "what is", text)
    text = re.sub(r"where's", "where is", text)
    text = re.sub(r"that's", "that is", text)
    text = re.sub(r"\'ll", " will", text)
    text = re.sub(r"\'ve", " have", text)
    text = re.sub(r"\'re", " are", text)
    text = re.sub(r"\'d", " would", text)
    text = re.sub(r"can't", "cannot", text)
    text = re.sub(r"won't", "will not", text)
    text = re.sub(r"[-()~@<>+=|.?\"#;:,{}]", "", text)
    return text

# Clean questions 
clean_questions = []
for question in questions:
    clean_questions.append(clean_text(question))

# Clean Answers
clean_answers = []
for answer in answers:
    clean_answers.append(clean_text(answer))

# count the frequencies of words 
word2count = {}
for question in clean_questions:
    for word in question.split(" "):
        if word2count.get(word) is None:
            word2count[word] = 1
        else:
            word2count[word] += 1
            
for ans in clean_answers:
    for word in ans.split(" "):
        if word2count.get(word) is None:
            word2count[word] = 1
        else:
            word2count[word] += 1

    
    
    