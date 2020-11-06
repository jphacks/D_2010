<template>
  <div class="home" style="display: flex; justify-content: center;">
    <div style="width: 650px; max-width: 100vw; margin-right: 0; margin-left: 0;">
      <div style="display: flex; flex-direction: row; ">
        <v-text-field v-model="query" @keydown.enter="changeVideo"></v-text-field>
        <v-btn depressed
               color="primary"
               @click="changeVideo">
          検索
        </v-btn>
      </div>

      <div style="width: 100%; padding: 10px;">
        <youtube :video-id="videoId" ref="youtube"></youtube>
      </div>

      <div style="display: flex; flex-direction: row; justify-content: center;">
        <v-btn depressed
               color="rgba(0,0,0,0.3)"
               @click="sendReaction('happy')">
          <img width="20" src="@/assets/happy.png">
        </v-btn>
        <v-btn depressed
               color="rgba(0,0,0,0.3)"
               @click="sendReaction('happy')">
          <img width="20" src="@/assets/sad.png">
        </v-btn>
        <v-btn depressed
               color="rgba(0,0,0,0.3)"
               @click="sendReaction('happy')">
          <img width="20" src="@/assets/wow.png">
        </v-btn>
        <v-btn depressed
               color="rgba(0,0,0,0.3)"
               @click="sendReaction('happy')">
          <img width="20" src="@/assets/love.png">
        </v-btn>
      </div>
    </div>
    <transition name="fade">
      <div v-if="isHappy" class="animation" :style="{ backgroundImage: 'url(' + require('@/assets/giphy.gif') + ')' }">
      </div>
    </transition>
  </div>
</template>

<script>
const axios = require('axios')

export default {
  name: 'Home',
  data() {
    return {
      videoId: "",
      query: "",
      reaction: "",
      interval: undefined,
      isHappy: false,
    }
  },
  created() {
    this.interval = setInterval(this.receiveReaction, 1000)
  },
  beforeDestroy() {
    if (this.interval) {
      clearInterval(this.interval)
      this.interval = undefined
    }
  },
  methods: {
    playVideo() {
      this.player.playVideo()
    },
    changeVideo() {
      let temp;
      this.getLiveid().then((response) => {
        temp = response.data;
        this.videoId = temp.id;
      })
    },
    sendReaction(reaction) {
      this.reaction = reaction;
      this.setReaction()
    },
    receiveReaction() {
      let temp;
      this.getReaction().then((response) => {
        temp = response.data;
        if (temp.reaction === "happy") {
          this.isHappy = true;
        } else {
          this.isHappy = false;
        }
      })
    },
    async getLiveid() {
      try {
        return await
            axios.get("http://l9vkj.mocklab.io/search", {params: this.axiosParams})
      } catch (error) {
        console.error(error)
      }
    },
    async getReaction() {
      try {
        return await
            axios.get("http://l9vkj.mocklab.io/getReaction", {params: this.getReactionParams})
      } catch (error) {
        console.error(error)
      }
    },
    async setReaction() {
      const client = axios.create({
        headers: {
          'Content-Type': 'application/json',
        },
      });
      try {
        return await await client.post("http://l9vkj.mocklab.io/setReaction", this.reactionParams);
      } catch (error) {
        console.error(error)
      }
    },

  },
  computed: {
    axiosParams() {
      const params = new URLSearchParams();
      params.append('name', this.query);
      return params;
    },
    reactionParams() {
      const body = new URLSearchParams();
      body.append('id', this.videoId);
      body.append('reaction', this.reaction);
      return body;
    },
    getReactionParams() {
      const body = new URLSearchParams();
      body.append('id', this.videoId);
      return body;
    },
    player() {
      return this.$refs.youtube.player
    }
  }
}
</script>

<style lang="scss">

iframe {
  width: 100%;
  max-width: 650px; /* Also helpful. Optional. */
}

.animation {
  width: 100vw;
  height: 100vh;
  z-index: 300;
  position: fixed;
  top: 0;
  left: 0;
  background-size: cover;
}

.fade-enter-active, .fade-leave-active {
  transition: opacity .8s;
}

.fade-enter, .fade-leave-to /* .fade-leave-active below version 2.1.8 */
{
  opacity: 0;
}
</style>
