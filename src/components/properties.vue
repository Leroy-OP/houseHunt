<template>
  <div class="properties-page">

    <!-- Notification Toast -->
    <transition name="toast">
      <div v-if="notification" class="notification-toast">
        <i class="fas fa-check-circle"></i>
        <span>{{ notification }}</span>
      </div>
    </transition>

    <!-- Header -->
    <div class="page-header">
      <div class="header-text">
        <p class="header-label">HUNTER STREET</p>
        <h1 class="header-title">Hunt Your <em>Perfect</em> Home</h1>
      </div>
      <router-link to="/saved" class="saved-link-btn">
        <i class="fas fa-heart"></i>
        <span>Saved</span>
      </router-link>
    </div>

    <!-- Search Bar -->
    <div class="search-bar">
      <div class="search-item">
        <i class="fas fa-map-marker-alt search-icon"></i>
        <input
          type="text"
          v-model="searchQuery"
          placeholder="Search by location or title..."
          class="search-input"
          @keyup.enter="performSearch"
        />
      </div>
      <button class="search-btn" @click="performSearch">
        <i class="fas fa-search"></i>
      </button>
      <button class="filters-btn" @click="showFilters = !showFilters">
        <i class="fas fa-sliders-h"></i>
        <span class="filter-count" v-if="activeFilterCount > 0">{{ activeFilterCount }}</span>
      </button>
    </div>

    <!-- Active Filter Chips -->
    <div class="filter-chips" v-if="activeFilterCount > 0">
      <span
        v-for="type in filters.propertyTypes"
        :key="'type-' + type"
        class="chip"
        @click="removeTypeFilter(type)"
      >
        {{ formatPropertyType(type) }} <i class="fas fa-times"></i>
      </span>
      <span
        v-for="loc in filters.locations"
        :key="'loc-' + loc"
        class="chip"
        @click="removeLocationFilter(loc)"
      >
        {{ loc }} <i class="fas fa-times"></i>
      </span>
      <button class="chip chip-clear" @click="resetFilters">Clear All</button>
    </div>

    <!-- Filters Popup -->
    <transition name="overlay">
      <div v-if="showFilters" class="filters-overlay" @click="showFilters = false">
        <div class="filters-card" @click.stop>
          <div class="filters-header">
            <h3>Filters</h3>
            <button class="close-btn" @click="showFilters = false">
              <i class="fas fa-times"></i>
            </button>
          </div>
          <div class="filters-body">
            <!-- Price Range Filter -->
            <div class="filter-group">
              <label class="filter-label">Price Range (KES/month)</label>
              <div class="price-range-inputs">
                <input
                  type="number"
                  v-model.number="filters.minPrice"
                  placeholder="Min"
                  class="price-input"
                />
                <span class="price-separator">—</span>
                <input
                  type="number"
                  v-model.number="filters.maxPrice"
                  placeholder="Max"
                  class="price-input"
                />
              </div>
              <div class="price-display">
                KES {{ formatPrice(filters.minPrice) }} &nbsp;→&nbsp; KES {{ formatPrice(filters.maxPrice) }}
              </div>
            </div>

            <!-- Property Type Filter -->
            <div class="filter-group">
              <label class="filter-label">Property Type</label>
              <div class="checkbox-group">
                <label v-for="type in propertyTypes" :key="type" class="checkbox-label">
                  <input type="checkbox" v-model="filters.propertyTypes" :value="type" />
                  <span class="checkbox-text">
                    <i :class="getPropertyTypeIcon(type)"></i>
                    {{ formatPropertyType(type) }}
                  </span>
                </label>
              </div>
            </div>

            <!-- Location Filter -->
            <div class="filter-group">
              <label class="filter-label">Location</label>
              <div class="checkbox-group">
                <label v-for="loc in uniqueLocations" :key="loc" class="checkbox-label">
                  <input type="checkbox" v-model="filters.locations" :value="loc" />
                  <span class="checkbox-text">
                    <i class="fas fa-map-marker-alt"></i>
                    {{ loc }}
                  </span>
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
    </transition>

    <!-- Properties Section -->
    <div class="properties-section">

      <!-- Live indicator shown while a background refresh is running -->
      <div class="section-meta" v-if="!loading">
        <span class="results-count">
          {{ filteredProperties.length }}
          <span>propert{{ filteredProperties.length === 1 ? 'y' : 'ies' }} found</span>
        </span>
        <span class="live-badge" v-if="refreshing">
          <i class="fas fa-sync fa-spin"></i> Updating…
        </span>
        <button class="refresh-btn" @click="fetchProperties(true)" title="Refresh listings" v-else>
          <i class="fas fa-sync"></i>
        </button>
      </div>

      <!-- Skeleton Loading (first load only) -->
      <div class="properties-grid" v-if="loading">
        <div v-for="n in 6" :key="n" class="skeleton-card">
          <div class="skeleton-img"></div>
          <div class="skeleton-body">
            <div class="skeleton-line short"></div>
            <div class="skeleton-line long"></div>
            <div class="skeleton-line medium"></div>
            <div class="skeleton-line price"></div>
          </div>
        </div>
      </div>

      <!-- Error State -->
      <div v-else-if="apiError" class="state-box error-state">
        <i class="fas fa-exclamation-triangle"></i>
        <p>{{ apiError }}</p>
        <button class="btn btn-primary" @click="fetchProperties(false)">Try Again</button>
      </div>

      <!-- Empty State -->
      <div v-else-if="filteredProperties.length === 0" class="state-box empty-state">
        <i class="fas fa-search"></i>
        <p>No properties match your criteria.</p>
        <button class="btn btn-secondary" @click="resetFilters">Clear Filters</button>
      </div>

      <!-- Properties Grid -->
      <div class="properties-grid" v-else>
        <div
          v-for="property in filteredProperties"
          :key="property.id"
          class="property-card"
          @click="viewDetails(property)"
        >
          <!-- Image Area -->
          <div class="card-image-wrap">
            <!-- Carousel for multiple images -->
            <div
              v-if="property.images && property.images.length > 1"
              class="image-carousel"
            >
              <img
                :src="getImageAtIndex(property, property._activeImageIndex || 0)"
                :alt="property.title"
                class="card-img"
                @error="onImageError($event)"
              />
              <div class="carousel-dots">
                <span
                  v-for="(img, idx) in property.images"
                  :key="idx"
                  class="dot"
                  :class="{ active: (property._activeImageIndex || 0) === idx }"
                  @click.stop="setActiveImage(property, idx)"
                ></span>
              </div>
              <button class="carousel-arrow left" @click.stop="prevImage(property)">
                <i class="fas fa-chevron-left"></i>
              </button>
              <button class="carousel-arrow right" @click.stop="nextImage(property)">
                <i class="fas fa-chevron-right"></i>
              </button>
            </div>

            <!-- Single Image -->
            <img
              v-else
              :src="getImage(property)"
              :alt="property.title"
              class="card-img"
              @error="onImageError($event)"
            />

            <!-- Overlays -->
            <div class="type-badge">{{ formatPropertyType(property.property_type) }}</div>

            <!-- Availability Date Badge -->
            <div
              class="availability-badge"
              :class="{ now: isAvailableNow(property.available_from) }"
              v-if="property.available_from"
            >
              <i class="fas fa-calendar-check"></i>
              <span>{{ formatAvailability(property.available_from) }}</span>
            </div>

            <div class="image-count-badge" v-if="property.images && property.images.length > 1">
              <i class="fas fa-images"></i> {{ property.images.length }}
            </div>

            <button class="save-btn" @click.stop="toggleSave(property)">
              <i :class="isSaved(property) ? 'fas fa-heart saved' : 'far fa-heart'"></i>
            </button>

            <div class="image-overlay"></div>
          </div>

          <!-- Card Body -->
          <div class="card-body">
            <div class="card-top">
              <h5 class="property-title">{{ property.title }}</h5>
              <p class="property-desc">{{ property.description }}</p>
            </div>

            <!--
              FIX: amenities are full objects { id, name, icon } from the API.
              Use object fields directly — no ID registry lookup needed.
            -->
            <div class="amenities-row" v-if="property.amenities && property.amenities.length > 0">
              <span
                v-for="amenity in property.amenities.slice(0, 5)"
                :key="amenity.id"
                class="amenity-chip"
                :title="amenity.name"
              >
                <i :class="amenity.icon"></i>
                <span class="amenity-label">{{ amenity.name }}</span>
              </span>
              <span class="amenity-chip amenity-more" v-if="property.amenities.length > 5">
                +{{ property.amenities.length - 5 }}
              </span>
            </div>

            <div class="card-meta">
              <span class="meta-item">
                <i class="fas fa-map-marker-alt"></i>
                {{ property.location }}
              </span>
              <span class="meta-item agent-meta" v-if="property.agencyName">
                <i class="fas fa-user-tie"></i>
                {{ property.agencyName }}
              </span>
            </div>

            <div class="card-footer-row">
              <div class="price-block">
                <span class="price-amount">KES {{ formatPrice(property.price) }}</span>
                <span class="price-period">/month</span>
              </div>
              <button class="view-btn">
                View <i class="fas fa-arrow-right"></i>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';

