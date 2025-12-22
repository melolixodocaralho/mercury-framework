import datetime

def fake_sms():
    # Simulate sending SMS
    return ["Hello", "World"]

def test_fake_sms_returns_list():
    messages = fake_sms()
    assert isinstance(messages, list)

def test_fake_sms_content():
    messages = fake_sms()
    assert "Hello" in messages
