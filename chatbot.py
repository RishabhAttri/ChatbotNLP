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
for convo in conversations[:-1]:
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

# Taking the words which don't appear more than the threshold
threshold = 20
questionswords2int = {}
word_number = 0
for word, count in word2count.items():
    if count >= threshold:
        questionswords2int[word] = word_number
        word_number += 1
answerswords2int = {}
word_number = 0
for word, count in word2count.items():
    if count >= threshold:
        answerswords2int[word] = word_number
        word_number += 1

# Creating the last tokens for Seq2Seq model
        
tokens = ['<PAD>','<OUT>','<EOS>','<SOS>']
for token in tokens:
    questionswords2int[token] = len(questionswords2int) + 1

for token in tokens:
    answerswords2int[token] = len(answerswords2int) + 1
    
# Creating inverse dictionary of answerswords2int
answersint2words = {w_i: w for w, w_i in answerswords2int.items()}

# Adding EOS token in clean_answers
for i in range(len(clean_answers)):
    clean_answers[i] += ' <EOS>'

#Mapping each word to its corresponding integer
#Filtering out the non-frequent word
question_into_ints = []
for question in clean_questions:
    ints = []
    for word in question.split():
        if word not in questionswords2int:
            ints.append(questionswords2int['<OUT>'])
        else:
            ints.append(questionswords2int[word])
    question_into_ints.append(ints)
answers_into_int = []
for answer in clean_answers:
    ints = []
    for word in answer.split():
        if word not in answerswords2int:
            ints.append(answerswords2int['<OUT>'])
        else:
            ints.append(answerswords2int[word])
    answers_into_int.append(ints)

#Sorting questions and answers acc.to the length of the questions
sorted_clean_questions = []
sorted_clean_answers = []
for length in range(1,26):
    for i in enumerate(question_into_ints):
        if len(i[1]) == length:
            sorted_clean_questions.append(question_into_ints[i[0]])
            sorted_clean_answers.append(answers_into_int[i[0]])
    
    
    