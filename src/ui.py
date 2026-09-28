from database import *

#using ascii art for design
def print_banner():
    print("\n")
    print("╔══════════════════════════════════════════════════╗")
    print("║                                                  ║")
    print("║         ♫  M U S I C   M A T C H  ♫              ║")
    print("║        Your Personal Song Recommender            ║")
    print("║                                                  ║")
    print("╚══════════════════════════════════════════════════╝")
    print()

def print_box(title, items):
    width = 50
    print(f"  ┌{'─' * width}┐")
    print(f"  │{title:^{width}}│")
    print(f"  ├{'─' * width}┤")
    for item in items:
        print(f"  │  {item:<{width - 2}}│")
    print(f"  └{'─' * width}┘")

def login_signup():
    print_banner()
    print("         ACCOUNT \n1. Log into existing account \n2. Create new account")
    ch = int(input("Enter your choice (1-2): "))

    if ch == 1:
        print()
        username = input("  ► Username: ")
        password = input("  ► Password: ")
        user_id = login_user(username, password)
        if user_id:
            print("Login successful!")
            return user_id
        else:
            print("Invalid credentials, please try again")
            return None

    elif ch == 2:
        print()
        username = input("  ► Create username: ")
        password = input("  ► Create password: ")
        user_id = add_user(username, password)
        print("Account created successfully!")
        return user_id
    
#using unicode symbols for design
def main_menu(user_id):
    while True:
        print_box("MAIN MENU", [
            "1. ♫  View all songs",
            "2. +  Add a song",
            "3. ★  Rate a song",
            "4. ♥  Get recommendations",
            "5. ☰  View my ratings",
            "6. ✗  Logout"
        ])
        ch = int(input("\n  ► Enter your choice (1-6): "))

        if ch == 1:
            get_all_songs()

        elif ch == 2:
            song_title = input("  ► Song name: ")
            artist = input("  ► Artist name: ")
            genre = input("  ► Genre: ")
            add_song(song_title, artist, genre)

        elif ch == 3:
            song_id = int(input("  ► Enter the song id: "))
            rating = int(input("  ► Enter rating (1-5): "))
            rate_song(user_id, song_id, rating)

        elif ch == 4:
            recs = get_recommendations(user_id)
            if recs:
                print(f"\n  ┌{'─' * 50}┐")
                print(f"  │{"♥  RECOMMENDATIONS":^50}│")
                print(f"  ├{"─" * 50}┤")
                for song in recs:
                    line = f"We'd recommend {song['Song Title']} by {song['Artist']}"
                    print(f"  │  {line:<48}│")
                print(f"  └{'─' * 50}┘")
            else:
                print("No recommendations yet. Rate more sonSas!")

        elif ch == 5:
            ratgs = get_user_ratings(user_id)
            if ratgs:
                w1, w2, w3, w4 = 22, 18, 8, 22
                total = w1 + w2 + w3 + w4 + 5
                print(f"\n  ┌{'─' * total}┐") 
                print(f"  │{'★  MY RATINGS':^{total}}│")
                print(f"  ├{'─' * w1}┬{'─' * w2}┬{'─' * w3}┬{'─' * (w4 + 2)}┤")
                print(f"  │ {'Song':<{w1 - 1}}│ {'Artist':<{w2 - 1}}│ {'Rating':<{w3 - 1}}│ {'Date':<{w4 + 1}}│")
                print(f"  ├{'─' * w1}┼{'─' * w2}┼{'─' * w3}┼{'─' * (w4 + 2)}┤")
                for r in ratgs:
                    date = r["rated_date"] or "N/A"
                    s = r["song_title"][:w1 - 2]
                    a = r["artist"][:w2 - 2]
                    rt = str(r["rating"])
                    d = str(date)[:w4]
                    print(f"  │ {s:<{w1 - 1}}│ {a:<{w2 - 1}}│ {rt:<{w3 - 1}}│ {d:<{w4 + 1}}│")
                print(f"  └{'─' * w1}┴{'─' * w2}┴{'─' * w3}┴{'─' * (w4 + 2)}┘")
            else:
                print("You haven't rated any songs yet!")

        elif ch == 6:
            print("Logged out successfully. Goodbye! ♫")
            break

        else:
            print("Invalid choice, please try again!")

def run():
    user_id = login_signup()
    if user_id:
        main_menu(user_id)
    else:
        print("Login failed due to invalid credentials!")
