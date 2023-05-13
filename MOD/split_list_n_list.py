class fc:
    def __init__(self, origin_list, Num) -> None:
        self.origin_list = origin_list
        self.Num = Num

    def split(self):
        if len(self.origin_list) % self.Num == 0:
            cnt = len(self.origin_list) // self.Num
        else:
            cnt = len(self.origin_list) // self.Num + 1

        for i in range(0, self.Num):
            yield self.origin_list[i*cnt:(i+1)*cnt]
