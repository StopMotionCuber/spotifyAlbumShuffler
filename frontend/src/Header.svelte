<script>
    let loggedIn = false;
</script>

<header>
    <h1>Spotify Back2Back Album Shuffler</h1>
    <img class="github-logo" src="resources/GitHub-Mark-Light-64px.png" alt="GitHub logo" height="64" width="64"/>
    <div class="login-to-spotify">
        {#if loggedIn === false}
            <span class="account-text">
                Connect Spotify Account
            </span>
        {:else }
            <span class="account-text">
                Disconnect Spotify Account
            </span>
        {/if}
        <img class="spotify-logo" src="resources/Spotify_Icon_RGB_Green.png" height="48" width="48">
    </div>
</header>
