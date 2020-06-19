import time

def timeDifference(epoch):
  timeA = round(time.time(), 2)
  timeB = round(epoch, 2)
  return int(timeB - timeA)