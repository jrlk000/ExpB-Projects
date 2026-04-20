from collections import deque

b = [1, 2, 3, 4, 5]
a = [3, 4, 5, 6 ,7]
counter = 0
step = 1
akk = list()

for idx_a, val_a in enumerate(a):
    #remaining list b is empty
    if len(b[counter:]) == 0:
        akk.extend(a[idx_a:])
        break

    #remaining elements are higher
    if val_a >= b[-1]:
        akk.extend(a[idx_a:])
        break


    #increase iterator in list, which is equivalent to an element is considered
    for val_b in b[counter:]:
        if val_a <= val_b:
            akk.append(val_a)
            break

        else:
            counter += step
            akk.append(val_b)

print(akk)


