

def parse_results(file):
    t = "Traversal"
    res = []
    with open(file) as f:
        for line in f:
            if t in line:
                res.append(int(line.split(":")[-1].strip()))
    return res

def main():
    res=parse_results("results_avl.txt")
    print(max(res))
    print(float(sum(res)) / len(res))

if __name__ == '__main__':
    main()
