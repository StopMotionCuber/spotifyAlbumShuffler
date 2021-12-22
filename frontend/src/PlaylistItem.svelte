<script>
    export let imgSource;
    export let playlistName;
    export let playlistID;
    export let backToBack;
</script>

<div class="b2b-item">
    <div class="b2b-artwork">
        <img alt="{playlistName} Cover Art" class="cover-art" src="{imgSource}" height="150" width="150"/>
        <div class="b2b-refresh"><img src="resources/refresh.svg"/></div>
        <div class="b2b-shuffle"><img src="resources/shuffle.svg"></div>
    </div>
    <div class="b2b-playlisttitle">{playlistName}</div>
</div>
