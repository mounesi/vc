


f = [1, 2, 3, 4, 5, 6, 8, 7, 9, 10, 11, 12, 13, 14, 15] # freq vector
print(f)
a = [4.94, 15]
b = [8, 2, 1 ] 

b_v = []
for j, a_j in enumerate(a):
    for i, f_i in enumerate(f):
        if f_i <= a_j: 
            b_v.append(b[j])
        else:
            f = f[i:]
            print(f)
            break

print(b_v)
print(len(b_v))










































