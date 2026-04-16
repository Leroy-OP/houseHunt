<template>
  <div class="saved-properties-page">
    <h1>Saved Properties</h1>
    <div v-if="savedProperties.length === 0" class="no-saved">
      <p>No saved properties yet. Go to <router-link to="/properties">Properties</router-link> to save some!</p>
    </div>
    <div v-else class="properties-list">
      <div class="row">
        <div v-for="property in savedProperties" :key="property.id" class="col-md-4 mb-4">
          <div class="card h-100 card-relative">
            <div class="save-overlay">
              <button class="save-btn" @click="toggleSave(property)">
                <i class="fas fa-heart text-danger"></i>
              </button>
            </div>
            <img :src="property.img" class="card-img-top" alt="Property Image" />
            <div class="card-body">
              <h5 class="card-title">{{ property.title }}</h5>
              <p class="card-text">{{ property.description }}</p>
              <p class="card-text"><small class="text-muted">{{ property.location }}</small></p>
              <p class="card-text"><strong>${{ property.price }}/month</strong></p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';

// Function to get saved properties from localStorage
const getSavedProperties = () => {
  const saved = localStorage.getItem('savedProperties');
  return saved ? JSON.parse(saved) : [];
};

// Function to save to localStorage
const saveToLocalStorage = (properties) => {
  localStorage.setItem('savedProperties', JSON.stringify(properties));
};

const savedProperties = ref(getSavedProperties());

const toggleSave = (property) => {
  const index = savedProperties.value.findIndex(p => p.id === property.id);
  if (index > -1) {
    savedProperties.value.splice(index, 1);
  } else {
    savedProperties.value.push(property);
  }
  saveToLocalStorage(savedProperties.value);
};

// Update localStorage when savedProperties changes
import { watch } from 'vue';
watch(savedProperties, (newVal) => {
  saveToLocalStorage(newVal);
}, { deep: true });
</script>

<style scoped>
.saved-properties-page {
  padding: 20px;
}

.no-saved {
  text-align: center;
  margin-top: 50px;
}

.properties-list {
  margin-top: 20px;
}

.card {
  transition: transform 0.2s;
  position: relative;
}

.card:hover {
  transform: scale(1.05);
}

.card-relative {
  position: relative;
}

.save-overlay {
  position: absolute;
  top: 10px;
  right: 10px;
  z-index: 10;
}

.save-btn {
  background: rgba(255, 255, 255, 0.8);
  border: none;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: background 0.3s;
}

.save-btn:hover {
  background: rgba(255, 255, 255, 1);
}
</style>