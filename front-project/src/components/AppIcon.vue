<template>
  <svg
    :width="size"
    :height="size"
    :aria-hidden="decorative"
    :role="decorative ? undefined : 'img'"
    :aria-label="decorative ? undefined : name"
    class="app-icon"
  >
    <use :href="`#i-${name}`" />
  </svg>
</template>

<script>
export default {
  name: 'AppIcon',
  props: {
    name: { type: String, required: true },
    size: { type: [Number, String], default: 16 },
    decorative: { type: Boolean, default: true },
  },
}
</script>

<style scoped>
.app-icon {
  display: inline-block;
  flex-shrink: 0;
  vertical-align: middle;
  stroke: currentColor;
  fill: none;
}
</style>
