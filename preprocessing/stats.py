import math
import pickle
import re
import matplotlib.pyplot as plt
import preprocessor as p

base_path = '/home/sarthak/Downloads/Twitter Datasets/1 - Cheng-Caverlee-Lee Scrape/twitter_cikm_2010/'
tweets_file_path = base_path + 'just_hashtagged_tweets.txt'

total_tweets = 0
valid_tweets = 0
invalid_tweets = 0
empty_lines = 0

total_words_in_valid_tweets = 0
number_of_words_in_tweets = []
number_of_word_occurrences = {}
number_of_word_count_occurrences = {}

number_of_tweets_with_emojis = 0
number_of_tweets_with_smileys = 0
number_of_tweets_with_RTs = 0
number_of_tweets_with_mentions = 0
number_of_tweets_with_urls = 0
hashtag_counts = {}
mention_counts = {}

number_of_hashtags_in_tweet = []
# min_words_tweet = ''
# min_word_tweet_count = 100
max_words_tweet = ''
max_word_tweet_count = 0


def process_tweet(tweet):
    global total_tweets
    global valid_tweets
    global invalid_tweets
    global empty_lines
    global total_words_in_valid_tweets
    global number_of_tweets_with_emojis
    global number_of_tweets_with_smileys
    global number_of_tweets_with_mentions
    global number_of_tweets_with_RTs
    global number_of_tweets_with_urls
    # global min_words_tweet
    # global min_word_tweet_count
    global max_words_tweet
    global max_word_tweet_count

    total_tweets += 1
    if len(tweet) == 0 or tweet == '\n':
        print('Empty line at : %d' % cnt)
        empty_lines += 1
        return
    # Set tweet preprocessor options to remove all of the below
    p.set_options(p.OPT.URL, p.OPT.EMOJI, p.OPT.MENTION, p.OPT.SMILEY, p.OPT.RESERVED)
    preparsed_tweet = p.parse(tweet)
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
        invalid_tweets += 1
        return

    hash_removed_tweet = cleaned_tweet
    removed = 0
    num_hashtags = 0
    for hashtag in hashtags:
        # Remove '#' from the tweet but keep the word
        index = hashtag.start_index - removed
        hash_removed_tweet = hash_removed_tweet[:index] + hash_removed_tweet[(index + 1):]
        removed += 1
        # Count the hashtag occurrences
        if hashtag.end_index - hashtag.start_index > 1:  # So that just hashes are not included
            num_hashtags += 1
            hashtag_text = hashtag.match[1:]
            if hashtag_text in hashtag_counts:
                hashtag_counts[hashtag_text] += 1
            else:
                hashtag_counts[hashtag_text] = 1

    number_of_hashtags_in_tweet.append(num_hashtags)

    # Count mentions
    if preparsed_tweet.mentions:
        for mention in preparsed_tweet.mentions:
            mention_text = mention.match[1:]
            if mention_text in mention_counts:
                mention_counts[mention_text] += 1
            else:
                mention_counts[mention_text] = 1

    valid_tweets += 1
    words = hash_removed_tweet.split()
    number_of_words = len(words)
    total_words_in_valid_tweets += number_of_words
    number_of_words_in_tweets.append(number_of_words)

    # if number_of_words < min_word_tweet_count:
    #     min_word_tweet_count = number_of_words
    #     min_words_tweet = tweet
    if number_of_words > max_word_tweet_count:
        max_word_tweet_count = number_of_words
        max_words_tweet = tweet

    for word in words:
        if word in number_of_word_occurrences:
            number_of_word_occurrences[word] += 1
        else:
            number_of_word_occurrences[word] = 1

    if number_of_words in number_of_word_count_occurrences:
        number_of_word_count_occurrences[number_of_words] += 1
    else:
        number_of_word_count_occurrences[number_of_words] = 1

    if preparsed_tweet.emojis:
        number_of_tweets_with_emojis += 1
    if preparsed_tweet.smileys:
        number_of_tweets_with_smileys += 1
    if preparsed_tweet.mentions:
        number_of_tweets_with_mentions += 1
    if preparsed_tweet.reserved:
        number_of_tweets_with_RTs += 1
    if preparsed_tweet.urls:
        number_of_tweets_with_urls += 1


