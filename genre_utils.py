GENRE_GROUPS = {
    'POP': ['pop'],
    'Rock': ['rock', 'metal', 'punk', 'grunge'],
    'Hip Hop': ['hip hop', 'rap', 'trap'],
    'Electronic': ['electro', 'house', 'techno', 'edm', 'dance'],
    'R&B': ['r&b', 'soul', 'funk'],
    'Jazz': ['jazz'],
    'Classical': ['classical', 'orchestra'],
    'Latin': ['latin', 'reggaeton', 'salsa', 'bachata'],
    'Country': ['country'],
    'Folk': ['folk', 'acoustic'],
    'Reggae': ['reggae', 'ska'],
    'Blues': ['blues']
}

UNRECOGNIZED_GENRES = set()

def normalize_genre(raw_genre):
    raw_genre = raw_genre.lower().strip()
    for group, keywords in GENRE_GROUPS.items():
        if any(keyword in raw_genre for keyword in keywords):
            return group
    UNRECOGNIZED_GENRES.add(raw_genre)
    return 'other'