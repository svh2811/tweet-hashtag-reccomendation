import re
import sys

import preprocessor as p

# Multiple hashtags in a tweet can be expanded to multiple tweets
# Remove URLs
# Emojis, smileys - removed
# Mentions - removing mentions from tweets as any handle won't have a lot of mentions to matter
# Reserved words - remove RT
base_path = '/home/sarthak/Downloads/Twitter Datasets/1 - Cheng-Caverlee-Lee Scrape/twitter_cikm_2010/'
tweets_file_path = base_path + 'just_hashtagged_tweets.txt'
output_file_path = base_path + 'processed_tweets.json'


def pre_process_tweets():
    total = 0
    valid_tweets = 0
    invalid_tweets = 0
    empty_lines = 0
    with open(tweets_file_path, 'r') as ip_file:
        with open(output_file_path, 'w+') as op_file:
            start_json_file(op_file)
            for cnt, tweet in enumerate(ip_file):
                total += 1
                if len(tweet) == 0 or tweet == '\n':
                    print('Empty line at : %d' % cnt)
                    empty_lines += 1
                    continue
                try:
                    processed_tweets = process_tweet(tweet)
                    for processed_tweet in processed_tweets:
                        write_json_record(op_file, processed_tweet[0], processed_tweet[1], processed_tweet[2])
                    valid_tweets += 1
                except:
                    print('Unexpected error at line %d : %s' % (cnt, sys.exc_info()[1]))
                    invalid_tweets += 1
                    continue
            end_json_file(op_file)
    print('Total tweets processed: %d' % total)
    print('Valid tweets: %d' % valid_tweets)
    print('Invalid tweets: %d' % invalid_tweets)
    print('Empty lines: %d' % empty_lines)


def start_json_file(file):
    file.write('{\n"data":[\n')


def end_json_file(file):
    file.write(']\n}\n')


def write_json_record(file, tweet, num_words, hashtag):
    file.write('{"tweet":"%s", "num_words":%d, "hashtag":"%s"},\n' % (tweet, num_words, hashtag))


# Returns list of tweet, number of words in tweet and hashtag, with one record in list for each hashtag
def process_tweet(tweet):
    # Set tweet preprocessor options to remove all of the below
    p.set_options(p.OPT.URL, p.OPT.EMOJI, p.OPT.MENTION, p.OPT.SMILEY, p.OPT.RESERVED)
    cleaned_tweet = p.clean(p.clean(p.clean(tweet)))  # To remove RT from multiple retweets
    cleaned_tweet = re.sub('[^a-zA-Z# ]', '', cleaned_tweet).strip()  # Keeping hash as it's required to extract hashtag later. Single hashes are also considered as hashtags by the library
    cleaned_tweet = cleaned_tweet.replace(' RT ', ' ').strip()  # Remove RT from within tweets
    if cleaned_tweet.endswith(' RT'):
        cleaned_tweet = cleaned_tweet.replace(' RT', '').strip()  # Remove RT from end of tweet if present

    cleaned_tweet = cleaned_tweet.lower()
    p.set_options(p.OPT.HASHTAG)
    parsed_tweet = p.parse(cleaned_tweet)
    hashtags = parsed_tweet.hashtags

    if hashtags is None:
        raise Exception('Tweet "%s" does not have hashtags' % tweet)

    hash_removed_tweet = cleaned_tweet
    removed = 0
    for hashtag in hashtags:
        index = hashtag.start_index - removed
        hash_removed_tweet = hash_removed_tweet[:index] + hash_removed_tweet[(index + 1):]
        removed += 1

    words = hash_removed_tweet.split()
    number_of_words = len(words)
    processed_tweets = []
    for hashtag in hashtags:
        if hashtag.end_index - hashtag.start_index > 1:  # So that just hashes are not included
            processed_tweets.append([hash_removed_tweet, number_of_words, hashtag.match[1:]])
    return processed_tweets


if __name__ == "__main__":
    pre_process_tweets()
