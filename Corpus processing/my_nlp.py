import nltk
import codecs
import re
from nltk.util import bigrams, ngrams


def main():
    tokens, tokens_frequency, tokens_frequency_without_punct, tokens_frequency_without_stopwords = get_tokens_and_freq_distribution()
    bigram_freq_dist = get_bigrams_frequency_dist(tokens)
    ngram_freq_dist = get_ngrams_frequency_dist(tokens)
    print_results(tokens, tokens_frequency, tokens_frequency_without_punct, tokens_frequency_without_stopwords)

    write_to_files(bigram_freq_dist, ngram_freq_dist, tokens, tokens_frequency, tokens_frequency_without_punct,
                   tokens_frequency_without_stopwords)



def get_tokens_and_freq_distribution():
    with open('microblog2011.txt', 'r') as f:
        f_read = f.read().decode('utf-8')

        tokens = nltk.word_tokenize(f_read)
        tokens_frequency = nltk.FreqDist(tokens)

        tokens_frequency_without_punct = {}
        tokens_frequency_without_stopwords = {}

        stop_set = set(line.strip() for line in open('stopwords.txt', mode='r'))

        for token in sorted(tokens_frequency, key=tokens_frequency.get, reverse=True):
            if re.search('[^A-Za-z0-9_]', token) is None:
                tokens_frequency_without_punct[token] = tokens_frequency.get(token)
            if token not in stop_set:
                tokens_frequency_without_stopwords[token] = tokens_frequency.get(token)

        f.close()
    return tokens, tokens_frequency, tokens_frequency_without_punct, tokens_frequency_without_stopwords


def get_bigrams_frequency_dist(tokens):
    bigram_freq_dist = {}
    list_for_ngrams = get_list_for_ngrams(tokens)

    bigram_list = list(bigrams(list_for_ngrams))
    for bigram_tuple in bigram_list:
        if bigram_freq_dist.has_key(bigram_tuple):
            bigram_freq_dist[bigram_tuple] += 1
        else:
            bigram_freq_dist[bigram_tuple] = 1
    return bigram_freq_dist


def get_ngrams_frequency_dist(tokens):
    ngram_freq_dist = {}
    list_for_ngrams = get_list_for_ngrams(tokens)

    ngram_list = list(bigrams(list_for_ngrams)) + list(ngrams(list_for_ngrams, 3)) + list(ngrams(list_for_ngrams, 4))
    for ngram in ngram_list:
        if ngram_freq_dist.has_key(ngram):
            ngram_freq_dist[ngram] += 1
        else:
            ngram_freq_dist[ngram] = 1
    return ngram_freq_dist


def get_list_for_ngrams(tokens):
    list_for_ngrams = []
    stop_set = set(line.strip() for line in open('stopwords.txt', mode='r'))
    for token in tokens:
        if re.search('[^A-Za-z0-9_]', token) is None and token not in stop_set:
            list_for_ngrams.append(token)
    return list_for_ngrams


def write_to_token_file(tokens, filename):
    target = codecs.open(filename, 'w', encoding='utf-8')
    for token in tokens:
        target.write(token + '\n')
    target.close()


def write_to_tokens_frequency_file(tokens_frequency, filename):
    freq_file = codecs.open(filename, 'w', encoding='utf-8')
    for token in sorted(tokens_frequency, key=tokens_frequency.get, reverse=True):
        freq_file.write(token + ' : ' + str(tokens_frequency[token]) + '\n')
    freq_file.close()


def write_to_bigrams_frequency_file(bigram_freq_dist, filename):
    bigram_file = codecs.open(filename, 'w', encoding='utf-8')
    for bigram in sorted(bigram_freq_dist, key=bigram_freq_dist.get, reverse=True):
        bigram_file.write(
                "({},{}):{}\n".format(bigram[0].encode('utf8'), bigram[1].encode('utf8'), bigram_freq_dist[bigram]))
    bigram_file.close()


def write_to_ngrams_frequency_file(ngram_freq_dist, filename):
    ngram_file = codecs.open(filename, 'w', encoding='utf-8')
    for ngram in sorted(ngram_freq_dist, key=ngram_freq_dist.get, reverse=True):
        if ngram.__len__() == 2:
            ngram_file.write(
                    "({},{}):{}\n".format(ngram[0].encode('utf8'), ngram[1].encode('utf8'), ngram_freq_dist[ngram]))
        elif ngram.__len__() == 3:
            ngram_file.write(
                    "({},{},{}):{}\n".format(ngram[0].encode('utf8'), ngram[1].encode('utf8'), ngram[2].encode('utf8'),
                                             ngram_freq_dist[ngram]))
        elif ngram.__len__() == 4:
            ngram_file.write(
                    "({},{},{},{}):{}\n".format(ngram[0].encode('utf8'), ngram[1].encode('utf8'),
                                                ngram[2].encode('utf8'), ngram[3].encode('utf8'),
                                                ngram_freq_dist[ngram]))

    ngram_file.close()


def write_to_files(bigram_freq_dist, ngram_freq_dist, tokens, tokens_frequency, tokens_frequency_without_punct,
                   tokens_frequency_without_stopwords):
    write_to_token_file(tokens, filename='microblog2011_tokenized.txt')
    write_to_tokens_frequency_file(tokens_frequency, filename='freq_file.txt')
    write_to_tokens_frequency_file(tokens_frequency_without_punct, filename='freq_file_WO_punct.txt')
    write_to_tokens_frequency_file(tokens_frequency_without_stopwords, filename='freq_file_WO_stopwords.txt')
    write_to_bigrams_frequency_file(bigram_freq_dist, filename='freq_bigrams.txt')
    write_to_ngrams_frequency_file(ngram_freq_dist, filename='freq_ngrams.txt')


def print_results(tokens, tokens_frequency, tokens_frequency_without_punct, tokens_frequency_without_stopwords):
    print('Number of tokens found :' + str(tokens.__len__()))
    print('Number of types of (unique) tokens found :' + str(tokens_frequency.__len__()))
    print('Type/Token ratio : ' + str(tokens_frequency.__len__() / float(tokens.__len__())))

    print('Number of tokens without punctuation found :' + str(sum(tokens_frequency_without_punct.values())))
    print('Number of types of (unique) tokens without punct found :' + str(tokens_frequency_without_punct.__len__()))
    print('Type/Token ratio without punctuations: ' + str(
            tokens_frequency_without_punct.__len__() / float(sum(tokens_frequency_without_punct.values()))))

    print('Number of tokens without stopwords found :' + str(sum(tokens_frequency_without_stopwords.values())))
    print(
        'Number of types of (unique) tokens without stopwords found :' + str(
                tokens_frequency_without_stopwords.__len__()))
    print('Type/Token ratio without stopwords: ' + str(
            tokens_frequency_without_stopwords.__len__() / float(sum(tokens_frequency_without_stopwords.values()))))

    single_word_count = sum(val == 1 for val in tokens_frequency.values())
    print single_word_count


if __name__ == '__main__':
    main()
