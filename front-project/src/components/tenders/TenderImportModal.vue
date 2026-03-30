<template>
  <div class="import-modal-overlay" @click.self="$emit('close')">
    <div class="import-modal">
      <div class="modal-header">
        <h3>Імпорт з Prozorro</h3>
        <button class="modal-close" @click="$emit('close')">&times;</button>
      </div>

      <div class="modal-body">
        <p class="modal-hint">Введіть ID тендера з Prozorro для автоматичного імпорту</p>

        <input
          class="app-input"
          v-model.trim="prozorroId"
          placeholder="UA-2024-01-01-000001-a або hex ID"
          @keydown.enter="handleImport"
        />

        <div v-if="error" class="modal-error">{{ error }}</div>
      </div>

      <div class="modal-footer">
        <AppButton variant="ghost" @click="$emit('close')">Скасувати</AppButton>
        <AppButton :disabled="!prozorroId || loading" @click="handleImport">
          {{ loading ? 'Імпортуємо...' : 'Імпортувати' }}
        </AppButton>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import AppButton from '@/components/AppButton.vue'
import { useTendersStore } from '@/stores/tenders'

export default {
  name: 'TenderImportModal',
  components: { AppButton },
  emits: ['close', 'imported'],
  setup(_, { emit }) {
    const store = useTendersStore()
    const prozorroId = ref('')
    const loading = ref(false)
    const error = ref(null)

    const handleImport = async () => {
      if (!prozorroId.value) return
      loading.value = true
      error.value = null
      try {
        const tender = await store.importFromProzorro(prozorroId.value)
        emit('imported', tender)
        emit('close')
      } catch (err) {
        error.value = err.response?.data?.detail || err.message || 'Помилка імпорту'
      } finally {
        loading.value = false
      }
    }

    return { prozorroId, loading, error, handleImport }
  },
}
</script>

<style scoped>
.import-modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 900;
}

.import-modal {
  background: var(--color-surface);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-xl);
  width: 100%;
  max-width: 500px;
  margin: var(--space-4);
}

.modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: var(--space-4) var(--space-5);
  border-bottom: 1px solid var(--color-border);
}

.modal-header h3 {
  font-size: var(--text-lg);
  font-weight: var(--font-bold);
  color: var(--color-heading);
  margin: 0;
}

.modal-close {
  background: none;
  border: none;
  font-size: var(--text-2xl);
  color: var(--color-text-secondary);
  cursor: pointer;
  padding: 0;
  line-height: 1;
}

.modal-close:hover {
  color: var(--color-text);
}

.modal-body {
  padding: var(--space-5);
}

.modal-hint {
  font-size: var(--text-sm);
  color: var(--color-text-secondary);
  margin-bottom: var(--space-3);
}

.modal-error {
  margin-top: var(--space-3);
  padding: var(--space-2) var(--space-3);
  background: var(--color-danger-light);
  color: var(--color-danger);
  border-radius: var(--radius-md);
  font-size: var(--text-sm);
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: var(--space-2);
  padding: var(--space-3) var(--space-5);
  border-top: 1px solid var(--color-border);
}
</style>
