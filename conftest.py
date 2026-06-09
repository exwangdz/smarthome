
"""
在请求之后清除数据
"""
import pytest
from commons.yaml_util import  clean_yaml

@pytest.fixture(scope="session",autouse=True)
def clean_extract():
    yield
    clean_yaml()