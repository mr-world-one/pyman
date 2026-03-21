<template>
  <div
    class="page-container"
    :class="{
      'page-container--sm': maxWidth === 'sm',
      'page-container--md': maxWidth === 'md',
      'page-container--lg': maxWidth === 'lg',
      'page-container--full': maxWidth === 'full',
      'page-container--centered': centered,
    }"
  >
    <slot />
  </div>
</template>

<script>
export default {
  name: 'PageContainer',
  props: {
    maxWidth: {
      type: String,
      default: 'lg',
      validator: (v) => ['sm', 'md', 'lg', 'full'].includes(v),
    },
    centered: { type: Boolean, default: false },
  },
}
</script>

<style scoped>
.page-container {
  width: 100%;
  margin: 0 auto;
  padding: calc(var(--header-height) + var(--space-8)) var(--space-4) var(--space-8);
}

.page-container--sm { max-width: 500px; }
.page-container--md { max-width: 800px; }
.page-container--lg { max-width: var(--container-max-width); }
.page-container--full { max-width: 100%; }

.page-container--centered {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: calc(100vh - var(--header-height) - var(--footer-height));
}
</style>
