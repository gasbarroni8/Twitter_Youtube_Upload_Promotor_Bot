class LocationTrends:
  def __init__(self):
    self.us = []
    self.gb = []
    self.france = []
    self.spain = []
    self.germany = []
    self.neatherlands = []
    self.australia = []
    self.canada = []

  def setData(self, data, location):
    if (location == 'us'):
      self.us = data
    if (location == 'gb'):
      self.gb = data
    if (location == 'france'):
      self.france = data
    if (location == 'spain'):
      self.spain = data
    if (location == 'germany'):
      self.germany = data
    if (location == 'neatherlands'):
      self.neatherlands = data
    if (location == 'australia'):
      self.australia = data
    if (location == 'canada'):
      self.canada = data