from random import random

def bubble_sort(A):
    n = len(A)
    for i in range(n):
        swapped = False
        for j in range(0, n-i-1):
            if A[j] > A[j+1]:
                A[j], A[j+1] = A[j+1], A[j]
                swapped = True
            yield A
        if not swapped:
            break

def linear_search(A, target=None):
    if target is None:
        target = random.choice(A)
    for i in range(len(A)):
        temp = list(A)
        temp[i] = max(A) + 5
        yield temp
        if A[i] == target:
            break
