<template>
  <div class="excel-page">
    <div class="excel-container">
      <h1>Завантаження Excel документа</h1>
      <p>
        Перетягніть файл сюди або натисніть, щоб вибрати Excel документ для перевірки та аналізу.
      </p>
      <div class="drop-area"
           @dragover.prevent
           @dragenter.prevent
           @drop.prevent="handleDrop"
           @click="triggerFileInput">
        <p v-if="!fileName">Перетягніть файл сюди або натисніть, щоб вибрати</p>
        <p v-else>Вибраний файл: {{ fileName }}</p>
      </div>
      <input type="file"
             ref="fileInput"
             @change="handleFileChange"
             accept=".xlsx, .xls"
             hidden />
      <button v-if="fileName" @click="handleUpload">Завантажити та перевірити</button>
    </div>
  </div>
</template>

<script>
  import { ref } from 'vue'

  export default {
    name: 'ExcelUpload',
    setup() {
      const fileName = ref('')
      const fileData = ref(null)
      const fileInput = ref(null)

      const triggerFileInput = () => {
        fileInput.value.click()
      }

      const handleFileChange = (event) => {
        const file = event.target.files[0]
        if (file) {
          fileName.value = file.name
          fileData.value = file
        }
      }

      const handleDrop = (event) => {
        const files = event.dataTransfer.files
        if (files.length) {
          const file = files[0]
          fileName.value = file.name
          fileData.value = file
        }
      }

      const handleUpload = () => {
        // Тут можна додати логіку перевірки та аналізу Excel-файлу (наприклад, через API або бібліотеку)
        console.log("Завантаження файлу:", fileName.value)
        alert(`Файл "${fileName.value}" завантажено та аналізовано!`)
        // Очистка даних після завантаження
        fileName.value = ''
        fileData.value = null
      }

      return { fileName, fileData, fileInput, triggerFileInput, handleFileChange, handleDrop, handleUpload }
    }
  }
</script>

<style scoped>
  .excel-page {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    padding: 2rem;
    padding-top: 100px;
  }

  .excel-container {
    background: #ffffff;
    padding: 2.5rem;
    border-radius: 12px;
    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
    max-width: 600px;
    width: 100%;
    text-align: center;
    font-family: 'Raleway', sans-serif;
    border: 2px solid #0efc3d;
  }

    .excel-container h1 {
      font-size: 2.5rem;
      color: #333;
      margin-bottom: 1rem;
      font-weight: 700;
      text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.15);
    }

    .excel-container p {
      font-size: 1.2rem;
      color: #444;
      margin-bottom: 1.5rem;
    }

  .drop-area {
    border: 3px dashed #0efc3d;
    border-radius: 8px;
    padding: 2.5rem;
    cursor: pointer;
    transition: background-color 0.3s ease, border-color 0.3s ease;
    margin-bottom: 1.5rem;
  }

    .drop-area:hover {
      background-color: rgba(0, 255, 0, 0.1); /* Легкий прозорий зелений */
      border-color: #b2221e;
    }

    .drop-area p {
      margin: 0;
      font-size: 1.1rem;
      color: #555;
    }

  button {
    margin-top: 1.5rem;
    padding: 0.85rem 2rem;
    font-size: 1.1rem;
    background: linear-gradient(135deg, #41ec22, #27ac0f);
    color: #fff;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    transition: background 0.3s ease, transform 0.2s ease;
  }

    button:hover {
      background: linear-gradient(135deg, #27ac0f, #41ec22);
      transform: scale(1.03);
    }
</style>
