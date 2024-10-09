import pytest
import requests


@pytest.fixture(autouse=True)
def hobble_network(monkeypatch, request):
    """Hobble all network calls made through the requests library"""

    if "no_hobble_network" in request.keywords:
        return

    def hobbled_send(session, request_object, **kwargs):
        raise RuntimeError(f"requests hobbled for testing: tried calling {request_object.url}")

    monkeypatch.setattr(requests.Session, "send", hobbled_send)
