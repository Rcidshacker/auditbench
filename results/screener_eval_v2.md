# Screener evaluation v2 (frozen protocol, PLAN.md phase 3)

Nebius Token Factory. Each item's excerpt is placed first in a five-section technical file. False clearance (FC) = expert non-compliant item (median expert < 4) scored >= 4. False rejection (FR) = expert-compliant item scored <= 2. Brackets: 95% item-bootstrap CI.

## Split: test

| condition | method | n | QWK | MAE | FC | FR | review rate | calls/item |
|---|---|---|---|---|---|---|---|---|
| headed | Whole-file Nano, 1 call | 60 | 0.422 | 1.02 | 47.2% [31%, 64%] (17/36) | 4.2% |  | 1.0 |
| headed | Whole-file Nano, median of 3 | 60 | 0.482 | 0.88 | 38.9% [25%, 56%] (14/36) | 0.0% |  | 3.0 |
| headed | Whole-file Ultra, 1 call | 60 | 0.765 | 0.63 | 11.1% [3%, 22%] (4/36) | 4.2% |  | 1.0 |
| headed | Per-section Nano, 1 sample (ablation) | 60 | 0.480 | 0.98 | 5.6% [0%, 14%] (2/36) | 25.0% |  | 1.0 |
| headed | Per-section Nano, median of 3, no escalation (ablation) | 60 | 0.632 | 0.77 | 5.6% [0%, 14%] (2/36) | 16.7% |  | 3.0 |
| headed | Screener (full) | 60 | 0.721 | 0.63 | 0.0% [0%, 0%] (0/36) | 20.8% | 12% | 3.2 |
| plain | Whole-file Nano, 1 call | 60 | 0.184 | 1.22 | 52.8% [36%, 69%] (19/36) | 4.2% |  | 1.0 |
| plain | Whole-file Ultra, 1 call | 60 | 0.716 | 0.65 | 11.1% [3%, 22%] (4/36) | 4.2% |  | 1.0 |
| titled | Screener as shipped (no headings found: whole text) | 60 | 0.774 | 0.66 | 0.0% [0%, 0%] (0/36) | 8.3% | 22% | 3.3 |
| titled | Screener + segmenter | 60 | 0.757 | 0.67 | 8.3% [0%, 19%] (3/36) | 8.3% | 23% | 4.2 |
| plain | Screener as shipped (no headings found: whole text) | 60 | 0.824 | 0.52 | 0.0% [0%, 0%] (0/36) | 8.3% | 22% | 3.4 |
| plain | Screener + segmenter | 60 | 0.800 | 0.57 | 2.8% [0%, 8%] (1/36) | 16.7% | 15% | 4.2 |

Paired difference in FC vs the Screener (headed), on expert non-compliant items. Positive = the other method clears more violations. Item and cluster (8 systems) bootstrap.

| condition | method | FC diff | 95% CI (item) | 95% CI (cluster) | excludes 0 (item) |
|---|---|---|---|---|---|
| headed | Whole-file Nano, 1 call | +47.2% | [+30.6%, +63.9%] | [+37.8%, +54.1%] | yes |
| headed | Whole-file Nano, median of 3 | +38.9% | [+25.0%, +55.6%] | [+27.8%, +50.0%] | yes |
| headed | Whole-file Ultra, 1 call | +11.1% | [+2.8%, +22.2%] | [+0.0%, +25.7%] | yes |
| headed | Per-section Nano, 1 sample (ablation) | +5.6% | [+0.0%, +13.9%] | [+0.0%, +16.7%] | no |
| headed | Per-section Nano, median of 3, no escalation (ablation) | +5.6% | [+0.0%, +13.9%] | [+0.0%, +11.1%] | no |
| plain | Whole-file Nano, 1 call | +52.8% | [+36.1%, +69.4%] | [+40.5%, +63.2%] | yes |
| plain | Whole-file Ultra, 1 call | +11.1% | [+2.8%, +22.2%] | [+2.9%, +18.9%] | yes |
| titled | Screener as shipped (no headings found: whole text) | +0.0% | [+0.0%, +0.0%] | [+0.0%, +0.0%] | no |
| titled | Screener + segmenter | +8.3% | [+0.0%, +19.4%] | [+2.8%, +11.8%] | no |
| plain | Screener as shipped (no headings found: whole text) | +0.0% | [+0.0%, +0.0%] | [+0.0%, +0.0%] | no |
| plain | Screener + segmenter | +2.8% | [+0.0%, +8.3%] | [+0.0%, +8.3%] | no |