const API_BASE = 'http://127.0.0.1:8000';

const properties   = ref([]);
const loading      = ref(false);
const refreshing   = ref(false);
const apiError     = ref('');
const searchQuery  = ref('');
const notification = ref(null);
const showFilters  = ref(false);

const filters = ref({
  minPrice: 0,
  maxPrice: 10000000,
  locations: [],
  propertyTypes: [],
});

const propertyTypes = ['apartment', 'house', 'condo', 'studio', 'bedsitter'];

// ─── Image URL resolution ─────────────────────────────────────────────────────
const resolveUrl = (url) => {
  if (!url) return null;
  if (url.startsWith('http://') || url.startsWith('https://')) return url;
  return `${API_BASE}${url.startsWith('/') ? '' : '/'}${url}`;
};

const normalizeImages = (images) => {
  if (!images || !Array.isArray(images) || images.length === 0) return [];
  return images.map(img => {
    if (typeof img === 'string')  return resolveUrl(img);
    if (img?.image_url)           return resolveUrl(img.image_url);
    if (img?.url)                 return resolveUrl(img.url);
    if (img?.image)               return resolveUrl(img.image);
    if (img?.file)                return resolveUrl(img.file);
    if (img?.photo)               return resolveUrl(img.photo);
    const vals = Object.values(img).filter(v => typeof v === 'string' && v.includes('/'));
    if (vals.length > 0) return resolveUrl(vals[0]);
    return null;
  }).filter(Boolean);
};

