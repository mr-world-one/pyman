<template>
  <span :class="['app-badge', `app-badge--${variant}`, { 'app-badge--dot': showDot }]">
    <span v-if="showDot" class="app-badge__dot" aria-hidden="true"></span>
    <slot />
  </span>
</template>

<script>
export default {
  name: 'AppBadge',
  props: {
    variant: {
      type: String,
      default: 'slate',
      validator: (v) => ['brand', 'info', 'warn', 'danger', 'slate'].includes(v),
    },
    showDot: { type: Boolean, default: false },
  },
}
</script>

<style scoped>
.app-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 2px 8px;
  border-radius: var(--radius-full);
  font-size: 11px;
  font-weight: var(--font-medium);
  line-height: 1.4;
  white-space: nowrap;
}

.app-badge__dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: currentColor;
  flex-shrink: 0;
}

.app-badge--brand {
  background: var(--color-green-50);
  color: var(--color-green-700);
}
[data-theme="dark"] .app-badge--brand {
  background: rgba(16, 185, 129, 0.15);
  color: #6ee7b7;
}

.app-badge--info {
  background: var(--color-info-bg);
  color: var(--color-info);
}
[data-theme="dark"] .app-badge--info {
  background: rgba(37, 99, 235, 0.15);
  color: #93c5fd;
}

.app-badge--warn {
  background: var(--color-warning-bg);
  color: var(--color-warning);
}
[data-theme="dark"] .app-badge--warn {
  background: rgba(217, 119, 6, 0.15);
  color: #fbbf24;
}

.app-badge--danger {
  background: var(--color-red-50);
  color: var(--color-red-700);
}
[data-theme="dark"] .app-badge--danger {
  background: rgba(248, 113, 113, 0.15);
  color: #fca5a5;
}

.app-badge--slate {
  background: var(--color-slate-100);
  color: var(--color-slate-600);
}
[data-theme="dark"] .app-badge--slate {
  background: var(--color-slate-200);
  color: var(--color-slate-300);
}
</style>
