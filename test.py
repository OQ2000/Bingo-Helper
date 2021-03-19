lst = [8, 68, 130]

for item in lst:
    print("item", item)
    if item < 20:
        print("top")
    if item > 20 and item < 90:
        print("middle")
    if item > 91:
        print("bottom")

