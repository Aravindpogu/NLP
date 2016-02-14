## Synopsis

Corpus processing: Tokenization and word counting
We have used nltk library of python for Natural language processing. The whole logic was written in single script file with name my_nlp.py. Following are the steps followed to solve all the questions of corpus processing.
 
1. To generate the tokens we used the nltk.word.tokenize() method of nltk.
2. Once the tokens were generated, they are stored in a list with variable name tokens. To count the number of tokens, tokens.__len__() method is called.
3. Then we calculated the frequency distribution using nltk.FreqDist(tokens). This will list out the tokens and their frequency count. We have stored this in frequency_dist variable. To print the 100 frequent words, sorted method on the frequency distribution is used in reverse order on frequency_dist variable. tokens_frequency.__len () –set return a list of unique tokens.
4. For removing the punctuation re.search('[^A-Za-z0-9_]', token) is used.
5. Set of stop words are imported from the attached list to remove the stop words from the generated tokens.
6. bigrams method of nltk.util is used on the tokens excluding stopwords and punctuations to find out the bigrams in the corpus.
7. Similarly, we have used ngrams from nltk.util to find out the multiword expressions.
8. Files containing just tokens, frequency distributions of tokens, tokens-without-punctuations, tokens-without-stopwords and bigrams and multiword expressions are saved with the corresponding names and can be found in the code itself. 

## Motivation

It will be head start for the ones who want to start learning NLP with nltk python library.

## Installation

``` python
pip install nltk
pip install stopwords

```
## Test and run the program 

python my_nlp.py

