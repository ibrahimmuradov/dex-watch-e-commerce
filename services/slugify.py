def slugify(name):
    symbol_mapping = (
        (' ', '-'),
        ('.', '-'),
        (',', '-'),
        ('!', '-'),
        ('?', '-'),
        ("'", '-'),
        (":", '-'),
        ("/", '-'),
        ("\\", '-'),
        ("|", '-'),
        ('"', '-'),
        ('ə', 'e'),
        ('ı', 'i'),
        ('ö', 'o'),
        ('ğ', 'g'),
        ('ü', 'u'),
        ('ş', 's'),
        ('ç', 'c'),
    )

    name_url = name.strip().lower()

    for before, after in symbol_mapping:
        name_url = name_url.replace(before, after)

    return name_url