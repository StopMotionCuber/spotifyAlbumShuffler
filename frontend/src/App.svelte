<script>

    export let name;
    import Header from "./Header.svelte";
    import PlaylistItem from "./PlaylistItem.svelte";

    let b2bPlaylists = [];
    let nonb2bPlaylists = [];

    async function fetchPlaylists() {
        let response = await fetch("http://localhost:8000/playlists/");
        let results = await response.json();
        for (const result of results) {
          if (result["back_to_back"]) {
            b2bPlaylists = [...b2bPlaylists, result];
          } else {
            nonb2bPlaylists = [...nonb2bPlaylists, result];
          }
        }
    }

    fetchPlaylists();


</script>

<main>
	<Header/>
	<div class="content">
    <h3>Your Back-to-back Album playlists:</h3>
    <div class="b2b-list">
        {#each b2bPlaylists as {id, playlist_name}, i}
            <PlaylistItem imgSource="resources/red-taylors-version.jpeg" playlistName="{playlist_name}"/>
        {/each}
    </div>
    <h3>Your other playlists:</h3>
    <div class="b2b-list">
        {#each nonb2bPlaylists as {id, playlist_name}, i}
            <PlaylistItem imgSource="resources/red-taylors-version.jpeg" playlistName="{playlist_name}"/>
        {/each}

    </div>
</div>
</main>

<style>
	main {
		margin: 0 auto;
	}
</style>
