<script>
  import {playlistsStore} from "./stores";
  import {shufflePlaylist} from "./common"
  import {createEventDispatcher} from "svelte";
  import Toggle from "./Toggle.svelte";

  export let playlistID = 0;
  $: imgSource = playlistsStore[playlistID]["picture"];
  $: playlistName = playlistsStore[playlistID]["name"];
  $: playlistsEnabled = playlistsStore[playlistID]["enabled"];
  const dispatch = createEventDispatcher()

  function disable() {
    console.log("Clicked Playlist");
    dispatch('closed', {
      playlistID: playlistID
    });
  }

  async function shufflePlaylistClick(event) {
    event.srcElement.disabled = true;
    await shufflePlaylist(playlistID);
    event.srcElement.disabled = false;
  }

  function handleSubscription() {
    console.log("Clicked Playlist")
  }

</script>

<div class="modal">

  <!-- Modal content -->
  <div class="modal-content">
    <span class="close" on:click={disable}>&times;</span>
    <h3>Settings for the "{playlistName}" playlist</h3>
    <div class="modal-container">
      <img src={imgSource} alt="{playlistName} Cover Art" width="150" height="150">
      <div class="grid-table">
        <span class="table-specifier">Automatic shuffling enabled:</span>
        <Toggle bind:value={playlistsEnabled} on:click={handleSubscription}/>
        <span class="table-specifier">Time for shuffling:</span>
        <span><input type="time" class="small"></span>
      </div>
    </div>
    <div class="button-area">
      <button on:click={shufflePlaylistClick} class="button" bind:disabled={}>
        Shuffle playlist now
      </button>
    </div>
  </div>
</div>
