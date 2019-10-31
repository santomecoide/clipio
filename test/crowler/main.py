from clipio import Crawler

c = Crawler()
c.run()
try:
    while True: pass
except KeyboardInterrupt:
    c.stop()

