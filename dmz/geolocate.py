#Using MaxMind, so import pygeoip
import pygeoip

def geolocate(ip_addresses):
  
  #Read in files, storing in memory for speed
  ip4_geo = pygeoip.GeoIP(filename = "/usr/share/GeoIP/GeoIP.dat", flags = 1)
  ip6_geo = pygeoip.GeoIP(filename = "/usr/share/GeoIP/GeoIPv6.dat", flags = 1)
  
  #Check type
  if not(isinstance(ip_addresses,list)):
    ip_addresses = [ip_addresses]
  
  #Construct output list
  output = []
    
  #For each entry in the input list, retrieve the country code and add it to the output object
  for entry in ip_addresses:
  
    if(bool(re.search(":",entry))):
      
      try:
        
        output.append(ip6_geo.country_code_by_addr(entry))
        
      except:
        
        output.append("Invalid")
        
    else:
      
      try:
        
        output.append(ip4_geo.country_code_by_addr(entry))
        
      except:
        
        output.append("Invalid")
  
  #Return
  return output
