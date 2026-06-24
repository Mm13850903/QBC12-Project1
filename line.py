class Line:
    def __init__(self, name, source, destination, station_count, stations):
        self.name = name
        self.source = source
        self.destination = destination
        self.station_count = station_count
        self.stations = stations

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
    
    def show_info(self):
        print(f"Line: {self.name}")
        print(f"Route: {self.source} to {self.destination}")
        print(f"Stations ({self.station_count}): {" -> ".join(self.stations)}")