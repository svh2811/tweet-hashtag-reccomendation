import pickle
import matplotlib.pyplot as plt

sorted_hashtag_counts = pickle.load(open("sorted_hashtag_counts.p", "rb"))
sorted_mention_counts = pickle.load(open("sorted_mention_counts.p", "rb"))

k = 30
print('Top %d most popular hashtags:' % k)
for i in range(1,k+1):
    print('Hashtag: %s, used %d times' % (sorted_hashtag_counts[-i][0], sorted_hashtag_counts[-i][1]))

hashtag_distribution = {}

for (hashtag, count) in sorted_hashtag_counts:
    if count in hashtag_distribution:
        hashtag_distribution[count] += 1
    else:
        hashtag_distribution[count] = 1

reduced_distribution = {}

for (k, v) in hashtag_distribution.items():
    if k < 10:
        reduced_distribution[k] = v

plt.plot(reduced_distribution.keys(), reduced_distribution.values())
plt.title('Plot of number of hashtag occurrences')
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
plt.title('Plot of number of mention occurrences')
plt.xlabel("Number of occurrences")
plt.ylabel("Number of mentions")
plt.savefig("mention_occurrences_plot.png")
plt.show()
