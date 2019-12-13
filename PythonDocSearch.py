#!/usr/bin/env python
# coding: utf-8

# In[19]:


import math
text = input("Welke tekst moet worden geanalyseerd?")

keywords = "maximumsnelheid stikstof VVD landbouw projecten verkeer crisis veevoer eiwit boeren minister rechter overheid bouw PAS rekenmethode vergunning boswachter vergrassing commissie gemiddeld producent Europa TNO weg ammoniak kabinet planten natuur juridisch Kamerleden maatregel buitenland natuurgebieden kilo RIVM runderen varkens kippen nieuwbouw PFAS doel problematiek huizen"
keywords_list = keywords.split()

cleanedtext = ""
illegal_chars = [",", ".", "'"]
for i in text:
    if i not in illegal_chars:
        cleanedtext += i
words = cleanedtext.split()
  

word_frequencies = {}
for i in words:
    if i in word_frequencies:
        word_frequencies[i] += 1
    else:
        word_frequencies[i] = 1

for i in word_frequencies: # print de table en het verkregen woord
    if i in keywords_list:
        print("{}: {}".format(i,word_frequencies[i]))


# In[ ]:




