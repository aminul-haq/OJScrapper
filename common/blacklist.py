from datetime import datetime

blacklist_map = {}


def add_to_blacklist(jti):
    timestamp = datetime.now().timestamp()
    blacklist_map[jti] = timestamp


def is_blacklisted(jti):
    return jti in blacklist_map


def remove_old_tokens():
    timestamp = datetime.now().timestamp()
    deleted = []
    for token in blacklist_map:
        if timestamp - blacklist_map[token] > 604800:  # added on 7 or more days ago
            deleted.append(token)
    for token in deleted:
        del blacklist_map[token]
