<template>
  <div class="form-group">
    <label v-if="label" :for="htmlFor" class="form-group__label">
      {{ label }}
      <span v-if="required" class="form-group__required">*</span>
    </label>
    <slot />
    <p v-if="error" class="form-group__error">{{ error }}</p>
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
  },
}
</script>

<style scoped>
.form-group {
  margin-bottom: var(--space-5);
}

.form-group__label {
  display: block;
  font-weight: var(--font-semibold);
  color: var(--color-text);
  margin-bottom: var(--space-1);
  font-size: var(--text-sm);
}

.form-group__required {
  color: var(--color-danger);
  margin-left: 2px;
}

.form-group__error {
  color: var(--color-danger);
  font-size: var(--text-xs);
  margin-top: var(--space-1);
}
</style>
