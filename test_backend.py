from backend.logic import Queue
from backend.package_service import add_package
from backend.drone_service import mark_package_delivered_by_index

q = Queue()
add_package(q, 'A', 'Item A', 'Menteng', 'Regular', 1.2)
add_package(q, 'B', 'Item B', 'Ciputat', 'Express', 0.8)
removed = mark_package_delivered_by_index(q, 0, [])
print('removed:', removed)
print('remaining queue:', q.get_all())
