<script setup>
import { onMounted, ref, watch } from 'vue';
import messages from './messages';

const props = defineProps(["message", "fromUser"]);

const currentAnimation = ref("/src/assets/Ortusa_Idle2.gif");
onMounted(() => {
    if (!props.fromUser && props.message.toLowerCase().includes("atvainojos,")) {
        currentAnimation.value = "/src/assets/Ortusa_Sad.gif";
    } else {
        currentAnimation.value = "/src/assets/Ortusa_Happy.gif";

    }
})
watch(messages.value, () => {
    currentAnimation.value = "/src/assets/Ortusa_Idle2.gif";
})
</script>
<template>
    <div class="message-wrapper" v-bind:class="fromUser ? 'user' : ''">
        <div class="ortusa" v-if="!fromUser"><img :src="currentAnimation" /></div>
        <div class="message-content">
            <div v-for="text of message.split('\n')" class="message">{{ text }}
            </div>
        </div>
    </div>
</template>

<style scoped>
.message-wrapper {
    display: flex;
    width: 100%;
}

.message-wrapper.user {
    justify-content: flex-end;
    margin-right: 10px;
}

.message-wrapper.user .message-content {
    margin-right: 10px;
}

.ortusa {
    margin-left: 5px;
    width: 35px;
    height: 35px;
    border-radius: 50%;
    overflow: hidden;
}

.ortusa img {
    width: 150%;
    height: 150%;
    object-fit: contain;
    left: -9px;
}

.message-content {
    max-width: 80%;

}

.message {
    float: left;
    clear: both;
    margin-left: 10px;
    margin-bottom: 5px;
    border-radius: 5px;
    background-color: #f0f0f0;
    word-wrap: break-word;
    padding: 4px 8px;
    align-self: flex-start;
}
</style>