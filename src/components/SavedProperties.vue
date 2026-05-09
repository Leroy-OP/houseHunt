<template>
  <div class="saved-page">

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
        <p class="header-label">MY COLLECTION</p>
        <h1 class="header-title">Saved <em>Properties</em></h1>
      </div>
      <router-link to="/properties" class="back-link-btn">
        <i class="fas fa-arrow-left"></i>
        <span>Browse All</span>
      </router-link>
    </div>

    <!-- Empty State -->
    <div v-if="savedProperties.length === 0" class="state-box empty-state">
      <i class="fas fa-heart"></i>
      <p>You haven't saved any properties yet.</p>
      <router-link to="/properties" class="btn btn-primary">Browse Properties</router-link>
    </div>

    <!-- Properties Grid -->
    <div v-else>
      <div class="section-meta">
        <span class="results-count">
          {{ savedProperties.length }}
          <span>saved propert{{ savedProperties.length === 1 ? 'y' : 'ies' }}</span>
        </span>
      </div>

      <div class="properties-grid">
        <div
          v-for="property in savedProperties"
          :key="property.id"
          class="property-card"
          @click="openDetail(property)"
        >
          <!-- Image Area -->
          <div class="card-image-wrap">
            <!-- Multi-image carousel -->
            <div v-if="normalizeImages(property).length > 1" class="image-carousel">
              <img
                :src="getImageAtIndex(property, property._activeIdx || 0)"
                :alt="property.title"
                class="card-img"
                @error="onImageError($event)"
              />
              <div class="carousel-dots">
                <span
                  v-for="(img, idx) in normalizeImages(property)"
                  :key="idx"
                  class="dot"
                  :class="{ active: (property._activeIdx || 0) === idx }"
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
              :src="getPrimaryImage(property)"
              :alt="property.title"
              class="card-img"
              @error="onImageError($event)"
            />

            <div class="type-badge">{{ formatPropertyType(property.property_type) }}</div>

            <div class="image-count-badge" v-if="normalizeImages(property).length > 1">
              <i class="fas fa-images"></i> {{ normalizeImages(property).length }}
            </div>

            <button class="unsave-btn" @click.stop="toggleSave(property)" title="Remove from saved">
              <i class="fas fa-heart saved"></i>
            </button>

            <div class="image-overlay"></div>
          </div>

          <!-- Card Body -->
          <div class="card-body">
            <div class="card-top">
              <h5 class="property-title">{{ property.title }}</h5>
              <p class="property-desc">{{ property.description || 'No description available.' }}</p>
            </div>

            <div class="card-meta">
              <span class="meta-item">
                <i class="fas fa-map-marker-alt"></i>
                {{ property.location }}
              </span>
              <span class="meta-item" v-if="property.agency && property.agency.name">
                <i class="fas fa-building"></i>
                {{ property.agency.name }}
              </span>
              <span class="meta-item" v-if="property.vacantDate">
                <i class="fas fa-calendar-alt"></i>
                Available {{ formatDate(property.vacantDate) }}
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

    <!-- ── Detail Panel ───────────────────────────────────────────── -->
    <transition name="panel">
      <div v-if="selectedProperty" class="detail-overlay" @click.self="closeDetail">
        <div class="detail-card">

          <button class="detail-close" @click="closeDetail">
            <i class="fas fa-times"></i>
          </button>

          <div class="detail-grid">
            <!-- Left: Images -->
            <div class="detail-images">
              <div class="main-image-wrap">
                <img
                  :src="currentImageSrc"
                  class="main-image"
                  alt="Property"
                  @error="onImageError($event)"
                />
                <!-- Arrow nav on detail image -->
                <button
                  v-if="detailImages.length > 1"
                  class="carousel-arrow left"
                  @click="currentImageIndex = (currentImageIndex - 1 + detailImages.length) % detailImages.length"
                >
                  <i class="fas fa-chevron-left"></i>
                </button>
                <button
                  v-if="detailImages.length > 1"
                  class="carousel-arrow right"
                  @click="currentImageIndex = (currentImageIndex + 1) % detailImages.length"
                >
                  <i class="fas fa-chevron-right"></i>
                </button>
              </div>
              <div class="thumbs" v-if="detailImages.length > 1">
                <img
                  v-for="(img, idx) in detailImages"
                  :key="idx"
                  :src="img"
                  :class="['thumb', { active: idx === currentImageIndex }]"
                  @click="currentImageIndex = idx"
                  @error="onImageError($event)"
                  :alt="`View ${idx + 1}`"
                />
              </div>
            </div>

            <!-- Right: Info -->
            <div class="detail-info">
              <span class="detail-type-badge">{{ formatPropertyType(selectedProperty.property_type) }}</span>
              <h2 class="detail-title">{{ selectedProperty.title }}</h2>

              <p class="detail-location">
                <i class="fas fa-map-marker-alt"></i>
                {{ selectedProperty.location }}
              </p>

              <p class="detail-description">
                {{ selectedProperty.description || 'No description available.' }}
              </p>

              <div class="detail-stats">
                <div class="stat">
                  <span class="stat-label">Monthly Rent</span>
                  <span class="stat-value price">KES {{ formatPrice(selectedProperty.price) }}</span>
                </div>
                <div class="stat" v-if="selectedProperty.vacantDate">
                  <span class="stat-label">Available From</span>
                  <span class="stat-value">{{ formatDate(selectedProperty.vacantDate) }}</span>
                </div>
              </div>

              <!-- Agency info -->
              <div class="agency-block" v-if="selectedProperty.agency">
                <p class="agency-label">LISTED BY</p>
                <p class="agency-name">{{ selectedProperty.agency.name }}</p>
                <div class="agency-contacts">
                  <a v-if="selectedProperty.agency.phone" :href="`tel:${selectedProperty.agency.phone}`" class="contact-chip">
                    <i class="fas fa-phone"></i> {{ selectedProperty.agency.phone }}
                  </a>
                  <a v-if="selectedProperty.agency.email" :href="mailtoLink" class="contact-chip">
                    <i class="fas fa-envelope"></i> {{ selectedProperty.agency.email }}
                  </a>
                </div>
              </div>

              <div class="detail-actions">
                <button class="btn btn-primary" @click="openBookingModal">
                  <i class="fas fa-calendar-check"></i> Book a Viewing
                </button>
                <button class="btn btn-outline" @click="messageAgent">
                  <i class="fas fa-envelope"></i> Message Agent
                </button>
              </div>

              <!-- Map -->
              <div class="map-wrap" v-if="selectedProperty.coords">
                <p class="map-label">LOCATION</p>
                <iframe
                  :src="mapSrc"
                  frameborder="0"
                  style="border:0; width:100%; height:200px; border-radius:10px;"
                  allowfullscreen
                  loading="lazy"
                ></iframe>
              </div>
            </div>
          </div>
        </div>
      </div>
    </transition>

    <!-- ── Booking Modal ───────────────────────────────────────────── -->
    <transition name="panel">
      <div v-if="showBookingModal" class="detail-overlay" @click.self="closeBookingModal">
        <div class="modal-card">
          <button class="detail-close" @click="closeBookingModal">
            <i class="fas fa-times"></i>
          </button>
          <p class="modal-eyebrow">SCHEDULE A VISIT</p>
          <h3 class="modal-title">Choose Date & Time</h3>
          <p class="modal-property-name">{{ selectedProperty?.title }}</p>

          <div class="modal-fields">
            <div class="field-group">
              <label class="field-label">Date</label>
              <input type="date" v-model="bookingDate" class="field-input" />
            </div>
            <div class="field-group">
              <label class="field-label">Time</label>
              <input type="time" v-model="bookingTime" class="field-input" />
            </div>
          </div>

          <div class="modal-footer">
            <button class="btn btn-outline" @click="closeBookingModal">Cancel</button>
            <button class="btn btn-primary" @click="proceedToConfirm">Continue</button>
          </div>
        </div>
      </div>
    </transition>

    <!-- ── Confirm Modal ───────────────────────────────────────────── -->
    <transition name="panel">
      <div v-if="showConfirmModal" class="detail-overlay" @click.self="closeConfirmModal">
        <div class="modal-card">
          <button class="detail-close" @click="closeConfirmModal">
            <i class="fas fa-times"></i>
          </button>
          <p class="modal-eyebrow">ALMOST THERE</p>
          <h3 class="modal-title">Confirm Booking</h3>

          <div class="confirm-summary">
            <div class="summary-row">
              <span class="summary-label">Property</span>
              <span class="summary-value">{{ selectedProperty?.title }}</span>
            </div>
            <div class="summary-row">
              <span class="summary-label">Date & Time</span>
              <span class="summary-value">{{ bookingDate }} at {{ bookingTime }}</span>
            </div>
            <div class="summary-row" v-if="selectedProperty?.agency">
              <span class="summary-label">Agent</span>
              <span class="summary-value">{{ selectedProperty.agency.name }} — {{ selectedProperty.agency.phone }}</span>
            </div>
          </div>

          <div class="modal-fields" style="margin-top:16px;">
            <div class="field-group">
              <label class="field-label">Full Name</label>
              <input placeholder="Your full name" v-model="customerName" class="field-input" />
            </div>
            <div class="field-group">
              <label class="field-label">Phone Number</label>
              <input placeholder="+254 7XX XXX XXX" v-model="customerPhone" class="field-input" />
            </div>
          </div>

          <div class="modal-footer">
            <button class="btn btn-outline" @click="closeConfirmModal">Back</button>
            <button class="btn btn-primary" @click="confirmBooking">
              <i class="fas fa-check"></i> Confirm Booking
            </button>
          </div>
        </div>
      </div>
    </transition>

  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue';

