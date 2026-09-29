# Paired cluster-bootstrap analysis

Differences are `provenance_aware - control`. Negative is better for unsafe acceptance/expected loss; positive is better for correct acceptance. Resampling unit is task (`n=10`), retaining all five seeds.

| regime | control | metric | abstention cost | difference | 95% cluster-bootstrap CI |
|---|---|---|---:|---:|---:|
| independent | fixed_k | unsafe_accept | n/a | 0.000 | [-0.060, 0.060] |
| independent | fixed_k | alarm | n/a | -0.060 | [-0.200, 0.080] |
| independent | fixed_k | accepted_correct | n/a | 0.060 | [-0.060, 0.200] |
| independent | fixed_k | expected_loss | 0.00 | 0.000 | [-0.060, 0.060] |
| independent | fixed_k | expected_loss | 0.10 | -0.006 | [-0.058, 0.048] |
| independent | fixed_k | expected_loss | 0.25 | -0.015 | [-0.065, 0.035] |
| independent | fixed_k | expected_loss | 0.50 | -0.030 | [-0.100, 0.040] |
| independent | fixed_k | expected_loss | 0.75 | -0.045 | [-0.145, 0.045] |
| independent | fixed_k | expected_loss | 1.00 | -0.060 | [-0.180, 0.060] |
| independent | random_k | unsafe_accept | n/a | -0.020 | [-0.080, 0.040] |
| independent | random_k | alarm | n/a | 0.060 | [-0.040, 0.180] |
| independent | random_k | accepted_correct | n/a | -0.040 | [-0.160, 0.060] |
| independent | random_k | expected_loss | 0.00 | -0.020 | [-0.080, 0.040] |
| independent | random_k | expected_loss | 0.10 | -0.014 | [-0.076, 0.048] |
| independent | random_k | expected_loss | 0.25 | -0.005 | [-0.065, 0.060] |
| independent | random_k | expected_loss | 0.50 | 0.010 | [-0.060, 0.080] |
| independent | random_k | expected_loss | 0.75 | 0.025 | [-0.060, 0.115] |
| independent | random_k | expected_loss | 1.00 | 0.040 | [-0.060, 0.160] |
| common_mode | fixed_k | unsafe_accept | n/a | -0.340 | [-0.420, -0.260] |
| common_mode | fixed_k | alarm | n/a | 0.640 | [0.520, 0.780] |
| common_mode | fixed_k | accepted_correct | n/a | -0.300 | [-0.420, -0.180] |
| common_mode | fixed_k | expected_loss | 0.00 | -0.340 | [-0.420, -0.260] |
| common_mode | fixed_k | expected_loss | 0.10 | -0.276 | [-0.354, -0.204] |
| common_mode | fixed_k | expected_loss | 0.25 | -0.180 | [-0.260, -0.115] |
| common_mode | fixed_k | expected_loss | 0.50 | -0.020 | [-0.110, 0.060] |
| common_mode | fixed_k | expected_loss | 0.75 | 0.140 | [0.035, 0.240] |
| common_mode | fixed_k | expected_loss | 1.00 | 0.300 | [0.180, 0.420] |
| common_mode | random_k | unsafe_accept | n/a | -0.060 | [-0.120, 0.000] |
| common_mode | random_k | alarm | n/a | 0.160 | [0.000, 0.320] |
| common_mode | random_k | accepted_correct | n/a | -0.100 | [-0.320, 0.100] |
| common_mode | random_k | expected_loss | 0.00 | -0.060 | [-0.120, 0.000] |
| common_mode | random_k | expected_loss | 0.10 | -0.044 | [-0.114, 0.020] |
| common_mode | random_k | expected_loss | 0.25 | -0.020 | [-0.110, 0.065] |
| common_mode | random_k | expected_loss | 0.50 | 0.020 | [-0.100, 0.140] |
| common_mode | random_k | expected_loss | 0.75 | 0.060 | [-0.100, 0.230] |
| common_mode | random_k | expected_loss | 1.00 | 0.100 | [-0.100, 0.320] |

CIs quantify uncertainty over these ten synthetic task fixtures only; they do not establish external validity.
