#by bearophile from http://code.activestate.com/recipes/572156-bk-tree/

def getDistance(s1, s2):
    if s1 == s2: return 0 # this is fast in Python

    if len(s1) > len(s2):
        s1, s2 = s2, s1
    r1 = range(len(s2) + 1)
    r2 = [0] * len(r1)
    i = 0
    for c1 in s1:
        r2[0] = i + 1
        j = 0
        for c2 in s2:
            if c1 == c2:
                r2[j + 1] = r1[j]
            else:
                a1 = r2[j]
                a2 = r1[j]
                a3 = r1[j + 1]
                if a1 > a2:
                    if a2 > a3:
                        r2[j + 1] = 1 + a3
                    else:
                        r2[j + 1] = 1 + a2
                else:
                    if a1 > a3:
                        r2[j + 1] = 1 + a3
                    else:
                        r2[j + 1] = 1 + a1
            j += 1
        aux = r1;
        r1 = r2;
        r2 = aux
        i += 1

    return r1[-1]


