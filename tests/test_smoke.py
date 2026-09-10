def test_smoke():
    from services.intent import detect_intent
    assert detect_intent("اشتراك عائلي") == "family_subscription"
    assert detect_intent("كم سعر الاشتراك") == "pricing_redirect"
