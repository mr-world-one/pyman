<template>
  <button
    :class="['app-btn', `app-btn--${variant}`, `app-btn--${size}`, { 'app-btn--icon': iconOnly }]"
    :disabled="disabled || loading"
    :type="type"
    v-bind="$attrs"
  >
    <span v-if="loading" class="app-btn__spinner" aria-hidden="true"></span>
    <slot v-else name="icon-left"></slot>
    <slot />
    <slot name="icon-right"></slot>
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
    type: { type: String, default: 'button' },
    loading: { type: Boolean, default: false },
    disabled: { type: Boolean, default: false },
    iconOnly: { type: Boolean, default: false },
  },
}
</script>

<style scoped>
.app-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: var(--space-2);
  border-radius: var(--radius-md);
  font-family: var(--font-body);
  font-weight: var(--font-medium);
  cursor: pointer;
  white-space: nowrap;
  border: 1px solid transparent;
  transition: background var(--transition-fast),
              border-color var(--transition-fast),
              color var(--transition-fast);
  line-height: 1;
}

.app-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Sizes */
.app-btn--sm {
  height: 28px;
  padding: 0 var(--space-3);
  font-size: var(--text-sm);
}

.app-btn--md {
  height: 36px;
  padding: 0 var(--space-4);
  font-size: var(--text-base);
}

.app-btn--lg {
  height: 44px;
  padding: 0 var(--space-5);
  font-size: var(--text-md);
}

.app-btn--icon {
  padding: 0;
  width: var(--btn-icon-size, 36px);
}

.app-btn--sm.app-btn--icon { width: 28px; }
.app-btn--lg.app-btn--icon { width: 44px; }

/* Variants */
.app-btn--primary {
  background: var(--color-primary);
  color: var(--color-white);
  border-color: var(--color-primary);
}

.app-btn--primary:hover:not(:disabled) {
  background: var(--color-primary-hover);
  border-color: var(--color-primary-hover);
}

[data-theme="dark"] .app-btn--primary {
  color: #052e1b;
}

.app-btn--secondary {
  background: var(--color-surface);
  color: var(--color-text);
  border-color: var(--color-border);
}

.app-btn--secondary:hover:not(:disabled) {
  background: var(--color-bg-subtle);
  border-color: var(--color-border-hover);
}

.app-btn--danger {
  background: var(--color-surface);
  color: var(--color-danger);
  border-color: var(--color-border);
}

.app-btn--danger:hover:not(:disabled) {
  background: var(--color-danger-light);
  border-color: var(--color-danger-border);
}

.app-btn--ghost {
  background: transparent;
  color: var(--color-text-secondary);
  border-color: transparent;
}

.app-btn--ghost:hover:not(:disabled) {
  background: var(--color-bg-subtle);
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
