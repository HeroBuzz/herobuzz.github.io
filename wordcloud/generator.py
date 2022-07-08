from os import path
import numpy as np
import matplotlib.pyplot as plt
import os
from PIL import Image


from wordcloud import WordCloud, STOPWORDS

# get data directory (using getcwd() is needed to support running example in generated IPython notebook)
d = path.dirname(__file__) if "__file__" in locals() else os.getcwd()

# Read the whole text.
text = open(path.join(d, 'alice.txt')).read()
# for i in range(80):
#     text += " HeroBuzz15\n"

# Picture Source
# https://www.printablee.com/post_cloud-outline-printable_395379/
mask = np.array(Image.open(path.join(d, "mask.png")))

# wordcloud already has some stopwords list
stopwords_default = set(STOPWORDS)
# but not in Portuguese, so we got this list from
# https://github.com/stopwords-iso/stopwords-pt
stopword_portuguese = set(open('stop.txt'))

# Let's join them
stopwords_n = set.union(
    stopwords_default, stopword_portuguese)

# it has \n let's remove them
stopwords = set()
for i in stopwords_n:
    stopwords.add(i.replace('\n', ''))


wc = WordCloud(background_color="white", colormap='ocean', max_words=100, mask=mask, collocations=False,
               stopwords=stopwords, contour_width=3, contour_color='white')

# generate word cloud
wc.generate(text)

# store to file
wc.to_file(path.join(d, "alice.png"))

# show
plt.axis("off")

plt.imshow(wc, interpolation='bilinear')
plt.show()
