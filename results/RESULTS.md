# AuditBench results

Items: 120 AIReg-Bench excerpts (EU AI Act Arts 9, 10, 12, 14, 15).

## 1. Reference points

Expert agreement: Krippendorff alpha (interval) = 0.657; leave-one-expert-out QWK vs other experts' median = 0.696.

Published AIReg-Bench annotations (single sample, original prompt):

| model | n | qwk | spearman | mae | bias | exact | f1 |
|---|---|---|---|---|---|---|---|
| pro | 120 | 0.863 | 0.856 | 0.458 | -0.225 | 0.600 | 0.911 |
| gpt5 | 120 | 0.849 | 0.838 | 0.450 | -0.067 | 0.575 | 0.903 |
| grok4 | 120 | 0.829 | 0.829 | 0.475 | 0.242 | 0.583 | 0.860 |
| 4o | 120 | 0.775 | 0.842 | 0.558 | 0.458 | 0.525 | 0.846 |
| sonnet | 120 | 0.772 | 0.779 | 0.600 | -0.150 | 0.467 | 0.845 |
| grok3_mini | 120 | 0.730 | 0.810 | 0.592 | 0.492 | 0.533 | 0.830 |
| flash | 120 | 0.729 | 0.825 | 0.625 | -0.108 | 0.417 | 0.913 |
| o3 | 120 | 0.723 | 0.809 | 0.658 | -0.192 | 0.383 | 0.903 |
| gemma | 120 | 0.696 | 0.757 | 0.692 | 0.258 | 0.400 | 0.796 |
| o3_mini | 120 | 0.624 | 0.798 | 0.775 | 0.742 | 0.442 | 0.736 |

## 2. Our auditors: validity vs experts and test-retest reliability

qwk etc. use the mean over k independent samples; qwk_1sample uses only the first sample (comparable to the single-sample published numbers above).

| config | n | k | qwk | qwk_1sample | spearman | mae | bias | f1 | mean_item_sd | alpha_interval | verdict_flip_rate |
|---|---|---|---|---|---|---|---|---|---|---|---|
| decomposed | 120 | 3 | 0.640 | 0.631 | 0.737 | 0.975 | -0.403 | 0.837 | 0.084 | 0.985 | 0.033 |
| decomposed_meanagg | 120 | 3 | 0.532 | 0.515 | 0.749 | 0.934 | 0.826 | 0.692 | 0.052 | 0.993 | 0.017 |
| generative | 120 | 3 | 0.828 | 0.830 | 0.833 | 0.539 | -0.033 | 0.832 | 0.043 | 0.989 | 0.025 |
| holistic | 120 | 3 | 0.877 | 0.866 | 0.852 | 0.460 | -0.176 | 0.901 | 0.034 | 0.999 | 0.017 |
| holistic_noarticle | 120 | 3 | 0.835 | 0.822 | 0.826 | 0.581 | -0.271 | 0.903 | 0.050 | 0.998 | 0.025 |
| holistic_nooutline | 120 | 3 | 0.849 | 0.843 | 0.828 | 0.485 | -0.129 | 0.911 | 0.031 | 0.999 | 0.008 |

## 3. Sensitivity to perturbations that add no evidence (ideal delta = 0)

delta = mean(score_perturbed - score_original) on the 1-5 scale; 95% bootstrap CI; false_clearance = share of expert-non-compliant items newly rated compliant.

