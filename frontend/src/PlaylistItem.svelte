<script>
    import {createEventDispatcher} from "svelte";

    export let imgSource;
    export let playlistName;
    export let playlistID;
    export let backToBack;
    const dispatch = createEventDispatcher()
    function playlistClick() {
        console.log("Clicked Playlist");
        dispatch('playlistClick', {
          playlistID: playlistID
        });
    }
</script>

<div class="b2b-item">
    <div class="b2b-artwork">
        <img loading="lazy" alt="{playlistName} Cover Art" class="cover-art" src="{imgSource}"
             on:click={playlistClick}
             height="120" width="120"/>
        <div class="b2b-refresh icon"><img src="resources/refresh.svg"/></div>
        <div class="b2b-shuffle icon"><img src="resources/shuffle.svg"></div>
    </div>
    <div class="b2b-playlisttitle"><div>{playlistName}</div></div>
</div>