// ─── Storage helpers ──────────────────────────────────────────────────────────
const getSavedProperties = () => {
  try { return JSON.parse(localStorage.getItem('savedProperties') || '[]'); } catch { return []; }
};
const saveToLocalStorage = (props) => {
  localStorage.setItem('savedProperties', JSON.stringify(props));
};
const getBookings = () => {
  try { return JSON.parse(localStorage.getItem('bookings') || '[]'); } catch { return []; }
};

// ─── State ────────────────────────────────────────────────────────────────────
const savedProperties  = ref(getSavedProperties());
const selectedProperty = ref(null);
const currentImageIndex = ref(0);
const notification = ref(null);

const showBookingModal = ref(false);
const showConfirmModal = ref(false);
const bookingDate   = ref('');
const bookingTime   = ref('');
const customerName  = ref('');
const customerPhone = ref('');

// ─── Image normalisation (same logic as properties page) ─────────────────────
const normalizeImages = (property) => {
  const raw = property.images;
  if (!raw || !Array.isArray(raw) || raw.length === 0) {
    return property.img ? [property.img] : [];
  }
  return raw
    .map(img => {
      if (typeof img === 'string') return img;
      if (img && img.image_url) return img.image_url;
      if (img && img.url) return img.url;
      return null;
    })
    .filter(Boolean);
};

