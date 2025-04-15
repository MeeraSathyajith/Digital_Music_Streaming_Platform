class SongNode:
    def __init__(self, song_name):
        self.song_name = song_name.lower()
        self.left = None
        self.right = None


class BST:
    def __init__(self):
        self.root = None

    def insertSong(self, song_name):
        def insert(node, song_name):
            if node is None:
                return SongNode(song_name)
            if song_name < node.song_name:
                node.left = insert(node.left, song_name)
            elif song_name > node.song_name:
                node.right = insert(node.right, song_name)
            return node
        self.root = insert(self.root, song_name.lower())

    def searchSong(self, song_name):
        def search(node, song_name):
            if node is None or node.song_name == song_name:
                return node
            if song_name < node.song_name:
                return search(node.left, song_name)
            return search(node.right, song_name)

        return search(self.root, song_name.lower())

    def deleteSong(self, song_name):
        def delete(node, song_name):
            if node is None:
                return node
            if song_name < node.song_name:
                node.left = delete(node.left, song_name)
            elif song_name > node.song_name:
                node.right = delete(node.right, song_name)
            else:
                if node.left is None:
                    return node.right
                elif node.right is None:
                    return node.left
                temp = self._minNode(node.right)
                node.song_name = temp.song_name
                node.right = delete(node.right, temp.song_name)
            return node
        self.root = delete(self.root, song_name.lower())

    def _minNode(self, node):
        current = node
        while current.left is not None:
            current = current.left
        return current

    def displayCatalogue(self):
        songs = []

        def inorder(node):
            if node:
                inorder(node.left)
                songs.append(node.song_name)
                inorder(node.right)

        inorder(self.root)
        return songs
    
    def loadCatalogue(self, filename="songs.txt"):
        try:
            with open(filename, "r") as file:
                for line in file:
                    song = line.strip()
                    if song:
                        self.insertSong(song)
            self.sortCatalogue()
            print("Catalogue loaded from file successfully.")
        except FileNotFoundError:
            print(f"File '{filename}' not found.")


    def getCatalogue(self):
        return self.displayCatalogue()

    def sortCatalogue(self):
        sorted_songs = self.displayCatalogue()
        self.root = None
        for song in sorted_songs:
            self.insertSong(song)


class PlaylistNode:
    def __init__(self, song_name):
        self.song_name = song_name.lower()
        self.next = None


class Playlist:
    def __init__(self, name):
        self.name = name  
        self.head = None

    def addSong(self, song_name):
        new_song = PlaylistNode(song_name)
        if not self.head:
            self.head = new_song
            return
        temp = self.head
        while temp.next:
            temp = temp.next
        temp.next = new_song

    def removeSong(self, song_name):
        song_name = song_name.lower()
        temp = self.head

        if temp and temp.song_name == song_name:
            self.head = temp.next
            return

        prev = None
        while temp and temp.song_name != song_name:
            prev = temp
            temp = temp.next

        if temp is None:
            print(f'Song "{song_name}" not found in the playlist.')
            return

        prev.next = temp.next

    def getPlaylist(self):
        songs = []
        temp = self.head
        while temp:
            songs.append(temp.song_name)
            temp = temp.next
        return songs


class LibraryNode:
    def __init__(self, playlist):
        self.playlist = playlist
        self.next = None


class Library:
    def __init__(self):
        self.head = None

    def addPlaylist(self, playlist):
        new_node = LibraryNode(playlist)
        if not self.head:
            self.head = new_node
            return
        temp = self.head
        while temp.next:
            temp = temp.next
        temp.next = new_node

    def deletePlaylist(self, playlist_name):
        temp = self.head
        if temp and temp.playlist.name == playlist_name:
            self.head = temp.next
            return
        prev = None
        while temp and temp.playlist.name != playlist_name:
            prev = temp
            temp = temp.next
        if temp is None:
            return
        prev.next = temp.next

    def getLibrary(self):
        playlists = []
        temp = self.head
        while temp:
            playlists.append(temp.playlist.name)
            temp = temp.next
        return playlists

