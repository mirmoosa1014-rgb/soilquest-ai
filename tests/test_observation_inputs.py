import numpy as np
import pytest
from soilquest.model import predict


@pytest.mark.parametrize('records',[[{'index':-1,'value':30}],[{'index':True,'value':30}],[{'index':0,'value':float('nan')}],[{'index':0,'value':10},{'index':0,'value':20}]])
def test_invalid_observations_rejected(records):
    with pytest.raises(ValueError):predict(np.array([[0.,0.],[10.,10.]]),records)


def test_numpy_index_and_finite_measurements_supported():
    mean,sd=predict(np.array([[0.,0.],[10.,10.]]),[{'index':np.int64(0),'value':30.}])
    assert np.isfinite(mean).all() and np.isfinite(sd).all()