const PLACEHOLDER = 'https://placehold.co/600x400/1a1a2e/ffffff?text=No+Image';

const getPrimaryImage = (property) => {
  const imgs = normalizeImages(property);
  return imgs.length > 0 ? imgs[0] : PLACEHOLDER;
};

const getImageAtIndex = (property, index) => {
  const imgs = normalizeImages(property);
  return imgs[index] || PLACEHOLDER;
};

const onImageError = (e) => { e.target.src = PLACEHOLDER; };

// ─── Card carousel controls ───────────────────────────────────────────────────
const setActiveImage = (property, index) => { property._activeIdx = index; };
const nextImage = (property) => {
  const count = normalizeImages(property).length;
  property._activeIdx = ((property._activeIdx || 0) + 1) % count;
};
const prevImage = (property) => {
  const count = normalizeImages(property).length;
  property._activeIdx = ((property._activeIdx || 0) - 1 + count) % count;
};

// ─── Detail panel ─────────────────────────────────────────────────────────────
const detailImages = computed(() =>
  selectedProperty.value ? normalizeImages(selectedProperty.value) : []
);

const currentImageSrc = computed(() =>
  detailImages.value[currentImageIndex.value] || PLACEHOLDER
);

const openDetail = (property) => {
  selectedProperty.value = property;
  currentImageIndex.value = 0;
  try { localStorage.setItem('selectedProperty', JSON.stringify(property)); } catch (e) {}
};

const closeDetail = () => {
  selectedProperty.value = null;
  try { localStorage.removeItem('selectedProperty'); } catch (e) {}
};

