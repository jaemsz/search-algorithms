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
            res = self.isMatch(idx, pat)
            if res == 0:
                ret = []
                m = mid
                while m >= 0 and not self.isMatch(self.suffixIdxs[m], pat):
                    ret.append(self.suffixIdxs[m])
                    m -= 1
                m = mid+1
                while m < len(self.suffixIdxs) and not self.isMatch(self.suffixIdxs[m], pat):
                    ret.append(self.suffixIdxs[m])
                    m += 1
                ret.sort()
                return ret
            elif res < 0:
                hi = mid-1
            else:
                lo = mid+1
        return []

    def isMatch(self, idx, pat):
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