// ─── Agency / Agent name resolver ─────────────────────────────────────────────
const resolveAgencyName = (p) => {
  const extractName = (obj) => {
    if (!obj || typeof obj !== 'object') return null;
    if (obj.first_name || obj.last_name)
      return [obj.first_name, obj.last_name].filter(Boolean).join(' ');
    if (obj.full_name)   return obj.full_name;
    if (obj.name)        return obj.name;
    if (obj.username)    return obj.username;
    if (obj.email)       return obj.email.split('@')[0];
    return null;
  };

  for (const key of ['agent', 'posted_by', 'owner']) {
    const val = p[key];
    if (val && typeof val === 'object') {
      const name = extractName(val);
      if (name) return name;
    }
  }

  const agency = p.agency_detail || p.agency;
  if (agency) {
    if (typeof agency === 'string' && agency.trim()) return agency.trim();
    if (typeof agency === 'object') {
      const name = extractName(agency);
      if (name) return name;
    }
  }

  return null;
};

const shapeProperty = (p) => ({
  id:                p.id,
  title:             p.title          || 'No Title',
  description:       p.description    || 'No description',
  location:          p.location       || 'Unknown',
  price:             parseFloat(p.price) || 0,
  property_type:     p.property_type  || 'apartment',
  images:            normalizeImages(p.images),
  agencyName:        resolveAgencyName(p),
  amenities:         Array.isArray(p.amenities) ? p.amenities : [],
  available_from:
    p.available_from    ||
    p.vacant_date       ||
    p.availability_date ||
    p.available_date    ||
    null,
  _activeImageIndex: 0,
});

// ─── Fetch / refresh ──────────────────────────────────────────────────────────
const fetchProperties = async (silent = false) => {
  if (silent) {
    refreshing.value = true;
  } else {
    loading.value  = true;
    apiError.value = '';
  }

  try {
    const res    = await axios.get(`${API_BASE}/api/properties/`);
    const shaped = res.data.map(shapeProperty);

    const existingMap = Object.fromEntries(properties.value.map(p => [p.id, p]));
    properties.value  = shaped.map(p => ({
      ...p,
      _activeImageIndex: existingMap[p.id]?._activeImageIndex ?? 0,
    }));

    if (!silent && properties.value.length > 0) {
      const prices = properties.value.map(p => p.price);
      filters.value.minPrice = Math.floor(Math.min(...prices));
      filters.value.maxPrice = Math.ceil(Math.max(...prices));
    }
  } catch (e) {
    console.error('[fetchProperties] error:', e);
    if (!silent) apiError.value = 'Failed to load properties. Please try again.';
  } finally {
    loading.value    = false;
    refreshing.value = false;
  }
};

// ─── Auto-refresh listeners ───────────────────────────────────────────────────
const onVisibilityChange = () => {
  if (document.visibilityState === 'visible') fetchProperties(true);
};
const onWindowFocus = () => { fetchProperties(true); };

let pollInterval = null;
const POLL_INTERVAL_MS = 30_000;

const listingsChannel = typeof BroadcastChannel !== 'undefined'
  ? new BroadcastChannel('listings-updated')
  : null;

onMounted(() => {
  fetchProperties(false);

  document.addEventListener('visibilitychange', onVisibilityChange);
  window.addEventListener('focus', onWindowFocus);

  pollInterval = setInterval(() => {
    if (document.visibilityState === 'visible') fetchProperties(true);
  }, POLL_INTERVAL_MS);

  if (listingsChannel) {
    listingsChannel.onmessage = () => fetchProperties(true);
  }
});

