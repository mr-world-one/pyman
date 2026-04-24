<template>
  <div class="home">
    <!-- Hero -->
    <section class="hero">
      <div class="hero__bg" aria-hidden="true"></div>
      <div class="hero__content">
        <div class="hero__chip">
          <span class="hero__chip-dot"></span>
          Технологія чесності
        </div>
        <h1 class="hero__title">
          Порівнюйте тендерні ціни<br />
          з реальними цінами магазинів.
        </h1>
        <p class="hero__subtitle">
          checkIT аналізує закупівлі Prozorro та зіставляє позиції з ринковими
          цінами в Rozetka, Сільпо та Епіцентрі — щоб ви бачили завищення
          й ризики до того, як їх знайдуть інші.
        </p>
        <div class="hero__actions">
          <router-link to="/register" class="btn btn--primary">
            Розпочати
            <AppIcon name="arrow-right" :size="14" />
          </router-link>
          <router-link to="/about" class="btn btn--secondary">Дізнатися більше</router-link>
        </div>
        <div class="hero__checks">
          <div class="hero__check">
            <AppIcon name="check" :size="14" class="hero__check-icon" />
            Дані Prozorro в реальному часі
          </div>
          <div class="hero__check">
            <AppIcon name="check" :size="14" class="hero__check-icon" />
            Експорт у Excel
          </div>
          <div class="hero__check">
            <AppIcon name="check" :size="14" class="hero__check-icon" />
            API для аудиторів
          </div>
        </div>
      </div>

      <!-- preview frame -->
      <div class="preview">
        <div class="preview__chrome">
          <div class="preview__dots">
            <span></span><span></span><span></span>
          </div>
          <div class="preview__url mono">checkit.app/tenders/UA-2024-03-15-012345-a</div>
          <div class="preview__chrome-spacer"></div>
        </div>
        <div class="preview__body">
          <aside class="preview__sidebar">
            <div class="preview__nav preview__nav--active">
              <AppIcon name="table" :size="14" />Мої тендери
            </div>
            <div class="preview__nav"><AppIcon name="search" :size="14" />Prozorro пошук</div>
            <div class="preview__nav"><AppIcon name="file" :size="14" />Excel перевірка</div>
            <div class="preview__nav"><AppIcon name="shield" :size="14" />Аналіз ризиків</div>
          </aside>
          <div class="preview__content">
            <div class="preview__row">
              <div>
                <div class="preview__id mono">UA-2024-03-15-012345-a</div>
                <div class="preview__title">Закупівля канцелярського приладдя для ДП «Укрзалізниця»</div>
              </div>
              <AppBadge variant="brand">Активний</AppBadge>
            </div>
            <div class="preview__stats">
              <div class="preview__stat">
                <div class="preview__stat-label">Сума</div>
                <div class="preview__stat-value num">487 320 ₴</div>
              </div>
              <div class="preview__stat">
                <div class="preview__stat-label">Позицій</div>
                <div class="preview__stat-value num">42</div>
              </div>
              <div class="preview__stat">
                <div class="preview__stat-label">Завищення</div>
                <div class="preview__stat-value num up">+18.4%</div>
              </div>
              <div class="preview__stat">
                <div class="preview__stat-label">Ризик</div>
                <div class="preview__stat-value warn">Середній</div>
              </div>
            </div>
            <div class="preview__table">
              <table>
                <thead>
                  <tr>
                    <th>Товар</th>
                    <th class="num-col">Тендер</th>
                    <th class="num-col">Ринок</th>
                    <th class="num-col">Δ</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td>Папір А4 80 г/м², 500 арк.</td>
                    <td class="num num-col">189,00 ₴</td>
                    <td class="num num-col">152,40 ₴</td>
                    <td class="num num-col up">+24.0%</td>
                  </tr>
                  <tr>
                    <td>Ручка кулькова синя</td>
                    <td class="num num-col">12,50 ₴</td>
                    <td class="num num-col">14,20 ₴</td>
                    <td class="num num-col down">−12.0%</td>
                  </tr>
                  <tr>
                    <td>Папка-реєстратор А4</td>
                    <td class="num num-col">85,00 ₴</td>
                    <td class="num num-col">72,90 ₴</td>
                    <td class="num num-col up">+16.6%</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Features -->
    <section class="features-wrap">
      <div class="features">
        <article class="feature">
          <div class="feature__icon"><AppIcon name="search" :size="18" /></div>
          <h3 class="feature__title">Prozorro аналіз</h3>
          <p class="feature__text">
            Введіть ID закупівлі — система вивантажить позиції, обчислить
            очікувану ринкову вартість і покаже діапазон відхилень.
          </p>
        </article>
        <article class="feature">
          <div class="feature__icon"><AppIcon name="file" :size="18" /></div>
          <h3 class="feature__title">Excel перевірка</h3>
          <p class="feature__text">
            Завантажте власний прайс-лист — checkIT зіставить кожну позицію
            з актуальним ринком і поверне розшифрований звіт.
          </p>
        </article>
        <article class="feature">
          <div class="feature__icon"><AppIcon name="store" :size="18" /></div>
          <h3 class="feature__title">Декілька магазинів</h3>
          <p class="feature__text">
            Rozetka, Сільпо, Епіцентр — порівняння виконується паралельно
            з урахуванням ваги/обсягу, а не лише по назві.
          </p>
        </article>
      </div>
    </section>

    <!-- How it works -->
    <section class="steps-section">
      <div class="steps-eyebrow">Як це працює</div>
      <h2 class="steps-title">Три кроки від ID закупівлі до звіту аудитора.</h2>

      <ol class="steps">
        <div class="steps__line" aria-hidden="true"></div>
        <li class="step">
          <div class="step__num mono">01</div>
          <h4 class="step__title">Введіть дані</h4>
          <p class="step__text">Вкажіть ID Prozorro або завантажте Excel-прайс із позиціями.</p>
        </li>
        <li class="step">
          <div class="step__num mono">02</div>
          <h4 class="step__title">Оберіть магазини</h4>
          <p class="step__text">Виберіть джерела для звірки — від одного маркетплейсу до повного набору.</p>
        </li>
        <li class="step">
          <div class="step__num mono">03</div>
          <h4 class="step__title">Отримайте результат</h4>
          <p class="step__text">Інтерактивний звіт з відхиленнями, ризиками й експортом у XLSX.</p>
        </li>
      </ol>
    </section>
  </div>
