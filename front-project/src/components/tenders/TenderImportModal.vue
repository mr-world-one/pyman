<template>
  <AppModal v-model="open" title="Імпорт з Prozorro" max-width="520px">
    <div class="import-body">
      <p class="import-hint">
        Введіть ID закупівлі — checkIT завантажить позиції, замовника
        та документи. Це займе 5–10 секунд.
      </p>

      <FormGroup label="ID закупівлі">
        <input
          class="app-input mono"
          v-model.trim="prozorroId"
          placeholder="UA-2024-01-01-000001-a"
          @keydown.enter="handleImport"
        />
      </FormGroup>

      <div class="alert alert-info import-callout">
        <AppIcon name="info" :size="14" class="import-callout__icon" />
        <span>Імпорт додає тендер до вашого списку. Аналіз запускається окремо.</span>
      </div>

      <div v-if="error" class="alert alert-error">{{ error }}</div>
    </div>

    <template #footer>
      <AppButton variant="secondary" @click="close">Скасувати</AppButton>
      <AppButton :disabled="!prozorroId || loading" :loading="loading" @click="handleImport">
        Імпортувати
      </AppButton>
    </template>
  </AppModal>
</template>

<script>
import { ref, watch } from 'vue'
import AppModal from '@/components/AppModal.vue'
import AppButton from '@/components/AppButton.vue'
import AppIcon from '@/components/AppIcon.vue'
import FormGroup from '@/components/FormGroup.vue'
import { useTendersStore } from '@/stores/tenders'

export default {
  name: 'TenderImportModal',
  components: { AppModal, AppButton, AppIcon, FormGroup },
  props: {
    modelValue: { type: Boolean, default: true },
  },
  emits: ['close', 'imported', 'update:modelValue'],
  setup(props, { emit }) {
    const store = useTendersStore()
    const open = ref(props.modelValue ?? true)
    const prozorroId = ref('')
    const loading = ref(false)
    const error = ref(null)

    watch(() => props.modelValue, (v) => { open.value = v })
    watch(open, (v) => {
      emit('update:modelValue', v)
      if (!v) emit('close')
    })

    const close = () => { open.value = false }

    const handleImport = async () => {
      if (!prozorroId.value || loading.value) return
      loading.value = true
      error.value = null
      try {
        const tender = await store.importFromProzorro(prozorroId.value)
        emit('imported', tender)
        close()
      } catch (err) {
        error.value = err.response?.data?.detail || err.message || 'Помилка імпорту'
      } finally {
        loading.value = false
      }
    }

    return { open, prozorroId, loading, error, handleImport, close }
  },
}
</script>

<style scoped>
.import-body {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
}

.import-hint {
  font-size: var(--text-base);
  color: var(--color-text-secondary);
  line-height: 1.55;
  margin: 0;
}

.import-callout {
  display: flex;
  align-items: flex-start;
  gap: var(--space-2);
  font-size: 12.5px;
  line-height: 1.5;
}

.import-callout__icon {
  flex-shrink: 0;
  margin-top: 2px;
}
</style>
