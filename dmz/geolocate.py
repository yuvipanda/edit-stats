"""
Provides simple functions that geo-locate an IP address (IPv4 or IPv4) using the
MaxMind Geo Database.
"""
import pygeoip
import socket


class GeoLocator(object):
    """Geo locate IP addresses using the MaxMind database"""
    def __init__(self, ipv4_geo_path='/usr/share/GeoIP/GeoIP.dat',
                 ipv6_geo_path='/usr/share/GeoIP/GeoIPv6.dat'):
        self.ipv4_geo_path = ipv4_geo_path
        self.ipv6_geo_path = ipv6_geo_path

    @property
    def ipv4_geo(self):
        """Return an instance of pygeoip.GeoIP loaded with IPv4 geolocation data.

        The data is stored in memory, and loaded up only when first requested"""
        if not hasattr(self, '_ipv4_geo'):
            self._ipv4_geo = pygeoip.GeoIP(filename=self.ipv4_geo_path, flags=1)
        return self._ipv4_geo

    @property
    def ipv6_geo(self):
        """Return an instance of pygeoip.GeoIP loaded with IPv6 geolocation data.

        The data is stored in memory, and loaded up only when first requested"""
        if not hasattr(self, '_ipv6_geo'):
            self._ipv6_geo = pygeoip.GeoIP(filename=self.ipv6_geo_path, flags=1)
        return self._ipv6_geo

    def _check_if_ipv6(self, ip_address):
        """Return true if given ip_address is IPv6, false otherwise"""
        try:
            # socket.inet_pton throws an exception if it isn't a valid address
            # of the stated address class
            socket.inet_pton(socket.AF_INET6, ip_address)
            return True
        except:
            return False

    def find_country(self, ip_address):
        """Return best guess of country in which this IP address resides"""
        if self._check_if_ipv6(ip_address):
            return self.ipv6_geo.country_code_by_addr(ip_address)
        else:
            return self.ipv4_geo.country_code_by_addr(ip_address)
