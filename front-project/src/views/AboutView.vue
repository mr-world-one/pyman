<template>
  <div class="about-us">
    <h2>Про нас</h2>
    <p class="intro">
      Ласкаво просимо на <span class="green">check</span> <span class="red">IT</span> – сервіс, який допомагає порівнювати ціни та умови тендерів для бізнесу та державних закупівель.
    </p>
    <div class="content">
      <p>
        Наша платформа створена для спрощення аналізу тендерних пропозицій. Ми надаємо можливість швидко знаходити та порівнювати ціни, умови та інші ключові параметри як державних, так і приватних тендерів. Забудьте про нескінченне блукання між різними сайтами – вся необхідна інформація зібрана в одному місці!
      </p>
      <h3>Наші можливості:</h3>
      <ul>
        <li>Аналіз державних тендерних пропозицій та закупівельних угод через Prozorro</li>
        <li>Порівняння умов приватних тендерів для бізнесу</li>
        <li>Зручний інтерфейс для швидкого доступу до актуальної інформації</li>
      </ul>
    </div>
    <div class="contacts">
      <h3>Контакти:</h3>
      <p><a href="tel:+380677557973">+380 67 755 7973</a></p>
      <p><a href="tel:+380960971750">+380 96 097 1750</a></p>
    </div>
  </div>
</template>

<script>
  export default {
    name: "About"
  };
</script>

<style scoped>
  @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700&display=swap');

  .about-us {
    text-align: center;
    padding: 10rem;
    max-width: 1200px;
    margin: 50px auto 0 auto;
    background: #ffffff;
    font-family: 'Montserrat', sans-serif;
  }

  h2 {
    font-size: 3rem;
    font-weight: 700;
    color: #333;
    text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.2);
  }

  .intro {
    font-size: 1.4rem;
    margin-bottom: 1.5rem;
    color: #555;
    font-weight: 600;
  }

  .green {
    color: #35f816;
    font-weight: bold;
  }

  .red {
    color: #f00808;
    font-weight: bold;
  }

  .content p {
    font-size: 1.2rem;
    color: #444;
    margin: 1rem 0;
  }

  .content h3 {
    font-size: 2rem;
    font-weight: 700;
    color: #f00808;
    margin: 1.5rem 0 1rem;
  }

  .content ul {
    list-style-type: disc;
    padding-left: 2rem;
    font-size: 1.2rem;
    color: #444;
    text-align: left;
    margin: 0 auto;
    max-width: 800px;
  }

  .content li {
    margin: 0.5rem 0;
    font-weight: 600;
  }

  .contacts {
    margin-top: 5rem;
    padding: 1.5rem;
    background: #f8f8f8;
    border-radius: 8px;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  }

    .contacts h3 {
      font-size: 2rem;
      color: #333;
    }

    .contacts p {
      font-size: 1.2rem;
      color: #555;
      font-weight: 600;
    }

    .contacts a {
      color: #35f816;
      text-decoration: none;
      font-weight: bold;
    }

      .contacts a:hover {
        text-decoration: underline;
      }
</style>
