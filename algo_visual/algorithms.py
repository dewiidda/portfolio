import random

print("DEBUG RANDOM =", random)
print("DEBUG FILE =", __file__)

def bubble_sort(arr):
    A = arr.copy()
    n = len(A)

    for i in range(n):
        swapped = False
        for j in range(n-i-1):
            if A[j] > A[j+1]:
                A[j], A[j+1] = A[j+1], A[j]
                swapped = True
            yield A.copy(), (j, j+1), None
        if not swapped:
            break
    yield A.copy(), None, None

def linear_search(arr, target=None):
    A = arr.copy()
    if target is None:
        target = random.choice(A)
    for i in range(len(A)):
        if A[i] == target:
            yield A.copy(), (i,), i
            return
        yield A.copy(), (i,), None
    yield A.copy(), None, None
