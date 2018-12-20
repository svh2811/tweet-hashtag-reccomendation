import pickle

import preprocessor as p

base_path = '/home/sarthak/Downloads/Twitter Datasets/1 - Cheng-Caverlee-Lee Scrape/twitter_cikm_2010/'
tweets_file_path = base_path + 'just_hashtagged_tweets.txt'

output_file_path = base_path + 'num_hashtags.csv'

if __name__ == "__main__":
    load_from_disk = 'yes'
    num_hashtags_distribution = {}
    if load_from_disk == 'yes':
        num_hashtags_distribution = pickle.load(open("num_hashtag_distribution.p", "rb"))
    else:
        with open(tweets_file_path, 'r') as ip_file:
            for cnt, tweet in enumerate(ip_file):
                # Set tweet preprocessor options to remove all of the below
                p.set_options(p.OPT.URL, p.OPT.EMOJI, p.OPT.MENTION, p.OPT.SMILEY, p.OPT.RESERVED)
                cleaned_tweet = p.clean(tweet)
                p.set_options(p.OPT.HASHTAG)
                parsed_tweet = p.parse(cleaned_tweet)
                hashtags = parsed_tweet.hashtags
                if hashtags is None:
                    continue
                num_hashtags = len(hashtags)
                if num_hashtags in num_hashtags_distribution:
                    num_hashtags_distribution[num_hashtags] += 1
                else:
                    num_hashtags_distribution[num_hashtags] = 1
        pickle.dump(num_hashtags_distribution, open('num_hashtag_distribution.p', 'wb'))
    sorted_num_hashtags_distribution = sorted(num_hashtags_distribution.items(), key=lambda kv:kv[0])

    with open(tweets_file_path, 'w+') as op_file:
        for (k,v) in sorted_num_hashtags_distribution:
            op_file.write('%s\t%d\n' % (k,v))
