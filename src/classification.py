import time
from collections import deque

# global empty queue is initialized upon library load.
from statistics import mode

import numpy as np

hands_maxlen = 10
min_sign_consistency = 7
hands = deque(maxlen=hands_maxlen)
time_since_last_action = time.time()
repeated_action = None


# hands are appended to a queue with a maximum length of 10, this means it takes at most 10 frames
# before the algorithm is primed for an appropriate response, but also makes it easier to ensure that the sign is valid.
def classification(hand):
    global hands, time_since_last_action
    hands.append(hand)
    if len(hands) < hands_maxlen:
        return None
    latest_hand = hands.popleft()
    if latest_hand is None or latest_hand.get_sign() is None:
        # If no hand or sign is found, no action can be performed this frame
        return None

    signs = [(h.get_sign() if h is not None else h) for h in hands]
    estimated_sign = estimate_sign_consistency(signs)
    return estimated_sign


def estimate_sign_consistency(list):
    if not list:
        return None
    unique_signs = []
    unique_sign_avg_index = []
    sign_count = []

    for i, sign in enumerate(list):
        if sign not in unique_signs:
            unique_signs.append(sign)
    for sign in unique_signs:
        sign_count.append(list.count(sign))
        list_of_indices = [i for i, x in enumerate(list) if x == sign]
        unique_sign_avg_index.append(sum(list_of_indices)/len(list_of_indices))
    index_most_reccuring = max(range(len(sign_count)), key=sign_count.__getitem__)
    print(f'The most reccuring value is {unique_signs[index_most_reccuring]}')
    if sign_count[index_most_reccuring] >= min_sign_consistency:
        return unique_signs[index_most_reccuring]
    else:
        return None

