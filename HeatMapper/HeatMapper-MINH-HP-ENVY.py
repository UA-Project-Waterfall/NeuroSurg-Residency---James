from pandas import read_excel
from pathlib import Path
import plotly.express as px

affMapInfo = ["AffiliationInfo.xlsx", "Count"]
resMapInfo = ["ResidencyInfo.xlsx", "Count"]

outputInfo = affMapInfo

filePath = Path.joinpath(Path(__file__).parent.resolve(), outputInfo[0])
dataframe = read_excel(filePath)
#dataframe["Count"] **= 2

fig = px.density_mapbox(dataframe, lat = 'Latitude', lon = 'Longitude', z = outputInfo[1],
                        radius = 30, zoom = 3.5, center = {"lat": 38, "lon": -105},
                        mapbox_style = 'open-street-map')
fig.show()