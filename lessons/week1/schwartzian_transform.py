# The Schwartzian transform.


def schwartzian_sort(to_sort, transformer):
    # This code could be more concise, but it's easy to understand:
    pairs = [(transformer(item), item) for item in to_sort]
    sorted_pairs = sorted(pairs, key=lambda item: item[0])
    sorted_items = [pair[1] for pair in sorted_pairs]
    return sorted_items


# Here's a second version which is arguably more "Pythonic".
def schwartzian_generator(to_sort, transformer):
    from heapq import heappush, heappop
    min_heap = []
    for item in to_sort:
        heappush(min_heap, (transformer(item), item))
    while min_heap:
        yield heappop(min_heap)[1]


def main():
    def hashify(s):
        return sha512(s.encode('utf-8')).hexdigest()

    from hashlib import sha512

    # We want to sort the following strings in increasing order
    # ** with respect to their SHA512 hash values **:
    to_sort = ['It was the best of times',
               'it was the worst of times',
               'it was the age of wisdom',
               'it was the age of foolishness',
               'it was the epoch of belief',
               'it was the epoch of incredulity',
               'it was the season of Light',
               'it was the season of Darkness',
               'it was the spring of hope',
               'it was the winter of despair',
               'we had everything before us',
               'we had nothing before us']

    # Here is the obvious way to do it:
    result1 = sorted(to_sort, key=hashify)

    # Instead we use the Schwartzian transform:
    result2 = schwartzian_sort(to_sort, hashify)
    # result2 = list(schwartzian_generator(to_sort, hashify))

    # Both methods return the same result:
    assert result1 == result2, 'Inconsistent sorting methods?!?'
    print('\n'.join(result1))

    # Assuming hashify() is kind of slow, make sure you understand why the
    # Schwartzian transform is faster than simply calling sorted(), and why
    # its speed advantage increases as the list gets larger.


main()
