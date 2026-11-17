import pytest
import numpy as np
from soilquest.field import generate,Sampler

@pytest.mark.parametrize('seed',[True,False,-1,100001,1.5,'1',None])
def test_invalid_field_seeds_rejected_before_sampling(seed):
    with pytest.raises(ValueError):generate(seed=seed)

def test_numpy_seed_replays_and_has_plain_integer_metadata():
    field=generate(seed=np.int64(41));plain=generate(seed=41)
    assert type(field['seed']) is int
    assert Sampler(field).sample(0)==Sampler(plain).sample(0)
