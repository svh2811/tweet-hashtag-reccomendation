cat test_set_tweets.txt training_set_tweets.txt | grep "#" >> all_hashtagged_tweets.txt
awk -F "\t" 'NF {print $3}' all_hashtagged_tweets.txt >> just_hashtagged_tweets.txt
sed '378271d' just_hashtagged_tweets.txt