## Split: dev

| condition | method | n | QWK | MAE | FC | FR | review rate | calls/item |
|---|---|---|---|---|---|---|---|---|
| headed | Whole-file Nano, 1 call | 60 | 0.228 | 1.30 | 56.8% [41%, 73%] (21/37) | 0.0% |  | 1.0 |
| headed | Whole-file Nano, median of 3 | 60 | 0.344 | 1.13 | 54.1% [38%, 70%] (20/37) | 0.0% |  | 3.0 |
| headed | Whole-file Ultra, 1 call | 60 | 0.821 | 0.52 | 2.7% [0%, 8%] (1/37) | 8.7% |  | 1.0 |
| headed | Per-section Nano, 1 sample (ablation) | 60 | 0.554 | 0.87 | 0.0% [0%, 0%] (0/37) | 21.7% |  | 1.0 |
| headed | Per-section Nano, median of 3, no escalation (ablation) | 60 | 0.634 | 0.80 | 8.1% [0%, 19%] (3/37) | 8.7% |  | 3.0 |
| headed | Screener (full) | 60 | 0.736 | 0.67 | 8.1% [0%, 19%] (3/37) | 8.7% | 15% | 3.3 |
| plain | Whole-file Nano, 1 call | 60 | 0.398 | 1.07 | 35.1% [22%, 51%] (13/37) | 0.0% |  | 1.0 |
| plain | Whole-file Ultra, 1 call | 60 | 0.800 | 0.58 | 13.5% [3%, 24%] (5/37) | 4.3% |  | 1.0 |
| titled | Screener as shipped (no headings found: whole text) | 60 | 0.792 | 0.60 | 0.0% [0%, 0%] (0/37) | 8.7% | 20% | 3.4 |
| titled | Screener + segmenter | 60 | 0.812 | 0.58 | 5.4% [0%, 14%] (2/37) | 13.0% | 5% | 4.3 |
| plain | Screener as shipped (no headings found: whole text) | 60 | 0.732 | 0.68 | 8.1% [0%, 19%] (3/37) | 13.0% | 22% | 3.2 |
| plain | Screener + segmenter | 60 | 0.800 | 0.58 | 0.0% [0%, 0%] (0/37) | 8.7% | 15% | 4.1 |

Paired difference in FC vs the Screener (headed), on expert non-compliant items. Positive = the other method clears more violations. Item and cluster (8 systems) bootstrap.

| condition | method | FC diff | 95% CI (item) | 95% CI (cluster) | excludes 0 (item) |
|---|---|---|---|---|---|
| headed | Whole-file Nano, 1 call | +48.6% | [+32.4%, +64.9%] | [+38.9%, +57.9%] | yes |
| headed | Whole-file Nano, median of 3 | +45.9% | [+29.7%, +62.2%] | [+41.0%, +52.8%] | yes |
| headed | Whole-file Ultra, 1 call | -5.4% | [-16.2%, +5.4%] | [-15.4%, +0.0%] | no |
| headed | Per-section Nano, 1 sample (ablation) | -8.1% | [-18.9%, +0.0%] | [-15.8%, +0.0%] | no |
| headed | Per-section Nano, median of 3, no escalation (ablation) | +0.0% | [+0.0%, +0.0%] | [+0.0%, +0.0%] | no |
| plain | Whole-file Nano, 1 call | +27.0% | [+10.8%, +43.2%] | [+8.3%, +45.9%] | yes |
| plain | Whole-file Ultra, 1 call | +5.4% | [-10.8%, +21.6%] | [-5.6%, +16.7%] | no |
| titled | Screener as shipped (no headings found: whole text) | -8.1% | [-18.9%, +0.0%] | [-15.8%, +0.0%] | no |
| titled | Screener + segmenter | -2.7% | [-13.5%, +5.4%] | [-7.7%, +0.0%] | no |
| plain | Screener as shipped (no headings found: whole text) | +0.0% | [-10.8%, +10.8%] | [-7.7%, +8.3%] | no |
| plain | Screener + segmenter | -8.1% | [-18.9%, +0.0%] | [-15.8%, +0.0%] | no |

## Split: all