| config | perturbation | n | delta | ci_low | ci_high | wilcoxon_p | verdict_flip_rate | false_clearance_rate | false_rejection_rate | delta_on_compliant | delta_on_noncompliant |
|---|---|---|---|---|---|---|---|---|---|---|---|
| decomposed | assurance | 120 | -0.103 | -0.206 | -0.011 | 0.283 | 0.050 | 0.014 | 0.064 | -0.165 | -0.063 |
| decomposed | authority | 120 | 0.017 | -0.077 | 0.111 | 0.214 | 0.025 | 0.027 | 0.021 | -0.049 | 0.060 |
| decomposed | negative | 120 | 0.023 | -0.093 | 0.139 | 0.698 | 0.067 | 0.055 | 0.043 | -0.034 | 0.060 |
| decomposed_meanagg | assurance | 120 | -0.083 | -0.140 | -0.032 | 0.001 | 0.033 | 0.000 | 0.043 | -0.095 | -0.075 |
| decomposed_meanagg | authority | 120 | 0.030 | -0.023 | 0.084 | 0.192 | 0.058 | 0.055 | 0.000 | -0.014 | 0.058 |
| decomposed_meanagg | negative | 120 | -0.007 | -0.069 | 0.059 | 0.649 | 0.067 | 0.055 | 0.021 | -0.049 | 0.021 |
| generative | assurance | 120 | -0.111 | -0.172 | -0.061 | 0.000 | 0.033 | 0.000 | 0.021 | -0.057 | -0.146 |
| generative | authority | 120 | -0.122 | -0.200 | -0.056 | 0.002 | 0.042 | 0.000 | 0.000 | -0.057 | -0.164 |
| generative | dossier_first | 120 | 0.392 | 0.280 | 0.506 | 0.000 | 0.108 | 0.151 | 0.000 | 0.085 | 0.589 |
| generative | dossier_last | 120 | -0.092 | -0.192 | -0.003 | 0.061 | 0.075 | 0.014 | 0.021 | -0.021 | -0.137 |
| generative | dossier_middle | 120 | 0.100 | 0.019 | 0.192 | 0.027 | 0.058 | 0.068 | 0.021 | 0.021 | 0.151 |
| generative | negative | 120 | -0.031 | -0.069 | 0.003 | 0.153 | 0.000 | 0.000 | 0.000 | 0.000 | -0.050 |
| generative | reformat | 120 | 0.008 | -0.036 | 0.053 | 0.561 | 0.000 | 0.000 | 0.000 | -0.014 | 0.023 |
| generative | rename | 120 | 0.011 | -0.042 | 0.061 | 0.703 | 0.008 | 0.000 | 0.000 | 0.000 | 0.018 |
| holistic | assurance | 120 | -0.098 | -0.121 | -0.075 | 0.000 | 0.008 | 0.000 | 0.000 | -0.042 | -0.133 |
| holistic | authority | 120 | -0.082 | -0.120 | -0.050 | 0.000 | 0.008 | 0.000 | 0.000 | -0.021 | -0.122 |
| holistic | dossier_first | 120 | 0.209 | 0.155 | 0.267 | 0.000 | 0.058 | 0.096 | 0.000 | 0.034 | 0.321 |
| holistic | dossier_last | 120 | 0.013 | -0.044 | 0.073 | 0.669 | 0.033 | 0.027 | 0.000 | 0.025 | 0.005 |
| holistic | dossier_middle | 120 | 0.122 | 0.052 | 0.201 | 0.029 | 0.058 | 0.082 | 0.000 | 0.030 | 0.181 |
| holistic | negative | 120 | -0.032 | -0.057 | -0.009 | 0.043 | 0.017 | 0.000 | 0.000 | -0.004 | -0.050 |
| holistic | reformat | 120 | 0.004 | -0.027 | 0.034 | 0.602 | 0.025 | 0.014 | 0.000 | 0.019 | -0.006 |
| holistic | rename | 120 | 0.011 | -0.022 | 0.044 | 0.668 | 0.017 | 0.014 | 0.000 | -0.002 | 0.020 |

## 4. By Article

| config | article | n | qwk | mae | bias | f1 |
|---|---|---|---|---|---|---|
| decomposed | 9 | 24 | 0.689 | 0.924 | -0.209 | 0.818 |
| decomposed | 10 | 24 | 0.646 | 0.972 | -0.394 | 0.941 |
| decomposed | 12 | 24 | 0.408 | 1.217 | 0.060 | 0.720 |
| decomposed | 14 | 24 | 0.881 | 0.469 | -0.273 | 0.947 |
| decomposed | 15 | 24 | 0.506 | 1.295 | -1.199 | 0.800 |
| decomposed_meanagg | 9 | 24 | 0.291 | 1.306 | 1.306 | 0.606 |
| decomposed_meanagg | 10 | 24 | 0.319 | 1.238 | 1.223 | 0.533 |
| decomposed_meanagg | 12 | 24 | 0.295 | 0.992 | 0.714 | 0.667 |
| decomposed_meanagg | 14 | 24 | 0.806 | 0.582 | 0.555 | 0.900 |
| decomposed_meanagg | 15 | 24 | 0.760 | 0.550 | 0.333 | 0.900 |
| generative | 9 | 24 | 0.899 | 0.403 | 0.153 | 0.818 |
| generative | 10 | 24 | 0.642 | 0.847 | 0.514 | 0.667 |
| generative | 12 | 24 | 0.806 | 0.542 | -0.458 | 0.842 |
| generative | 14 | 24 | 0.858 | 0.514 | -0.208 | 0.941 |
| generative | 15 | 24 | 0.875 | 0.389 | -0.167 | 0.947 |
| holistic | 9 | 24 | 0.921 | 0.354 | -0.097 | 0.900 |
| holistic | 10 | 24 | 0.829 | 0.552 | -0.066 | 1.000 |
| holistic | 12 | 24 | 0.802 | 0.596 | -0.382 | 0.800 |
| holistic | 14 | 24 | 0.922 | 0.376 | -0.143 | 0.941 |
| holistic | 15 | 24 | 0.873 | 0.423 | -0.194 | 0.889 |
| holistic_noarticle | 9 | 24 | 0.853 | 0.463 | -0.211 | 0.900 |
| holistic_noarticle | 10 | 24 | 0.721 | 0.791 | -0.249 | 0.941 |
| holistic_noarticle | 12 | 24 | 0.768 | 0.607 | -0.162 | 0.818 |
| holistic_noarticle | 14 | 24 | 0.895 | 0.470 | -0.263 | 0.941 |
| holistic_noarticle | 15 | 24 | 0.875 | 0.574 | -0.468 | 0.941 |
| holistic_nooutline | 9 | 24 | 0.900 | 0.420 | -0.119 | 0.947 |
| holistic_nooutline | 10 | 24 | 0.821 | 0.514 | 0.099 | 0.941 |
| holistic_nooutline | 12 | 24 | 0.730 | 0.647 | -0.345 | 0.842 |
| holistic_nooutline | 14 | 24 | 0.885 | 0.432 | -0.110 | 0.941 |
| holistic_nooutline | 15 | 24 | 0.873 | 0.414 | -0.169 | 0.889 |
