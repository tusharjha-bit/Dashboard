import numpy as np
import json

# ---------------- Parameters ----------------
TICKER = "NIFTY 50"
S0 = 24343.0
sigma_annual = 0.09
mu_annual = 0.09
n_sims = 10000
n_days = 30

np.random.seed(42)

dt = 1.0
mu_daily = mu_annual / 252
sigma_daily = sigma_annual / np.sqrt(252)

Z = np.random.standard_normal((n_sims, n_days))
daily_returns = (mu_daily - 0.5 * sigma_daily**2) * dt + sigma_daily * np.sqrt(dt) * Z
log_paths = np.cumsum(daily_returns, axis=1)
paths = S0 * np.exp(log_paths)
paths = np.hstack([np.full((n_sims, 1), S0), paths])

final_prices = paths[:, -1]

expected_price = final_prices.mean()
median_price = np.median(final_prices)
p5 = np.percentile(final_prices, 5)
p95 = np.percentile(final_prices, 95)
p_gain = (final_prices > S0).mean() * 100
p_loss = (final_prices < S0).mean() * 100
std_final = final_prices.std()

print(f"===== Monte Carlo GBM Simulation: {TICKER} =====")
print(f"Current Price       : {S0:,.2f}")
print(f"Annual Drift (mu)   : {mu_annual*100:.2f}%")
print(f"Annual Volatility   : {sigma_annual*100:.2f}%")
print(f"Simulations         : {n_sims:,}")
print(f"Horizon (days)      : {n_days}")
print("-" * 50)
print(f"Expected Price      : {expected_price:,.2f}")
print(f"Median Price        : {median_price:,.2f}")
print(f"Std Dev (final)     : {std_final:,.2f}")
print(f"P5  (5th pct)       : {p5:,.2f}")
print(f"P95 (95th pct)      : {p95:,.2f}")
print(f"P(gain)             : {p_gain:.2f}%")
print(f"P(loss)             : {p_loss:.2f}%")

# ---- 200 sample paths for chart 1 ----
n_plot_paths = 200
sample_idx = np.random.choice(n_sims, n_plot_paths, replace=False)
sample_paths = paths[sample_idx]
sample_final = sample_paths[:, -1]
sample_colors = np.where(sample_final > S0, "green", "red")

mean_path = paths.mean(axis=0)

# ---- histogram bins for chart 2 ----
hist_counts, hist_edges = np.histogram(final_prices, bins=50)
bin_centers = (hist_edges[:-1] + hist_edges[1:]) / 2

lower_band = S0 * 0.95
upper_band = S0 * 1.05

bar_colors = []
for c in bin_centers:
    if c < lower_band:
        bar_colors.append("red")
    elif c > upper_band:
        bar_colors.append("green")
    else:
        bar_colors.append("blue")

output = {
    "ticker": TICKER,
    "params": {
        "S0": S0, "mu_annual": mu_annual, "sigma_annual": sigma_annual,
        "n_sims": n_sims, "n_days": n_days,
        "mu_daily": mu_daily, "sigma_daily": sigma_daily,
    },
    "stats": {
        "expected_price": round(expected_price, 2),
        "median_price": round(median_price, 2),
        "std_final": round(std_final, 2),
        "p5": round(p5, 2),
        "p95": round(p95, 2),
        "p_gain": round(p_gain, 2),
        "p_loss": round(p_loss, 2),
    },
    "sample_paths": sample_paths.round(2).tolist(),
    "sample_colors": sample_colors.tolist(),
    "mean_path": mean_path.round(2).tolist(),
    "hist_counts": hist_counts.tolist(),
    "hist_centers": bin_centers.round(2).tolist(),
    "hist_colors": bar_colors,
    "hist_bin_width": round(hist_edges[1] - hist_edges[0], 2),
}


with open("mc_output.json", "w") as f:
    json.dump(output, f)

print("\nData exported to mc_output.json")