| condition | method | n | QWK | MAE | FC | FR | review rate | calls/item |
|---|---|---|---|---|---|---|---|---|
| headed | Whole-file Nano, 1 call | 120 | 0.315 | 1.16 | 52.1% [41%, 63%] (38/73) | 2.1% |  | 1.0 |
| headed | Whole-file Nano, median of 3 | 120 | 0.402 | 1.01 | 46.6% [36%, 59%] (34/73) | 0.0% |  | 3.0 |
| headed | Whole-file Ultra, 1 call | 120 | 0.793 | 0.57 | 6.8% [1%, 14%] (5/73) | 6.4% |  | 1.0 |
| headed | Per-section Nano, 1 sample (ablation) | 120 | 0.515 | 0.93 | 2.7% [0%, 7%] (2/73) | 23.4% |  | 1.0 |
| headed | Per-section Nano, median of 3, no escalation (ablation) | 120 | 0.631 | 0.78 | 6.8% [1%, 14%] (5/73) | 12.8% |  | 3.0 |
| headed | Screener (full) | 120 | 0.727 | 0.65 | 4.1% [0%, 10%] (3/73) | 14.9% | 13% | 3.2 |
| plain | Whole-file Nano, 1 call | 120 | 0.298 | 1.14 | 43.8% [33%, 55%] (32/73) | 2.1% |  | 1.0 |
| plain | Whole-file Ultra, 1 call | 120 | 0.761 | 0.62 | 12.3% [5%, 21%] (9/73) | 4.3% |  | 1.0 |
| titled | Screener as shipped (no headings found: whole text) | 120 | 0.783 | 0.63 | 0.0% [0%, 0%] (0/73) | 8.5% | 21% | 3.4 |
| titled | Screener + segmenter | 120 | 0.785 | 0.62 | 6.8% [1%, 14%] (5/73) | 10.6% | 14% | 4.2 |
| plain | Screener as shipped (no headings found: whole text) | 120 | 0.777 | 0.60 | 4.1% [0%, 10%] (3/73) | 10.6% | 22% | 3.3 |
| plain | Screener + segmenter | 120 | 0.800 | 0.58 | 1.4% [0%, 4%] (1/73) | 12.8% | 15% | 4.1 |

Paired difference in FC vs the Screener (headed), on expert non-compliant items. Positive = the other method clears more violations. Item and cluster (8 systems) bootstrap.

| condition | method | FC diff | 95% CI (item) | 95% CI (cluster) | excludes 0 (item) |
|---|---|---|---|---|---|
| headed | Whole-file Nano, 1 call | +47.9% | [+37.0%, +58.9%] | [+41.1%, +54.1%] | yes |
| headed | Whole-file Nano, median of 3 | +42.5% | [+31.5%, +53.4%] | [+35.1%, +48.6%] | yes |
| headed | Whole-file Ultra, 1 call | +2.7% | [-5.5%, +11.0%] | [-6.6%, +13.0%] | no |
| headed | Per-section Nano, 1 sample (ablation) | -1.4% | [-6.8%, +4.1%] | [-9.2%, +6.8%] | no |
| headed | Per-section Nano, median of 3, no escalation (ablation) | +2.7% | [+0.0%, +6.8%] | [+0.0%, +6.8%] | no |
| plain | Whole-file Nano, 1 call | +39.7% | [+28.8%, +52.1%] | [+24.7%, +53.4%] | yes |
| plain | Whole-file Ultra, 1 call | +8.2% | [-1.4%, +17.8%] | [+1.3%, +15.5%] | no |
| titled | Screener as shipped (no headings found: whole text) | -4.1% | [-9.6%, +0.0%] | [-9.5%, +0.0%] | no |
| titled | Screener + segmenter | +2.7% | [-2.7%, +9.6%] | [-2.6%, +7.4%] | no |
| plain | Screener as shipped (no headings found: whole text) | +0.0% | [-5.5%, +5.5%] | [-3.9%, +4.1%] | no |
| plain | Screener + segmenter | -2.7% | [-8.2%, +2.7%] | [-9.3%, +2.8%] | no |

## Run-to-run variation (headed, all items)

| method | FC per rep | QWK per rep |
|---|---|---|
| Whole-file Nano | 52.1%, 45.2%, 42.5% | 0.315, 0.380, 0.312 |
| Screener | 4.1%, 5.5%, 4.1% | 0.727, 0.797, 0.835 |

## Segmenter

Target section recovered (excerpt's last line inside the target section): 98% of 240 runs; target Article missing, whole text used: 1%.
