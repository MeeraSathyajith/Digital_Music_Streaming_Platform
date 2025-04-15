import streamlit as st
from music import BST, Playlist, Library, Favorites

# --- Session State Initialization ---
if 'catalogue' not in st.session_state:
    st.session_state.catalogue = BST()
    st.session_state.catalogue.loadCatalogue()

if 'library' not in st.session_state:
    st.session_state.library = Library()

# Create an instance of the Favorites class
if 'favorites' not in st.session_state:
    st.session_state.favorites = Favorites()

# Shortcuts
catalogue = st.session_state.catalogue
library = st.session_state.library
favorites = st.session_state.favorites

st.title("Music Streaming Platform")

st.sidebar.header("Select an Action")
menu = st.sidebar.radio("Options", [
    "Add Song to Catalogue", "Search Song", "Delete Song",
    "Display Catalogue","Add Favorites", "Create Playlist", "Add Song to Playlist",
    "Remove Song from Playlist", "Display Playlists",
    "Display Songs in Playlist", "Remove Playlist", "View Favorites"
])

st.divider()

if menu == "Add Song to Catalogue":
    song = st.text_input("Enter song name")
    if st.button("Add Song"):
        if catalogue.searchSong(song):
            st.warning(f'"{song}" already exists.')
        else:
            catalogue.insertSong(song)
            catalogue.sortCatalogue()
            st.success(f'"{song}" added to catalogue.')

elif menu == "Search Song":
    song = st.text_input("Enter song name to search")
    if st.button("Search"):
        if catalogue.searchSong(song):
            st.success(f'"{song}" found.')
        else:
            st.error(f'"{song}" not found.')

elif menu == "Delete Song":
    song = st.text_input("Enter song name to delete")
    if st.button("Delete"):
        if catalogue.searchSong(song):
            catalogue.deleteSong(song)
            st.success(f'"{song}" deleted.')
        else:
            st.warning(f'"{song}" not found in catalogue.')

elif menu == "Display Catalogue":
    st.subheader("🎶 Catalogue")
    st.write(catalogue.displayCatalogue())


elif menu == "Add Favorites":
    st.subheader("Favorites")
    songs = catalogue.displayCatalogue()

    # Loop through the songs and display them with a heart button
    for song in songs:
        cols = st.columns([8, 1])
        with cols[0]:
            st.write(song)
        with cols[1]:
            if st.button(f"❤️", key=song):
                favorites.add_favorite(song)
                with cols[0]:
                    st.success(f'"{song}" added to favorites!')
                



elif menu == "Create Playlist":
    playlist_name = st.text_input("Enter playlist name")
    if st.button("Create"):
        existing = any(pl.playlist.name == playlist_name for pl in iter(lambda: library.head, None))
        temp = library.head
        while temp:
            if temp.playlist.name == playlist_name:
                existing = True
                break
            temp = temp.next

        if existing:
            st.warning(f'Playlist "{playlist_name}" already exists!')
        else:
            playlist = Playlist(playlist_name)
            library.addPlaylist(playlist)
            st.success(f'Playlist "{playlist_name}" created.')

elif menu == "Add Song to Playlist":
    playlist_name = st.text_input("Enter playlist name")
    song = st.text_input("Enter song name to add")
    if st.button("Add to Playlist"):
        temp = library.head
        playlist_found = None
        while temp:
            if temp.playlist.name == playlist_name:
                playlist_found = temp.playlist
                break
            temp = temp.next

        if not playlist_found:
            st.error(f'Playlist "{playlist_name}" not found!')
        elif not catalogue.searchSong(song):
            st.error(f'Song "{song}" not in catalogue.')
        elif song.lower() in playlist_found.getPlaylist():
            st.warning(f'"{song}" already in "{playlist_name}".')
        else:
            playlist_found.addSong(song)
            st.success(f'"{song}" added to "{playlist_name}".')

elif menu == "Remove Song from Playlist":
    playlist_name = st.text_input("Enter playlist name")
    song = st.text_input("Enter song to remove")
    if st.button("Remove Song"):
        temp = library.head
        while temp:
            if temp.playlist.name == playlist_name:
                if song.lower() in temp.playlist.getPlaylist():
                    temp.playlist.removeSong(song)
                    st.success(f'"{song}" removed from "{playlist_name}".')
                else:
                    st.error(f'"{song}" not found in "{playlist_name}".')
                break
            temp = temp.next
        else:
            st.warning(f'Playlist "{playlist_name}" not found!')

elif menu == "Display Playlists":
    st.subheader("🎧 All Playlists")
    st.write(library.getLibrary())

elif menu == "Display Songs in Playlist":
    name = st.text_input("Enter playlist name")
    if st.button("Show Songs"):
        temp = library.head
        while temp:
            if temp.playlist.name == name:
                st.write(temp.playlist.getPlaylist())
                break
            temp = temp.next
        else:
            st.warning(f'Playlist "{name}" not found!')

elif menu == "Remove Playlist":
    name = st.text_input("Enter playlist name to delete")
    if st.button("Delete Playlist"):
        temp = library.head
        found = False
        while temp:
            if temp.playlist.name == name:
                library.deletePlaylist(name)
                st.success(f'Playlist "{name}" deleted.')
                found = True
                break
            temp = temp.next
        if not found:
            st.error(f'Playlist "{name}" not found!')

elif menu == "View Favorites":
    st.subheader("❤️ Your Favorite Songs")
    favorite_songs = favorites.get_favorites()

    if favorite_songs:
        for song in favorite_songs:
            cols = st.columns([8, 1])
            with cols[0]:
                st.write(song)
            with cols[1]:
                if st.button("❤️", key=song):
                    favorites.remove_favorite(song)
                    with cols[0]:
                        st.success(f'"{song}" removed from favorites.')
                    break  # stop after one update to avoid Streamlit re-run issues
    else:
        st.info("You have no favorite songs yet.")


   
