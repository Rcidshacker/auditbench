# L4: ground-truth noise

## Is the gap real? Paired bootstrap of QWK(ours:holistic) − QWK(auditor), 5,000 resamples

| auditor | qwk | holistic_minus_this | ci_low | ci_high | significant |
|---|---|---|---|---|---|
| ours:holistic | 0.877 | 0.000 | 0.000 | 0.000 | no |
| published:pro | 0.863 | 0.013 | -0.020 | 0.050 | no |
| ours:holistic_nooutline | 0.849 | 0.028 | 0.004 | 0.056 | yes |
| published:gpt5 | 0.849 | 0.028 | -0.021 | 0.079 | no |
| ours:holistic_noarticle | 0.835 | 0.042 | 0.003 | 0.083 | yes |
| published:grok4 | 0.829 | 0.048 | -0.003 | 0.100 | no |
| ours:generative | 0.828 | 0.049 | 0.021 | 0.082 | yes |
| published:4o | 0.775 | 0.102 | 0.043 | 0.167 | yes |
| published:sonnet | 0.772 | 0.104 | 0.062 | 0.152 | yes |
| published:grok3_mini | 0.730 | 0.146 | 0.075 | 0.223 | yes |
| published:flash | 0.729 | 0.148 | 0.086 | 0.211 | yes |
| published:o3 | 0.723 | 0.153 | 0.102 | 0.206 | yes |
| published:gemma | 0.696 | 0.180 | 0.109 | 0.260 | yes |
| ours:decomposed | 0.640 | 0.237 | 0.145 | 0.339 | yes |
| published:o3_mini | 0.624 | 0.253 | 0.172 | 0.337 | yes |

## Agreement with each expert separately (QWK)

| auditor | expert_1 | expert_2 | expert_3 | min | max |
|---|---|---|---|---|---|
| ours:holistic | 0.826 | 0.732 | 0.840 | 0.732 | 0.840 |
| ours:decomposed | 0.685 | 0.565 | 0.617 | 0.565 | 0.685 |
| ours:holistic_noarticle | 0.816 | 0.688 | 0.779 | 0.688 | 0.816 |
| ours:holistic_nooutline | 0.811 | 0.728 | 0.832 | 0.728 | 0.832 |
| ours:generative | 0.775 | 0.702 | 0.816 | 0.702 | 0.816 |
| published:gpt5 | 0.737 | 0.703 | 0.841 | 0.703 | 0.841 |
| published:o3 | 0.605 | 0.594 | 0.707 | 0.594 | 0.707 |
| published:o3_mini | 0.445 | 0.609 | 0.719 | 0.445 | 0.719 |
| published:4o | 0.587 | 0.698 | 0.855 | 0.587 | 0.855 |
| published:sonnet | 0.698 | 0.637 | 0.769 | 0.637 | 0.769 |
| published:pro | 0.836 | 0.726 | 0.804 | 0.726 | 0.836 |
| published:flash | 0.588 | 0.565 | 0.741 | 0.565 | 0.741 |
| published:gemma | 0.532 | 0.622 | 0.737 | 0.532 | 0.737 |
| published:grok3_mini | 0.552 | 0.670 | 0.805 | 0.552 | 0.805 |
| published:grok4 | 0.699 | 0.703 | 0.850 | 0.699 | 0.850 |
| human: expert 1 vs others' mean |  |  |  | 0.639 | 0.639 |
| human: expert 2 vs others' mean |  |  |  | 0.690 | 0.690 |
| human: expert 3 vs others' mean |  |  |  | 0.759 | 0.759 |

## High-agreement subset (experts span ≤ 1 point): 79/120 items

| auditor | n | qwk | mae | f1 |
|---|---|---|---|---|
| ours:holistic | 79 | 0.935 | 0.310 | 0.962 |
| published:pro | 79 | 0.933 | 0.291 | 0.962 |
| ours:holistic_nooutline | 79 | 0.916 | 0.352 | 0.974 |
| ours:holistic_noarticle | 79 | 0.904 | 0.423 | 0.925 |
| published:gpt5 | 79 | 0.895 | 0.380 | 0.987 |
| ours:generative | 79 | 0.890 | 0.405 | 0.927 |
| published:grok4 | 79 | 0.871 | 0.418 | 0.963 |
| published:sonnet | 79 | 0.831 | 0.582 | 0.938 |
| published:4o | 79 | 0.807 | 0.582 | 0.929 |
| ours:decomposed | 79 | 0.790 | 0.657 | 0.925 |
| published:grok3_mini | 79 | 0.780 | 0.595 | 0.927 |
| published:o3 | 79 | 0.774 | 0.709 | 0.987 |
| published:gemma | 79 | 0.740 | 0.722 | 0.918 |
| published:flash | 79 | 0.736 | 0.759 | 0.974 |
| published:o3_mini | 79 | 0.695 | 0.747 | 0.857 |

## AUROC: separating compliant from violation documents

`auroc_vs_intent` uses which file the item came from (compliant vs violation), a label independent of the experts.

| auditor | auroc_vs_intent | auroc_vs_expert_median |
|---|---|---|
| ours:holistic | 1.000 | 0.967 |
| ours:holistic_noarticle | 1.000 | 0.972 |
| ours:holistic_nooutline | 1.000 | 0.964 |
| published:pro | 1.000 | 0.957 |
| published:grok4 | 0.998 | 0.958 |
| human: expert median | 0.995 |  |
| published:grok3_mini | 0.994 | 0.944 |
| ours:generative | 0.992 | 0.947 |
| published:4o | 0.988 | 0.959 |
| published:gpt5 | 0.985 | 0.971 |
| published:o3_mini | 0.963 | 0.942 |
| published:sonnet | 0.963 | 0.895 |
| published:o3 | 0.962 | 0.929 |
| ours:decomposed | 0.958 | 0.927 |
| published:flash | 0.957 | 0.951 |
| published:gemma | 0.907 | 0.886 |
