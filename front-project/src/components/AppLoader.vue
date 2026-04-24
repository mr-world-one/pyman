<template>
  <div v-if="overlay" class="loader-overlay" role="progressbar" aria-label="Завантаження">
    <div class="loader-content">
      <div class="spinner"></div>
      <p v-if="text" class="loader-text">{{ text }}</p>
    </div>
  </div>
  <div v-else class="loader-inline" role="progressbar" aria-label="Завантаження">
    <div class="spinner spinner--inline"></div>
    <p v-if="text" class="loader-text loader-text--inline">{{ text }}</p>
  </div>
</template>

<script>
export default {
  name: 'AppLoader',
  props: {
    overlay: { type: Boolean, default: true },
    text: { type: String, default: '' },
  },
}
</script>

<style scoped>
.loader-overlay {
  position: fixed;
  inset: 0;
  background: rgba(15, 23, 42, 0.55);
  backdrop-filter: blur(4px);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 700;
}

.loader-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--space-4);
  padding: var(--space-8);
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-xl);
  box-shadow: var(--shadow-xl);
  min-width: 220px;
}

.loader-inline {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: var(--space-3);
  padding: var(--space-10) 0;
}

.spinner {
  width: 32px;
  height: 32px;
  border: 2.5px solid var(--color-border);
  border-top-color: var(--color-primary);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

.spinner--inline {
  width: 24px;
  height: 24px;
  border-width: 2px;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.loader-text {
  color: var(--color-text);
  font-size: var(--text-base);
  text-align: center;
  max-width: 320px;
  line-height: 1.5;
}

.loader-text--inline {
  color: var(--color-text-secondary);
}
</style>