class Favorites:
    def __init__(self):
        self.favorites = []  # List to store favorite songs

    def add_favorite(self, song_name):
        if song_name not in self.favorites:
            self.favorites.append(song_name)
        else:
            print(f'"{song_name}" is already in your favorites.')

    def remove_favorite(self, song_name):
        if song_name in self.favorites:
            self.favorites.remove(song_name)
        else:
            print(f'"{song_name}" is not in your favorites.')

    def get_favorites(self):
        return self.favorites



if __name__ == "__main__":
    allSongsBST = BST()
    musicLibrary = Library()
    allSongsBST.loadCatalogue()  


    while True:
        print("\nMusic Streaming Platform")
        print("1. Add Song to Catalogue")
        print("2. Search Song")
        print("3. Delete Song")
        print("4. Display Catalogue")
        print("5. Create Playlist")
        print("6. Add Song to Playlist")
        print("7. Remove Song from Playlist")
        print("8. Display Playlists")
        print("9. Display Songs in Playlist")
        print("10. Remove Playlist")
        print("11. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            song = input("Enter song name: ")
            found = allSongsBST.searchSong(song)
            if found:
                print(f'"{song}" already exists.')
            else:
                allSongsBST.insertSong(song)
                allSongsBST.sortCatalogue()
                print(f'"{song}" added.')

        elif choice == "2":
            song = input("Enter song name: ")
            found = allSongsBST.searchSong(song)
            print(f'"{song}" found.' if found else f'"{song}" not found.')

        elif choice == "3":
            song = input("Enter song name: ")
            found = allSongsBST.searchSong(song)
            if found:
                allSongsBST.deleteSong(song)
                print(f'"{song}" deleted.')
            else:
                print(f'"{song}" not found.')
            

        elif choice == "4":
            print("Catalogue:", allSongsBST.displayCatalogue())

        elif choice == "5":
            name = input("Enter playlist name: ")
            existing = False
            current = musicLibrary.head
            while current:
                if current.playlist.name == name:
                    existing = True
                    break
                current = current.next

            if existing:
                print(f'Playlist "{name}" already exists!')
            else:
                playlist = Playlist(name)
                musicLibrary.addPlaylist(playlist)
                print(f'Playlist "{name}" created.')

        elif choice == "6":
            name = input("Enter playlist name: ")
            temp = musicLibrary.head
            playlist_found = None
            
            while temp:
                if temp.playlist.name == name:
                    playlist_found = temp.playlist
                    break
                temp = temp.next

            if not playlist_found:
                print(f'Error: Playlist "{name}" not found!')
            else:
                song = input("Enter song name: ")
                if not allSongsBST.searchSong(song):
                    print(f'Error: "{song}" not found in catalogue')
                elif song.lower() in [s.lower() for s in playlist_found.getPlaylist()]:
                    print(f'"{song}" is already in "{name}"!')
                else:
                    playlist_found.addSong(song)
                    print(f'"{song}" added to "{name}".')


        elif choice == "7":
            name = input("Enter playlist name: ")
            song = input("Enter song name: ")
            temp = musicLibrary.head

            while temp:
                if temp.playlist.name == name:
                    if song.lower() in temp.playlist.getPlaylist():
                        temp.playlist.removeSong(song)
                        print(f'"{song}" removed from "{name}".')
                    else:
                        print(f'"{song}" not found in playlist "{name}".')
                    break 
                temp = temp.next  

            else:
                print(f'Playlist "{name}" not found!')


        elif choice == "8":
            print("Playlists:", musicLibrary.getLibrary())

        elif choice == "9":
            name = input("Enter playlist name: ")
            temp = musicLibrary.head
            while temp:
                if temp.playlist.name == name:
                    print("Songs:", temp.playlist.getPlaylist())
                    break
                temp = temp.next
            else:
                print(f'Playlist "{name}" not found!')

        elif choice == "10":
            name = input("Enter playlist name to be deleted: ")
            temp = musicLibrary.head
            while temp:
                if temp.playlist.name == name:
                    musicLibrary.deletePlaylist(name)
                    print(f'"{name}" deleted.')
                    break
                temp = temp.next
            else:
                print(f'Playlist "{name}" not found!')
        
        elif choice == "11":
            break

        else:
            print("Invalid choice! Try again.")

