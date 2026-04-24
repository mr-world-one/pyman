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
  border: 1px solid var(--color-border);
  border-radius: var(--radius-xl);
  box-shadow: var(--shadow-soft);
  padding: var(--space-8);
  width: 100%;
}
</style>
