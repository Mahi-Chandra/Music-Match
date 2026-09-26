import sqlite3
def init_database():
    conn = sqlite3.connect("musicmatch.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS songs(
            song_id INTEGER PRIMARY KEY,
            song_title TEXT NOT NULL,
            artist TEXT NOT NULL,
            genre TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ratings(
            rating_id INTEGER PRIMARY KEY,
            user_id INTEGER,
            song_id INTEGER,
            rating INTEGER NOT NULL,
            rated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(user_id),
            FOREIGN KEY (song_id) REFERENCES songs(song_id)
        )
    """)

    conn.commit()
    conn.close()

def add_user(username,password):
    conn = sqlite3.connect("musicmatch.db")
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO users(username,password)
            VALUES(?,?)
        """, (username,password))
        conn.commit()
        user_id = cursor.lastrowid
        return user_id
    except sqlite3.IntegrityError:
        cursor.execute("SELECT user_id FROM users WHERE username = ?",(username,))
        existing = cursor.fetchone()
        if existing:
            return existing[0]
        return None
    finally:
        conn.close()

def login_user(username,password):
    conn = sqlite3.connect("musicmatch.db")
    cursor = conn.cursor()
    cursor.execute("SELECT user_id FROM users where username = ? AND password = ?", (username,password))
    user = cursor.fetchone()
    conn.close()
    if user:
        return user[0]
    return None

def add_song(title,artist,genre):
    conn = sqlite3.connect("musicmatch.db")
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO songs
            (song_title,artist,genre)
            VALUES(?,?,?)
        """, (title,artist,genre))
        conn.commit()
        print(f"Song added successfully")
    except sqlite3.IntegrityError as error:
        print(f"Error: {error}")
    finally:
        conn.close()

def rate_song(user_id, song_id, rating):
    conn = sqlite3.connect("musicmatch.db")
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO ratings
            (user_id, song_id, rating)
            VALUES(?,?,?)
        """, (user_id, song_id, rating))
        conn.commit()
        print(f"Rating successfully added!")
    except sqlite3.IntegrityError as error:
        print(f"Error: {error}")
    finally:
        conn.close()

def get_all_songs():
    conn = sqlite3.connect("musicmatch.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, song_title, artist, genre FROM songs")
    songs = cursor.fetchall()
    conn.close()
    print("="*30, "SONG LIST", "="*30)
    for i in songs:
        print(i)

def get_user_ratings(user_id):
    conn = sqlite3.connect("musicmatch.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT song_id, rating
        FROM ratings WHERE user_id = ?
    """, (user_id,))
    rows = cursor.fetchall()
    conn.close()
    return[
        {"song_id": r[0], "rating": r[1]}
        for r in rows
    ]

def get_song_ratings(song_id):
    conn = sqlite3.connect("musicmatch.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT songs.song_title, users.user_id, ratings.rating, ratings.rated_date
        FROM ratings
        JOIN users ON ratings.user_id = users.user_id
        JOIN songs ON ratings.song_id = songs.id
        WHERE ratings.song_id = ?
    """,(song_id,))
    rows = cursor.fetchall()
    conn.close()
    if rows:
        return [
            {"Song_Title": r[0], "User_ID": r[1], "Rating": r[2], "On date": r[3]}
            for r in rows
        ]
    return None

def get_recommendations(user_id):
    my_songs = get_user_ratings(user_id)
    my_song_ids = [s["song_id"] for s in my_songs]

    similar_users = set()
    for song_id in my_song_ids:
        all_raters = get_song_ratings(song_id)
        if all_raters:
            for rater in all_raters:
                other_user_id = rater["User_ID"]
                if other_user_id != user_id: 
                    similar_users.add(other_user_id)
    
    recommended_songs = {} 
    for similar_user_id in similar_users:
        their_ratings = get_user_ratings(similar_user_id)
        for song in their_ratings:
            song_id = song["song_id"]
            if song_id not in my_song_ids: 
                recommended_songs[song_id] = recommended_songs.get(song_id, 0) + 1
    
    top_recommendations = sorted(recommended_songs.items(), key=lambda x: x[1], reverse=True)[:3]
    return top_recommendations

