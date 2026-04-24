<template>
  <teleport to="body">
    <div class="toast-container" v-if="toasts.length">
      <transition-group name="toast">
        <div
          v-for="toast in toasts"
          :key="toast.id"
          :class="['toast', `toast--${toast.type}`]"
          @click="remove(toast.id)"
        >
          <AppIcon :name="iconFor(toast.type)" :size="16" class="toast__icon" />
          <span class="toast__message">{{ toast.message }}</span>
        </div>
      </transition-group>
    </div>
  </teleport>
</template>

<script>
import { useToast } from '@/composables/useToast'
import AppIcon from '@/components/AppIcon.vue'

export default {
  name: 'AppToast',
  components: { AppIcon },
  setup() {
    const { toasts, remove } = useToast()
    const iconFor = (type) => ({
      success: 'check-circle',
      error: 'alert',
      warning: 'alert',
      info: 'info',
    })[type] || 'info'
    return { toasts, remove, iconFor }
  },
}
</script>

<style scoped>
.toast-container {
  position: fixed;
  top: calc(var(--header-height) + var(--space-3));
  right: var(--space-4);
  z-index: 900;
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
  max-width: 380px;
  width: calc(100% - var(--space-8));
}

.toast {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-3) var(--space-4);
  border-radius: var(--radius-md);
  font-size: var(--text-base);
  font-weight: var(--font-medium);
  cursor: pointer;
  box-shadow: var(--shadow-pop);
  border: 1px solid transparent;
  background: var(--color-surface);
}

.toast--success {
  background: var(--color-green-50);
  color: var(--color-green-700);
  border-color: var(--color-green-200);
}

.toast--error {
  background: var(--color-red-50);
  color: var(--color-red-700);
  border-color: var(--color-danger-border);
}

.toast--warning {
  background: var(--color-warning-bg);
  color: var(--color-warning);
  border-color: var(--color-warning-border);
}

.toast--info {
  background: var(--color-info-bg);
  color: var(--color-info);
  border-color: var(--color-info-border);
}

.toast__icon { flex-shrink: 0; }
.toast__message { flex: 1; line-height: 1.4; }

.toast-enter-active, .toast-leave-active {
  transition: all 0.25s ease;
}
.toast-enter-from, .toast-leave-to {
  opacity: 0;
  transform: translateX(60px);
}
</style>
