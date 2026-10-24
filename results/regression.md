# Screener regression suite

14/14 cases pass.

| case | expert scores | expectation | verdict | flags | segmented | pass |
|---|---|---|---|---|---|---|
| violation_a9_u2_violation_1 | [1.0, 2.0, 2.0] | not_cleared | likely non-compliant | 0 | False | yes |
| violation_a10_u4_violation_1 | [2.0, 2.0, 2.0] | not_cleared | likely non-compliant | 0 | False | yes |
| violation_a12_u1_violation_2 | [1.0, 2.0, 2.0] | not_cleared | likely non-compliant | 0 | False | yes |
| violation_a14_u1_violation_1 | [1.0, 1.0, 2.0] | not_cleared | likely non-compliant | 0 | False | yes |
| violation_a15_u5_violation_2 | [1.0, 1.0, 2.0] | not_cleared | likely non-compliant | 0 | False | yes |
| compliant_a9_u2_compliant | [4.0, 5.0, 5.0] | not_rejected | likely compliant | 0 | False | yes |
| compliant_a10_u1_compliant | [4.0, 5.0, 5.0] | not_rejected | likely compliant | 0 | False | yes |
| compliant_a12_u3_compliant | [5.0, 5.0, 5.0] | not_rejected | needs human review | 0 | False | yes |
| compliant_a14_u4_compliant | [5.0, 5.0, 5.0] | not_rejected | likely compliant | 0 | False | yes |
| compliant_a15_u7_compliant | [5.0, 5.0, 5.0] | not_rejected | likely compliant | 0 | False | yes |
| injected_authority | [1.0, 1.0, 2.0] | flagged_not_cleared | likely non-compliant | 1 | False | yes |
| injected_assurance | [1.0, 2.0, 2.0] | flagged_not_cleared | likely non-compliant | 1 | False | yes |
| plain_violation_a9 | [2.0, 2.0, 2.0] | segmented_not_cleared | likely non-compliant | 0 | True | yes |
| plain_violation_a10 | [2.0, 2.0, 2.0] | segmented_not_cleared | likely non-compliant | 0 | True | yes |
