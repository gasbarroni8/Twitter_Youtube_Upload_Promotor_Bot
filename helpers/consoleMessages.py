from helpers.style import Style
import pprint

def successMessage(message):
  print(Style['green'])
  print(message)
  print(Style['white'])

def errorMessage(message):
  print(Style['red'])
  print(message)
  print(Style['white'])

def pretify(message):
  pprint.pprint(message)