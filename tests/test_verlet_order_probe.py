"""VERLET-ORDER 探针单元测试(轮 104):观测阶数契约。"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from benchmarks.verlet_order_probe import observed_orders, verlet_rollout


def test_energy_drift_shrinks_at_second_order():
    """energy drift 相邻折半的 log2 阶 ∈ [1.8, 2.2](2 阶辛积分器契约)。"""
    errs = []
    for dt in (0.2, 0.1, 0.05):
        k = round(10.0 / dt)
        _, hs = verlet_rollout(0.7, -0.4, 1.3, dt, k)
        h0 = 0.5 * 0.4 ** 2 + 0.5 * 1.3 ** 2 * 0.7 ** 2
        errs.append(abs(hs[-1] - h0) / h0)
    orders = observed_orders(errs)
    assert all(1.8 <= p <= 2.2 for p in orders), orders


def test_rollout_rmse_second_order_and_mse_fourth():
    """点均位移误差 O(h²) ⇒ RMSE 阶 2、MSE(平方量)阶 4——轮 104 排查:
    平方指标使观测阶翻倍,不是实现异常(能量轴与 RMSE 轴同判 2 阶)。"""
    q0, p0, w = 0.7, -0.4, 1.3
    errs = []
    for dt in (0.2, 0.1, 0.05):
        k = round(10.0 / dt)
        qs, _ = verlet_rollout(q0, p0, w, dt, k)
        t = [i * dt for i in range(k + 1)]
        q_exact = [q0 * math.cos(w * ti) + (p0 / w) * math.sin(w * ti)
                   for ti in t]
        errs.append(sum((a - b) ** 2 for a, b in zip(qs, q_exact)) / len(qs))
    rmse_orders = observed_orders([math.sqrt(e) for e in errs])
    assert all(1.8 <= p <= 2.2 for p in rmse_orders), rmse_orders
    mse_orders = observed_orders(errs)
    assert all(3.8 <= p <= 4.2 for p in mse_orders), mse_orders
