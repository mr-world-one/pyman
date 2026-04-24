<template>
  <AppBadge :variant="variant">{{ label }}</AppBadge>
</template>

<script>
import AppBadge from '@/components/AppBadge.vue'

const TYPE_LABELS = {
  product: 'Товари',
  service: 'Послуги',
  work: 'Роботи',
  consulting: 'Консалтинг',
  mixed: 'Змішаний',
}

const TYPE_VARIANTS = {
  product: 'brand',
  service: 'info',
  work: 'warn',
  consulting: 'slate',
  mixed: 'danger',
}

export default {
  name: 'TenderTypeBadge',
  components: { AppBadge },
  props: {
    type: { type: String, required: true },
  },
  computed: {
    label() { return TYPE_LABELS[this.type] || this.type },
    variant() { return TYPE_VARIANTS[this.type] || 'slate' },
  },
}
</script>
