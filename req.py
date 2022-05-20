import requests
import threading


def do_req():
    x = "done"
    while True:
        req = requests.get('http://www.istanadivan.com/index.php')
        text = req.text
        print(x)


threads = []
for i in range(50):
    t = threading.Thread(target=do_req)
    t.daemon = True
    threads.append(t)

for i in range(50):
    threads[i].start()

for i in range(50):
    threads[i].join()
