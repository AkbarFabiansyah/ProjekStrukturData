"""Backend drone service: pure functions to manage dispatch, marking delivered,
and processing active deliveries. No Streamlit usage here.
"""
import time
from typing import Any, List


def dispatch_next(queue: Any, drones: List[dict], active_deliveries: List[dict]) -> (bool, str):
    ready = [d for d in drones if d.get("status") == "Ready"]
    if not ready:
        return False, "Tidak ada drone siap."

    paket = queue.dequeue()
    if not paket:
        return False, "Antrean kosong."

    drone = ready[0]
    # update drone
    for d in drones:
        if d.get("id") == drone.get("id"):
            d["status"] = "Delivering"
            d["current_job"] = paket
            break

    active_delivery = {
        "drone_id": drone.get("id"),
        "paket": paket,
        "progress": 0,
        "status": "Terbang",
        "timestamp": time.time(),
    }
    active_deliveries.append(active_delivery)

    return True, f"Drone {drone['id']} mengirim {paket['paket']} ke {paket['tujuan']}"


def mark_package_delivered_by_index(queue: Any, index: int, history: List[dict]) -> dict | None:
    removed = queue.remove_at(index)
    if not removed:
        return None
    removed["status"] = "Terkirim"
    history.append(removed)
    return removed


def process_active_deliveries(drones: List[dict], active_deliveries: List[dict], history: List[dict], now: float | None = None, threshold_seconds: int = 2) -> int:
    """Process active deliveries; move completed ones into history.
    Returns number of completed deliveries processed.
    """
    if now is None:
        now = time.time()

    completed_indexes = []
    for idx, delivery in enumerate(active_deliveries):
        elapsed = now - delivery.get("timestamp", now)
        if delivery.get("progress", 0) >= 100 or elapsed >= threshold_seconds:
            completed_indexes.append(idx)

    for idx in reversed(completed_indexes):
        done = active_deliveries.pop(idx)
        paket = done.get("paket")
        if paket is not None:
            paket["status"] = "Terkirim"
            history.append(paket)

        # reset drone
        for d in drones:
            if d.get("id") == done.get("drone_id"):
                d["status"] = "Ready"
                d["current_job"] = None
                d["battery"] = max(10, d.get("battery", 100) - 15)
                break

    return len(completed_indexes)
