<script>
export let visible;
export let playlistID;

function disable(){
    visible=false;
}
</script>


<div class="modal" class:visible={false}>

    <!-- Modal content -->
    <div class="modal-content">
        <span class="close" on:click={disable}>&times;</span>
        <div class="modal-container">
            <div>Foo</div>
        </div>
    </div>

</div>
