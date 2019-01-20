import requests
import numpy as np
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
from datetime import datetime
from pandas import Series


URL = "https://data.treasury.gov/feed.svc/DailyTreasuryYieldCurveRateData"

response = requests.get(URL)
root = ET.fromstring(response.content)

ns = {'m': 'http://schemas.microsoft.com/ado/2007/08/dataservices/metadata',
      'd': 'http://schemas.microsoft.com/ado/2007/08/dataservices', 
      't': 'http://www.w3.org/2005/Atom'}


dates = []
year1 = []
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


del dates[6831]
del year1[6831]
del year3[6831]
del year5[6831]
del year10[6831]
del year20[6831]
del year30[6831]

idx   = np.argsort(dates)
dates = np.array(dates)[idx]
year1 = np.array(year1)[idx]
year3 = np.array(year3)[idx]
year5 = np.array(year5)[idx]
year10 = np.array(year10)[idx]
year20 = np.array(year20)[idx]
year30 = np.array(year30)[idx]


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


