from ._anvil_designer import HomeTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

class Home(HomeTemplate):
  markers = []
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
    impacts = anvil.server.call("get_bomb_impacts") # einschlag_id, einschlag_name, bomben_name, datum, latitude, longitude, todesopfer, verletzte, beschreibung
    
    for impact in impacts:
      marker = GoogleMap.Marker(position={"lat": impact['latitude'], "lng": impact['longitude']}, title=impact['einschlag_name'])
      marker.set_event_handler('click', lambda i_id=impact['einschlag_id'], **e: self.open_details(i_id))

      #i =GoogleMap.InfoWindow(content=Label(text=impact['einschlag_name']))
      #i.open(map, marker)
      self.markers.append(marker)
      
      self.map_1.add_component(marker)


  def open_details(self, impact_id: int):

    open_form('Impact_Detail',impact_id)