// ─── Computed links ───────────────────────────────────────────────────────────
const mailtoLink = computed(() => {
  if (!selectedProperty.value?.agency?.email) return '#';
  return `mailto:${selectedProperty.value.agency.email}?subject=Inquiry about ${encodeURIComponent(selectedProperty.value.title)}`;
});

const mapSrc = computed(() => {
  if (!selectedProperty.value?.coords) return '';
  const { lat, lng } = selectedProperty.value.coords;
  return `https://www.google.com/maps?q=${lat},${lng}&z=15&output=embed`;
});

// ─── Save toggle ──────────────────────────────────────────────────────────────
const showNotification = (msg) => {
  notification.value = msg;
  setTimeout(() => { notification.value = null; }, 3000);
};

const toggleSave = (property) => {
  const index = savedProperties.value.findIndex(p => p.id === property.id);
  if (index > -1) {
    savedProperties.value.splice(index, 1);
    showNotification('Property removed from saved');
    if (selectedProperty.value?.id === property.id) closeDetail();
  } else {
    savedProperties.value.push(property);
    showNotification(`"${property.title}" saved!`);
  }
  saveToLocalStorage(savedProperties.value);
};

// ─── Booking flow ─────────────────────────────────────────────────────────────
const openBookingModal = () => {
  if (!selectedProperty.value) { alert('Select a property first.'); return; }
  bookingDate.value = '';
  bookingTime.value = '';
  showBookingModal.value = true;
};

const closeBookingModal = () => { showBookingModal.value = false; };

const proceedToConfirm = () => {
  if (!bookingDate.value || !bookingTime.value) {
    alert('Please select a date and time.'); return;
  }
  customerName.value = '';
  customerPhone.value = '';
  showBookingModal.value = false;
  showConfirmModal.value = true;
};

const closeConfirmModal = () => { showConfirmModal.value = false; };

const confirmBooking = () => {
  if (!customerName.value || !customerPhone.value) {
    alert('Please provide your name and phone number.'); return;
  }
  const booking = {
    id: Date.now(),
    propertyId: selectedProperty.value.id,
    propertyTitle: selectedProperty.value.title,
    agent: selectedProperty.value.agency || null,
    date: bookingDate.value,
    time: bookingTime.value,
    customer: { name: customerName.value, phone: customerPhone.value }
  };
  const list = getBookings();
  list.push(booking);
  try { localStorage.setItem('bookings', JSON.stringify(list)); } catch (e) {}
  showConfirmModal.value = false;
  showNotification('Booking confirmed! We\'ll be in touch soon.');
};

const messageAgent = () => {
  if (!selectedProperty.value) return;
  const email = selectedProperty.value.agency?.email;
  if (email) {
    window.location.href = `mailto:${email}?subject=Viewing request for ${encodeURIComponent(selectedProperty.value.title)}`;
  } else {
    alert('No agent contact available.');
  }
};

// ─── Formatters ───────────────────────────────────────────────────────────────
const formatPrice = (price) => Number(parseFloat(price)).toLocaleString();
const formatPropertyType = (type) =>
  ({ apartment: 'Apartment', house: 'House', condo: 'Condo' }[type] || type || 'Property');
const formatDate = (dateStr) => {
  try { return new Date(dateStr).toLocaleDateString('en-KE', { day: 'numeric', month: 'long', year: 'numeric' }); }
  catch { return dateStr; }
};

// ─── Watchers / mount ─────────────────────────────────────────────────────────
watch(savedProperties, (val) => { saveToLocalStorage(val); }, { deep: true });

onMounted(() => {
  try {
    const sel = localStorage.getItem('selectedProperty');
    if (sel) { selectedProperty.value = JSON.parse(sel); currentImageIndex.value = 0; }
  } catch (e) {}
});
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,600;1,400&family=DM+Sans:wght@300;400;500;600&display=swap');

/* ─── Base ─────────────────────────────────── */
.saved-page {
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

.back-link-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  border: 1.5px solid #1c1c1c;
  border-radius: 50px;
  text-decoration: none;
  color: #1c1c1c;
  font-size: 13px;
  font-weight: 500;
  transition: all 0.25s;
  white-space: nowrap;
}