onUnmounted(() => {
  document.removeEventListener('visibilitychange', onVisibilityChange);
  window.removeEventListener('focus', onWindowFocus);
  clearInterval(pollInterval);
  listingsChannel?.close();
});

// ─── Image helpers ────────────────────────────────────────────────────────────
const PLACEHOLDER = 'https://placehold.co/600x400/1a1a2e/ffffff?text=No+Image';

const getImage = (property) =>
  property.images?.length > 0 ? property.images[0] : PLACEHOLDER;

const getImageAtIndex = (property, index) =>
  property.images?.length > index ? property.images[index] : PLACEHOLDER;

const onImageError = (e) => { e.target.src = PLACEHOLDER; };

// ─── Carousel controls ────────────────────────────────────────────────────────
const setActiveImage = (property, index) => { property._activeImageIndex = index; };
const nextImage = (property) => {
  const count = property.images.length;
  property._activeImageIndex = ((property._activeImageIndex || 0) + 1) % count;
};
const prevImage = (property) => {
  const count = property.images.length;
  property._activeImageIndex = ((property._activeImageIndex || 0) - 1 + count) % count;
};

// ─── Computed ─────────────────────────────────────────────────────────────────
const uniqueLocations = computed(() =>
  [...new Set(properties.value.map(p => p.location))].sort()
);

const activeFilterCount = computed(() =>
  filters.value.propertyTypes.length + filters.value.locations.length
);

const filteredProperties = computed(() => {
  let results = properties.value;
  if (searchQuery.value) {
    const q = searchQuery.value.toLowerCase();
    results = results.filter(p =>
      p.location.toLowerCase().includes(q) || p.title.toLowerCase().includes(q)
    );
  }
  const min = Number(filters.value.minPrice) || 0;
  const max = Number(filters.value.maxPrice) || Infinity;
  results = results.filter(p => p.price >= min && p.price <= max);
  if (filters.value.locations.length > 0)
    results = results.filter(p => filters.value.locations.includes(p.location));
  if (filters.value.propertyTypes.length > 0)
    results = results.filter(p => filters.value.propertyTypes.includes(p.property_type));
  return results;
});

// ─── Formatters ───────────────────────────────────────────────────────────────
const formatPrice = (price) => Number(parseFloat(price)).toLocaleString();

const formatPropertyType = (type) =>
  ({ apartment:'Apartment', house:'House', condo:'Condo', studio:'Studio', bedsitter:'Bedsitter' }[type] || type);

const getPropertyTypeIcon = (type) =>
  ({ apartment:'fas fa-building', house:'fas fa-home', condo:'fas fa-city',
     studio:'fas fa-door-open', bedsitter:'fas fa-bed' }[type] || 'fas fa-home');

// ─── Availability helpers ─────────────────────────────────────────────────────
const isAvailableNow = (dateStr) => {
  if (!dateStr) return false;
  try {
    const avail = new Date(dateStr);
    const today = new Date();
    const a = new Date(avail.getFullYear(), avail.getMonth(), avail.getDate());
    const t = new Date(today.getFullYear(), today.getMonth(), today.getDate());
    return a <= t;
  } catch { return false; }
};

const formatAvailability = (dateStr) => {
  if (!dateStr) return null;
  try {
    const date  = new Date(dateStr);
    const today = new Date();
    const avail = new Date(date.getFullYear(), date.getMonth(), date.getDate());
    const base  = new Date(today.getFullYear(), today.getMonth(), today.getDate());
    const diff  = Math.round((avail - base) / 86_400_000);

    if (diff <= 0)  return 'Available Now';
    if (diff === 1) return 'Available Tomorrow';
    if (diff <= 7)  return `Available in ${diff} days`;
    if (diff <= 30) return `Available in ${diff} days`;
    return 'From ' + date.toLocaleDateString('en-KE', {
      day: 'numeric', month: 'short', year: diff > 365 ? 'numeric' : undefined,
    });
  } catch { return dateStr; }
};

// ─── Notification ─────────────────────────────────────────────────────────────
const showNotification = (message) => {
  notification.value = message;
  setTimeout(() => { notification.value = null; }, 3000);
};

// ─── Routing / Save ───────────────────────────────────────────────────────────
const router = useRouter();

const viewDetails = (property) => {
  try { localStorage.setItem('selectedProperty', JSON.stringify(property)); } catch (e) {}
  router.push({ name: 'saved' });
};

const getSavedProperties = () => {
  try { return JSON.parse(localStorage.getItem('savedProperties') || '[]'); } catch { return []; }
};

const isSaved = (property) => getSavedProperties().some(p => p.id === property.id);

