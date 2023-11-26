from collections import defaultdict
import sys

class SuffixSearch:
    def __init__(self, txt):
        self.txt = txt
        self.suffixIdxs = []
        self.init()

    def init(self):
        suffixToIdx = defaultdict(int)
        for i in range(len(self.txt)):
            suffix = self.txt[i:]
            suffixToIdx[suffix] = i
        suffixes = list(suffixToIdx.keys())
        suffixes.sort()
        for suffix in suffixes:
            i = suffixToIdx[suffix]
            self.suffixIdxs.append(i)

    def search(self, pat):
        if len(pat) > len(self.txt):
            return []
        lo = 0
        hi = len(self.suffixIdxs)-1
        while lo <= hi:
            mid = (lo+hi)//2
            idx = self.suffixIdxs[mid]
            res = self.isSuffix(idx, pat)
            if res == 0:
                ret = []
                mu, u = self.searchUpper(pat, 0, mid-1)
                ml, l = self.searchLower(pat, mid+1, len(self.suffixIdxs)-1)
                if mu != -1 and ml != -1:
                    for m in range(mu, ml+1):
                        ret.append(self.suffixIdxs[m])
                elif mu != -1:
                    for m in range(mu, mid+1):
                        ret.append(self.suffixIdxs[m])
                elif ml != -1:
                    for m in range(mid, ml+1):
                        ret.append(self.suffixIdxs[m])
                else:
                    ret.append(idx)
                ret.sort()
                return ret
            elif res < 0:
                hi = mid-1
            else:
                lo = mid+1
        return []

    def searchUpper(self, pat, lo, hi):
        while lo <= hi:
            mid = (lo+hi)//2
            idx = self.suffixIdxs[mid]
            res = self.isSuffix(idx, pat)
            if res == 0:
                if mid-1 >= 0:
                    idx2 = self.suffixIdxs[mid-1]
                    res2 = self.isSuffix(idx2, pat)
                    if res2 != 0:
                        return mid,idx
                    hi = mid-1
                else:
                    return mid,idx
            elif res < 0:
                hi = mid-1
            else:
                lo = mid+1
        return -1,-1

    def searchLower(self, pat, lo, hi):
        while lo <= hi:
            mid = (lo+hi)//2
            idx = self.suffixIdxs[mid]
            res = self.isSuffix(idx, pat)
            if res == 0:
                if mid+1 < len(self.suffixIdxs):
                    idx2 = self.suffixIdxs[mid+1]
                    res2 = self.isSuffix(idx2, pat)
                    if res2 != 0:
                        return mid,idx
                    lo = mid+1
                else:
                    return mid,idx
            elif res < 0:
                hi = mid-1
            else:
                lo = mid+1
        return -1,-1

    def isSuffix(self, idx, pat):
        i, m = idx, len(self.txt)
        j, n = 0, len(pat)
        while i < m and j < n:
            if self.txt[i] < pat[j]:
                return 1
            elif self.txt[i] > pat[j]:
                return -1
            i += 1
            j += 1
        return 0 if j == len(pat) else 1

def main(txt, pat):
    ss = SuffixSearch(txt)
    res = ss.search(pat)
    out = []
    i, j = 0, 0
    while i < len(txt) and j < len(res):
        if i != res[j]:
            out.append(txt[i])
        else:
            out.append(f"[{txt[i]}]")
            j += 1
        i += 1
    while i < len(txt):
        out.append(txt[i])
        i += 1 
    print("".join(out))

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
