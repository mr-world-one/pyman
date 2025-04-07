<template>
    <div class="excel-page">
        <div class="excel-container">
            <h1>Завантаження Excel документа</h1>
            <p>Перетягніть файл сюди або натисніть, щоб вибрати Excel документ для перевірки та аналізу.</p>
            <div class="drop-area" @dragover.prevent @dragenter.prevent @drop.prevent="handleDrop" @click="triggerFileInput">
                <p v-if="!fileName">Перетягніть файл сюди або натисніть, щоб вибрати</p>
                <p v-else>Вибраний файл: {{ fileName }}</p>
            </div>
            <input type="file" ref="fileInput" @change="handleFileChange" accept=".xlsx, .xls" hidden />
            <button v-if="fileName" @click="handleUpload">Завантажити та перевірити</button>
            <div v-if="comparisonData">
                <h2>Результати порівняння</h2>
                <table>
                    <thead>
                        <tr>
                            <th>Назва товару</th>
                            <th>Ціна з тендеру, грн</th>
                            <th>Найнижча ціна з Rozetka, грн</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="item in comparisonData" :key="item.name">
                            <td>{{ item.name }}</td>
                            <td>{{ item.excelPrice || 'Н/Д' }}</td>
                            <td>{{ item.rozetkaPrice || 'Н/Д' }}</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</template>

<script>
    //import { ref } from 'vue';
    //import axios from 'axios';

    //export default {
    //    name: 'ExcelUpload',
    //    setup() {
    //        const fileName = ref('');
    //        const fileData = ref(null);
    //        const fileInput = ref(null);
    //        const comparisonData = ref(null);

    //        const triggerFileInput = () => {
    //            fileInput.value.click();
    //        };

    //        const handleFileChange = (event) => {
    //            const file = event.target.files[0];
    //            if (file) {
    //                fileName.value = file.name;
    //                fileData.value = file;
    //            }
    //        };

    //        const handleDrop = (event) => {
    //            const files = event.dataTransfer.files;
    //            if (files.length) {
    //                const file = files[0];
    //                fileName.value = file.name;
    //                fileData.value = file;
    //            }
    //        };

    //        const handleUpload = async () => {
    //            if (!fileData.value) return;

    //            const formData = new FormData();
    //            formData.append('file', fileData.value);

    //            try {
    //                const response = await axios.post('http://localhost:8000/upload-excel', formData, {
    //                    headers: { 'Content-Type': 'multipart/form-data' },
    //                });
    //                comparisonData.value = response.data;
    //                fileName.value = '';
    //                fileData.value = null;
    //            } catch (error) {
    //                console.error('Помилка:', error);
    //                alert('Сталася помилка під час обробки файлу');
    //            }
    //        };

    //        return { fileName, fileData, fileInput, comparisonData, triggerFileInput, handleFileChange, handleDrop, handleUpload };
    //    },
    //};
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
        max-width: 800px;
        width: 100%;
        text-align: center;
        font-family: 'Raleway', sans-serif;
        border: 2px solid #0efc3d;
    }

        .excel-container h1 {
            font-size: 2.5rem;
            color: #333;
            margin-bottom: 1rem;
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
        transition: background-color 0.3s ease;
    }

        .drop-area:hover {
            background-color: rgba(0, 255, 0, 0.1);
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
    }

        button:hover {
            background: linear-gradient(135deg, #27ac0f, #41ec22);
        }

    table {
        width: 100%;
        border-collapse: collapse;
        margin-top: 20px;
    }

    th, td {
        border: 1px solid #ddd;
        padding: 8px;
        text-align: left;
    }

    th {
        background-color: #f2f2f2;
    }
</style>