<template>
    <div id="app">
        <header>
            <h1>Welcome to Pyman project!</h1>
        </header>

        <main>
            <div class="emoji-container">
                <div class="emoji">😊</div>
            </div>
        </main>

        <footer>
            <p>© 2025. All rights are reserved.</p>
        </footer>
    </div>
</template>

<script>
    export default {
        name: 'App'
    };
</script>

<style>
    body, html {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
        overflow-x: hidden;
        height: 100%; 
    }

    #app {
        display: flex;
        flex-direction: column;
        min-height: 100vh;
    }

    header {
        background-color: #42b883;
        color: white;
        padding: 20px;
        border-radius: 0 0 20px 20px;
        text-align: center;
        width: 100%;
        box-sizing: border-box;
    }

        header h1 {
            margin: 0;
            font-size: 2rem;
        }

    main {
        flex: 1;
        display: flex;
        justify-content: center;
        align-items: center;
    }

    .emoji-container {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 200px;
    }

    .emoji {
        font-size: 5rem;
        animation: bounce 1s infinite;
        transform-origin: center;
    }

    @keyframes bounce {
        0%, 100% {
            transform: translateY(0);
        }

        50% {
            transform: translateY(-20px);
        }
    }

    footer {
        background: #2c3e50;
        color: white;
        padding: 10px;
        text-align: center;
        border-radius: 20px 20px 0 0;
        width: 100%;
        box-sizing: border-box; 
        position: relative;
    }
</style>