</template>

<script>
import AppIcon from '@/components/AppIcon.vue'
import AppBadge from '@/components/AppBadge.vue'

export default {
  name: 'HomeView',
  components: { AppIcon, AppBadge },
}
</script>

<style scoped>
.home {
  display: flex;
  flex-direction: column;
}

/* ===== Hero ===== */
.hero {
  position: relative;
  max-width: var(--container-narrow);
  width: 100%;
  margin: 0 auto;
  padding: var(--space-20) var(--space-6) var(--space-16);
  overflow: hidden;
}

.hero__bg {
  position: absolute;
  inset: 0;
  pointer-events: none;
  background-image:
    linear-gradient(to right, rgb(15 23 42 / 0.04) 1px, transparent 1px),
    linear-gradient(to bottom, rgb(15 23 42 / 0.04) 1px, transparent 1px);
  background-size: 56px 56px;
  -webkit-mask-image: radial-gradient(ellipse 80% 60% at 50% 0%, black 30%, transparent 75%);
  mask-image: radial-gradient(ellipse 80% 60% at 50% 0%, black 30%, transparent 75%);
}

[data-theme="dark"] .hero__bg {
  background-image:
    linear-gradient(to right, rgb(148 163 184 / 0.08) 1px, transparent 1px),
    linear-gradient(to bottom, rgb(148 163 184 / 0.08) 1px, transparent 1px);
}

.hero__content {
  position: relative;
  max-width: 720px;
}

