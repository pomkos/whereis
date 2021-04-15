from whereis import message_maker


def test_message_maker():
    message = message_maker(['a', 'Austin, tx'], 'loc_current')
    assert message.lstrip() == '* As of a he is in __Austin, tx__.'
