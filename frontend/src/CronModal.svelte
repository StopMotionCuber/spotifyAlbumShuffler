<script>
  import {playlistsStore} from "./stores";
  import {setSchedule, shufflePlaylist} from "./common"
  import {createEventDispatcher} from "svelte";

  export let playlistID = 0;
  $: imgSource = playlistsStore[playlistID]["picture"];
  $: playlistName = playlistsStore[playlistID]["name"];
  $: playlistsInitiallyEnabled = playlistsStore[playlistID]["enabled"];
  let playlistEnabledState = playlistsStore[playlistID]["enabled"];
  let playlistTime = `${padNum(playlistsStore[playlistID]["hour"])}:${padNum(playlistsStore[playlistID]["minute"])}`;
  $: console.log(playlistTime);
  const dispatch = createEventDispatcher()

  function padNum(num) {
    return num.toString().padStart(2, '0');
  }

  function disable() {
    console.log("Clicked Playlist");
    dispatch('closed', {
      playlistID: playlistID
    });
  }

  async function saveState(event) {
    event.srcElement.disabled = true;
    await setSchedule(playlistID, playlistTime, playlistEnabledState);
    event.srcElement.disabled = false;
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

<div class="modal" on:click={disable}>

  <!-- Modal content -->
  <div class="modal-content" on:click={(e) => e.stopPropagation()}>
    <span class="close" on:click={disable}>&times;</span>
    <h3>Settings for the "{playlistName}" playlist</h3>
    Enabling the schedule for this playlist will shuffle it each day at a certain time.
    The time can be adjusted to specify the time of the day that the playlist is shuffled.
    Time will be given as local time
    <div class="modal-container">
      <img src={imgSource} alt="{playlistName} Cover Art" width="150" height="150">
      <div class="grid-table">
        <span class="table-specifier">Automatic shuffling enabled:</span>
        <label class="switch">
          <input type="checkbox" on:click bind:checked="{playlistEnabledState}">
          <span class="slider round"></span>
        </label>
        <span class="table-specifier">Time for shuffling:</span>
        <span><input type="time" class="small" bind:value={playlistTime}></span>
      </div>
    </div>
    <div class="button-area">
      <button on:click={shufflePlaylistClick} class="button">
        Shuffle playlist now
      </button>
      <button on:click={saveState} class="button">
        Save Schedule
      </button>
    </div>
  </div>
</div>