const toggleSave = (property) => {
  let saved = getSavedProperties();
  const index = saved.findIndex(p => p.id === property.id);
  if (index > -1) {
    saved.splice(index, 1);
    showNotification('Removed from saved properties');
  } else {
    saved.push(property);
    showNotification(`"${property.title}" saved!`);
  }
  localStorage.setItem('savedProperties', JSON.stringify(saved));
};

// ─── Filters ──────────────────────────────────────────────────────────────────
const performSearch = () => {};

const applyFilters = () => {
  showFilters.value = false;
  showNotification('Filters applied');
};

const resetFilters = () => {
  if (properties.value.length > 0) {
    const prices = properties.value.map(p => p.price);
    filters.value.minPrice = Math.floor(Math.min(...prices));
    filters.value.maxPrice = Math.ceil(Math.max(...prices));
  }
  filters.value.locations     = [];
  filters.value.propertyTypes = [];
  showNotification('Filters cleared');
};

const removeTypeFilter     = (type) => { filters.value.propertyTypes = filters.value.propertyTypes.filter(t => t !== type); };
const removeLocationFilter = (loc)  => { filters.value.locations     = filters.value.locations.filter(l => l !== loc); };
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,600;1,400&family=DM+Sans:wght@300;400;500;600&display=swap');

/* ─── Base ─────────────────────────────────── */
.properties-page {
  font-family: 'DM Sans', sans-serif;
  background: #f6f4f1;
  min-height: 100vh;
  padding: 36px 32px 60px;
  color: #1c1c1c;
}

