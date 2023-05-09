#!/usr/bin/python3
"""Contains the count_words function"""

import requests


def count_words(subreddit, word_list, after=None):
    '''Prints counts of given words found in hot posts of a given subreddit.
    Args:
        subreddit (str): The subreddit to search.
        word_list (list): The list of words to search for in post titles.
        after (str): The parameter for the next page of the API results.
    '''
    user_agent = {'User-agent': 'test45'}
    if after is None:
        word_list = [word.lower() for word in word_list]
        found_list = []
    else:
        found_list = count_words(subreddit, word_list, after=after)

    posts = requests.get('http://www.reddit.com/r/{}/hot.json?after={}'
                         .format(subreddit, after), headers=user_agent)

    if posts.status_code == 200:
        posts = posts.json()['data']
        aft = posts['after']
        posts = posts['children']
        for post in posts:
            title = post['data']['title'].lower()
            for word in title.split(' '):
                if word.isalpha() and word.lower() in word_list:
                    found_list.append(word.lower())
        if aft is not None:
            found_list += count_words(subreddit, word_list, aft)
    return found_list


def print_results(found_list):
    '''Prints the counts of each word in the list, sorted by count and then alphabetically.'''
    result = {}
    for word in found_list:
        if word in result.keys():
            result[word] += 1
        else:
            result[word] = 1
    for key, value in sorted(result.items(), key=lambda item: (-item[1], item[0])):
        print('{}: {}'.format(key, value))


subreddit = 'learnpython'
word_list = ['Python', 'javascript', 'Java', 'SQL', 'CSS']
found_list = count_words(subreddit, word_list)
print_results(found_list)
