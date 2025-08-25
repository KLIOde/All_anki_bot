n, m = list(map(int, input().split()))
res = {i: [] for i in range(1, n+1)}
R = {i: [] for i in range(1, n+1)}
for i in range(m):
    s = list(map(int, input().split()))
    res[s[0]].append(s[1])
if m % 2 == 1:
    print(-1)
else:
    visit = set()
    def razv(k):
        if len(res[k]) % 2 == 0:
            return False
        else:
            return True
    print(res)
    C = 0
    for i in res:
        V  =0 
        while len(res[i]) % 2 != 0 and (i not in visit) and V <= len(res[i]):
            k = (res[i]).pop(0)
            if razv(k):
                res[k].append(i)
                visit.add(i)
            else:
                res[i].append(k)
                V += 1
            if V > len(res[i]):
                C = -1
    #print(res)
    if C != -1:
        for i in res:
            for j in range(len(res[i])):
                print(i, res[i][j])
    else:
        print(C)
# n = int(input())
# potok = [0 for _ in range(n)]
# l = [0 for _ in range(n)]
# r = [0 for _ in range(n)]
# for i in range(n):
#     s = list(map(int, input().split()))
#     potok[i] = s[2]
#     l[i] = s[0]
#     r[i] = s[1]

# def bfs(i):
#     ul = [0 for _ in  range(n)]
#     ur = [0 for _ in range(n)]
#     S = [0 for _ in range(n)]
#     S[i] = potok[i]
#     res = potok[i]
#     start = [i]
#     vis = set()
#     while start:
#         k = start.pop(0)
#         if ur[k] < r[k]:
#             if k < n-1:
#                 a = r[k] - ur[k]
#                 b = potok[k+1] - S[k+1]
#                 f = min(a, b)
#                 S[k+1] += f
#                 res+=f
#                 ur[k] += f
#                 if S[k+1] == potok[k+1]:
#                     if k+1 not in vis:
#                         start.append(k+1)
#                         vis.add(k+1)
#         if ul[k] < l[k]:
#             if k > 0:
#                 a = l[k] - ul[k]
#                 b = potok[k-1] - S[k-1]
#                 f = min(a, b)
#                 S[k-1] += f
#                 res+=f
#                 ul[k] += f
#                 if S[k-1] == potok[k-1]:
#                     if k-1 not in vis:
#                         start.append(k-1)
#                         vis.add(k-1)
#     return res
# res = []
# for i in range(n):
#     res.append(bfs(i))
# print(max(res))
# def dp_govno(mod):
#     res[0] = 1
#     lll = {}
#     print(res)
#     for i in range(1, n+1):
#         if s[i-1] in lll:
#             res[i] = ((res[i-1] * 2 - res[lll[s[i-1]]]) % mod)
#         else:
#             res[i] = ((res[i-1]* 2) % mod)
#         print(res)
#         lll[s[i-1]] = i
#     return res
# n = int(input())
# s = list(map(int, input().split()))
# res = [0 for i in range(n+1)]
# print(round(max(dp_govno(mod = 10e9 + 7))-1))

# n = int(input())
# def merge(l, r):
#     i,j = 0,0
#     res = []
#     ll, rr = len(l), len(r)
#     while i < ll and j < rr:
#         if l[i] < r[j]:
#             res.append(l[i])
#             i += 1
#         else:
#             res.append(r[j])
#             j+=1
#     res.extend(l[i:])
#     res.extend(r[j:])
#     return res
# def merge_sort(s):
#     if len(s) == 0 or len(s) == 1:
#         return s
#     m = len(s)//2
#     left = merge_sort(s[:m])
#     right = merge_sort(s[m:])
#     res = merge(left, right)
#     return res
# d = list(str(n))
# res = merge_sort(d)
# print(res)
# i = 0 
# while i < n:
#     if res[i] != '0':
#         res[i], res[0] = res[0], res[i]
#         break
#     i+=1
# print(res)
# def bfs(start):
#     S = [0] * n
#     u_l = [0] * n
#     u_r = [0] * n
#     S[start] = potok[start]
#     queue = [start]
#     res = potok[start]  
#     visited = set()
#     while queue:
#         k = queue.pop(0) 
#         if k > 0 and u_l[k] < l[k]:
#             a = l[k] - u_l[k]
#             b = potok[k-1] - S[k-1] 
#             f = min(a, b)
#             S[k-1] += f
#             u_l[k] += f
#             res += f
#             if S[k-1] == potok[k-1] and (k-1 not in visited):
#                 queue.append(k-1)
#                 visited.add(k-1)
#         if k < n-1 and u_r[k] < r[k]: 
#             a = r[k] - u_r[k]
#             b = potok[k+1] - S[k+1]
#             f = min(a, b)
#             S[k+1] += f
#             u_r[k] += f
#             res += f
#             if S[k+1] == potok[k+1] and (k+1 not in visited):
#                 queue.append(k+1)
#                 visited.add(k+1)
#     return res

# n = int(input())
# l = [0] * (n)
# r = [0] * (n)
# potok = [0] * (n)
# for k  in range(n):
#     s = list(map(int, input().split()))
#     potok[k] = s[2]
#     l[k], r[k] = s[0], s[1]
# RRR = []
# for i in range(n):
#     RRR.append(bfs(i))
# print(RRR)

