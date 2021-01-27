import pytest

from transport.sanic.endpoints.employees.get_all import AllEmployeeEndpoint


@pytest.mark.asyncio
async def test_all_employee_endpoint(request_factory, patched_context, mocker):
    patched_query = mocker.patch('db.queries.employee.get_employees')
    patched_query.return_value = []

    request = request_factory(method='get')
    endpoint = AllEmployeeEndpoint(None, patched_context, '', ())

    response = await endpoint(request)

    assert response.status == 200
