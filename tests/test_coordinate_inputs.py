import numpy as np
import pytest
from soilquest.model import predict
@pytest.mark.parametrize('coords',[np.ones(3),np.ones((2,3)),np.array([[np.nan,0]]),np.array([[np.inf,0]])])
def test_invalid_coordinates_rejected_even_without_samples(coords):
 with pytest.raises(ValueError):predict(coords,[])
