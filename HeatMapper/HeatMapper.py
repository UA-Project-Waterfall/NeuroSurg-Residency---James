from pandas import read_excel
from pathlib import Path
import plotly.express as px

filePath = Path.joinpath(Path(__file__).parent.resolve(), "AffiliationInfo.xlsx")
dataframe = read_excel(filePath)
#dataframe["Count"] **= 2

fig = px.density_mapbox(dataframe, lat = 'Latitude', lon = 'Longitude', z = 'Count',
                        radius = 20, zoom = 5, center = {"lat": 37.0902, "lon": -95.7129},
                        mapbox_style = 'open-street-map')
fig.show()