if __name__ == "__main__":
    with open(tweets_file_path, 'r') as ip_file:
        for cnt, tweet in enumerate(ip_file):
            process_tweet(tweet)

    # Compute mean
    mean = total_words_in_valid_tweets / valid_tweets

    # Compute median
    number_of_words_in_tweets.sort()
    if len(number_of_words_in_tweets) % 2 == 0:
        mid = int(len(number_of_words_in_tweets) / 2)
        median = (number_of_words_in_tweets[mid - 1] + number_of_words_in_tweets[mid]) / 2
    else:
        median = number_of_words_in_tweets[math.floor(len(number_of_words_in_tweets) / 2)]

    # Mode of words
    max_count = 0
    max_count_word = ''
    for (word, count) in number_of_word_occurrences.items():
        if count > max_count:
            max_count = count
            max_count_word = word

    # Mode of number of words in tweets
    max_number_of_words_count = 0
    max_number_of_words = 0
    for (number_of_words, count) in number_of_word_count_occurrences.items():
        if count > max_number_of_words_count:
            max_number_of_words_count = count
            max_number_of_words = number_of_words

    # Standard deviation of number of words
    sum_for_std_deviation = 0
    for number_of_words_in_tweet in number_of_words_in_tweets:
        sum_for_std_deviation += ((number_of_words_in_tweet - mean) ** 2)
    std_deviation = math.sqrt(sum_for_std_deviation / valid_tweets)

    sorted_hashtag_counts = sorted(hashtag_counts.items(), key=lambda kv:kv[1])
    sorted_mention_counts = sorted(mention_counts.items(), key=lambda kv:kv[1])

    print('Total number of tweets: %d' % total_tweets)
    print('Valid number of tweets: %d' % valid_tweets)
    print('Mean number of words: %f' % mean)
    print('Median number of words: %d' % median)
    print('Mode of words: %s' % max_count_word)
    print('Mode of number of words in tweets: %d' % max_number_of_words)
    print('Standard deviation of number of words: %f' % std_deviation)

    print('Number of tweets with emojis: %d' % number_of_tweets_with_emojis)
    print('Number of tweets with smileys: %d' % number_of_tweets_with_smileys)
    print('Number of tweets with RTs: %d' % number_of_tweets_with_RTs)
    print('Number of tweets with mentions: %d' % number_of_tweets_with_mentions)
    print('Number of tweets with urls: %d' % number_of_tweets_with_urls)
    print('Maximum number of words in a tweet: %d' % max_word_tweet_count)
    print('Max word tweet: %s' % max_words_tweet)
    # print('Minimum number of words in a tweet: %d' % min_word_tweet_count)
    # print('Min word tweet: %s' % min_words_tweet)
    k = 30
    print('Top %d most popular mentions:' % k)
    for i in range(1, k+1):
        print('Mention: %s, used %d times' % (sorted_mention_counts[-i][0], sorted_mention_counts[-i][1]))
    print('Top %d most popular hashtags:' % k)
    for i in range(1, k+1):
        print('Hashtag: %s, used %d times' % (sorted_hashtag_counts[-i][0], sorted_hashtag_counts[-i][1]))

    pickle.dump(sorted_hashtag_counts, open('sorted_hashtag_counts.p', 'wb'))
    pickle.dump(sorted_mention_counts, open('sorted_mention_counts.p', 'wb'))

    hashtag_distribution = {}
    for (hashtag, count) in sorted_hashtag_counts:
        if count in hashtag_distribution:
            hashtag_distribution[count] += 1
        else:
            hashtag_distribution[count] = 1

    reduced_distribution = {}

    for (k, v) in hashtag_distribution.items():
        if k < 20:
            reduced_distribution[k] = v

    plt.plot(reduced_distribution.keys(), reduced_distribution.values())
    plt.title('Plot of Number of Hashtag Occurrences')
    plt.xlabel("Number of occurrences")
    plt.ylabel("Number of hashtags")
    plt.savefig("hashtag_occurrences_plot.png")
    plt.show()

    mention_distribution = {}
    for (mention, count) in sorted_mention_counts:
        if count in mention_distribution:
            mention_distribution[count] += 1
        else:
            mention_distribution[count] = 1

    reduced_distribution = {}

    for (k, v) in mention_distribution.items():
        if k < 20:
            reduced_distribution[k] = v

    plt.clf()
    plt.plot(reduced_distribution.keys(), reduced_distribution.values())
    plt.title('Plot of Number of Mention Occurrences')
    plt.xlabel("Number of occurrences")
    plt.ylabel("Number of mentions")
    plt.savefig("mention_occurrences_plot.png")
    plt.show()
