<template>
  <PageContainer max-width="md">
    <div class="about">
      <div class="about__eyebrow">Про нас</div>
      <h1 class="about__title">
        <span class="logo-green">check</span><span class="logo-red">IT</span> —
        <span class="about__title-sub">сервіс порівняння тендерних цін</span>
      </h1>
      <p class="about__intro">
        Наша платформа спрощує аналіз тендерних пропозицій. Ми дозволяємо
        швидко знаходити й порівнювати ціни, умови та інші ключові параметри
        як державних, так і приватних тендерів — уся потрібна інформація
        зібрана в одному місці.
      </p>

      <section class="about__section">
        <h2>Можливості платформи</h2>
        <ul class="about__list">
          <li>
            <AppIcon name="check" :size="16" class="about__list-icon" />
            Аналіз державних тендерних пропозицій через Prozorro
          </li>
          <li>
            <AppIcon name="check" :size="16" class="about__list-icon" />
            Порівняння цін з реальними маркетплейсами (Rozetka, Сільпо, Епіцентр)
          </li>
          <li>
            <AppIcon name="check" :size="16" class="about__list-icon" />
            Оцінка корупційних ризиків та дискримінаційних вимог
          </li>
          <li>
            <AppIcon name="check" :size="16" class="about__list-icon" />
            Зручний інтерфейс і швидкий доступ до актуальних даних
          </li>
        </ul>
      </section>

      <section class="about__section about__contacts">
        <h2>Контакти</h2>
        <div class="about__contact-row">
          <a href="tel:+380677557973" class="about__contact">
            <AppIcon name="info" :size="14" /> +380 67 755 7973
          </a>
          <a href="tel:+380960971750" class="about__contact">
            <AppIcon name="info" :size="14" /> +380 96 097 1750
          </a>
        </div>
      </section>
    </div>
  </PageContainer>
</template>

<script>
import PageContainer from '@/components/PageContainer.vue'
import AppIcon from '@/components/AppIcon.vue'

export default {
  name: 'AboutView',
  components: { PageContainer, AppIcon },
}
</script>

<style scoped>
.about {
  max-width: 720px;
  margin: 0 auto;
}

.about__eyebrow {
  font-size: var(--text-xs);
  text-transform: uppercase;
  letter-spacing: var(--tracking-wider);
  color: var(--color-text-secondary);
  margin-bottom: var(--space-3);
}

.about__title {
  font-size: clamp(1.75rem, 4vw, 2.5rem);
  font-weight: var(--font-semibold);
  letter-spacing: var(--tracking-display);
  line-height: 1.15;
  margin-bottom: var(--space-6);
}

.about__title-sub {
  color: var(--color-text-secondary);
  font-weight: var(--font-normal);
}

.logo-green { color: var(--color-primary); }
.logo-red { color: var(--color-danger); }

.about__intro {
  font-size: var(--text-lg);
  line-height: 1.7;
  color: var(--color-text);
}

.about__section {
  margin-top: var(--space-10);
}

.about__section h2 {
  font-size: var(--text-xl);
  font-weight: var(--font-semibold);
  margin-bottom: var(--space-4);
}

.about__list {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
  padding: 0;
  list-style: none;
}

.about__list li {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-3) var(--space-4);
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  font-size: var(--text-base);
  color: var(--color-text);
}

.about__list-icon { color: var(--color-primary); flex-shrink: 0; }

.about__contacts {
  padding: var(--space-6);
  background: var(--color-bg-subtle);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
}

.about__contact-row {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-4);
}

.about__contact {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: var(--text-base);
  font-weight: var(--font-medium);
  color: var(--color-primary);
  text-decoration: none;
  font-variant-numeric: tabular-nums;
}

.about__contact:hover { text-decoration: underline; }
</style>
