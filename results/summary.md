# Pilot summary

Seeds: `[11, 23, 37, 51, 79]`; independent corruption probability per tool: `0.25`.

| regime | policy | episodes | selected_fault_cases | detection_recall | unsafe_accept_rate | correct_accept_rate | selective_accuracy | abstention_rate | mean_extra_tool_calls |
|---|---|---|---|---|---|---|---|---|---|
| clean | fixed_k | 50 | 0 | n/a | 0.000 | 1.000 | 1.000 | 0.000 | 1.000 |
| clean | provenance_aware | 50 | 0 | n/a | 0.000 | 1.000 | 1.000 | 0.000 | 1.000 |
| clean | random_k | 50 | 0 | n/a | 0.000 | 1.000 | 1.000 | 0.000 | 1.000 |
| clean | single | 50 | 0 | n/a | 0.000 | 1.000 | 1.000 | 0.000 | 0.000 |
| common_mode | fixed_k | 50 | 17 | 0.000 | 0.340 | 0.660 | 0.660 | 0.000 | 1.000 |
| common_mode | provenance_aware | 50 | 32 | 1.000 | 0.000 | 0.360 | 1.000 | 0.640 | 1.000 |
| common_mode | random_k | 50 | 27 | 0.889 | 0.060 | 0.460 | 0.885 | 0.480 | 1.000 |
| common_mode | single | 50 | 17 | 0.000 | 0.340 | 0.660 | 0.660 | 0.000 | 0.000 |
| independent | fixed_k | 50 | 22 | 0.955 | 0.020 | 0.560 | 0.966 | 0.420 | 1.000 |
| independent | provenance_aware | 50 | 19 | 0.947 | 0.020 | 0.620 | 0.969 | 0.360 | 1.000 |
| independent | random_k | 50 | 17 | 0.882 | 0.040 | 0.660 | 0.943 | 0.300 | 1.000 |
| independent | single | 50 | 12 | 0.000 | 0.240 | 0.760 | 0.760 | 0.000 | 0.000 |

## Safety–utility sensitivity under common-mode faults

Expected loss = `unsafe_accept_rate + abstention_cost × abstention_rate`; wrong accept cost được chuẩn hóa bằng `1`.

| abstention cost | fixed_k | random_k | provenance_aware | best |
|---:|---:|---:|---:|---|
| 0.00 | 0.340 | 0.060 | 0.000 | provenance_aware |
| 0.10 | 0.340 | 0.108 | 0.064 | provenance_aware |
| 0.25 | 0.340 | 0.180 | 0.160 | provenance_aware |
| 0.50 | 0.340 | 0.300 | 0.320 | random_k |
| 0.75 | 0.340 | 0.420 | 0.480 | fixed_k |
| 1.00 | 0.340 | 0.540 | 0.640 | fixed_k |

## Common-mode effect by task stratum

| difficulty | episodes/policy | fixed unsafe | provenance unsafe | provenance alarms |
|---|---:|---:|---:|---:|
| already_refunded | 5 | 2 | 0 | 4 |
| expired | 10 | 5 | 0 | 6 |
| happy | 10 | 3 | 0 | 4 |
| non_refundable | 10 | 2 | 0 | 6 |
| restocking | 10 | 3 | 0 | 7 |
| wrong_customer | 5 | 2 | 0 | 5 |

`detection_recall` chỉ dùng các episode nơi ít nhất một selected tool bị corrupt.
`unsafe_accept_rate` là tỷ lệ accept một giá trị sai trên toàn bộ episode.
`selective_accuracy` chỉ chấm các episode policy đã accept, nên phải đọc cùng coverage/abstention.
Kết quả này chỉ kiểm tra fault-model mechanics; chưa phải live-agent evidence.
