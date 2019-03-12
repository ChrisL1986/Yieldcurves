import requests
import numpy as np
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
from datetime import datetime
from pandas import Series

def getData(URL):
      response = requests.get(URL)
      response.raise_for_status()
      return response.content

def parseXML(xmlData):
      root = ET.fromstring(xmlData)

      #xml namespaces
      ns = {'m': 'http://schemas.microsoft.com/ado/2007/08/dataservices/metadata',
      'd': 'http://schemas.microsoft.com/ado/2007/08/dataservices', 
      't': 'http://www.w3.org/2005/Atom'}

      dates = []
      year1 = []
      year2 = []
      year3 = []
      year5 = []
      year10 = []
      year20 = []
      year30 = []

      for entry in root.findall('t:entry', ns):
            for content in entry.findall('t:content', ns):
                  for properties in content.findall('m:properties', ns):
                        for date in properties.findall('d:NEW_DATE', ns):
                              dates.append(datetime.strptime(date.text[0:10], '%Y-%m-%d'))
                        for y1 in properties.findall('d:BC_1YEAR', ns):
                              if y1.text is not None:
                                    year1.append(float(y1.text))
                              else:
                                    year1.append(None)
                        for y2 in properties.findall('d:BC_2YEAR', ns):
                              if y2.text is not None:
                                    year2.append(float(y2.text))
                              else:
                                    year2.append(None)
                        for y3 in properties.findall('d:BC_3YEAR', ns):
                              if y3.text is not None:
                                    year3.append(float(y3.text))
                              else:
                                    year3.append(None)
                        for y5 in properties.findall('d:BC_5YEAR', ns):
                              if y5.text is not None:
                                    year5.append(float(y5.text))
                              else:
                                    year5.append(None)
                        for y10 in properties.findall('d:BC_10YEAR', ns):
                              if y10.text is not None:
                                    year10.append(float(y10.text))
                              else:
                                    year10.append(None)
                        for y20 in properties.findall('d:BC_20YEAR', ns):
                              if y20.text is not None:
                                    year20.append(float(y20.text))
                              else:
                                    year20.append(None)
                        for y30 in properties.findall('d:BC_30YEAR', ns):
                              if y30.text is not None:
                                    year30.append(float(y30.text))
                              else:
                                    year30.append(None)


      #delete faulty data (manually checked)
      del dates[6831]
      del year1[6831]
      del year2[6831]
      del year3[6831]
      del year5[6831]
      del year10[6831]
      del year20[6831]
      del year30[6831]
      del dates[3457]
      del year1[3457]
      del year2[3457]
      del year3[3457]
      del year5[3457]
      del year10[3457]
      del year20[3457]
      del year30[3457]

      #sort data chronologically
      idx   = np.argsort(dates)
      dates = np.array(dates)[idx]
      year1 = np.array(year1)[idx]
      year2 = np.array(year2)[idx]
      year3 = np.array(year3)[idx]
      year5 = np.array(year5)[idx]
      year10 = np.array(year10)[idx]
      year20 = np.array(year20)[idx]
      year30 = np.array(year30)[idx]

      return dates, year1, year2, year3, year5, year10, year20, year30

def plotYieldCurves(dates, year1, year3, year5, year10, year20, year30):
      plt.plot(dates, year1, linewidth=0.75)
      plt.plot(dates, year3, linewidth=0.75)
      plt.plot(dates, year5, linewidth=0.75)
      plt.plot(dates, year10, linewidth=0.75)
      plt.plot(dates, year20, linewidth=0.75)
      plt.plot(dates, year30, linewidth=0.75)
      plt.axvspan(dates[125], dates[310], color='gray', alpha=0.5)
      plt.axvspan(dates[4482], dates[4877], color='gray', alpha=0.5)
      plt.axvspan(dates[2794], dates[2981], color='gray', alpha=0.5)
      plt.axvspan(dates[4386], dates[4448], color='red', alpha=0.25)
      plt.axvspan(dates[2560], dates[2672], color='red', alpha=0.25)
      plt.axvspan(dates[106], dates[134], color='red', alpha=0.25)
      plt.show()

def plot10yMinus2y(dates, y2, y10):
      diff = np.subtract(y10, y2)
      plt.plot(dates, diff, linewidth=0.75)
      plt.axhline(y=0.0, xmin=0.0, xmax=1.0, color='k', linewidth=0.75)
      plt.axhline(y=diff[-1], xmin=0.0, xmax=1.0, color='k', linewidth=0.75, linestyle = ':')
      plt.axvspan(dates[125], dates[310], color='gray', alpha=0.5)
      plt.axvspan(dates[4482], dates[4877], color='gray', alpha=0.5)
      plt.axvspan(dates[2794], dates[2981], color='gray', alpha=0.5)
      plt.axvspan(dates[4386], dates[4448], color='red', alpha=0.25)
      plt.axvspan(dates[2560], dates[2672], color='red', alpha=0.25)
      plt.axvspan(dates[106], dates[134], color='red', alpha=0.25)
      plt.show()

def main():
      URL = "https://data.treasury.gov/feed.svc/DailyTreasuryYieldCurveRateData"
      xmlData = getData(URL)
      d, y1, y2, y3, y5, y10, y20, y30 = parseXML(xmlData)
      plotYieldCurves(d, y1, y3, y5, y10, y20, y30)
      plot10yMinus2y(d, y2, y10)

if __name__ == "__main__":
      main()