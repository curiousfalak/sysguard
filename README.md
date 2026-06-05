# 🖥️ SysGuard — System Metrics Monitor

A Python tool that watches your computer's health in real time and tells you only when something is **actually** wrong.

---

## 🤔 Wait — doesn't Windows Task Manager already do this?

Yes. But Task Manager has three big problems:

| | Task Manager | SysGuard |
|---|---|---|
| Shows history? | ❌ Only right now | ✅ Stores data over time |
| Smart alerts? | ❌ No alerts at all | ✅ Alerts only on real problems |
| Filters noise? | ❌ Every spike looks scary | ✅ Ignores short spikes |
| Runs in background? | ❌ You have to open it | ✅ Always watching silently |

**Task Manager is a window you open. SysGuard is a watchman that never sleeps.**

---

## 😤 The Real Problem

Your CPU jumps up and down every second — even when everything is fine.

```
Normal day:  45% → 46% → 91% → 44% → 45%
                          ↑
                    Chrome just opened a tab
                    Nothing is actually wrong!
```

If you alert every time CPU crosses 85%, you get **100 false alarms a day.**

SysGuard fixes this by looking at the **average of last 5 readings** instead of reacting to every spike.

```
Single spike:   [45, 46, 91, 44, 45] → average = 54% → no alert ✓

Actually bad:   [88, 91, 89, 92, 90] → average = 90% → ALERT!  ✓
```

---

## 🧠 Two Smart Ideas Inside

### Idea 1 — Sliding Window (noise filter)

Keep a rolling memory of the last 5 CPU readings. Take the average. Alert only if the average is high — not if one reading is high.

```python
window = deque(maxlen=5)   # only remembers last 5, auto-forgets old ones
window.append(91)          # one spike
average = sum(window) / len(window)  # still low → no panic
```

Think of it like this: if your friend says "I'm tired" once, you don't panic. If they say it every day for a week — then you worry.

---

### Idea 2 — Min-Heap (find top 5 greedy processes)

200+ processes run at any moment. Instead of sorting all of them every 5 seconds (slow), SysGuard keeps a shortlist of exactly 5 and swaps out anyone who doesn't deserve to be there.

```
Running processes: chrome, spotify, python, system, dwm...
                                    ↓
                   Only track the 5 biggest CPU hogs
                   Swap out weaker ones as new data comes in
```

**Result:** You always know exactly which apps are slowing your computer down.

---

## 🛠️ How It Works (Simple Flow)

```
Every 5 seconds:

1. Read CPU, Memory, Disk  ← psutil
2. Smooth out noise        ← sliding window
3. Find top 5 processes    ← min-heap
4. Publish the numbers     ← prometheus_client
5. Prometheus saves them   ← time-series database
6. Open localhost:9090     ← see live graphs
```

---

## 🚀 Run It

```bash
pip install psutil prometheus-client
python monitor.py
```

Open `http://localhost:8000/metrics` — you'll see your computer's vitals live.

---

## 📁 Files

```
sysguard/
├── monitor.py    # the whole project lives here
└── .gitignore
```

---

## 💬 One Line Summary

> Task Manager shows you what's happening right now.  
> SysGuard remembers the past, filters the noise, and tells you when to actually worry.
