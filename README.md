# SysGuard — System Metrics Monitor

Monitors CPU, memory, and disk in real time. Alerts only when something is genuinely wrong — not on every spike.

---

## Why not just use Task Manager?

Task Manager shows you what's happening right now. That's it.

| | Task Manager | SysGuard |
|---|---|---|
| History | No | Yes |
| Alerts | No | Yes |
| Filters noise | No | Yes |
| Runs in background | No | Yes |

---

## The Problem

CPU usage spikes every few seconds naturally — Chrome loading a tab, antivirus running, a background update. If you alert at anything above 85%, you get false alarms all day.

SysGuard looks at the average of the last 5 readings instead of reacting to every spike.

```
Spike:      [45, 46, 91, 44, 45] → avg = 54% → no alert
Actually bad: [88, 91, 89, 92, 90] → avg = 90% → alert
```

---

## How it works

```
Every 5 seconds:
1. Read CPU, Memory, Disk
2. Smooth noise with sliding window
3. Find top 5 CPU processes with min-heap
4. Send to Prometheus → view graphs at localhost:9090
```

---

## Algorithms Used

**Sliding Window** — keeps last 5 CPU readings in a deque. Average them. Alert only if the average is high. Prevents false alarms from momentary spikes.

**Min-Heap** — 200+ processes run at any time. Instead of sorting all of them every cycle, a min-heap of size 5 tracks only the top CPU hogs efficiently. O(n log k) instead of O(n log n).

---

## Use Cases

- Know which app is slowing your laptop before it freezes
- Monitor a server and get alerted before it goes down
- See if a new deployment caused CPU to trend upward
- Investigate if your computer was struggling at 3am while you slept

---

## Run It

```bash
pip install psutil prometheus-client
python monitor.py
```

Metrics live at `http://localhost:8000/metrics`
Graphs at `http://localhost:9090`

---

> Task Manager tells you what's happening. SysGuard tells you what's wrong.
