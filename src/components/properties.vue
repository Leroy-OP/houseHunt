<template>
  <div class="properties-page">
    <!-- Notification Toast -->
    <div v-if="notification" class="notification-toast">
      {{ notification }}
    </div>

    <!-- Search Bar -->
    <div class="search-bar">
      <div class="search-item">
        <span class="input-icon"><i class="fas fa-map-marker-alt"></i></span>
        <input type="text" v-model="searchQuery" placeholder="Location" class="form-control with-icon" />
      </div>
      <button class="search-btn" @click="performSearch">
        <i class="fas fa-search"></i>
      </button>
      <button class="filters-btn" @click="showFilters = !showFilters">
        <i class="fas fa-sliders-h"></i>
      </button>
    </div>

    <!-- Filters Popup -->
    <div v-if="showFilters" class="filters-overlay" @click="showFilters = false">
      <div class="filters-card" @click.stop>
        <div class="filters-header">
          <h3>Filters</h3>
          <button class="close-btn" @click="showFilters = false">
            <i class="fas fa-times"></i>
          </button>
        </div>
        <div class="filters-body">
          <div class="filter-group">
            <label>Price Range</label>
            <div class="price-inputs">
              <input type="number" v-model.number="filters.minPrice" placeholder="Min Price" class="form-control" />
              <span>-</span>
              <input type="number" v-model.number="filters.maxPrice" placeholder="Max Price" class="form-control" />
            </div>
          </div>
          <div class="filter-group">
            <label>Location</label>
            <div class="checkbox-group">
              <label v-for="loc in locations" :key="loc" class="checkbox-label">
                <input type="checkbox" v-model="filters.locations" :value="loc" />
                {{ loc }}
              </label>
            </div>
          </div>
        </div>
        <div class="filters-footer">
          <button class="btn btn-secondary" @click="resetFilters">Reset</button>
          <button class="btn btn-primary" @click="applyFilters">Apply Filters</button>
        </div>
      </div>
    </div>

    <!-- Properties List -->
    <div class="properties-list">
      <div class="saved-link">
        <router-link to="/saved" class="btn btn-outline-primary">View Saved Properties</router-link>
      </div>
      <h2>Available Properties</h2>
      <div class="row">
        <div v-for="property in filteredProperties" :key="property.id" class="col-md-4 mb-4">
          <div class="card h-100 card-relative">
            <div class="save-overlay">
              <button class="save-btn" @click="toggleSave(property)">
                <i :class="isSaved(property) ? 'fas fa-heart text-danger' : 'far fa-heart'"></i>
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
import { ref, computed } from 'vue';

// Sample properties data
const properties = ref([
  {
    id: 1,
    title: 'Cozy Apartment',
    description: 'A nice cozy apartment in the city center.',
    location: 'New York',
    price: 1200,
    img: 'https://mdbootstrap.com/img/new/standard/city/041.webp'
  },
  {
    id: 2,
    title: 'Modern Studio',
    description: 'Modern studio with great amenities.',
    location: 'Los Angeles',
    price: 1500,
    img: 'https://mdbootstrap.com/img/new/standard/city/042.webp'
  },
  {
    id: 3,
    title: 'Spacious House',
    description: 'Large house perfect for families.',
    location: 'Chicago',
    price: 2000,
    img: 'https://mdbootstrap.com/img/new/standard/city/043.webp'
  },
  {
    id: 4,
    title: 'Downtown Loft',
    description: 'Stylish loft in downtown area.',
    location: 'New York',
    price: 1800,
    img: 'https://mdbootstrap.com/img/new/standard/city/044.webp'
  }
]);

const searchQuery = ref('');
const notification = ref(null);
const showFilters = ref(false);

const filters = ref({
  minPrice: 0,
  maxPrice: 10000,
  locations: []
});

const locations = ['New York', 'Los Angeles', 'Chicago'];

const showNotification = (message) => {
  notification.value = message;
  setTimeout(() => {
    notification.value = null;
  }, 3000);
};

const filteredProperties = computed(() => {
  let results = properties.value;

  // Apply search query filter
  if (searchQuery.value) {
    results = results.filter(property =>
      property.location.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      property.title.toLowerCase().includes(searchQuery.value.toLowerCase())
    );
  }

  // Apply price filter
  results = results.filter(property =>
    property.price >= filters.value.minPrice && property.price <= filters.value.maxPrice
  );

  // Apply location filter
  if (filters.value.locations.length > 0) {
    results = results.filter(property =>
      filters.value.locations.includes(property.location)
    );
  }

  return results;
});

