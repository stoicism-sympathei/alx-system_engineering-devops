#!/usr/bin/python3
"""Contains the count_words function"""
import requests


def count_words(subreddit, word_list, found_dict={}, after=None):
    '''Prints counts of given words found in hot posts of a given subreddit.
    Args:
        subreddit (str): The subreddit to search.
        word_list (list): The list of words to search for in post titles.
        found_dict (dict): Key/value pairs of words/counts.
        after (str): The parameter for the next page of the API results.
    '''
    user_agent = {'User-agent': 'test45'}
    url = 'https://www.reddit.com/r/{}/hot.json'.format(subreddit)
    if after is not None:
        url += '?after={}'.format(after)
    posts = requests.get(url, headers=user_agent)

    if posts.status_code == 404:
        print('Subreddit not found')
        return
    elif posts.status_code != 200:
        print('Error while fetching data from subreddit')
        return

    posts = posts.json()['data']
    aft = posts['after']
    posts = posts['children']

    if not found_dict:
        word_list = [word.lower() for word in word_list]

    for post in posts:
        title = post['data']['title'].lower()
        for word in title.split():
            if word in word_list:
                if word in found_dict:
                    found_dict[word] += 1
                else:
                    found_dict[word] = 1

    if aft is not None:
        count_words(subreddit, word_list, found_dict, aft)
    else:
        if not found_dict:
            print('No results found for given keywords')
        else:
            for key, value in sorted(found_dict.items(), key=lambda item: item[1], reverse=True):
                print('{}: {}'.format(key, value))
