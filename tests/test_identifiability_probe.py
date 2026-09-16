"""D3 的最小单元测试(wave-10 轮 10):Fisher 信息闭式解对中心差分。"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from benchmarks.identifiability_probe import fisher_j, fisher_j_fd


def test_closed_form_matches_finite_differences():
    for om in (0.7, 1.2, 1.8):
        ja = fisher_j(om, q0=0.8, p0=-0.5, t_obs=24, dt=0.1)
        jf = fisher_j_fd(om, q0=0.8, p0=-0.5, t_obs=24, dt=0.1)
        assert ja > 0.0
        assert abs(ja - jf) / ja < 1e-4


def test_fisher_grows_with_window_and_is_positive():
    j12 = fisher_j(1.2, 0.8, -0.5, t_obs=12, dt=0.1)
    j24 = fisher_j(1.2, 0.8, -0.5, t_obs=24, dt=0.1)
    assert j24 > j12 > 0.0   # longer window -> strictly more information