.back-link-btn:hover { background: #1c1c1c; color: #fff; }

/* ─── Section Meta ──────────────────────────── */
.section-meta { margin-bottom: 20px; }
.results-count { font-size: 13px; color: #888; }
.results-count span { font-weight: 400; }

/* ─── State boxes ───────────────────────────── */
.state-box {
  text-align: center;
  padding: 80px 24px;
  border-radius: 16px;
}

.empty-state { background: #f9f9f9; }
.empty-state i { font-size: 52px; color: #ddd; display: block; margin-bottom: 16px; }
.empty-state p { font-size: 15px; color: #888; margin-bottom: 20px; }

/* ─── Properties Grid ───────────────────────── */
.properties-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 28px;
}

/* ─── Property Card ─────────────────────────── */
.property-card {
  background: #fff;
  border-radius: 16px;
  overflow: hidden;
  cursor: pointer;
  transition: transform 0.25s, box-shadow 0.25s;
  box-shadow: 0 2px 12px rgba(0,0,0,0.06);
  display: flex;
  flex-direction: column;
}

.property-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 16px 40px rgba(0,0,0,0.12);
}

/* ─── Image Area ────────────────────────────── */
.card-image-wrap {
  position: relative;
  height: 240px;
  overflow: hidden;
  background: #e8e4df;
}

.image-carousel { width: 100%; height: 100%; position: relative; }

.card-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
  transition: transform 0.4s ease;
}

.property-card:hover .card-img { transform: scale(1.04); }

.image-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(to top, rgba(0,0,0,0.45) 0%, transparent 50%);
  pointer-events: none;
}

/* Carousel arrows */
.carousel-arrow {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  background: rgba(255,255,255,0.9);
  border: none;
  border-radius: 50%;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  font-size: 12px;
  color: #1c1c1c;
  opacity: 0;
  transition: opacity 0.2s;
  z-index: 5;
}

.card-image-wrap:hover .carousel-arrow,
.main-image-wrap:hover .carousel-arrow { opacity: 1; }
.carousel-arrow.left  { left: 10px; }
.carousel-arrow.right { right: 10px; }
.carousel-arrow:hover { background: #fff; transform: translateY(-50%) scale(1.1); }

.carousel-dots {
  position: absolute;
  bottom: 10px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  gap: 5px;
  z-index: 5;
}

.dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: rgba(255,255,255,0.5);
  cursor: pointer;
  transition: background 0.2s, transform 0.2s;
}

.dot.active { background: #fff; transform: scale(1.3); }

.type-badge {
  position: absolute;
  top: 14px;
  left: 14px;
  background: rgba(183,63,42,0.92);
  color: #fff;
  padding: 5px 12px;
  border-radius: 20px;
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 0.5px;
  text-transform: uppercase;
  z-index: 3;
}

.image-count-badge {
  position: absolute;
  bottom: 14px;
  left: 14px;
  background: rgba(0,0,0,0.55);
  color: #fff;
  padding: 4px 10px;
  border-radius: 20px;
  font-size: 11px;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 5px;
  z-index: 3;
}

.unsave-btn {
  position: absolute;
  top: 14px;
  right: 14px;
  background: rgba(255,255,255,0.92);
  border: none;
  border-radius: 50%;
  width: 38px;
  height: 38px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s;
  z-index: 3;
  font-size: 15px;
}

.unsave-btn:hover { background: #fff; transform: scale(1.1); }
.unsave-btn .saved { color: #e53e3e; }

/* ─── Card Body ─────────────────────────────── */
.card-body {
  padding: 18px 20px 20px;
  display: flex;
  flex-direction: column;
  gap: 12px;
  flex-grow: 1;
}

.property-title {
  font-family: 'Cormorant Garamond', serif;
  font-size: 19px;
  font-weight: 600;
  color: #111;
  margin: 0 0 4px;
  line-height: 1.3;
}

.property-desc {
  font-size: 13px;
  color: #777;
  margin: 0;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  line-height: 1.5;
}

.card-meta { display: flex; gap: 12px; flex-wrap: wrap; }

.meta-item {
  display: flex;
  align-items: center;
  gap: 5px;
  font-size: 12.5px;
  color: #888;
}

.meta-item i { color: #b73f2a; font-size: 11px; }

.card-footer-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 12px;
  border-top: 1px solid #f0f0f0;
  margin-top: auto;
}

.price-block { display: flex; align-items: baseline; gap: 3px; }

.price-amount {
  font-family: 'Cormorant Garamond', serif;
  font-size: 22px;
  font-weight: 600;
  color: #b73f2a;
}

.price-period { font-size: 12px; color: #aaa; }

.view-btn {
  background: #1c1c1c;
  color: #fff;
  border: none;
  padding: 8px 16px;
  border-radius: 8px;
  font-family: 'DM Sans', sans-serif;
  font-size: 12.5px;
  font-weight: 500;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.2s;
}

.view-btn i { font-size: 11px; transition: transform 0.2s; }
.view-btn:hover { background: #b73f2a; }
.view-btn:hover i { transform: translateX(3px); }

/* ─── Detail / Modal Overlay ────────────────── */
.detail-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.5);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1050;
  padding: 20px;
}

/* ─── Detail Card ───────────────────────────── */
.detail-card {
  background: #fff;
  width: 95%;
  max-width: 960px;
  max-height: 92vh;
  border-radius: 20px;
  overflow-y: auto;
  position: relative;
  box-shadow: 0 24px 80px rgba(0,0,0,0.25);
  animation: panelIn 0.3s ease;
}

@keyframes panelIn {
  from { transform: translateY(40px); opacity: 0; }
  to   { transform: translateY(0);    opacity: 1; }
}

.detail-close {
  position: absolute;
  top: 18px;
  right: 18px;
  background: #f0efed;
  border: none;
  border-radius: 50%;
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  font-size: 15px;
  color: #555;
  z-index: 10;
  transition: background 0.2s;
}

.detail-close:hover { background: #e0dedd; color: #111; }

.detail-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0;
}

/* ─── Detail Images ─────────────────────────── */
.detail-images {
  padding: 0;
  background: #111;
}

.main-image-wrap {
  position: relative;
  height: 380px;
  overflow: hidden;
}

.main-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.thumbs {
  display: flex;
  gap: 4px;
  padding: 8px;
  background: #0a0a0a;
  flex-wrap: wrap;
}

.thumb {
  width: 72px;
  height: 52px;
  object-fit: cover;
  border-radius: 5px;
  cursor: pointer;
  opacity: 0.6;
  transition: opacity 0.2s, outline 0.2s;
  border: 2px solid transparent;
}

.thumb.active { opacity: 1; border-color: #b73f2a; }
.thumb:hover  { opacity: 0.9; }

/* ─── Detail Info ───────────────────────────── */
.detail-info {
  padding: 36px 32px;
  overflow-y: auto;
  max-height: 92vh;
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.detail-type-badge {
  display: inline-block;
  background: rgba(183,63,42,0.1);
  color: #b73f2a;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 1px;
  text-transform: uppercase;
}

.detail-title {
  font-family: 'Cormorant Garamond', serif;
  font-size: 30px;
  font-weight: 600;
  color: #111;
  margin: 0;
  line-height: 1.2;
}

.detail-location {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 14px;
  color: #888;
  margin: 0;
}

.detail-location i { color: #b73f2a; }

.detail-description {
  font-size: 14px;
  color: #555;
  line-height: 1.7;
  margin: 0;
}

/* Stats row */
.detail-stats {
  display: flex;
  gap: 24px;
  padding: 16px 0;
  border-top: 1px solid #f0f0f0;
  border-bottom: 1px solid #f0f0f0;
  flex-wrap: wrap;
}

.stat { display: flex; flex-direction: column; gap: 4px; }
.stat-label { font-size: 10px; letter-spacing: 2px; text-transform: uppercase; color: #aaa; font-weight: 600; }
.stat-value { font-size: 15px; color: #1c1c1c; font-weight: 500; }
.stat-value.price { font-family: 'Cormorant Garamond', serif; font-size: 22px; color: #b73f2a; }

/* Agency block */
.agency-block {
  background: #f9f8f6;
  border-radius: 10px;
  padding: 14px 16px;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.agency-label { font-size: 10px; letter-spacing: 2px; color: #aaa; font-weight: 600; text-transform: uppercase; margin: 0; }
.agency-name  { font-size: 15px; font-weight: 600; color: #111; margin: 0; }

.agency-contacts { display: flex; gap: 8px; flex-wrap: wrap; }

.contact-chip {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 6px 12px;
  background: #fff;
  border: 1px solid #e5e5e5;
  border-radius: 20px;
  font-size: 12px;
  color: #444;
  text-decoration: none;
  transition: all 0.2s;
}

.contact-chip:hover { border-color: #b73f2a; color: #b73f2a; }
.contact-chip i { font-size: 11px; color: #b73f2a; }

/* Action buttons */
.detail-actions { display: flex; gap: 10px; flex-wrap: wrap; }

.map-label { font-size: 10px; letter-spacing: 2px; text-transform: uppercase; color: #aaa; font-weight: 600; margin: 0 0 8px; }

.map-wrap iframe { border-radius: 10px; }

/* ─── Modal Card ────────────────────────────── */
.modal-card {
  background: #fff;
  width: 95%;
  max-width: 480px;
  border-radius: 20px;
  padding: 36px;
  position: relative;
  box-shadow: 0 24px 80px rgba(0,0,0,0.25);
  animation: panelIn 0.3s ease;
}

.modal-eyebrow { font-size: 10px; letter-spacing: 2.5px; text-transform: uppercase; color: #b73f2a; font-weight: 600; margin: 0 0 6px; }
.modal-title { font-family: 'Cormorant Garamond', serif; font-size: 26px; font-weight: 600; margin: 0 0 4px; }
.modal-property-name { font-size: 13px; color: #888; margin: 0 0 20px; }

.modal-fields { display: flex; flex-direction: column; gap: 14px; }

.field-group { display: flex; flex-direction: column; gap: 6px; }
.field-label { font-size: 11px; letter-spacing: 1.5px; text-transform: uppercase; color: #888; font-weight: 600; }

.field-input {
  padding: 11px 14px;
  border: 1.5px solid #e0e0e0;
  border-radius: 8px;
  font-size: 14px;
  font-family: 'DM Sans', sans-serif;
  outline: none;
  transition: border-color 0.2s;
  color: #e0e0e0;
}

.field-input:focus { border-color: #b73f2a; }

/* Confirm summary */
.confirm-summary {
  background: #f9f8f6;
  border-radius: 10px;
  padding: 14px 16px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.summary-row { display: flex; justify-content: space-between; gap: 12px; }
.summary-label { font-size: 12px; color: #aaa; font-weight: 600; flex-shrink: 0; }
.summary-value { font-size: 13px; color: #333; text-align: right; }

.modal-footer { display: flex; justify-content: flex-end; gap: 10px; margin-top: 24px; }

/* ─── Shared Buttons ────────────────────────── */
.btn {
  padding: 11px 22px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-family: 'DM Sans', sans-serif;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.2s;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  text-decoration: none;
}

.btn-primary { background: #b73f2a; color: #fff; }
.btn-primary:hover { background: #9a3523; }

.btn-outline {
  background: transparent;
  color: #1c1c1c;
  border: 1.5px solid #ddd;
}

.btn-outline:hover { border-color: #1c1c1c; }

/* ─── Notification Toast ────────────────────── */
.notification-toast {
  position: fixed;
  top: 24px;
  right: 24px;
  background: #1c1c1c;
  color: #fff;
  padding: 14px 20px;
  border-radius: 10px;
  box-shadow: 0 8px 24px rgba(0,0,0,0.2);
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 14px;
  z-index: 9999;
  max-width: 320px;
}

.notification-toast i { color: #4caf50; font-size: 16px; }

.toast-enter-active,  .toast-leave-active  { transition: all 0.3s ease; }
.toast-enter-from,    .toast-leave-to      { opacity: 0; transform: translateX(30px); }
.panel-enter-active,  .panel-leave-active  { transition: opacity 0.3s ease; }
.panel-enter-from,    .panel-leave-to      { opacity: 0; }

@media (max-width: 768px) {
  .saved-page    { padding: 24px 16px 48px; }
  .header-title  { font-size: 30px; }
  .page-header   { flex-direction: column; align-items: flex-start; gap: 16px; }
  .properties-grid { grid-template-columns: 1fr; }
  .detail-grid   { grid-template-columns: 1fr; }
  .main-image-wrap { height: 240px; }
  .detail-info   { padding: 24px 20px; max-height: none; }
  .modal-card    { padding: 24px 20px; }
  .card-image-wrap { height: 200px; }
}
</style>