/* ─── Header ────────────────────────────────── */
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  margin-bottom: 32px;
}
.header-label {
  font-size: 11px;
  letter-spacing: 3px;
  font-weight: 600;
  color: #b73f2a;
  margin-bottom: 6px;
  text-transform: uppercase;
}
.header-title {
  font-family: 'Cormorant Garamond', serif;
  font-size: 42px;
  font-weight: 600;
  line-height: 1.1;
  color: #111;
  margin: 0;
}
.header-title em { font-style: italic; color: #b73f2a; }

.saved-link-btn {
  display: flex; align-items: center; gap: 8px;
  padding: 10px 20px; border: 1.5px solid #1c1c1c; border-radius: 50px;
  text-decoration: none; color: #1c1c1c; font-size: 13px; font-weight: 500;
  transition: all 0.25s; white-space: nowrap;
}
.saved-link-btn:hover { background: #1c1c1c; color: #fff; }
.saved-link-btn i { color: #b73f2a; transition: color 0.25s; }
.saved-link-btn:hover i { color: #fff; }

/* ─── Search Bar ────────────────────────────── */
.search-bar {
  display: flex; align-items: center; gap: 10px;
  background: #fff; border-radius: 50px;
  padding: 8px 8px 8px 20px;
  box-shadow: 0 4px 24px rgba(0,0,0,0.08);
  max-width: 560px; margin-bottom: 16px;
}
.search-item { flex: 1; display: flex; align-items: center; gap: 10px; min-width: 0; }
.search-icon { color: #b73f2a; font-size: 14px; flex-shrink: 0; }
.search-input {
  border: none; outline: none; background: transparent;
  font-family: 'DM Sans', sans-serif; font-size: 14px; color: #1c1c1c; width: 100%;
}
.search-input::placeholder { color: #aaa; }

.search-btn, .filters-btn {
  background: #b73f2a; color: #fff; border: none; border-radius: 50px;
  width: 46px; height: 46px; cursor: pointer;
  display: flex; align-items: center; justify-content: center;
  flex-shrink: 0; transition: background 0.2s, transform 0.2s; position: relative;
}
.filters-btn { background: #1c1c1c; }
.search-btn:hover  { background: #9a3523; transform: scale(1.05); }
.filters-btn:hover { background: #333;    transform: scale(1.05); }

.filter-count {
  position: absolute; top: -4px; right: -4px;
  background: #b73f2a; color: #fff; font-size: 10px; font-weight: 700;
  width: 17px; height: 17px; border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
}

/* ─── Filter Chips ──────────────────────────── */
.filter-chips { display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 20px; }
.chip {
  background: #fff; border: 1px solid #ddd; padding: 5px 12px;
  border-radius: 20px; font-size: 12px;
  display: flex; align-items: center; gap: 6px; cursor: pointer; transition: all 0.2s;
}
.chip:hover { border-color: #b73f2a; color: #b73f2a; }
.chip i { font-size: 10px; }
.chip-clear {
  background: #b73f2a; color: #fff; border-color: #b73f2a;
  font-family: 'DM Sans', sans-serif; cursor: pointer;
}
.chip-clear:hover { background: #9a3523; }

/* ─── Filters Modal ─────────────────────────── */
.filters-overlay {
  position: fixed; inset: 0; background: rgba(0,0,0,0.4); backdrop-filter: blur(3px);
  display: flex; align-items: center; justify-content: center; z-index: 999;
}
.filters-card {
  background: #fff; border-radius: 16px;
  width: 90%; max-width: 480px; max-height: 90vh;
  display: flex; flex-direction: column; overflow: hidden;
  box-shadow: 0 20px 60px rgba(0,0,0,0.2); animation: filterSlide 0.3s ease;
}
@keyframes filterSlide {
  from { transform: translateY(30px); opacity: 0; }
  to   { transform: translateY(0);    opacity: 1; }
}
.filters-header {
  display: flex; justify-content: space-between; align-items: center;
  padding: 22px 24px; border-bottom: 1px solid #eee;
}
.filters-header h3 { font-family: 'Cormorant Garamond', serif; font-size: 22px; margin: 0; font-weight: 600; }
.close-btn {
  background: none; border: none; font-size: 18px; cursor: pointer; color: #888;
  width: 32px; height: 32px; border-radius: 50%;
  display: flex; align-items: center; justify-content: center; transition: background 0.2s;
}
.close-btn:hover { background: #f0f0f0; color: #333; }
.filters-body { padding: 24px; overflow-y: auto; flex-grow: 1; }
.filter-group { margin-bottom: 28px; }
.filter-group:last-child { margin-bottom: 0; }
.filter-label {
  font-size: 11px; letter-spacing: 2px; text-transform: uppercase;
  color: #888; font-weight: 600; display: block; margin-bottom: 14px;
}
.price-range-inputs { display: flex; align-items: center; gap: 12px; margin-bottom: 10px; }
.price-input {
  flex: 1; padding: 10px 14px; border: 1.5px solid #e0e0e0; border-radius: 8px;
  font-size: 14px; font-family: 'DM Sans', sans-serif; outline: none; transition: border-color 0.2s;
}
.price-input:focus { border-color: #b73f2a; }
.price-separator { color: #bbb; font-weight: 500; }
.price-display { font-size: 12px; color: #666; background: #f8f8f8; padding: 8px 14px; border-radius: 6px; margin-top: 4px; }
.checkbox-group { display: flex; flex-direction: column; gap: 4px; }
.checkbox-label {
  display: flex; align-items: center; gap: 12px;
  padding: 10px 12px; border-radius: 8px; cursor: pointer; transition: background 0.15s;
}
.checkbox-label:hover { background: #f5f5f5; }
.checkbox-label input[type="checkbox"] { width: 16px; height: 16px; accent-color: #b73f2a; cursor: pointer; }
.checkbox-text { display: flex; align-items: center; gap: 10px; font-size: 14px; color: #444; }
.checkbox-text i { color: #b73f2a; width: 16px; }
.filters-footer {
  display: flex; gap: 10px; padding: 20px 24px;
  border-top: 1px solid #eee; justify-content: flex-end;
}
.btn {
  padding: 11px 22px; border: none; border-radius: 8px; cursor: pointer;
  font-family: 'DM Sans', sans-serif; font-size: 14px; font-weight: 500; transition: all 0.2s;
}
.btn-primary         { background: #b73f2a; color: #fff; }
.btn-primary:hover   { background: #9a3523; }
.btn-secondary       { background: #f0f0f0; color: #333; }
.btn-secondary:hover { background: #e0e0e0; }

/* ─── Section Meta ──────────────────────────── */
.section-meta { display: flex; align-items: center; gap: 12px; margin-bottom: 20px; }
.results-count { font-size: 13px; color: #888; }
.results-count span { font-weight: 400; }
.live-badge { display: flex; align-items: center; gap: 6px; font-size: 12px; color: #b73f2a; font-weight: 500; }
.refresh-btn {
  background: none; border: 1.5px solid #ddd; border-radius: 50%;
  width: 30px; height: 30px;
  display: flex; align-items: center; justify-content: center;
  cursor: pointer; color: #aaa; font-size: 12px; transition: all 0.2s;
}
.refresh-btn:hover { border-color: #b73f2a; color: #b73f2a; transform: rotate(30deg); }

/* ─── Properties Grid ───────────────────────── */
.properties-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 28px;
}

/* ─── Property Card ─────────────────────────── */
.property-card {
  background: #fff; border-radius: 16px; overflow: hidden;
  cursor: pointer; transition: transform 0.25s, box-shadow 0.25s;
  box-shadow: 0 2px 12px rgba(0,0,0,0.06);
  display: flex; flex-direction: column;
}
.property-card:hover { transform: translateY(-6px); box-shadow: 0 16px 40px rgba(0,0,0,0.12); }

/* ─── Image Area ────────────────────────────── */
.card-image-wrap { position: relative; height: 240px; overflow: hidden; background: #e8e4df; }
.image-carousel  { width: 100%; height: 100%; position: relative; }
.card-img { width: 100%; height: 100%; object-fit: cover; display: block; transition: transform 0.4s ease; }
.property-card:hover .card-img { transform: scale(1.04); }
.image-overlay {
  position: absolute; inset: 0;
  background: linear-gradient(to top, rgba(0,0,0,0.45) 0%, transparent 50%);
  pointer-events: none;
}

.carousel-arrow {
  position: absolute; top: 50%; transform: translateY(-50%);
  background: rgba(255,255,255,0.9); border: none; border-radius: 50%;
  width: 32px; height: 32px;
  display: flex; align-items: center; justify-content: center;
  cursor: pointer; font-size: 12px; color: #1c1c1c; opacity: 0;
  transition: opacity 0.2s; z-index: 5;
}
.card-image-wrap:hover .carousel-arrow { opacity: 1; }
.carousel-arrow.left  { left: 10px; }
.carousel-arrow.right { right: 10px; }
.carousel-arrow:hover { background: #fff; transform: translateY(-50%) scale(1.1); }

.carousel-dots {
  position: absolute; bottom: 10px; left: 50%; transform: translateX(-50%);
  display: flex; gap: 5px; z-index: 5;
}
.dot { width: 6px; height: 6px; border-radius: 50%; background: rgba(255,255,255,0.5); cursor: pointer; transition: background 0.2s, transform 0.2s; }
.dot.active { background: #fff; transform: scale(1.3); }

.type-badge {
  position: absolute; top: 14px; left: 14px;
  background: rgba(183,63,42,0.92); color: #fff;
  padding: 5px 12px; border-radius: 20px;
  font-size: 11px; font-weight: 600; letter-spacing: 0.5px; text-transform: uppercase; z-index: 3;
}

/* Availability Badge */
.availability-badge {
  position: absolute; bottom: 14px; right: 14px;
  display: flex; align-items: center; gap: 6px;
  padding: 6px 12px; border-radius: 20px;
  font-size: 11.5px; font-weight: 600; letter-spacing: 0.2px; z-index: 4;
  backdrop-filter: blur(8px); -webkit-backdrop-filter: blur(8px);
  background: rgba(255,255,255,0.18); border: 1px solid rgba(255,255,255,0.35);
  color: #fff; text-shadow: 0 1px 3px rgba(0,0,0,0.4);
  box-shadow: 0 2px 12px rgba(0,0,0,0.2); transition: background 0.2s;
}
.availability-badge.now {
  background: rgba(34,197,94,0.28);
  border-color: rgba(34,197,94,0.5);
}
.availability-badge i { font-size: 11px; opacity: 0.9; }

.image-count-badge {
  position: absolute; bottom: 14px; left: 14px;
  background: rgba(0,0,0,0.55); color: #fff;
  padding: 4px 10px; border-radius: 20px;
  font-size: 11px; font-weight: 500;
  display: flex; align-items: center; gap: 5px; z-index: 3;
}

.save-btn {
  position: absolute; top: 14px; right: 14px;
  background: rgba(255,255,255,0.92); border: none; border-radius: 50%;
  width: 38px; height: 38px;
  display: flex; align-items: center; justify-content: center;
  cursor: pointer; transition: all 0.2s; z-index: 3; font-size: 15px; color: #555;
}
.save-btn:hover { background: #fff; transform: scale(1.1); }
.save-btn .saved { color: #e53e3e; }

/* ─── Card Body ─────────────────────────────── */
.card-body { padding: 18px 20px 20px; display: flex; flex-direction: column; gap: 12px; flex-grow: 1; }

.property-title {
  font-family: 'Cormorant Garamond', serif;
  font-size: 19px; font-weight: 600; color: #111; margin: 0 0 4px; line-height: 1.3;
}
.property-desc {
  font-size: 13px; color: #777; margin: 0;
  display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical;
  overflow: hidden; line-height: 1.5;
}

/* Amenities Row */
.amenities-row { display: flex; flex-wrap: wrap; gap: 6px; }

.amenity-chip {
  display: inline-flex; align-items: center; gap: 5px;
  padding: 4px 10px; border-radius: 20px;
  background: #f4f0eb; border: 1px solid #e8e2d9;
  font-size: 11.5px; color: #555; font-weight: 500; letter-spacing: 0.1px;
  transition: background 0.18s, border-color 0.18s, color 0.18s;
  white-space: nowrap; cursor: default;
}
.amenity-chip i { font-size: 10px; color: #b73f2a; flex-shrink: 0; }
.amenity-chip:hover { background: #fdf0ed; border-color: #d4836e; color: #b73f2a; }
.amenity-chip:hover i { color: #b73f2a; }

.amenity-more {
  background: #1c1c1c; border-color: #1c1c1c; color: #fff;
  font-weight: 600; font-size: 11px;
}
.amenity-more:hover { background: #333; border-color: #333; color: #fff; }

/* ─── Card Meta ─────────────────────────────── */
.card-meta { display: flex; gap: 14px; flex-wrap: wrap; }
.meta-item { display: flex; align-items: center; gap: 5px; font-size: 12.5px; color: #888; }
.meta-item i { color: #b73f2a; font-size: 11px; }
.agent-meta { font-weight: 500; color: #555; }
.agent-meta i { color: #b73f2a; }

/* ─── Card Footer ───────────────────────────── */
.card-footer-row {
  display: flex; justify-content: space-between; align-items: center;
  padding-top: 12px; border-top: 1px solid #f0f0f0; margin-top: auto;
}
.price-block { display: flex; align-items: baseline; gap: 3px; }
.price-amount { font-family: 'Cormorant Garamond', serif; font-size: 22px; font-weight: 600; color: #b73f2a; }
.price-period { font-size: 12px; color: #aaa; font-weight: 400; }

.view-btn {
  background: #1c1c1c; color: #fff; border: none;
  padding: 8px 16px; border-radius: 8px;
  font-family: 'DM Sans', sans-serif; font-size: 12.5px; font-weight: 500;
  cursor: pointer; display: flex; align-items: center; gap: 8px; transition: all 0.2s;
}
.view-btn i { font-size: 11px; transition: transform 0.2s; }
.view-btn:hover { background: #b73f2a; }
.view-btn:hover i { transform: translateX(3px); }

/* ─── Skeleton Loading ──────────────────────── */
.skeleton-card { background: #fff; border-radius: 16px; overflow: hidden; box-shadow: 0 2px 12px rgba(0,0,0,0.06); }
.skeleton-img {
  height: 240px;
  background: linear-gradient(90deg, #ececec 25%, #f5f5f5 50%, #ececec 75%);
  background-size: 200% 100%; animation: shimmer 1.4s infinite;
}
.skeleton-body { padding: 18px 20px 20px; display: flex; flex-direction: column; gap: 10px; }
.skeleton-line {
  height: 12px; border-radius: 6px;
  background: linear-gradient(90deg, #ececec 25%, #f5f5f5 50%, #ececec 75%);
  background-size: 200% 100%; animation: shimmer 1.4s infinite;
}
.skeleton-line.short  { width: 40%; }
.skeleton-line.long   { width: 85%; }
.skeleton-line.medium { width: 60%; }
.skeleton-line.price  { width: 50%; height: 18px; margin-top: 6px; }
@keyframes shimmer { 0% { background-position: 200% 0; } 100% { background-position: -200% 0; } }

/* ─── State Boxes ───────────────────────────── */
.state-box { text-align: center; padding: 80px 24px; border-radius: 16px; }
.state-box i { font-size: 48px; display: block; margin-bottom: 16px; opacity: 0.35; }
.state-box p { font-size: 15px; color: #888; margin-bottom: 20px; }
.error-state { background: #fff5f5; }
.error-state i { color: #b73f2a; }
.empty-state  { background: #f9f9f9; }
.empty-state  i { color: #aaa; }

/* ─── Notification Toast ────────────────────── */
.notification-toast {
  position: fixed; top: 24px; right: 24px;
  background: #1c1c1c; color: #fff;
  padding: 14px 20px; border-radius: 10px;
  box-shadow: 0 8px 24px rgba(0,0,0,0.2);
  display: flex; align-items: center; gap: 10px;
  font-size: 14px; z-index: 9999; max-width: 320px;
}
.notification-toast i { color: #4caf50; font-size: 16px; }

.toast-enter-active,   .toast-leave-active   { transition: all 0.3s ease; }
.toast-enter-from,     .toast-leave-to       { opacity: 0; transform: translateX(30px); }
.overlay-enter-active, .overlay-leave-active { transition: opacity 0.3s; }
.overlay-enter-from,   .overlay-leave-to     { opacity: 0; }

/* ─── Responsive ────────────────────────────── */
@media (max-width: 768px) {
  .properties-page { padding: 24px 16px 48px; }
  .header-title    { font-size: 30px; }
  .page-header     { flex-direction: column; align-items: flex-start; gap: 16px; }
  .properties-grid { grid-template-columns: 1fr; }
  .search-bar      { max-width: 100%; }
  .card-image-wrap { height: 200px; }
  .amenity-label   { display: none; }
  .amenity-chip    { padding: 5px 8px; }
}
</style>