# n, k = list(map(int, input().split()))
# MOD = 10**9 + 7
# ma = 190
# C = [[0] * (ma+1) for _ in range(ma+1)]
# for i in range(ma+1):
#     C[i][0] = 1
#     for j in range(1, i + 1):
#         C[i][j] = (C[i - 1][j] + C[i - 1][j - 1]) % MOD
# dp = [0] * (n+1)
# dp[0] = 1
# for a in range(1, n+1):
#     for j in range(n,-1,-1):
#         if dp[j] == 0:
#             continue
#         c = 1
#         while j + a * c <= n:
#             comb = C[c + k - 1][k - 1]
#             dp[j + a * c] = (dp[j + a * c] + dp[j] * comb) % MOD
#             c += 1
#             print(dp)
# print(dp[n] % MOD)

# n = int(input())
# s = list(map(int, input().split()))

# dp = [0] * (n + 1)
# dp[0] = 1
# last = {}

# for i in range(1, n + 1):
#     dp[i] = (2 * dp[i - 1])
#     dp[i] %= (10**9 + 7)

#     if s[i-1] in last:
#         p = last[s[i-1]]
#         dp[i] = dp[i]-dp[p-1] + (10**9 + 7) 
#         dp[i] %= (10**9 + 7)
#     last[s[i-1]] = i
# print(dp)
# print((dp[n]-1) % (10**9 + 7))
# def merge(left, right):
#     res = []
#     i, j = 0, 0
#     while i < len(left) and j < len(right):
#         if left[i] <= right[j]:
#             res.append(left[i])
#             i += 1
#         else:
#             res.append(right[j])
#             j += 1
#     res.extend(left[i:])
#     res.extend(right[j:])
#     return res

# def merge_sort(arr):
#     if len(arr) <= 1:
#         return arr
    
#     mid = len(arr) // 2
#     left = merge_sort(arr[:mid])
#     right = merge_sort(arr[mid:])
#     return merge(left, right)
# def quick(n):
#     d = list(str(n))
#     s = merge_sort(d)
#     for i in range(len(s)):
#         if s[i] != '0':
#             s[0], s[i] = s[i], s[0]
#             break
    
#     return int(''.join(s))

# n = input()
# print(quick(n))


# n = int(input())
# for i in range(n):
#     m = int(input())
#     s = list(map(int, input().split()))
#     a = max(s)
#     res = 0
#     for j in range(m):
#         if s[j] < a:
#             res += s[j]
#     if res % 2 == 0:
#         print('Second')
#     else:
#         print('First')



# n, k = 3, 2#list(map(int, input().split()))
# res = [[0 for i in range(n)] for j in range(k)]
# for i in range(k):
#     res[i][0] = 1
# for j in range(n):
#     res[0][j] = 1
# print(res)
# for i in range(k):
#     for j in range(n):
#         if j == 0:
#             res[i][j] += res[i-1][j]
#         print(res)
# n = int(input())

# # Чтение данных
# a = []
# l = []  # l[i] — канал из i+1 в i (для i от 1 до n-1)
# r = []  # r[i] — канал из i в i+1 (для i от 0 до n-2)

# for i in range(n):
#     data = list(map(int, input().split()))
#     if i == 0:
#         a.append(data[0])
#         r.append(data[1])
#     elif i == n-1:
#         a.append(data[0])
#         l.append(data[1])
#     else:
#         a.append(data[0])
#         l.append(data[1])
#         r.append(data[2])

# # Добавим недостающие элементы
# if len(l) < n:
#     l.append(0)
# if len(r) < n:
#     r.append(0)

# max_water = 0

# # Попробуем каждый резервуар как источник
# for start in range(n):
#     # water[i] — сколько воды в резервуаре i
#     water = [0] * n
#     # used_l[i] — сколько воды прошло через канал l[i] (из i+1 в i)
#     used_l = [0] * n
#     # used_r[i] — сколько воды прошло через канал r[i] (из i в i+1)
#     used_r = [0] * n
    
#     # Используем очередь для BFS
#     from collections import deque
#     q = deque([start])
    
#     total = 0
#     while q:
#         i = q.popleft()
#         # Если резервуар не заполнен, заполняем его
#         if water[i] < a[i]:
#             fill = a[i] - water[i]
#             water[i] += fill
#             total += fill
            
#             # Вода может течь вправо
#             if i < n-1 and used_r[i] < r[i]:
#                 flow = min(fill, r[i] - used_r[i])
#                 used_r[i] += flow
#                 if water[i+1] < a[i+1]:
#                     water[i+1] += flow
#                     if water[i+1] < a[i+1]:
#                         q.append(i+1)
#                     else:
#                         q.append(i+1)
            
#             # Вода может течь влево
#             if i > 0 and used_l[i] < l[i]:
#                 flow = min(fill, l[i] - used_l[i])
#                 used_l[i] += flow
#                 if water[i-1] < a[i-1]:
#                     water[i-1] += flow
#                     if water[i-1] < a[i-1]:
#                         q.append(i-1)
#                     else:
#                         q.append(i-1)
    
#     max_water = max(max_water, total)

# print(max_water)




# n = int(input())
# s = list(map(int, input().split()))
# dp = [0] * (n+1)
# dp[0] = 1
# last =  {}
# for i in  range(1, n+1):
#     if s[i-1] in last:
#         dp[i-1] -= dp[last[s[i-1]]-1]
#         #print('!', dp, last[s[i-1]])
#     dp[i] = 2 * dp[i-1]
#     last[s[i-1]] = i
#     #print(dp, last)
# print(dp[-1] - 1)