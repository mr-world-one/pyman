<template>
  <div v-if="overlay" class="loader-overlay">
    <div class="loader-content">
      <div class="swing" aria-busy="true" aria-label="Loading" role="progressbar">
        <div class="swing-l"></div>
        <div></div>
        <div></div>
        <div></div>
        <div></div>
        <div></div>
        <div class="swing-r"></div>
      </div>
      <div class="shadow">
        <div class="shadow-l"></div>
        <div></div>
        <div></div>
        <div></div>
        <div></div>
        <div></div>
        <div class="shadow-r"></div>
      </div>
      <p v-if="text" class="loader-text">{{ text }}</p>
    </div>
  </div>
  <div v-else class="loader-inline">
    <div class="swing" aria-busy="true" aria-label="Loading" role="progressbar">
      <div class="swing-l"></div>
      <div></div>
      <div></div>
      <div></div>
      <div></div>
      <div></div>
      <div class="swing-r"></div>
    </div>
    <div class="shadow">
      <div class="shadow-l"></div>
      <div></div>
      <div></div>
      <div></div>
      <div></div>
      <div></div>
      <div class="shadow-r"></div>
    </div>
    <p v-if="text" class="loader-text loader-text--dark">{{ text }}</p>
  </div>
</template>

<script>
export default {
  name: 'AppLoader',
  props: {
    overlay: { type: Boolean, default: true },
    text: { type: String, default: 'Виконується аналіз, це може трішки тривати...' },
  },
}
</script>

<style scoped>
.loader-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 5000;
}

.loader-content {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.loader-inline {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: var(--space-8) 0;
}

.swing div {
  border-radius: 50%;
  float: left;
  height: 1.5em;
  width: 1.5em;
  margin: 0 0.3em;
}

.swing div:nth-of-type(1) { background: linear-gradient(to right, #1aad3f, #22c54e); }
.swing div:nth-of-type(2) { background: linear-gradient(to right, #22c54e, #4ade80); }
.swing div:nth-of-type(3) { background: linear-gradient(to right, #4ade80, #86efac); }
.swing div:nth-of-type(4) { background: linear-gradient(to right, #86efac, #bfcf9c); }
.swing div:nth-of-type(5) { background: linear-gradient(to right, #bfcf9c, #e8c5be); }
.swing div:nth-of-type(6) { background: linear-gradient(to right, #e8c5be, #f87171); }
.swing div:nth-of-type(7) { background: linear-gradient(to right, #f87171, #c41a12); }

.shadow {
  clear: left;
  padding-top: 1.5em;
  text-align: center;
}

.shadow div {
  filter: blur(1px);
  float: left;
  width: 1.5em;
  height: 0.25em;
  border-radius: 50%;
  background: var(--color-gray-300);
  margin: 0 0.3em;
}

.shadow .shadow-l { background: var(--color-gray-200); }
.shadow .shadow-r { background: var(--color-gray-400); }

.swing-l { animation: ball-l 0.425s ease-in-out infinite alternate; }
.swing-r { animation: ball-r 0.425s ease-in-out infinite alternate; }
.shadow-l { animation: shadow-l-n 0.425s ease-in-out infinite alternate; }
.shadow-r { animation: shadow-r-n 0.425s ease-in-out infinite alternate; }

@keyframes ball-l {
  0%, 50% { transform: rotate(0) translateX(0); }
  100% { transform: rotate(50deg) translateX(-2.5em); }
}

@keyframes ball-r {
  0% { transform: rotate(-50deg) translateX(2.5em); }
  50%, 100% { transform: rotate(0) translateX(0); }
}

@keyframes shadow-l-n {
  0%, 50% { opacity: 0.5; transform: translateX(0); }
  100% { opacity: 0.125; transform: translateX(-1.75em); }
}

@keyframes shadow-r-n {
  0% { opacity: 0.125; transform: translateX(1.75em); }
  50%, 100% { opacity: 0.5; transform: translateX(0); }
}

.loader-text {
  color: var(--color-white);
  font-size: var(--text-lg);
  margin-top: var(--space-8);
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
  text-align: center;
}

.loader-text--dark {
  color: var(--color-text-secondary);
  text-shadow: none;
}
</style>
