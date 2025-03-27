<script>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { apiClient } from '@/api/config';

export default {
  name: "App",
  setup() {
    const router = useRouter();
    const menuOpen = ref(false);
    const isAuthenticated = ref(false);

    const toggleMenu = () => {
      menuOpen.value = !menuOpen.value;
    };

    const checkAuth = () => {
      const token = localStorage.getItem('token');
      isAuthenticated.value = !!token;
    };

    const handleLogout = async () => {
      localStorage.removeItem('token');
      isAuthenticated.value = false;
      await router.push('/signin');
    };

    onMounted(() => {
      checkAuth();
    });

    return { 
      menuOpen, 
      toggleMenu, 
      isAuthenticated,
      handleLogout 
    };
  }
};
</script>

<template>
  <div id="app">
    <header>
      <img src="@/assets/picture.png" alt="Лого" class="picture">
      <h1 class="logo">
        <span class="green">check</span> <span class="red">IT</span>
        <span class="subtitle">Технологія чесності</span>
      </h1>
      <div class="menu-container">
        <button @click="toggleMenu" :class="{ clicked: menuOpen }" class="button">
          <svg xmlns="http://www.w3.org/2000/svg" width="50" height="50" viewBox="0 0 20 20" fill="none" class="svg-icon">
            <g stroke-width="1.5" stroke-linecap="round" stroke="#000000">
              <circle r="2.5" cy="10" cx="10"></circle>
              <path fill-rule="evenodd" d="m8.39079 2.80235c.53842-1.51424 2.67991-1.51424 3.21831-.00001.3392.95358 1.4284 1.40477 2.3425.97027 1.4514-.68995 2.9657.82427 2.2758 2.27575-.4345.91407.0166 2.00334.9702 2.34248 1.5143.53842 1.5143 2.67996 0 3.21836-.9536.3391-1.4047 1.4284-.9702 2.3425.6899 1.4514-.8244 2.9656-2.2758 2.2757-.9141-.4345-2.0033.0167-2.3425.9703-.5384 1.5142-2.67989.00001-3.21831 0-.33914-.9536-1.4284-1.4048-2.34247-.9703-1.45148.6899-2.96571-.8243-2.27575-2.2757.43449-.9141-.01669-2.0034-.97028-2.3425-1.51422-.5384-1.51422-2.67994.00001-3.21836.95358-.33914 1.40476-1.42841.97027-2.34248-.68996-1.45148.82427-2.9657 2.27575-2.27575.91407.4345 2.00333-.01669 2.34247-.97026z" clip-rule="evenodd"></path>
            </g>
          </svg>
          <span class="lable">Menu</span>
        </button>
        <transition name="slide">
          <div v-if="menuOpen" class="side-menu-overlay" @click="toggleMenu">
            <div class="side-menu" @click.stop>
              <ul>
                <li><router-link to="/" @click="toggleMenu">Головна</router-link></li>
                <li><router-link to="/about" @click="toggleMenu">Про нас</router-link></li>
                <li><router-link to="/register" @click="toggleMenu">Реєстрація</router-link></li>
                <li><router-link to="/signin" @click="toggleMenu">Увійти</router-link></li>
                <li v-if="!isAuthenticated"><router-link to="/xpath" @click="toggleMenu">X-Path</router-link></li>
                <li v-if="!isAuthenticated"><router-link to="/excel-page" @click="toggleMenu">Excel tenders</router-link></li>
                <li v-if="!isAuthenticated"><router-link to="/search-tender" @click="toggleMenu">Prozorro tenders</router-link></li>
                <li v-if="!isAuthenticated"><a href="#" @click.prevent="handleLogout">Вийти</a></li>
              </ul>
            </div>
          </div>
        </transition>
      </div>
    </header>

    <main>
      <router-view></router-view>
    </main>

    <footer>
      <p>© 2025. All rights are reserved.</p>
    </footer>
  </div>
</template>



