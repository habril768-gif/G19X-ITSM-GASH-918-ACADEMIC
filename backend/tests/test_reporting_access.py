from unittest.mock import Mock
import pytest
from app.reporting.access import provision,ReportingAccessError

@pytest.mark.parametrize('name,password',[('postgres;drop database','Synthetic-123456789'),('x','Synthetic-123456789'),('qa_bi','short')])
def test_invalid_login_is_rejected_before_database(name,password):
    connection=Mock()
    with pytest.raises(ReportingAccessError): provision(connection,name,password)
    assert connection.mock_calls==[]
