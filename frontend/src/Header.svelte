<script>
    export let loggedIn = false;
    export let username = "";
</script>

<header>
    <h1>Spotify Back2Back Album Shuffler</h1>
    <img class="github-logo" src="resources/GitHub-Mark-Light-64px.png" alt="GitHub logo" height="64" width="64"/>
    <div class="login-to-spotify">
        {#if loggedIn === false}
            <a href="http://localhost/login/">
            <span class="account-text">
                Connect Spotify Account
            </span>
            </a>
        {:else }
            <span class="account-text">
                Hello { username }
            </span>
        {/if}
        <img class="spotify-logo" src="resources/Spotify_Icon_RGB_Green.png" height="48" width="48">
    </div>
</header>
