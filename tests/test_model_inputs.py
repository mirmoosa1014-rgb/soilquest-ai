import numpy as np
import pytest
from soilquest.model import predict


@pytest.mark.parametrize('field,value',[('length_m',0),('length_m',-1),('amplitude',-1),('noise_mgkg',-1),('mean',float('nan'))])
def test_invalid_gp_parameters_rejected_before_prediction(field,value):
    params=dict(length_m=18,mean=18,amplitude=45,noise_mgkg=3)
    params[field]=value
    with pytest.raises(ValueError):predict(np.array([[0.,0.],[1.,1.]]),[],params)
