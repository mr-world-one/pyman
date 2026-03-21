<template>
  <div class="card-panel">
    <slot />
  </div>
</template>

<script>
export default {
  name: 'CardPanel',
}
</script>

<style scoped>
.card-panel {
  background: var(--color-surface);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-md);
  padding: var(--space-8);
  width: 100%;
}
</style>
