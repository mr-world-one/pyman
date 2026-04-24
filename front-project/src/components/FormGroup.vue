<template>
  <div class="form-group">
    <label v-if="label" :for="htmlFor" class="form-group__label">
      {{ label }}
      <span v-if="required" class="form-group__required">*</span>
    </label>
    <slot />
    <p v-if="error" class="form-group__error">{{ error }}</p>
    <p v-else-if="hint" class="form-group__hint">{{ hint }}</p>
  </div>
</template>

<script>
export default {
  name: 'FormGroup',
  props: {
    label: { type: String, default: '' },
    htmlFor: { type: String, default: '' },
    required: { type: Boolean, default: false },
    error: { type: String, default: '' },
    hint: { type: String, default: '' },
  },
}
</script>

<style scoped>
.form-group {
  margin-bottom: var(--space-4);
}

.form-group__label {
  display: block;
  font-size: var(--text-xs);
  font-weight: var(--font-medium);
  color: var(--color-text);
  margin-bottom: 6px;
}

.form-group__required {
  color: var(--color-danger);
  margin-left: 2px;
}

.form-group__error {
  color: var(--color-danger);
  font-size: var(--text-xs);
  margin-top: 6px;
}

.form-group__hint {
  color: var(--color-text-secondary);
  font-size: var(--text-xs);
  margin-top: 6px;
}
</style>
