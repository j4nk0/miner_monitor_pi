from status import *

class HashboardView:
    
    def __init__(self, status):
        self.hw_errors = int(status.hw_errors)
        self.temp_pcb = int(status.temp_pcb)
        self.temp_chip = int(status.temp_chip)
        self.chip_status = status.chip_status

    def max_temp(self):
        return max(self.temp_pcb, self.temp_chip)

    def failed_chip_count(self):
        count = 0
        for chip in self.chip_status:
            if chip != 'o' and chip != ' ': count += 1
        return count
            
class PoolView:

    def __init__(self, status):
        self.url = status.url
        self.worker = status.worker
        self.accepted = int(status.accepted)
        self.rejected = int(status.rejected)
        self.stales = int(status.stales)

    def total(self):
        return self.accepted + self.rejected + self.stales

    def rejected_quotient(self):
        return (self.rejected + self.stales) / self.total()

    def rejection_rate_ok(self):
        return self.rejected_quotient() < 0.1

class MinerView:

    def __init__(self, status):
        self.datetime = status.datetime     # parse ???
        self.hashrate = int(float(status.hashrate))
        self.elapsed_time = self.parse_elapsed(status.elapsed_time)
        self.fan1_rpm = int(status.fan1_rpm)
        self.fan2_rpm = int(status.fan2_rpm)
        self.pools = [ PoolView(p) for p in status.pools ]
        self.hashboards = [ HashboardView(h) for h in status.hashboards ]

    @staticmethod
    def parse_elapsed(time_str):
        total_seconds = 0
        d_idx = time_str.find('d')
        if d_idx > 0:
            total_seconds += 60*60*24* int(time_str[:d_idx])
            time_str = time_str[d_idx + 1:]
        h_idx = time_str.find('h')
        if h_idx > 0:
            total_seconds += 60*60* int(time_str[:h_idx])
            time_str = time_str[h_idx + 1:]
        m_idx = time_str.find('m')
        if m_idx > 0:
            total_seconds += 60* int(time_str[:m_idx])
            time_str = time_str[m_idx + 1:]
        s_idx = time_str.find('s')
        if s_idx > 0:
            total_seconds += int(time_str[:s_idx])
        return total_seconds

    def max_temp(self):
        temp = 0
        for h in self.hashboards:
            if h.max_temp() > temp: temp = h.max_temp()
        return temp

    def failed_chip_count(self):
        count = 0
        for h in self.hashboards:
            count += h.failed_chip_count()
        return count

    def boards_ok(self):
        return self.failed_chip_count() == 0

    def rejected_quotient(self):
        total = 0
        failed = 0
        for p in self.pools:
            total += p.total()
            failed += p.rejected
            failed += p.stales
        return failed / total

    def rejection_rate_ok(self):
        return self.rejected_quotient() < 0.1

if __name__ == '__main__':
    hbs = Hashboard_status(5, 87, 93, ' oo ooo ')
    ps = Pool_status('litecoinpool.org', 'zosimus.1', 58, 23, 4)
    ms = Miner_status(datetime.now(), 500, '1h05m34s', 200, 300, [ ps for _ in range(3) ], [ hbs for _ in range(4) ])
    mv = Miner_view(ms)
    print(mv.elapsed_time)
    print(mv.max_temp())
    print(mv.failed_chip_count())
    print(mv.boards_ok())
    print(mv.rejected_quotient())
    print(mv.rejection_rate_ok())

