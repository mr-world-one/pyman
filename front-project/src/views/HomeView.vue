<template>
  <div class="home">
    <!-- Hero Section -->
    <section class="hero">
      <div class="hero__content">
        <h1 class="hero__title">
          Порівнюйте тендерні ціни<br />з реальними цінами магазинів
        </h1>
        <p class="hero__subtitle">
          Приватні чи державні — немає значення. checkIT аналізує закупівлі Prozorro та порівнює з актуальними цінами в магазинах.
        </p>
        <div class="hero__actions">
          <router-link to="/register" class="hero__btn hero__btn--primary">Розпочати</router-link>
          <router-link to="/about" class="hero__btn hero__btn--secondary">Дізнатися більше</router-link>
        </div>
      </div>
    </section>

    <!-- Features Section -->
    <section class="features">
      <h2 class="section-title">Можливості платформи</h2>
      <div class="features__grid">
        <div class="feature-card">
          <div class="feature-card__icon">&#x1F50D;</div>
          <h3 class="feature-card__title">Prozorro аналіз</h3>
          <p class="feature-card__text">
            Автоматичний пошук та порівняння цін з державних тендерів Prozorro з реальними ринковими цінами.
          </p>
        </div>
        <div class="feature-card">
          <div class="feature-card__icon">&#x1F4CA;</div>
          <h3 class="feature-card__title">Excel перевірка</h3>
          <p class="feature-card__text">
            Завантажте Excel-файл з тендерними даними та отримайте миттєве порівняння з цінами магазинів.
          </p>
        </div>
        <div class="feature-card">
          <div class="feature-card__icon">&#x1F6D2;</div>
          <h3 class="feature-card__title">Декілька магазинів</h3>
          <p class="feature-card__text">
            Порівнюйте ціни з Rozetka, Сільпо, Епіцентр та інших магазинів одночасно.
          </p>
        </div>
      </div>
    </section>

    <!-- How It Works Section -->
    <section class="how-it-works">
      <h2 class="section-title">Як це працює</h2>
      <div class="steps">
        <div class="step">
          <div class="step__number">1</div>
          <h3 class="step__title">Введіть дані</h3>
          <p class="step__text">Вкажіть ID тендеру Prozorro або завантажте Excel-файл</p>
        </div>
        <div class="step__arrow">&#x2192;</div>
        <div class="step">
          <div class="step__number">2</div>
          <h3 class="step__title">Оберіть магазини</h3>
          <p class="step__text">Виберіть магазини для порівняння цін</p>
        </div>
        <div class="step__arrow">&#x2192;</div>
        <div class="step">
          <div class="step__number">3</div>
          <h3 class="step__title">Отримайте результат</h3>
          <p class="step__text">Перегляньте детальне порівняння цін та аналітику</p>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
export default {
  name: 'HomeView',
}
</script>

<style scoped>
.home {
  padding-top: var(--header-height);
}

/* ===== Hero ===== */
.hero {
  background: linear-gradient(135deg, var(--color-green-50), var(--color-surface));
  padding: var(--space-16) var(--space-4);
  text-align: center;
}

.hero__content {
  max-width: 700px;
  margin: 0 auto;
}

.hero__title {
  font-size: var(--text-4xl);
  font-weight: var(--font-bold);
  color: var(--color-heading);
  margin-bottom: var(--space-4);
  line-height: 1.2;
}

.hero__subtitle {
  font-size: var(--text-lg);
  color: var(--color-text-secondary);
  margin-bottom: var(--space-8);
  line-height: 1.7;
}

.hero__actions {
  display: flex;
  gap: var(--space-4);
  justify-content: center;
  flex-wrap: wrap;
}

.hero__btn {
  padding: var(--space-3) var(--space-8);
  border-radius: var(--radius-md);
  font-weight: var(--font-semibold);
  font-size: var(--text-base);
  text-decoration: none;
  transition: background var(--transition-fast), transform var(--transition-fast), box-shadow var(--transition-fast);
}

.hero__btn--primary {
  background: linear-gradient(135deg, var(--color-green-500), var(--color-green-600));
  color: var(--color-white);
}

.hero__btn--primary:hover {
  background: linear-gradient(135deg, var(--color-green-600), var(--color-green-700));
  transform: translateY(-1px);
  box-shadow: var(--shadow-md);
  color: var(--color-white);
}

.hero__btn--secondary {
  background: var(--color-surface);
  color: var(--color-text);
  border: 1px solid var(--color-border);
}

.hero__btn--secondary:hover {
  background: var(--color-gray-50);
  border-color: var(--color-border-hover);
}

/* ===== Section Title ===== */
.section-title {
  text-align: center;
  font-size: var(--text-2xl);
  margin-bottom: var(--space-10);
  color: var(--color-heading);
}

/* ===== Features ===== */
.features {
  padding: var(--space-16) var(--space-4);
  max-width: var(--container-max-width);
  margin: 0 auto;
}

.features__grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: var(--space-6);
}

.feature-card {
  background: var(--color-surface);
  border-radius: var(--radius-lg);
  padding: var(--space-8);
  text-align: center;
  box-shadow: var(--shadow-sm);
  transition: transform var(--transition-fast), box-shadow var(--transition-fast);
}

.feature-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-lg);
}

.feature-card__icon {
  font-size: 2.5rem;
  margin-bottom: var(--space-4);
}

.feature-card__title {
  font-size: var(--text-lg);
  margin-bottom: var(--space-3);
  color: var(--color-heading);
}

.feature-card__text {
  font-size: var(--text-sm);
  color: var(--color-text-secondary);
  line-height: 1.7;
}

/* ===== How It Works ===== */
.how-it-works {
  padding: var(--space-16) var(--space-4);
  background: var(--color-surface);
  max-width: var(--container-max-width);
  margin: 0 auto var(--space-8);
  border-radius: var(--radius-lg);
}

.steps {
  display: flex;
  align-items: flex-start;
  justify-content: center;
  gap: var(--space-4);
  flex-wrap: wrap;
}

.step {
  text-align: center;
  max-width: 240px;
  flex: 1;
  min-width: 200px;
}

.step__number {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--color-green-500), var(--color-green-600));
  color: var(--color-white);
  font-size: var(--text-xl);
  font-weight: var(--font-bold);
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto var(--space-4);
}

.step__title {
  font-size: var(--text-base);
  margin-bottom: var(--space-2);
  color: var(--color-heading);
}

.step__text {
  font-size: var(--text-sm);
  color: var(--color-text-secondary);
  line-height: 1.6;
}

.step__arrow {
  font-size: var(--text-2xl);
  color: var(--color-gray-300);
  align-self: center;
  margin-top: var(--space-4);
}

@media (max-width: 640px) {
  .hero__title {
    font-size: var(--text-2xl);
  }

  .step__arrow {
    display: none;
  }

  .steps {
    flex-direction: column;
    align-items: center;
  }
}
</style>