// Function to get saved properties from localStorage
const getSavedProperties = () => {
  const saved = localStorage.getItem('savedProperties');
  return saved ? JSON.parse(saved) : [];
};

// Function to check if a property is saved
const isSaved = (property) => {
  const saved = getSavedProperties();
  return saved.some(p => p.id === property.id);
};

const toggleSave = (property) => {
  let saved = getSavedProperties();
  const index = saved.findIndex(p => p.id === property.id);
  if (index > -1) {
    saved.splice(index, 1);
    showNotification('Property removed from saved!');
  } else {
    saved.push(property);
    showNotification(property.title + ' has been saved!');
  }
  localStorage.setItem('savedProperties', JSON.stringify(saved));
};

const performSearch = () => {
  // The filtering is reactive, so no need for extra logic here
  console.log('Searching for:', searchQuery.value);
};

const applyFilters = () => {
  showFilters.value = false;
  showNotification('Filters applied!');
};

const resetFilters = () => {
  filters.value = {
    minPrice: 0,
    maxPrice: 10000,
    locations: []
  };
  showNotification('Filters reset!');
};
</script>

<style scoped>
.properties-page {
  padding: 20px;
}

.search-bar {
  margin-bottom: 30px;
  background: #fff;
  border-radius: 20px;
  padding: 10px;
  display: flex;
  align-items: center;
  gap: 10px;
  width: 80%;
  max-width: 500px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.search-item {
  flex: 1;
  text-align: left;
  padding: 10px;
  position: relative;
}

.search-item label {
  font-size: 12px;
  color: gray;
  display: block;
  margin-bottom: 5px;
}

.search-item {
  flex: 1;
  text-align: left;
  padding: 10px;
  position: relative;
}

.input-icon {
  position: absolute;
  left: 18px;
  top: 50%;
  transform: translateY(-50%);
  color: #888;
  pointer-events: none;
}

.search-item input {
  width: 100%;
  border: none;
  outline: none;
  font-weight: 500;
  color: black;
  padding-left: 38px;
}

.search-btn {
  background: rgb(183, 63, 42);
  color: white;
  border: none;
  border-radius: 20px;
  width: 50px;
  height: 50px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}

.filters-btn {
  background: rgb(183, 63, 42);
  color: white;
  border: none;
  border-radius: 20px;
  width: 50px;
  height: 50px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}

.filters-btn:hover {
  background: rgb(163, 43, 22);
}

.filters-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 999;
}

.filters-card {
  background: white;
  border-radius: 12px;
  width: 90%;
  max-width: 500px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
  overflow: hidden;
  animation: slideUp 0.3s ease-in-out;
}

@keyframes slideUp {
  from {
    transform: translateY(50px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

.filters-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  border-bottom: 1px solid #eee;
}

.filters-header h3 {
  margin: 0;
  color: #333;
}

.close-btn {
  background: none;
  border: none;
  font-size: 20px;
  cursor: pointer;
  color: #666;
}

.filters-body {
  padding: 20px;
  max-height: 400px;
  overflow-y: auto;
}

.filter-group {
  margin-bottom: 20px;
}

.filter-group label {
  display: block;
  font-weight: 600;
  margin-bottom: 10px;
  color: #333;
}

.price-inputs {
  display: flex;
  gap: 10px;
  align-items: center;
}

.price-inputs input {
  flex: 1;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.checkbox-group {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  color: #555;
}

.checkbox-label input[type="checkbox"] {
  cursor: pointer;
}

.filters-footer {
  display: flex;
  gap: 10px;
  padding: 20px;
  border-top: 1px solid #eee;
  justify-content: flex-end;
}

.btn {
  padding: 10px 20px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 500;
}

.btn-primary {
  background: rgb(183, 63, 42);
  color: white;
}

.btn-secondary {
  background: #f0f0f0;
  color: #333;
}

.properties-list h2 {
  margin-bottom: 20px;
  color: #333;
}

.saved-link {
  text-align: right;
  margin-bottom: 10px;
}

.notification-toast {
  position: fixed;
  top: 20px;
  right: 20px;
  background: #28a745;
  color: white;
  padding: 15px 20px;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  animation: slideIn 0.3s ease-in-out;
  z-index: 1000;
}

@keyframes slideIn {
  from {
    transform: translateX(400px);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
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