import pytest
from src.channel import Channel


@pytest.fixture
def chanel():
    return Channel('UC-OVMPlMA3-YCIeg4z5z23A')

def test_(chanel):
    assert chanel.print_info() == None

