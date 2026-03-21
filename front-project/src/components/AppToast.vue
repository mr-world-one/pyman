<template>
  <teleport to="body">
    <div class="toast-container" v-if="toasts.length">
      <transition-group name="toast">
        <div
          v-for="toast in toasts"
          :key="toast.id"
          class="toast"
          :class="'toast--' + toast.type"
          @click="remove(toast.id)"
        >
          <span class="toast__icon">{{ icons[toast.type] }}</span>
          <span class="toast__message">{{ toast.message }}</span>
        </div>
      </transition-group>
    </div>
  </teleport>
</template>

<script>
import { useToast } from '@/composables/useToast'

export default {
  name: 'AppToast',
  setup() {
    const { toasts, remove } = useToast()
    const icons = {
      success: '\u2713',
      error: '\u2717',
      warning: '\u26A0',
      info: '\u2139',
    }
    return { toasts, remove, icons }
  },
}
</script>

<style scoped>
.toast-container {
  position: fixed;
  top: var(--space-4);
  right: var(--space-4);
  z-index: 9000;
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
  max-width: 380px;
  width: 100%;
}

.toast {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-3) var(--space-4);
  border-radius: var(--radius-md);
  font-size: var(--text-sm);
  font-weight: var(--font-medium);
  cursor: pointer;
  box-shadow: var(--shadow-lg);
  animation: slide-in 0.3s ease;
}

.toast--success {
  background: var(--color-green-100);
  color: var(--color-success);
  border: 1px solid var(--color-green-200);
}

.toast--error {
  background: var(--color-red-100);
  color: var(--color-danger);
  border: 1px solid var(--color-danger-border);
}

.toast--warning {
  background: var(--color-warning-bg);
  color: var(--color-warning);
  border: 1px solid var(--color-warning-border);
}

.toast--info {
  background: var(--color-info-bg);
  color: var(--color-info);
  border: 1px solid var(--color-info-border);
}

.toast__icon {
  font-size: var(--text-lg);
  flex-shrink: 0;
}

.toast__message {
  flex: 1;
  line-height: 1.4;
}

.toast-enter-active,
.toast-leave-active {
  transition: all 0.3s ease;
}

.toast-enter-from {
  opacity: 0;
  transform: translateX(60px);
}

.toast-leave-to {
  opacity: 0;
  transform: translateX(60px);
}

@keyframes slide-in {
  from {
    opacity: 0;
    transform: translateX(60px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}
</style>