.hero__chip {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 4px 10px;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-full);
  font-size: var(--text-xs);
  color: var(--color-text-secondary);
  background: var(--color-surface);
  margin-bottom: var(--space-6);
}

.hero__chip-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: var(--color-primary);
}

.hero__title {
  font-size: clamp(2rem, 5vw, 3.5rem);
  line-height: 1.05;
  letter-spacing: var(--tracking-display);
  font-weight: var(--font-semibold);
  color: var(--color-heading);
  margin-bottom: var(--space-5);
}

.hero__subtitle {
  font-size: var(--text-lg);
  line-height: 1.65;
  color: var(--color-text-secondary);
  max-width: 640px;
  margin-bottom: var(--space-8);
}

.hero__actions {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-3);
}

.btn {
  display: inline-flex;
  align-items: center;
  gap: var(--space-2);
  height: 44px;
  padding: 0 var(--space-5);
  border-radius: var(--radius-md);
  font-size: var(--text-md);
  font-weight: var(--font-medium);
  text-decoration: none;
  border: 1px solid transparent;
  transition: background var(--transition-fast), border-color var(--transition-fast);
}

.btn--primary {
  background: var(--color-primary);
  color: var(--color-white);
  border-color: var(--color-primary);
}

.btn--primary:hover {
  background: var(--color-primary-hover);
  border-color: var(--color-primary-hover);
  color: var(--color-white);
}

[data-theme="dark"] .btn--primary { color: #052e1b; }

.btn--secondary {
  background: var(--color-surface);
  color: var(--color-text);
  border-color: var(--color-border);
}

.btn--secondary:hover {
  background: var(--color-bg-subtle);
  border-color: var(--color-border-hover);
}

.hero__checks {
  margin-top: var(--space-10);
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-6);
  font-size: var(--text-xs);
  color: var(--color-text-secondary);
}

.hero__check {
  display: flex;
  align-items: center;
  gap: 6px;
}

.hero__check-icon {
  color: var(--color-primary);
}

/* ===== Preview frame ===== */
.preview {
  position: relative;
  margin-top: var(--space-12);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-xl);
  overflow: hidden;
  background: var(--color-surface);
  box-shadow: var(--shadow-pop);
}

.preview__chrome {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 var(--space-4);
  height: 36px;
  border-bottom: 1px solid var(--color-border);
  background: var(--color-bg-subtle);
}

.preview__dots {
  display: flex;
  gap: 6px;
}

.preview__dots span {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: var(--color-slate-300);
}

[data-theme="dark"] .preview__dots span { background: var(--color-slate-700); }

.preview__url {
  font-size: 11px;
  color: var(--color-text-secondary);
}

.preview__chrome-spacer { width: 48px; }

.preview__body {
  display: grid;
  grid-template-columns: 240px 1fr;
  min-height: 320px;
}

.preview__sidebar {
  border-right: 1px solid var(--color-border);
  padding: var(--space-4);
  background: var(--color-bg-subtle);
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.preview__nav {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  padding: 6px 8px;
  border-radius: var(--radius-sm);
  font-size: var(--text-sm);
  color: var(--color-text-secondary);
}

.preview__nav--active {
  background: var(--color-slate-100);
  color: var(--color-heading);
}

[data-theme="dark"] .preview__nav--active { background: var(--color-slate-200); }

.preview__content {
  padding: var(--space-5);
}

.preview__row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--space-4);
  margin-bottom: var(--space-4);
}

.preview__id {
  font-size: 11px;
  color: var(--color-text-secondary);
}

.preview__title {
  font-size: var(--text-md);
  font-weight: var(--font-medium);
  color: var(--color-heading);
  margin-top: 2px;
}

.preview__stats {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: var(--space-3);
}

.preview__stat {
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  padding: var(--space-3);
}

.preview__stat-label {
  font-size: 10px;
  text-transform: uppercase;
  letter-spacing: var(--tracking-wider);
  color: var(--color-text-secondary);
}

