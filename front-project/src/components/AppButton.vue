<template>
  <button
    :class="['app-btn', 'app-btn--' + variant, 'app-btn--' + size]"
    :disabled="disabled || loading"
    v-bind="$attrs"
  >
    <span v-if="loading" class="app-btn__spinner"></span>
    <slot />
  </button>
</template>

<script>
export default {
  name: 'AppButton',
  inheritAttrs: false,
  props: {
    variant: {
      type: String,
      default: 'primary',
      validator: (v) => ['primary', 'secondary', 'danger', 'ghost'].includes(v),
    },
    size: {
      type: String,
      default: 'md',
      validator: (v) => ['sm', 'md', 'lg'].includes(v),
    },
    loading: { type: Boolean, default: false },
    disabled: { type: Boolean, default: false },
  },
}
</script>

<style scoped>
.app-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: var(--space-2);
  border: none;
  border-radius: var(--radius-md);
  font-family: var(--font-body);
  font-weight: var(--font-semibold);
  cursor: pointer;
  transition: background var(--transition-fast), transform var(--transition-fast), box-shadow var(--transition-fast);
  white-space: nowrap;
}

.app-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none !important;
}

/* Sizes */
.app-btn--sm {
  padding: var(--space-1) var(--space-3);
  font-size: var(--text-sm);
}

.app-btn--md {
  padding: var(--space-2) var(--space-5);
  font-size: var(--text-base);
}

.app-btn--lg {
  padding: var(--space-3) var(--space-8);
  font-size: var(--text-lg);
}

/* Variants */
.app-btn--primary {
  background: linear-gradient(135deg, var(--color-green-500), var(--color-green-600));
  color: var(--color-white);
}

.app-btn--primary:hover:not(:disabled) {
  background: linear-gradient(135deg, var(--color-green-600), var(--color-green-700));
  transform: translateY(-1px);
  box-shadow: var(--shadow-md);
}

.app-btn--secondary {
  background: var(--color-white);
  color: var(--color-text);
  border: 1px solid var(--color-border);
}

.app-btn--secondary:hover:not(:disabled) {
  background: var(--color-gray-50);
  border-color: var(--color-border-hover);
}

.app-btn--danger {
  background: var(--color-danger);
  color: var(--color-white);
}

.app-btn--danger:hover:not(:disabled) {
  background: var(--color-red-600);
  transform: translateY(-1px);
}

.app-btn--ghost {
  background: transparent;
  color: var(--color-text-secondary);
}

.app-btn--ghost:hover:not(:disabled) {
  background: var(--color-gray-100);
  color: var(--color-text);
}

/* Spinner */
.app-btn__spinner {
  width: 1em;
  height: 1em;
  border: 2px solid currentColor;
  border-right-color: transparent;
  border-radius: 50%;
  animation: btn-spin 0.6s linear infinite;
}

@keyframes btn-spin {
  to { transform: rotate(360deg); }
}
</style>