<style>
  @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500&family=Raleway:wght@300;700&display=swap');
  @import url('https://fonts.googleapis.com/css2?family=Rubik:wght@700&family=Anton&display=swap');

  body, html {
    box-sizing: border-box;
    overflow-x: hidden;
    height: 100%;
    background: url('@/assets/upscalemedia-transformed.jpeg') no-repeat center;
    background-size: cover;
  }

  #app {
    max-width: 1280px;
    margin: auto;
    display: flex;
    flex-direction: column;
    min-height: 100vh;
  }

  .picture {
    position: fixed;
    height: 150px;
    left: 10px;
  }

  header {
    position: fixed;
    background: #ffffff;
    width: 100%;
    right: 1px;
    box-sizing: border-box;
    display: flex;
  }

  .logo {
    font-family: 'Rubik', sans-serif;
    flex-grow: 1;
    text-align: center;
    font-size: 4rem;
    margin-top: 0;
    margin-bottom: 3px;
    font-family: 'Rubik';
    font-size: 5rem;
    font-weight: 700;
    letter-spacing: 4px;
    color: #000000;
    -webkit-text-stroke: 2px #000000;
    margin-top: 0;
    margin-bottom: 3px;
  }

  .green {
    color: #35f816;
    text-transform: lowercase;
  }

  .red {
    color: #f00808;
  }

  .subtitle {
    font-size: 1rem;
    display: block;
    font-family: 'Raleway', sans-serif;
    font-weight: 300;
    opacity: 0.9;
    margin-top: 5px;
    color: black;
  }

  .menu-container {
    position: fixed;
    top: 42px;
    right: 20px;
    z-index: 1000;
  }

  .button {
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 6px 12px;
    gap: 8px;
    height: 36px;
    width: 120px;
    border: none;
    background: #ffffff;
    border-radius: 20px;
    cursor: pointer;
  }

  .lable {
    line-height: 20px;
    font-size: 17px;
    color: #000000;
    font-family: 'Rubik', sans-serif;
    letter-spacing: 1px;
  }

  .button:hover {
    background: #ffffff;
  }

    .button:hover .svg-icon {
      animation: spin 2s linear infinite;
    }

  @keyframes spin {
    0% {
      transform: rotate(0deg);
    }

    100% {
      transform: rotate(360deg);
    }
  }

  .fade-enter-active, .fade-leave-active {
    transition: opacity 0.3s;
  }

  .fade-enter, .fade-leave-to {
    opacity: 0;
  }

  main {
    flex: 1;
    display: flex;
    justify-content: center;
    align-items: center;
  }

  footer {
    position: fixed;
    bottom: 0;
    left: 0;
    width: 100%;
    background: #ffffff;
    color: #000000;
    padding: 15px;
    text-align: center;
    border-radius: 20px 20px 0 0;
    box-sizing: border-box;
    font-family: 'Raleway', sans-serif;
    font-weight: 700;
    letter-spacing: 1px;
    z-index: 1000; 
  }


  .side-menu-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.3);
    z-index: 1100;
    display: flex;
    justify-content: flex-end;
  }

  .side-menu {
    width: 250px;
    height: 100%;
    background: #aa1108;
    padding: 20px;
    box-sizing: border-box;
    z-index: 1200;
  }

    .side-menu ul {
      list-style: none;
      margin: 0;
      padding: 0;
    }

    .side-menu li {
      margin-bottom: 15px;
    }

      .side-menu li:last-child {
        margin-bottom: 0;
      }

    .side-menu a {
      color: #ffffff;
      text-decoration: none;
      font-size: 1.1rem;
    }

  .slide-enter-active, .slide-leave-active {
    transition: transform 0.3s ease;
  }

  .slide-enter-from, .slide-leave-to {
    transform: translateX(100%);
  }

  .slide-enter-to, .slide-leave-from {
    transform: translateX(0);
  }
  .auth-buttons {
  display: flex;
  gap: 10px;
  align-items: center;
}

.auth-link {
  color: #000000;
  text-decoration: none;
  padding: 5px 10px;
  border-radius: 5px;
  transition: background-color 0.3s;
}

.auth-link:hover {
  background-color: rgba(0, 0, 0, 0.1);
}
</style>
