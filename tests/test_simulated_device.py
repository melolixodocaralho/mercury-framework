from mercury.simulated_device import SimulatedDevice


def test_device_info_contains_simulated():
    d = SimulatedDevice()
    info = d.device_info()
    assert "Simulated" in info or "simulated" in info.lower()


def test_fake_sms_returns_list():
    d = SimulatedDevice()
    sms = d.fake_sms()
    assert isinstance(sms, list)
    assert len(sms) >= 1
