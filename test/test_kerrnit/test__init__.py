import kerrnit

def test_load_alteration_rules():
    kerrnit.load_alteration_rules("test/_data/rules.txt")
    assert kerrnit._alt_rules == (
            ('m', 'rn'),
            ('l', 'I'),
            ('l', '1'),
            ('d', 'cl'),
            ('i', 'j'),
            ('w', 'vv'),
            ('y', 'v'),
            ('v', 'y'),
            ('rn', 'm')
            )

def test_get_alterations():
    kerrnit._alt_rules = [
        ('m', 'rn'),
        ('l', 'I'),
        ('l', '1'),
        ('d', 'cl'),
        ('i', 'j'),
        ('w', 'vv'),
        ('y', 'v')
    ]
    results = kerrnit.get_alterations("amazom")
    assert results == set((
        'arnazorn',
        'arnazom',
        'amazorn'
        ))

