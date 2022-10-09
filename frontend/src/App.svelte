<script>

    export let name;
    import Header from "./Header.svelte";
    import PlaylistItem from "./PlaylistItem.svelte";

    let b2bPlaylists = [];
    let nonb2bPlaylists = [];
    let loggedIn = false;
    let playlistsFetched = false;
    let playlistFetchMsg = "";
    let username = "";

    async function refreshPlaylists() {
        playlistsFetched = false;
        playlistFetchMsg = "Refreshing playlists..."
        await fetch("http://localhost/api/refresh/", {credentials: 'include'});
        await fetchPlaylists(false);
    }

    async function fetchPlaylists(changeMessage=true) {
        console.log("Fetching playlists...");
        if (changeMessage) {
            playlistFetchMsg = "Fetching playlists..."
        }
        playlistsFetched = false;
        let response = await fetch("http://localhost/api/playlists/", {credentials: 'include'});
        let results = await response.json();
        b2bPlaylists = [];
        nonb2bPlaylists = [];
        for (const result of results) {
          if (result["back_to_back"]) {
            b2bPlaylists = [...b2bPlaylists, result];
          } else {
            nonb2bPlaylists = [...nonb2bPlaylists, result];
          }
        }
        playlistsFetched = true;
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
        await fetchPlaylists();
        console.log("Logged in");
      }
      else {
        console.log("not logged in");
      }
    }
    main();


</script>

<main>
	<Header loggedIn={loggedIn} username="{username}"/>
	<div class="content">
        {#if playlistsFetched}
            <h3 class="heading">Your Back-to-back Album playlists:</h3>
        {:else}
            <h3 class="heading">{playlistFetchMsg}</h3>

        {/if}
        <div class="b2b-list">
        {#each b2bPlaylists as {id, playlist_name, playlist_picture_url}, i}
            <PlaylistItem imgSource="{playlist_picture_url}" playlistName="{playlist_name}" backToBack="true" playlistID="{id}"/>
        {/each}
        </div>
        <button on:click={refreshPlaylists} class="button">
            Refresh playlists
        </button>
    </div>
</main>

<style>
	main {
		margin: 0 auto;
	}
</style>
