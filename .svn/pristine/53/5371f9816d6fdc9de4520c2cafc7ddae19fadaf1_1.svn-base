#!/usr/bin/env python3

import socket
import time

def main():
  payload = [0x0b] * 1024

  counter = 1

  try:
    while True:
      s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM, 0)
      s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

      s.setsockopt(socket.SOL_SOCKET, 25, str("net0.2" + '\0').encode('utf-8'))
      s.bind(("fd53:7cb8:383:2::10f", 13400))

      s.settimeout(2)
      s.connect(("fd53:7cb8:383:5::e", counter, 0, 0))

      s.send(bytes(payload))
      counter = counter + 1

      s.shutdown(socket.SHUT_RDWR)
      s.close()

      time.sleep(2)
  except socket.timeout:
    print("except - socket.timeout")
    pass
  except KeyboardInterrupt:
    print("except - KeyboardInterrupt")
    pass

  print("counter = %d" % counter)

if __name__ == '__main__':
  main()


