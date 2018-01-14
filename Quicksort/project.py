"""
Name: QuickSort

Purpose: Do a partition based sort. Find a pivot in an array,
	     than sort all smaller elements to its left and all
	     bigger elements to its right.
"""

def partition(arr, low, high):
	
	pivot = arr[high]
	i = low

	for j in range(low, high):
		if arr[j] <= pivot:
			arr[j],arr[i] = arr[i],arr[j]
			i += 1

	arr[i],arr[high] = arr[high],arr[i]
	return i

def quicksort(arr, low, high):

	print("iteration")
	if low < high:
		pi = partition(arr, low, high)
		quicksort(arr, low, pi - 1)
		quicksort(arr, pi + 1, high)


def main():
	l = [10,30,20,80,60,100,120,150,130,110,200,180,190]
	quicksort(l, 0, len(l)-1)
	print(l)

if __name__ == "__main__":
	main()