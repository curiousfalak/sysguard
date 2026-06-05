import psutil
import time
import heapq
from collections import deque
from prometheus_client import start_http_server, Gauge

# ── Prometheus metrics ──────────────────────────────
CPU_RAW      = Gauge('cpu_usage_percent',    'Raw CPU %')
CPU_SMOOTHED = Gauge('cpu_smoothed_percent', 'Smoothed CPU %')
MEM_USAGE    = Gauge('memory_usage_percent', 'Memory %')
DISK_USAGE   = Gauge('disk_usage_percent',   'Disk %')

# ── Sliding window (last 5 readings) ────────────────
cpu_window = deque(maxlen=5)

# ── Min-heap: top 5 CPU processes ───────────────────
def top_processes(k=5):
    heap = []
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
        try:
            cpu = proc.info['cpu_percent'] or 0.0
            heapq.heappush(heap, (cpu, proc.info['name']))
            if len(heap) > k:
                heapq.heappop(heap)        # evict smallest
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    return sorted(heap, reverse=True)

# ── Collect and publish metrics ──────────────────────
def collect():
    cpu  = psutil.cpu_percent(interval=1)
    mem  = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent  # works on Windows too

    cpu_window.append(cpu)
    smoothed = sum(cpu_window) / len(cpu_window)

    # Push to Prometheus
    CPU_RAW.set(cpu)
    CPU_SMOOTHED.set(smoothed)
    MEM_USAGE.set(mem)
    DISK_USAGE.set(disk)

    print(f"CPU: {cpu}%  smoothed: {smoothed:.1f}%  MEM: {mem}%  DISK: {disk}%")
    print(f"Top processes: {top_processes()}\n")

# ── Start ────────────────────────────────────────────
if __name__ == '__main__':
    start_http_server(8000)
    print("SysGuard running → http://localhost:8000/metrics\n")
    while True:
        collect()
        time.sleep(5)