.preview__stat-value {
  margin-top: 4px;
  font-size: var(--text-xl);
  font-weight: var(--font-semibold);
  color: var(--color-heading);
}

.preview__stat-value.up { color: var(--color-danger); }
.preview__stat-value.down { color: var(--color-primary); }
.preview__stat-value.warn { color: var(--color-warning); }

.preview__table {
  margin-top: var(--space-4);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  overflow: hidden;
}

.preview__table table {
  width: 100%;
  font-size: var(--text-sm);
  border-collapse: collapse;
}

.preview__table th {
  background: var(--color-bg-subtle);
  color: var(--color-text-secondary);
  padding: 8px 12px;
  text-align: left;
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: var(--tracking-wider);
  font-weight: var(--font-medium);
}

.preview__table th.num-col { text-align: right; }

.preview__table td {
  padding: 8px 12px;
  border-top: 1px solid var(--color-border);
  color: var(--color-text);
}

.preview__table td.num-col { text-align: right; }
.preview__table td.up { color: var(--color-danger); }
.preview__table td.down { color: var(--color-primary); }

/* ===== Features ===== */
.features-wrap {
  max-width: var(--container-narrow);
  width: 100%;
  margin: 0 auto;
  padding: var(--space-8) var(--space-6);
}

.features {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-xl);
  overflow: hidden;
  background: var(--color-border);
  gap: 1px;
}

.feature {
  background: var(--color-surface);
  padding: var(--space-8);
}

.feature__icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  border-radius: var(--radius-md);
  background: var(--color-bg-subtle);
  border: 1px solid var(--color-border);
  color: var(--color-text);
}

.feature__title {
  margin-top: var(--space-4);
  font-size: var(--text-lg);
  font-weight: var(--font-semibold);
}

.feature__text {
  margin-top: var(--space-2);
  font-size: var(--text-base);
  color: var(--color-text-secondary);
  line-height: 1.65;
}

/* ===== Steps ===== */
.steps-section {
  max-width: var(--container-narrow);
  width: 100%;
  margin: 0 auto;
  padding: var(--space-16) var(--space-6);
}

.steps-eyebrow {
  font-size: var(--text-xs);
  text-transform: uppercase;
  letter-spacing: var(--tracking-wider);
  color: var(--color-text-secondary);
  margin-bottom: var(--space-3);
}

.steps-title {
  font-size: clamp(1.5rem, 3vw, 2rem);
  font-weight: var(--font-semibold);
  letter-spacing: var(--tracking-display);
  max-width: 640px;
  margin-bottom: var(--space-10);
}

.steps {
  position: relative;
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: var(--space-6);
}

.steps__line {
  position: absolute;
  left: 0;
  right: 0;
  top: 26px;
  height: 1px;
  background: var(--color-border);
}

.step {
  position: relative;
  padding-right: var(--space-5);
}

.step__num {
  position: relative;
  z-index: 1;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 52px;
  height: 52px;
  border-radius: 50%;
  border: 1px solid var(--color-border);
  background: var(--color-surface);
  font-size: var(--text-base);
  color: var(--color-text-secondary);
}

.step__title {
  margin-top: var(--space-4);
  font-size: var(--text-md);
  font-weight: var(--font-semibold);
}

.step__text {
  margin-top: 6px;
  font-size: var(--text-base);
  color: var(--color-text-secondary);
  line-height: 1.6;
}

/* ===== Responsive ===== */
@media (max-width: 900px) {
  .preview__body { grid-template-columns: 1fr; }
  .preview__sidebar { display: none; }
  .preview__stats { grid-template-columns: repeat(2, 1fr); }
  .features { grid-template-columns: 1fr; }
  .steps { grid-template-columns: 1fr; }
  .steps__line { display: none; }
}

@media (max-width: 640px) {
  .hero { padding: var(--space-10) var(--space-4) var(--space-8); }
  .hero__actions .btn { flex: 1; justify-content: center; }
  .features-wrap, .steps-section { padding-left: var(--space-4); padding-right: var(--space-4); }
}
</style>
