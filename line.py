class Line:
    def __init__(self, name, source, destination, station_count, stations):
        self.name = name
        self.source = source
        self.destination = destination
        if int(station_count) != len(stations):
            raise ValueError(f"Error: The number of stations entered ({station_count}) does not match the list of stations ({len(stations)})")

        self._station_count = int(station_count)
        self.stations = stations

    @property
    def station_count(self):
        return self._station_count
    
    @station_count.setter
    def station_count(self, value):
        if value < 0:
            raise ValueError("station_count cannot be negative")
        self._station_count = value

    def get_name(self):
        return self.name
    def get_source(self):
        return self.source
    def get_destination(self):
        return self.destination
    def get_station_count(self):
        return self.station_count
    def get_stations(self):
        return self.stations
    
    def show_information(self):
        print(f"Line: {self.name}")
        print(f"Route: {self.source} to {self.destination}")
        print(f"Stations ({self.station_count}): {' -> '.join(self.stations)}")

    def __str__(self):
        return f"Line: {self.name} | Stations: {self.station_count}"
