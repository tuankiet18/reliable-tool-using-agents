---
title: "R3F: lỗi lint react-hooks/refs khi map mảng ref, và CSS HUD ngoài layer đè Tailwind"
category: skills
tags:
  - topic/react-three-fiber
  - react
  - css
summary: "Map một mảng useRef trong JSX bị rule react-hooks/refs (React Compiler) chặn; CSS dùng chung không nằm trong layer sẽ đè class tiện ích của Tailwind v4."
tier: supporting
related: []
extends: null
contradicts: null
superseded_by: null
capture_source: claude-session
project: "StuWork"
base_confidence: 0.75
lifecycle: draft
lifecycle_changed: 2026-10-06
provenance:
  extracted: 0.8
  inferred: 0.2
sources:
  - "StuWork session (2026-10-06)"
---

# R3F / React Compiler: gotcha về ref và lớp CSS của HUD

Ghi lại khi đồng bộ HUD và marker 3D của game StuPort với game HR trong StuWork.

## Map một mảng ref trong JSX bị react-hooks/refs chặn

**Problem:** `const ripples = [useRef<Mesh>(null), useRef<Mesh>(null)]` rồi `{ripples.map((ref) => <mesh ref={ref} />)}` khiến ESLint báo "Cannot access refs during render" (rule `react-hooks/refs`).

**Root cause:** rule của React Compiler coi việc lặp qua một mảng chứa ref trong lúc render là đọc giá trị ref. Gán trực tiếp `ref={rippleA}` cho từng phần tử thì không bị coi là đọc. ^[inferred]

**Fix:**
```tsx
// ❌ trước
{ripples.map((ref, i) => <mesh key={i} ref={ref} />)}
// ✅ sau: khai báo từng ref; chỉ lặp mảng bên trong useFrame
const rippleA = useRef<Mesh>(null), rippleB = useRef<Mesh>(null)
useFrame(() => { [rippleA, rippleB].forEach(...) })
<mesh ref={rippleA} /> <mesh ref={rippleB} />
```

**Confirmed by:** eslint và tsc đều qua.

## CSS HUD dùng chung không nằm trong layer sẽ đè class tiện ích Tailwind

**Behavior:** trong `simulation-hud.css`, các selector như `.simulation-hud .simulation-action-zone > button { background: #087b73 }` và `.simulation-station-label { font-size: 11px }` đè lên class tiện ích Tailwind đặt trên cùng phần tử (gradient, `text-[10px]`).

**Why:** CSS không nằm trong layer luôn thắng CSS trong `@layer utilities`, bất kể specificity. ^[inferred]

**How to apply:** muốn đổi style một phần tử nằm dưới `.simulation-hud` thì sửa trong file CSS dùng chung, hoặc dùng selector có specificity cao hơn. Đừng thêm class tiện ích lên chính phần tử đó.
