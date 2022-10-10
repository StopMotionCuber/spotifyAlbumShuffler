import {writable, get} from "svelte/store";

export const playlistsStore = {}
export const b2bPlaylists = writable([])
export const nonb2bPlaylists = writable([])

export async function fetchPlaylists() {
  console.log("Fetching playlists...");
  let response = await fetch("http://localhost/api/playlists/", {credentials: 'include'});
  let results = await response.json();
  for (const result of results) {
    add_playlist(result);
  }
  b2bPlaylists.set(Object.values(playlistsStore).filter(x => x['back_to_back']))
  nonb2bPlaylists.set(Object.values(playlistsStore).filter(x => !x['back_to_back']))
  console.log(get(b2bPlaylists))
}


function add_playlist(playlist) {
  const id = playlist["id"]
  playlistsStore[id] = {
    "last_snapshot": playlist["last_snapshot"],
    "name": playlist["playlist_name"],
    "spotify_id": playlist["spotify_playlist_id"],
    "id": id,
    "albums": playlist["albums_included"],
    "back_to_back": playlist["back_to_back"],
    "enabled": playlist["enabled"],
    "picture": playlist["playlist_picture_url"]
  }
}
