"""Backend package service: pure functions operating on Queue objects.
This module does NOT import or use Streamlit so it can be tested independently.
"""
from typing import Any


def add_package(queue: Any, penerima: str, paket: str, tujuan: str, priority: str, berat: float) -> dict:
    data = {
        "penerima": penerima,
        "paket": paket,
        "tujuan": tujuan,
        "priority": priority,
        "berat": berat,
        "status": "Pending",
    }
    queue.enqueue(data)
    return data


def get_queue_list(queue: Any) -> list:
    return queue.get_all()
