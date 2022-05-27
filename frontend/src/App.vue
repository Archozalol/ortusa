<script setup>
import { ref } from "vue";
import messages from "./components/messages.js";
import Message from "./components/Message.vue";
import TypingIndicator from "./components/TypingIndicator.vue";
fetch("http://localhost:8000/restart");
const message = ref("");
const loadingMessage = ref(false);
async function sendMessage() {
  loadingMessage.value = true;
  const messageText = message.value.toLowerCase();
  messages.value.push({ message: messageText, fromUser: true });
  message.value = "";
  setTimeout(async () => {
    if (messageText) {
      if (messageText.includes("/restart")) {
        location.reload();
      } else if (messageText.includes("/train")) {
        messages.value.push({ message: "Modeļa apmācība uzsākta, lūdzu uzgaidiet", fromUser: false });
        let ans = await fetch("http://localhost:8000/train?c=" + messageText.replace("/train ", ""));
        let ansText = await ans.json();
        messages.value.push({ message: ansText, fromUser: false });
      } else if (messageText.includes("/course")) {
        let ans = await fetch("http://localhost:8000/course");
        let ansText = await ans.json();
        messages.value.push({ message: ansText, fromUser: false });
      } else {
        let ans = await fetch("http://localhost:8000/ask?q=" + messageText);
        let ansText = await ans.json();
        messages.value.push({ message: ansText, fromUser: false });
      }
      loadingMessage.value = false;
      // message.value = "";
    }
    setTimeout(() => {
      const container = document.getElementById("messageBox");
      container.scrollTop = container.scrollHeight;
    }, 100);
  }, 1000);

}
function checkIfEnter(event) {
  if (event.keyCode === 13) {
    event.preventDefault();
    sendMessage();
  }
}
</script>

<template>
  <header>
    <h1>ORTUSA</h1>
    <hr />
  </header>

  <main>
    <div id="messageBox">
      <Message v-for="message in messages" v-bind:message="message.message" v-bind:fromUser="message.fromUser" />
      <TypingIndicator v-if="loadingMessage" />

    </div>
    <div class="inputBox">
      <textarea type="text" v-model="message" v-on:keypress="checkIfEnter"></textarea>
      <button v-on:click="sendMessage()">Send</button>
    </div>
  </main>
</template>

<style>
@import "./assets/base.css";

#messageBox {
  display: flex;
  flex-direction: column;
  height: 100%;
  padding-top: 10px;
  padding-bottom: 10px;
  overflow-y: scroll;
}

body,
html,
#app {
  width: 100%;
  height: 100%;
  position: relative;
}

.inputBox {
  display: flex;
}

.inputBox button {
  flex-grow: 2;
  margin-left: 10px;
  margin-right: 10px;
}

.inputBox textarea {
  flex-grow: 3;
  margin-left: 10px;
  box-sizing: border-box;
  padding-top: 5px;
  padding-left: 5px;
}

main {
  height: 100%;
  max-height: 90%;
  padding-bottom: 10px;
}

header {
  margin: 0 auto;
  max-height: 10%;
}

h1 {
  text-align: center;
}
</style>
