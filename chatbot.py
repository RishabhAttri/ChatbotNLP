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
    _convo = convo.splitby(" +++$+++ ")[-1][1:-1].replace("'","").replace(" ","")
    conversation_ids.append()