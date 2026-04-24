<template>
  <teleport to="body">
    <transition name="modal">
      <div v-if="modelValue" class="app-modal" role="dialog" aria-modal="true">
        <div class="app-modal__backdrop" @click="close"></div>
        <div class="app-modal__panel" :style="{ maxWidth }">
          <header v-if="title || $slots.header" class="app-modal__header">
            <slot name="header">
              <h3 class="app-modal__title">{{ title }}</h3>
            </slot>
            <button class="app-modal__close" aria-label="Закрити" @click="close">
              <AppIcon name="x" :size="16" />
            </button>
          </header>
          <div class="app-modal__body">
            <slot />
          </div>
          <footer v-if="$slots.footer" class="app-modal__footer">
            <slot name="footer" />
          </footer>
        </div>
      </div>
    </transition>
  </teleport>
</template>

<script>
import { onBeforeUnmount, watch } from 'vue'
import AppIcon from '@/components/AppIcon.vue'

export default {
  name: 'AppModal',
  components: { AppIcon },
  props: {
    modelValue: { type: Boolean, default: false },
    title: { type: String, default: '' },
    maxWidth: { type: String, default: '520px' },
  },
  emits: ['update:modelValue'],
  setup(props, { emit }) {
    const close = () => emit('update:modelValue', false)

    const onKey = (e) => {
      if (e.key === 'Escape' && props.modelValue) close()
    }

    watch(
      () => props.modelValue,
      (open) => {
        if (open) document.addEventListener('keydown', onKey)
        else document.removeEventListener('keydown', onKey)
      },
      { immediate: true },
    )

    onBeforeUnmount(() => document.removeEventListener('keydown', onKey))

    return { close }
  },
}
</script>

<style scoped>
.app-modal {
  position: fixed;
  inset: 0;
  z-index: 800;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: var(--space-4);
}

.app-modal__backdrop {
  position: absolute;
  inset: 0;
  background: rgba(15, 23, 42, 0.55);
  backdrop-filter: blur(4px);
}

.app-modal__panel {
  position: relative;
  width: 100%;
  max-width: 520px;
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-xl);
  box-shadow: var(--shadow-xl);
  display: flex;
  flex-direction: column;
  max-height: calc(100vh - var(--space-8));
  overflow: hidden;
}

.app-modal__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: var(--space-4) var(--space-5);
  border-bottom: 1px solid var(--color-border);
}

.app-modal__title {
  font-size: var(--text-lg);
  font-weight: var(--font-semibold);
  margin: 0;
}

.app-modal__close {
  width: 32px;
  height: 32px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border-radius: var(--radius-md);
  color: var(--color-text-secondary);
  background: transparent;
  border: none;
  transition: background var(--transition-fast);
}

.app-modal__close:hover {
  background: var(--color-bg-subtle);
  color: var(--color-text);
}

.app-modal__body {
  padding: var(--space-5);
  overflow-y: auto;
}

.app-modal__footer {
  padding: var(--space-4) var(--space-5);
  border-top: 1px solid var(--color-border);
  background: var(--color-bg-subtle);
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: var(--space-2);
}

.modal-enter-active, .modal-leave-active {
  transition: opacity 180ms ease;
}
.modal-enter-active .app-modal__panel,
.modal-leave-active .app-modal__panel {
  transition: transform 180ms ease, opacity 180ms ease;
}
.modal-enter-from, .modal-leave-to { opacity: 0; }
.modal-enter-from .app-modal__panel,
.modal-leave-to .app-modal__panel {
  transform: translateY(8px);
  opacity: 0;
}
</style>
