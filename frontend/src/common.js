import {add_playlist} from "./stores";

export async function shufflePlaylist(playlistID) {

}

export async function setSchedule(playlistID, localTime, enabled) {
  let hour, minute;
  [hour, minute] = localTime.split(":");
  const date = new Date()
  date.setHours(hour, minute)
  const response = await fetch(`http://localhost/api/playlists/${playlistID}/`, {
    credentials: 'include',
    method: 'PATCH',
    body: JSON.stringify({
        "enabled": enabled,
        "playlist_schedule_minute": minute,
        "playlist_schedule_hour": hour
      }
    ),
    headers: {
      'Content-Type': 'application/json'
    }
  });
  add_playlist(await response.json());
}