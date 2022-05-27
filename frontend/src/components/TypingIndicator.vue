<script setup>
</script>
<template>
    <div class="message-wrapper">
        <div class="ortusa"><img src="/src/assets/Ortusa_Idle2.gif" /></div>
        <div class=" message-content">
            <div class="message lds-ellipsis">
                <div></div>
                <div></div>
                <div></div>
                <div></div>
            </div>
        </div>
    </div>

</template>
<style scoped>
.message-wrapper {
    display: flex;
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

.message {
    float: left;
    clear: both;
    margin-left: 10px;
    margin-bottom: 5px;
    border-radius: 5px;
    background-color: #f0f0f0;
    word-wrap: break-word;
    padding: 4px 8px;
    max-width: 80%;
    align-self: flex-start;
}

/* writing animation https://loading.io/css/ */

.lds-ellipsis {
    display: inline-block;
    position: relative;
    width: 80px;
    height: 40px;
}

.lds-ellipsis div {
    position: absolute;
    top: 13px;
    width: 13px;
    height: 13px;
    border-radius: 50%;
    background: #005551;
    animation-timing-function: cubic-bezier(0, 1, 1, 0);
}

.lds-ellipsis div:nth-child(1) {
    left: 8px;
    animation: lds-ellipsis1 0.6s infinite;
}

.lds-ellipsis div:nth-child(2) {
    left: 8px;
    animation: lds-ellipsis2 0.6s infinite;
}

.lds-ellipsis div:nth-child(3) {
    left: 32px;
    animation: lds-ellipsis2 0.6s infinite;
}

.lds-ellipsis div:nth-child(4) {
    left: 56px;
    animation: lds-ellipsis3 0.6s infinite;
}

@keyframes lds-ellipsis1 {
    0% {
        transform: scale(0);
    }

    100% {
        transform: scale(1);
    }
}

@keyframes lds-ellipsis3 {
    0% {
        transform: scale(1);
    }

    100% {
        transform: scale(0);
    }
}

@keyframes lds-ellipsis2 {
    0% {
        transform: translate(0, 0);
    }

    100% {
        transform: translate(24px, 0);
    }
}
</style>