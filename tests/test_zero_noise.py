import numpy as np
from soilquest.model import predict

def test_duplicate_coordinates_zero_noise_are_stable():
 coords=np.array([[0.,0.],[0.,0.],[10.,10.]])
 records=[{'index':0,'value':30.},{'index':1,'value':30.}]
 mean,sd=predict(coords,records,dict(length_m=20.,mean=10.,amplitude=30.,noise_mgkg=0.))
 assert np.isfinite(mean).all() and np.isfinite(sd).all()
 assert abs(mean[0]-30)<1e-5 and np.all(sd>=0)
