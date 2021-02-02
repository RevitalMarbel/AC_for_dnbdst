# from poliastro.twobody import Orbit
#
# Orbit.from_horizons('Ceres')
#
# Orbit.from_sbdb('apophis')

from poliastro.examples import  molniya, iss,Orbit
from poliastro.czml.extract_czml import CZMLExtractor
from astropy.time import Time
from astropy import units as u



start_epoch = iss.epoch
print(start_epoch)
end_epoch = iss.epoch + molniya.period
print(end_epoch)
N = 100

EPOCH = Time(start_epoch, scale="tdb")
extractor = CZMLExtractor(start_epoch, end_epoch, N)
#roadster = Orbit.from_horizons(name="SpaceX Roadster", epoch=EPOCH, id_type="majorbody")

#extractor.add_orbit(roadster, label_text="SpaceX Roadster")
extractor.add_orbit(iss, label_text="ISS")
print(extractor.packets)