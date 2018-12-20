import pickle

import preprocessor as p

import matplotlib.pyplot as plt

base_path = '/home/sarthak/Downloads/Twitter Datasets/1 - Cheng-Caverlee-Lee Scrape/twitter_cikm_2010/'
tweets_file_path = base_path + 'just_hashtagged_tweets.txt'

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

    print('Number of hashtags in tweets:')
    for kv in sorted_num_hashtags_distribution:
        print('%d hashtags in %d tweets' % (kv[0], kv[1]))

    plt.bar([k[0] for k in sorted_num_hashtags_distribution], [k[1] for k in sorted_num_hashtags_distribution])
    plt.title('Number of hashtags in tweets')
    plt.xlabel("Number of hashtags in a tweet")
    plt.ylabel("Number of tweets")
    plt.savefig("num_hashtags_bar.png")
    plt.show()

    k = 5
    top_k_distribution = []
    for kv in sorted_num_hashtags_distribution:
        if kv[0] <= k:
            top_k_distribution.append(kv)

    plt.bar([k[0] for k in top_k_distribution], [k[1] for k in top_k_distribution])
    plt.title('Number of hashtags in tweets (maximum 5 hashtags in a tweet)')
    plt.xlabel("Number of hashtags in a tweet")
    plt.ylabel("Number of tweets")
    plt.savefig("num_hashtags_top_5_bar.png")
    plt.show()

    over_k_distribution = []
    for kv in sorted_num_hashtags_distribution:
        if kv[0] > k:
            over_k_distribution.append(kv)

    plt.bar([k[0] for k in over_k_distribution], [k[1] for k in over_k_distribution])
    plt.title('Number of hashtags in tweets (over 5 hashtags in a tweet)')
    plt.xlabel("Number of hashtags in a tweet")
    plt.ylabel("Number of tweets")
    plt.savefig("num_hashtags_over_5_bar.png")
    plt.show()
