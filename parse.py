

def parse_results(file):
    t = "Traversal"
    r = "Rotations"
    ts = []
    rs = []
    with open(file) as f:
        for line in f:
            if t in line:
                ts.append(int(line.split(":")[-1].strip()))
            if r in line:
                rs.append(int(line.split(":")[-1].strip()))
    return ts, rs

def main():
    ts, rs=parse_results("results_avl.txt")

    print("Max traversal: %d" % max(ts))
    print("Average traversal: %f" % (float(sum(ts)) / len(ts)))

    print("Max rotations: %d" % max(rs))
    print("Average rotations: %f" % (float(sum(rs)) / len(rs)))


if __name__ == '__main__':
    main()
