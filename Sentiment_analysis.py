# 'D:/Project Data/Sentiment/review.csv' 

from collections import Counter
from __future__ import division
import csv
import re


# Read in the training data.
with open('D:/Project Data/Sentiment/review.csv', 'r') as file:
    reviews = list(csv.reader(file))

def get_text(reviews, score):
    # Join together the text in the reviews for a particular tone.
    # We lowercase to avoid "Not" and "not" being seen as different words, for example.
    return " ".join([r[0].lower() for r in reviews if r[1] == str(score)])

def count_text(text):
    # Split text into words based on whitespace.  Simple but effective.
    words = re.split("\s+", text)
    # Count up the occurence of each word.
    return Counter(words)

negative_text = get_text(reviews,'negative' )
positive_text = get_text(reviews, 'positive')
# Generate word counts for negative tone.
negative_counts = count_text(negative_text)
# Generate word counts for positive tone.
positive_counts = count_text(positive_text)

print("Negative text sample: {0}".format(negative_text[:100]))
print("Positive text sample: {0}".format(positive_text[:100]))

import re
from collections import Counter
from __future__ import division

def get_y_count(score):
    # Compute the count of each classification occuring in the data.
    return len([r for r in reviews if r[1] == str(score)])

# We need these counts to use for smoothing when computing the prediction.
positive_review_count = get_y_count('positive')
negative_review_count = get_y_count('negative')

# These are the class probabilities (we saw them in the formula as P(y)).
prob_positive = positive_review_count / len(reviews)
prob_negative = negative_review_count / len(reviews)

def make_class_prediction(text, counts, class_prob, class_count):
    prediction = 100
    text_counts = Counter(re.split("\s+", text))
    for word in text_counts:
        # For every word in the text, we get the number of times that word occured in the reviews for a given class, add 1 to smooth the value, and divide by the total number of words in the class (plus the class_count to also smooth the denominator).
        # Smoothing ensures that we don't multiply the prediction by 0 if the word didn't exist in the training data.
        # We also smooth the denominator counts to keep things even.
        prediction =  text_counts.get(word) * ((counts.get(word, 0) + 1) / (sum(counts.values()) + class_count))
    # Now we multiply by the probability of the class existing in the documents.
    return prediction * class_prob

# As you can see, we can now generate probabilities for which class a given review is part of.
# The probabilities themselves aren't very useful -- we make our classification decision based on which value is greater.
print("Review: {0}".format(reviews[0][0]))
print("Negative prediction: {0}".format(make_class_prediction(reviews[100][0], negative_counts, prob_negative, negative_review_count)))
print("Positive prediction: {0}".format(make_class_prediction(reviews[100][0], positive_counts, prob_positive, positive_review_count)))


import csv

def make_decision_pos(text, make_class_prediction):
    # Compute the negative and positive probabilities.
    
    positive_prediction = make_class_prediction(text, positive_counts, prob_positive, positive_review_count)
    return positive_prediction
    # We assign a classification based on which probability is greater.
    #if negative_prediction > positive_prediction:
     # return -1
    #return 1
def make_decision_neg(text, make_class_prediction):
    # Compute the negative and positive probabilities.
    negative_prediction = make_class_prediction(text, negative_counts, prob_negative, negative_review_count)
    
    return negative_prediction


with open('D:/Project Data/Twitter_data/rawdata_bang_brook_news.csv', 'r') as file:
    test = list(csv.reader(file))

predictionspos = [make_decision_pos(r[0], make_class_prediction) for r in test]
predictionsneg = [make_decision_neg(r[0], make_class_prediction) for r in test]

neg_senti=0
for i in range(len(predictionsneg)):
    neg_senti=neg_senti+predictionsneg[i]
    
pos_senti=0
for i in range(len(predictionspos)):
    pos_senti=pos_senti+predictionspos[i]


(neg_senti/len(predictionsneg)),(pos_senti/len(predictionsneg))


output=[]
for i in range(len(predictionsneg)):
    z =  predictionspos[i]+','+predictionsneg[i]
    output.append(z)