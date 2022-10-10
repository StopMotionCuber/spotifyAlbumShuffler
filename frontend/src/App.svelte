<script>

  import CronModal from "./CronModal.svelte";

  export let name;
  import Header from "./Header.svelte";
  import PlaylistItem from "./PlaylistItem.svelte";
  import {fetchPlaylists, b2bPlaylists} from "./stores";

  let loggedIn = false;
  let playlistsFetched = false;
  let playlistFetchMsg = "Fetching playlists...";
  let username = "";

  async function refreshPlaylists(event) {
    event.srcElement.disabled = true;
    playlistsFetched = false;
    playlistFetchMsg = "Refreshing playlists..."
    await fetch("http://localhost/api/refresh/", {credentials: 'include'});
    await fetchPlaylists(false);
    playlistsFetched = true;
    event.srcElement.disabled = false;
  }

  async function fetchUsernameInformation() {
    let response = await fetch("http://localhost/api/status/", {credentials: 'include'});
    let results = await response.json();
    loggedIn = results['logged_in'];
    username = results['display_name'];
  }

  async function main() {
    await fetchUsernameInformation();
    if (loggedIn) {
      console.log("Logged in");
      playlistFetchMsg = "Fetching playlists..."
      playlistsFetched = false;
      await fetchPlaylists();
      playlistsFetched = true;
    } else {
      console.log("not logged in");
    }
  }

  main();


</script>

<main>
  <Header loggedIn={loggedIn} username="{username}"/>
  {#if loggedIn}
  <div class="content">
    {#if playlistsFetched}
      <h3 class="heading">Your Back-to-back Album playlists:</h3>
    {:else}
      <h3 class="heading">{playlistFetchMsg}</h3>

    {/if}
    <div class="b2b-list">
      {#each $b2bPlaylists as {id, name, picture}, i}
        <PlaylistItem imgSource="{picture}" playlistName="{name}" backToBack="true"
                      playlistID="{id}"/>
      {/each}
    </div>
    <div class="general-interaction">
      <button on:click={refreshPlaylists} class="button" id="refresh-playlist">
        Refresh playlists
      </button>
    </div>
  </div>
  {:else}
    <h3 class="heading">You need to login via Spotify to use the spotify album shuffler</h3>
  {/if}
  <CronModal visible="true"/>
</main>

<style>
  main {
    margin: 0 auto;
  }
</style>
