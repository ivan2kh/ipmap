from intervaltree import IntervalTree, Interval

class IpTree:
    def __init__(self):
        self.tree = IntervalTree()

    def add_interval(self, begin, end, data):
        interval = Interval(begin, end, data)
        overlapped = self.tree[interval.begin: interval.end]
        for o in overlapped:
            if o.contains_interval(interval):
                return
            elif interval.contains_interval(o):
                self.tree.remove(o)
        self.tree.chop(interval.begin, interval.end)
        self.tree.add(interval)

    def update_w(self):
        for i in self.tree.all_intervals:
            i.data['w'] = i.end - i.begin

    def get_all(self):
        return self.tree.all_intervals



