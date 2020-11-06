<template>
  <div class="home">

  </div>
</template>

<script>
// @ is an alias to /src

export default {
  name: 'SearchBar',
  data() {
    return {
      videoId: 'BRBdvdvj9jA'
    }
  },
  methods: {
    playVideo() {
      this.player.playVideo()
    },
  },
  computed: {
    player() {
      return this.$refs.youtube.player
    }
  }
}
</script>
