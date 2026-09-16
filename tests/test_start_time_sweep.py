"""D1g 的最小单元测试(wave-10 轮 18):起点-时间分箱的数学。"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from benchmarks.start_time_sweep import time_bins


def test_time_bins_cover_all_steps_exactly_once():
    edges, bin_of = time_bins(160, 16)
    assert edges[0] == 0 and edges[-1] == 160
    assert all(edges[i] < edges[i + 1] for i in range(len(edges) - 1))
    assert len(bin_of) == 160
    assert sorted(bin_of) == [b for b in range(16) for _ in range(10)]


def test_time_bins_uneven_remainder_goes_to_last_bin():
    edges, bin_of = time_bins(161, 16)
    assert edges[-1] == 161
    assert len(bin_of) == 161
    assert max(bin_of) == 15          # no index outside the bin range
    assert min(bin_of) == 0
