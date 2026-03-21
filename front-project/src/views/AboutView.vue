<template>

<PageContainer max-width="md">
    <CardPanel>
      <h2 class="about__title">Про нас</h2>
      <p class="about__intro">
        Ласкаво просимо на <span class="brand-green">check</span><span class="brand-red">IT</span> — сервіс, який допомагає порівнювати ціни та умови тендерів для бізнесу та державних закупівель.
      </p>
      <div class="about__content">
        <p>
          Наша платформа створена для спрощення аналізу тендерних пропозицій. Ми надаємо можливість швидко знаходити та порівнювати ціни, умови та інші ключові параметри як державних, так і приватних тендерів. Забудьте про нескінченне блукання між різними сайтами — вся необхідна інформація зібрана в одному місці!
        </p>
        <h3>Наші можливості:</h3>
        <ul>
          <li>Аналіз державних тендерних пропозицій та закупівельних угод через Prozorro</li>
          <li>Порівняння умов приватних тендерів для бізнесу</li>
          <li>Зручний інтерфейс для швидкого доступу до актуальної інформації</li>
        </ul>
      </div>
      <div class="about__contacts">
        <h3>Контакти:</h3>
        <p><a href="tel:+380677557973">+380 67 755 7973</a></p>
        <p><a href="tel:+380960971750">+380 96 097 1750</a></p>
      </div>
    </CardPanel>
  </PageContainer>
</template>

<script>
import PageContainer from '@/components/PageContainer.vue'
import CardPanel from '@/components/CardPanel.vue'

export default {
  name: 'AboutView',
  components: { PageContainer, CardPanel },
}
</script>

<style scoped>
.about__title {
  font-size: var(--text-3xl);
  text-align: center;
  margin-bottom: var(--space-6);
}

.about__intro {
  font-size: var(--text-lg);
  color: var(--color-text-secondary);
  text-align: center;
  margin-bottom: var(--space-6);
  font-weight: var(--font-semibold);
}

.brand-green {
  color: var(--color-green-600);
  font-weight: var(--font-bold);
}

.brand-red {
  color: var(--color-red-600);
  font-weight: var(--font-bold);
}

.about__content p {
  font-size: var(--text-base);
  color: var(--color-text);
  margin-bottom: var(--space-4);
  line-height: 1.7;
}

.about__content h3 {
  font-size: var(--text-xl);
  color: var(--color-red-600);
  margin: var(--space-6) 0 var(--space-4);
}

.about__content ul {
  list-style: disc;
  padding-left: var(--space-8);
  max-width: 700px;
  margin: 0 auto;
}

.about__content li {
  font-size: var(--text-base);
  color: var(--color-text);
  margin-bottom: var(--space-2);
  font-weight: var(--font-semibold);
  line-height: 1.6;
}

.about__contacts {
  margin-top: var(--space-10);
  padding: var(--space-6);
  background: var(--color-gray-50);
  border-radius: var(--radius-md);
  text-align: center;
}

.about__contacts h3 {
  font-size: var(--text-xl);
  margin-bottom: var(--space-3);
}

.about__contacts p {
  font-size: var(--text-base);
  margin-bottom: var(--space-2);
}

.about__contacts a {
  color: var(--color-primary);
  font-weight: var(--font-bold);
}

.about__contacts a:hover {
  text-decoration: underline;
}
</style>
