<template>
  <div class="agent-page">

    <!-- ── Notification Toast ── -->
    <transition name="toast">
      <div v-if="notification" class="notification-toast" :class="notification.type">
        <i :class="notification.type === 'success' ? 'fas fa-check-circle' : 'fas fa-exclamation-circle'"></i>
        <span>{{ notification.message }}</span>
      </div>
    </transition>

    <!-- ── Page Header ── -->
    <div class="page-header">
      <div>
        <p class="page-eyebrow">AGENT DASHBOARD</p>
        <h1 class="page-title">My <em>Listings</em></h1>
        <p class="page-sub">Manage your properties and reach thousands of potential tenants.</p>
      </div>
      <button class="add-btn" @click="openForm()">
        <i class="fas fa-plus"></i> Add Property
      </button>
    </div>

    <!-- ── Stats Strip ── -->
    <div class="stats-strip">
      <div class="stat-card">
        <span class="stat-icon"><i class="fas fa-building"></i></span>
        <div>
          <p class="stat-num">{{ myProperties.length }}</p>
          <p class="stat-label">Total Listings</p>
        </div>
      </div>
      <div class="stat-card">
        <span class="stat-icon active"><i class="fas fa-check-circle"></i></span>
        <div>
          <p class="stat-num">{{ myProperties.filter(p => p.status === 'available').length }}</p>
          <p class="stat-label">Available</p>
        </div>
      </div>
      <div class="stat-card">
        <span class="stat-icon pending"><i class="fas fa-clock"></i></span>
        <div>
          <p class="stat-num">{{ myProperties.filter(p => p.status === 'pending').length }}</p>
          <p class="stat-label">Pending Review</p>
        </div>
      </div>
      <div class="stat-card">
        <span class="stat-icon views"><i class="fas fa-eye"></i></span>
        <div>
          <p class="stat-num">{{ totalViews }}</p>
          <p class="stat-label">Total Views</p>
        </div>
      </div>
    </div>

    <!-- ── Properties Grid ── -->
    <div v-if="loadingProperties" class="properties-grid">
      <div v-for="n in 3" :key="n" class="skeleton-card">
        <div class="skeleton-img"></div>
        <div class="skeleton-body">
          <div class="skeleton-line short"></div>
          <div class="skeleton-line long"></div>
          <div class="skeleton-line medium"></div>
        </div>
      </div>
    </div>

    <div v-else-if="myProperties.length === 0" class="empty-state">
      <div class="empty-icon"><i class="fas fa-home"></i></div>
      <h3>No listings yet</h3>
      <p>Start by adding your first property to reach potential tenants.</p>
      <button class="add-btn" @click="openForm()">
        <i class="fas fa-plus"></i> Add Your First Property
      </button>
    </div>

    <div class="properties-grid" v-else>
      <div class="prop-card" v-for="property in myProperties" :key="property.id">

        <!-- Image -->
        <div class="card-img-wrap">
          <img
            :src="getPrimaryImage(property)"
            :alt="property.title"
            class="card-img"
            @error="onImgError($event)"
          />
          <div class="card-img-overlay"></div>
          <span class="status-badge" :class="property.status">
            {{ statusLabel(property.status) }}
          </span>

          <!-- Availability date badge -->
          <div class="avail-badge" v-if="property.available_from">
            <i class="fas fa-calendar-check"></i>
            <span>{{ formatAvailability(property.available_from) }}</span>
          </div>

          <div class="card-actions">
            <button class="card-action-btn" @click="openForm(property)" title="Edit">
              <i class="fas fa-pen"></i>
            </button>
            <button class="card-action-btn danger" @click="confirmDelete(property)" title="Delete">
              <i class="fas fa-trash"></i>
            </button>
          </div>
        </div>

        <!-- Body -->
        <div class="card-body">
          <div class="card-top-row">
            <span class="type-chip">{{ formatType(property.property_type) }}</span>
          </div>
          <h4 class="card-title">{{ property.title }}</h4>
          <p class="card-desc">{{ property.description }}</p>

          <!-- Amenities strip — uses objects returned directly by the API -->
          <div class="amenities-strip" v-if="property.amenities && property.amenities.length > 0">
            <span
              v-for="amenity in property.amenities.slice(0, 5)"
              :key="amenity.id"
              class="amenity-pill"
              :title="amenity.name"
            >
              <i :class="amenity.icon"></i>
              <span class="pill-label">{{ amenity.name }}</span>
            </span>
            <span class="amenity-pill pill-more" v-if="property.amenities.length > 5">
              +{{ property.amenities.length - 5 }}
            </span>
          </div>

          <div class="card-meta">
            <span class="meta-item">
              <i class="fas fa-map-marker-alt"></i> {{ property.location }}
            </span>
          </div>

          <div class="card-footer-row">
            <div class="price-block">
              <span class="price-amount">KES {{ formatPrice(property.price) }}</span>
              <span class="price-per">/month</span>
            </div>
            <span class="views-chip"><i class="fas fa-eye"></i> {{ property.views || 0 }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- ── Add / Edit Modal ── -->
    <transition name="panel">
      <div v-if="showForm" class="modal-overlay" @click.self="closeForm">
        <div class="modal-card">

          <div class="modal-head">
            <div>
              <p class="modal-eyebrow">{{ editingProperty ? 'EDIT LISTING' : 'NEW LISTING' }}</p>
              <h2 class="modal-title">{{ editingProperty ? 'Update Property' : 'Add a Property' }}</h2>
            </div>
            <button class="modal-close" @click="closeForm"><i class="fas fa-times"></i></button>
          </div>

          <div class="modal-body">
            <transition name="fade">
              <div v-if="formError" class="form-alert">
                <i class="fas fa-exclamation-circle"></i> {{ formError }}
              </div>
            </transition>

            <form @submit.prevent="submitForm" novalidate>

              <!-- Image upload zone -->
              <div class="upload-section">
                <p class="section-label">PROPERTY PHOTOS</p>
                <div
                  class="upload-zone"
                  :class="{ dragging: isDragging, 'has-images': previewImages.length > 0 }"
                  @dragover.prevent="isDragging = true"
                  @dragleave="isDragging = false"
                  @drop.prevent="onDrop"
                  @click="$refs.fileInput.click()"
                >
                  <input
                    ref="fileInput"
                    type="file"
                    multiple
                    accept="image/*"
                    class="hidden-input"
                    @change="onFileSelect"
                  />
                  <div v-if="previewImages.length === 0" class="upload-placeholder">
                    <i class="fas fa-cloud-upload-alt"></i>
                    <p class="upload-text">Drag &amp; drop photos here</p>
                    <p class="upload-sub">or click to browse · JPG, PNG, WEBP · Max 5MB each</p>
                  </div>
                  <div v-else class="preview-grid" @click.stop>
                    <div
                      v-for="(img, idx) in previewImages"
                      :key="idx"
                      class="preview-item"
                      :class="{ primary: idx === 0 }"
                    >
                      <img :src="img.url" :alt="`Preview ${idx + 1}`" />
                      <span class="primary-tag" v-if="idx === 0">Cover</span>
                      <button type="button" class="remove-img" @click="removeImage(idx)">
                        <i class="fas fa-times"></i>
                      </button>
                    </div>
                    <div class="add-more" @click="$refs.fileInput.click()">
                      <i class="fas fa-plus"></i>
                      <span>Add more</span>
                    </div>
                  </div>
                </div>
                <span class="field-error" v-if="formErrors.images">{{ formErrors.images }}</span>
              </div>

              <!-- Two-column fields -->
              <div class="form-grid">

                <div class="field-group full" :class="{ error: formErrors.title }">
                  <label class="field-label">Property Title</label>
                  <div class="field-wrap">
                    <i class="fas fa-home field-icon"></i>
                    <input v-model="form.title" class="field-input" placeholder="e.g. Spacious 2BR in Kilimani" />
                  </div>
                  <span class="field-error" v-if="formErrors.title">{{ formErrors.title }}</span>
                </div>

                <div class="field-group" :class="{ error: formErrors.property_type }">
                  <label class="field-label">Property Type</label>
                  <div class="field-wrap select-wrap">
                    <i class="fas fa-building field-icon"></i>
                    <!-- Options match backend PROPERTY_TYPES exactly -->
                    <select v-model="form.property_type" class="field-input field-select">
                      <option value="" disabled>Select type…</option>
                      <option value="apartment">Apartment</option>
                      <option value="studio">Studio</option>
                      <option value="single_room">Single Room</option>
                      <option value="bedsitter">Bedsitter</option>
                    </select>
                    <i class="fas fa-chevron-down select-arrow"></i>
                  </div>
                  <span class="field-error" v-if="formErrors.property_type">{{ formErrors.property_type }}</span>
                </div>

                <div class="field-group" :class="{ error: formErrors.price }">
                  <label class="field-label">Monthly Rent (KES)</label>
                  <div class="field-wrap">
                    <span class="field-prefix">KES</span>
                    <input v-model.number="form.price" type="number" min="0" class="field-input prefix-input" placeholder="25,000" />
                  </div>
                  <span class="field-error" v-if="formErrors.price">{{ formErrors.price }}</span>
                </div>

                <div class="field-group full" :class="{ error: formErrors.location }">
                  <label class="field-label">Location / Address</label>
                  <div class="field-wrap">
                    <i class="fas fa-map-marker-alt field-icon"></i>
                    <input v-model="form.location" class="field-input" placeholder="e.g. Kilimani, Nairobi" />
                  </div>
                  <span class="field-error" v-if="formErrors.location">{{ formErrors.location }}</span>
                </div>

                <!-- Available From — bound to available_from, matching backend field name -->
                <div class="field-group" :class="{ error: formErrors.available_from }">
                  <label class="field-label">Available From</label>
                  <div class="field-wrap date-wrap">
                    <i class="fas fa-calendar-check field-icon date-icon"></i>
                    <input
                      v-model="form.available_from"
                      type="date"
                      class="field-input date-input"
                      :min="today"
                    />
                    <transition name="fade">
                      <span class="date-preview-pill" v-if="form.available_from">
                        <i class="fas fa-circle-dot"></i>
                        {{ formatAvailability(form.available_from) }}
                      </span>
                    </transition>
                  </div>
                  <span class="field-hint" v-if="!formErrors.available_from">
                    Tenants will see this displayed on your listing card.
                  </span>
                  <span class="field-error" v-if="formErrors.available_from">{{ formErrors.available_from }}</span>
                </div>

                <div class="field-group" :class="{ error: formErrors.status }">
                  <label class="field-label">Status</label>
                  <div class="field-wrap select-wrap">
                    <i class="fas fa-toggle-on field-icon"></i>
                    <select v-model="form.status" class="field-input field-select">
                      <option value="available">Available</option>
                      <option value="pending">Pending Review</option>
                      <option value="rented">Rented</option>
                    </select>
                    <i class="fas fa-chevron-down select-arrow"></i>
                  </div>
                </div>

                <div class="field-group full" :class="{ error: formErrors.description }">
                  <label class="field-label">Description</label>
                  <textarea
                    v-model="form.description"
                    class="field-input field-textarea"
                    rows="4"
                    placeholder="Describe the property — layout, features, nearby amenities…"
                  ></textarea>
                  <div class="char-count" :class="{ warn: form.description.length > 450 }">
                    {{ form.description.length }} / 500
                  </div>
                  <span class="field-error" v-if="formErrors.description">{{ formErrors.description }}</span>
                </div>

              </div>

              <!-- ── Amenities — rendered from API data ── -->
              <div class="amenities-section">
                <div class="amenities-header">
                  <p class="section-label">AMENITIES</p>
                  <transition name="fade">
                    <span class="amenity-count-badge" v-if="form.amenity_ids.length > 0">
                      {{ form.amenity_ids.length }} selected — shown on listing
                    </span>
                  </transition>
                </div>

                <!-- Loading state for amenities -->
                <div v-if="loadingAmenities" class="amenities-grid">
                  <div v-for="n in 8" :key="n" class="amenity-chip skeleton-chip"></div>
                </div>

                <div v-else class="amenities-grid">
                  <label
                    v-for="a in amenityOptions"
                    :key="a.id"
                    class="amenity-chip"
                    :class="{ selected: form.amenity_ids.includes(a.id) }"
                  >
                    <input type="checkbox" :value="a.id" v-model="form.amenity_ids" />
                    <i :class="a.icon"></i>
                    <span>{{ a.name }}</span>
                    <i class="fas fa-check check-mark" v-if="form.amenity_ids.includes(a.id)"></i>
                  </label>
                </div>

                <!-- Live preview of selected amenities -->
                <transition name="fade">
                  <div class="amenity-preview" v-if="form.amenity_ids.length > 0">
                    <p class="preview-label">
                      <i class="fas fa-eye"></i> Preview on listing card
                    </p>
                    <div class="preview-pills">
                      <span
                        v-for="id in form.amenity_ids.slice(0, 5)"
                        :key="id"
                        class="preview-pill"
                      >
                        <i :class="amenityById[id]?.icon || 'fas fa-check-circle'"></i>
                        {{ amenityById[id]?.name || id }}
                      </span>
                      <span class="preview-pill pill-more" v-if="form.amenity_ids.length > 5">
                        +{{ form.amenity_ids.length - 5 }}
                      </span>
                    </div>
                  </div>
                </transition>
              </div>

              <!-- Footer buttons -->
              <div class="modal-footer">
                <button type="button" class="btn-cancel" @click="closeForm">Cancel</button>
                <button type="submit" class="btn-submit" :disabled="submitting">
                  <span v-if="submitting"><i class="fas fa-spinner fa-spin"></i> Saving…</span>
                  <span v-else>
                    {{ editingProperty ? 'Update Listing' : 'Publish Listing' }}
                    <i class="fas fa-arrow-right"></i>
                  </span>
                </button>
              </div>

            </form>
          </div>
        </div>
      </div>
    </transition>

    <!-- ── Delete Confirm Modal ── -->
    <transition name="panel">
      <div v-if="deleteTarget" class="modal-overlay" @click.self="deleteTarget = null">
        <div class="confirm-card">
          <div class="confirm-icon"><i class="fas fa-trash"></i></div>
          <h3 class="confirm-title">Remove Listing?</h3>
          <p class="confirm-sub">
            "<strong>{{ deleteTarget.title }}</strong>" will be permanently removed from your listings and the properties page.
          </p>
          <div class="confirm-actions">
            <button class="btn-cancel" @click="deleteTarget = null">Cancel</button>
            <button class="btn-delete" @click="deleteProperty" :disabled="deleting">
              <span v-if="deleting"><i class="fas fa-spinner fa-spin"></i> Removing…</span>
              <span v-else><i class="fas fa-trash"></i> Yes, Remove</span>
            </button>
          </div>
        </div>
      </div>
    </transition>

  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue';
import axios from 'axios';

// ── Config ─────────────────────────────────────────────────────────────────
const API_BASE = 'http://127.0.0.1:8000';

// ── Cross-tab broadcast ────────────────────────────────────────────────────
const listingsChannel = typeof BroadcastChannel !== 'undefined'
  ? new BroadcastChannel('listings-updated')
  : null;

const broadcastUpdate = (type = 'change') => {
  listingsChannel?.postMessage({ type, ts: Date.now() });
};

onUnmounted(() => listingsChannel?.close());

// ── Auth ───────────────────────────────────────────────────────────────────
const currentUser = JSON.parse(localStorage.getItem('currentUser') || '{}');

const getRawToken = () => {
  const stored =
    localStorage.getItem('authToken') ||
    localStorage.getItem('access_token') ||
    '';
  return stored.startsWith('Bearer ') ? stored.slice(7).trim() : stored.trim();
};

const buildAuthHeaders = () => {
  const token = getRawToken();
  return token ? { Authorization: `Bearer ${token}` } : {};
};

// ── State ──────────────────────────────────────────────────────────────────
const myProperties      = ref([]);
const loadingProperties = ref(false);
const loadingAmenities  = ref(false);

// Amenities fetched from the API — no more hardcoded list
const amenityOptions = ref([]);

// Fast O(1) lookup map: { [id]: { id, name, icon } }
const amenityById = computed(() =>
  Object.fromEntries(amenityOptions.value.map(a => [a.id, a]))
);

const showForm        = ref(false);
const editingProperty = ref(null);
const submitting      = ref(false);
const formError       = ref('');
const deleteTarget    = ref(null);
const deleting        = ref(false);
const notification    = ref(null);
const isDragging      = ref(false);
const fileInput       = ref(null);
const previewImages   = ref([]);

const today = new Date().toISOString().split('T')[0];

const blankForm = () => ({
  title:         '',
  description:   '',
  location:      '',
  price:         '',
  property_type: '',
  available_from: '',
  status:        'available',
  amenity_ids:   [],   // array of numeric IDs — matches backend write field name
});

const form       = ref(blankForm());
const formErrors = ref({});

// ── Computed ───────────────────────────────────────────────────────────────
const totalViews = computed(() =>
  myProperties.value.reduce((sum, p) => sum + (p.views || 0), 0)
);

// ── Image helpers ──────────────────────────────────────────────────────────
const PLACEHOLDER = 'https://placehold.co/600x400/1a1a2e/ffffff?text=No+Image';

const resolveUrl = (url) => {
  if (!url) return null;
  if (url.startsWith('http://') || url.startsWith('https://')) return url;
  return `${API_BASE}${url.startsWith('/') ? '' : '/'}${url}`;
};

const normalizeImages = (p) => {
  const raw = p.images;
  if (!Array.isArray(raw) || raw.length === 0) return [];
  return raw.map(img => {
    if (typeof img === 'string') return resolveUrl(img);
    // Backend PropertyImageSerializer returns { id, image_url }
    if (img?.image_url) return resolveUrl(img.image_url);
    if (img?.url)       return resolveUrl(img.url);
    if (img?.image)     return resolveUrl(img.image);
    return null;
  }).filter(Boolean);
};

const getPrimaryImage = (p) => {
  const imgs = normalizeImages(p);
  return imgs.length > 0 ? imgs[0] : PLACEHOLDER;
};

const onImgError = (e) => { e.target.src = PLACEHOLDER; };

// ── Formatters ─────────────────────────────────────────────────────────────
const statusLabel = (s) =>
  ({ available: 'Available', pending: 'Pending', rented: 'Rented' }[s] || s);

const formatType = (t) =>
  ({ apartment: 'Apartment', studio: 'Studio', single_room: 'Single Room', bedsitter: 'Bedsitter' }[t] || t);

const formatPrice = (p) => Number(parseFloat(p)).toLocaleString();

const formatAvailability = (dateStr) => {
  if (!dateStr) return null;
  try {
    const avail = new Date(dateStr);
    const base  = new Date();
    base.setHours(0, 0, 0, 0);
    avail.setHours(0, 0, 0, 0);
    const diff = Math.round((avail - base) / 86_400_000);

    if (diff <= 0)  return 'Available Now';
    if (diff === 1) return 'Available Tomorrow';
    if (diff <= 30) return `Available in ${diff} days`;
    return 'From ' + avail.toLocaleDateString('en-KE', {
      day: 'numeric', month: 'short', year: diff > 365 ? 'numeric' : undefined,
    });
  } catch { return dateStr; }
};

const showNotification = (message, type = 'success') => {
  notification.value = { message, type };
  setTimeout(() => { notification.value = null; }, 3500);
};

// ── Fetch amenities from API ───────────────────────────────────────────────
// This ensures IDs always match the database — no hardcoded mismatch.
const fetchAmenities = async () => {
  loadingAmenities.value = true;
  try {
    const res = await axios.get(`${API_BASE}/api/amenities/`);
    amenityOptions.value = res.data;
  } catch (err) {
    console.error('[fetchAmenities] failed:', err.message);
  } finally {
    loadingAmenities.value = false;
  }
};

// ── Fetch agent's properties ───────────────────────────────────────────────
const fetchMyProperties = async () => {
  loadingProperties.value = true;
  try {
    const res = await axios.get(`${API_BASE}/api/properties/my/`, {
      headers: buildAuthHeaders(),
    });
    myProperties.value = res.data;
  } catch {
    // Fallback: filter all properties by current user agency
    try {
      const res = await axios.get(`${API_BASE}/api/properties/`);
      myProperties.value = res.data.filter(
        p => p.agent_id === currentUser?.id || p.agency === currentUser?.id
      );
    } catch (err) {
      console.error('[fetchMyProperties] fallback failed:', err.message);
    }
  } finally {
    loadingProperties.value = false;
  }
};

onMounted(() => {
  fetchAmenities();
  fetchMyProperties();
});

// ── Image handling ─────────────────────────────────────────────────────────
const onFileSelect = (e) => {
  addFiles(Array.from(e.target.files));
  e.target.value = ''; // allow re-selecting the same file
};

const onDrop = (e) => {
  isDragging.value = false;
  addFiles(Array.from(e.dataTransfer.files));
};

const addFiles = (files) => {
  files.forEach(file => {
    if (!file.type.startsWith('image/')) return;
    const isDuplicate = previewImages.value.some(
      img => img.file && img.file.name === file.name && img.file.size === file.size
    );
    if (isDuplicate) return;
    previewImages.value.push({ url: URL.createObjectURL(file), file });
  });
};

const removeImage = (idx) => {
  URL.revokeObjectURL(previewImages.value[idx].url);
  previewImages.value.splice(idx, 1);
};

// ── Form open / close ──────────────────────────────────────────────────────
const openForm = (property = null) => {
  editingProperty.value = property;
  formError.value  = '';
  formErrors.value = {};
  previewImages.value = [];

  if (property) {
    form.value = {
      title:          property.title         || '',
      description:    property.description   || '',
      location:       property.location      || '',
      price:          property.price         || '',
      property_type:  property.property_type || '',
      available_from: property.available_from || '',
      status:         property.status        || 'available',
      // Backend returns full amenity objects [{id, name, icon}] — extract IDs only
      amenity_ids: Array.isArray(property.amenities)
        ? property.amenities.map(a => (typeof a === 'object' ? a.id : Number(a)))
        : [],
    };

    // Populate image previews from existing property images
    normalizeImages(property).forEach(url => {
      previewImages.value.push({ url, file: null });
    });
  } else {
    form.value = blankForm();
  }

  showForm.value = true;
};

const closeForm = () => {
  showForm.value = false;
  previewImages.value.forEach(img => { if (img.file) URL.revokeObjectURL(img.url); });
  previewImages.value = [];
};

// ── Validation ─────────────────────────────────────────────────────────────
const validate = () => {
  const e = {};
  if (!form.value.title.trim())                   e.title          = 'Title is required.';
  if (!form.value.description.trim())             e.description    = 'Description is required.';
  if (!form.value.location.trim())                e.location       = 'Location is required.';
  if (!form.value.price || form.value.price <= 0) e.price          = 'Enter a valid price.';
  if (!form.value.property_type)                  e.property_type  = 'Select a property type.';
  if (!form.value.available_from)                 e.available_from = 'Select an availability date.';
  if (previewImages.value.length === 0)           e.images         = 'Upload at least one photo.';
  formErrors.value = e;
  return Object.keys(e).length === 0;
};

// ── Submit ─────────────────────────────────────────────────────────────────
const submitForm = async () => {
  if (!validate()) return;
  submitting.value = true;
  formError.value  = '';

  try {
    const fd = new FormData();
    fd.append('title',          form.value.title);
    fd.append('description',    form.value.description);
    fd.append('location',       form.value.location);
    fd.append('price',          form.value.price);
    fd.append('property_type',  form.value.property_type);
    fd.append('status',         form.value.status);
    fd.append('available_from', form.value.available_from);

    // Amenities — send each ID under the key the backend serializer expects: amenity_ids
    // PrimaryKeyRelatedField(many=True) reads repeated form keys, not a single JSON blob
    form.value.amenity_ids.forEach(id => fd.append('amenity_ids', id));

    // Images — only send new File objects; existing previews have file === null
    previewImages.value.forEach(img => {
      if (img.file) fd.append('images', img.file);
    });

    const headers = { ...buildAuthHeaders(), 'Content-Type': 'multipart/form-data' };

    if (editingProperty.value) {
      await axios.patch(
        `${API_BASE}/api/properties/${editingProperty.value.id}/`,
        fd,
        { headers }
      );
      showNotification('Listing updated successfully!');
      broadcastUpdate('update');
    } else {
      await axios.post(`${API_BASE}/api/properties/`, fd, { headers });
      showNotification('Property published successfully!');
      broadcastUpdate('create');
    }

    closeForm();
    fetchMyProperties();
  } catch (err) {
    console.error('[submitForm]', err.response?.data || err.message);
    const data = err.response?.data;
    // Show the first field-level error if available, otherwise a generic message
    const firstError = data && typeof data === 'object'
      ? Object.values(data).flat()[0]
      : null;
    formError.value = firstError || data?.detail || 'Something went wrong. Please try again.';
  } finally {
    submitting.value = false;
  }
};

// ── Delete ─────────────────────────────────────────────────────────────────
const confirmDelete = (property) => { deleteTarget.value = property; };

const deleteProperty = async () => {
  if (!deleteTarget.value) return;
  deleting.value = true;
  try {
    await axios.delete(
      `${API_BASE}/api/properties/${deleteTarget.value.id}/`,
      { headers: buildAuthHeaders() }
    );
    myProperties.value = myProperties.value.filter(p => p.id !== deleteTarget.value.id);
    showNotification('Listing removed.');
    broadcastUpdate('delete');
    deleteTarget.value = null;
  } catch {
    showNotification('Could not delete. Please try again.', 'error');
  } finally {
    deleting.value = false;
  }
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,300;1,400;1,600&family=DM+Sans:wght@300;400;500;600&display=swap');

/* ─── Base ────────────────────────────── */
.agent-page {
  font-family: 'DM Sans', sans-serif;
  background: #f6f4f1;
  min-height: 100vh;
  padding: 36px 32px 60px;
  color: #1c1c1c;
}

/* ─── Header ──────────────────────────── */
.page-header {
  display: flex; justify-content: space-between; align-items: flex-end;
  margin-bottom: 28px; flex-wrap: wrap; gap: 16px;
}
.page-eyebrow { font-size: 10px; letter-spacing: 3px; font-weight: 600; color: #b73f2a; margin: 0 0 6px; }
.page-title   { font-family: 'Cormorant Garamond', serif; font-size: 40px; font-weight: 600; color: #111; margin: 0 0 6px; line-height: 1.1; }
.page-title em { font-style: italic; color: #b73f2a; }
.page-sub { font-size: 14px; color: #888; margin: 0; }

.add-btn {
  display: flex; align-items: center; gap: 8px;
  padding: 12px 24px; background: #b73f2a; color: #fff;
  border: none; border-radius: 10px;
  font-family: 'DM Sans', sans-serif; font-size: 14px; font-weight: 600;
  cursor: pointer; transition: background 0.2s, transform 0.2s, box-shadow 0.2s;
  white-space: nowrap;
}
.add-btn:hover { background: #9a3523; transform: translateY(-2px); box-shadow: 0 8px 24px rgba(183,63,42,0.25); }

/* ─── Stats Strip ─────────────────────── */
.stats-strip { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin-bottom: 32px; }
.stat-card {
  background: #fff; border-radius: 14px; padding: 18px 20px;
  display: flex; align-items: center; gap: 14px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.05);
}
.stat-icon {
  width: 44px; height: 44px; border-radius: 12px; background: #f0ede9; color: #888;
  display: flex; align-items: center; justify-content: center; font-size: 17px; flex-shrink: 0;
}
.stat-icon.active  { background: rgba(56,161,105,0.1);  color: #38a169; }
.stat-icon.pending { background: rgba(221,155,23,0.1);  color: #dd9b17; }
.stat-icon.views   { background: rgba(49,130,206,0.1);  color: #3182ce; }
.stat-num   { font-family: 'Cormorant Garamond', serif; font-size: 26px; font-weight: 600; color: #111; margin: 0; line-height: 1; }
.stat-label { font-size: 12px; color: #aaa; margin: 4px 0 0; }

/* ─── Properties Grid ─────────────────── */
.properties-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 24px; }

/* ─── Prop Card ───────────────────────── */
.prop-card {
  background: #fff; border-radius: 16px; overflow: hidden;
  box-shadow: 0 2px 12px rgba(0,0,0,0.06);
  transition: transform 0.25s, box-shadow 0.25s; display: flex; flex-direction: column;
}
.prop-card:hover { transform: translateY(-5px); box-shadow: 0 14px 36px rgba(0,0,0,0.1); }

.card-img-wrap { position: relative; height: 210px; overflow: hidden; background: #e8e4df; }
.card-img { width: 100%; height: 100%; object-fit: cover; transition: transform 0.4s; }
.prop-card:hover .card-img { transform: scale(1.04); }
.card-img-overlay {
  position: absolute; inset: 0;
  background: linear-gradient(to top, rgba(0,0,0,0.45) 0%, transparent 55%);
  pointer-events: none;
}

.status-badge {
  position: absolute; top: 12px; left: 12px;
  padding: 4px 10px; border-radius: 20px;
  font-size: 11px; font-weight: 600; text-transform: capitalize; letter-spacing: 0.5px;
}
.status-badge.available { background: rgba(56,161,105,0.9);   color: #fff; }
.status-badge.pending   { background: rgba(221,155,23,0.9);   color: #fff; }
.status-badge.rented    { background: rgba(100,100,100,0.85); color: #fff; }

.avail-badge {
  position: absolute; bottom: 12px; right: 12px;
  display: flex; align-items: center; gap: 6px;
  padding: 5px 11px; border-radius: 20px; font-size: 11px; font-weight: 600;
  backdrop-filter: blur(8px); -webkit-backdrop-filter: blur(8px);
  background: rgba(255,255,255,0.18); border: 1px solid rgba(255,255,255,0.35);
  color: #fff; text-shadow: 0 1px 3px rgba(0,0,0,0.4);
  box-shadow: 0 2px 12px rgba(0,0,0,0.2); z-index: 3;
}
.avail-badge i { font-size: 10px; opacity: 0.9; }

.card-actions {
  position: absolute; top: 10px; right: 10px;
  display: flex; gap: 6px; opacity: 0; transition: opacity 0.2s;
}
.prop-card:hover .card-actions { opacity: 1; }
.card-action-btn {
  width: 34px; height: 34px; border-radius: 8px; border: none;
  background: rgba(255,255,255,0.92); color: #555; font-size: 13px;
  cursor: pointer; display: flex; align-items: center; justify-content: center; transition: all 0.2s;
}
.card-action-btn:hover        { background: #fff; color: #b73f2a; }
.card-action-btn.danger:hover { color: #e53e3e; }

/* Card body */
.card-body { padding: 16px 18px 18px; display: flex; flex-direction: column; gap: 8px; flex-grow: 1; }
.card-top-row { display: flex; align-items: center; gap: 10px; }
.type-chip {
  display: inline-block; padding: 3px 10px; border-radius: 20px;
  background: rgba(183,63,42,0.08); color: #b73f2a;
  font-size: 11px; font-weight: 600; letter-spacing: 0.5px;
}
.card-title { font-family: 'Cormorant Garamond', serif; font-size: 18px; font-weight: 600; color: #111; margin: 0; line-height: 1.3; }
.card-desc {
  font-size: 13px; color: #777; margin: 0;
  display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical;
  overflow: hidden; line-height: 1.5; flex-grow: 1;
}

/* Amenities strip on listing card */
.amenities-strip { display: flex; flex-wrap: wrap; gap: 5px; }
.amenity-pill {
  display: inline-flex; align-items: center; gap: 4px;
  padding: 3px 9px; border-radius: 20px;
  background: #f4f0eb; border: 1px solid #e8e2d9;
  font-size: 11px; color: #555; font-weight: 500; white-space: nowrap;
}
.amenity-pill i { font-size: 10px; color: #b73f2a; flex-shrink: 0; }
.pill-more {
  background: #1c1c1c; border-color: #1c1c1c;
  color: #fff; font-size: 10.5px; font-weight: 600;
}

.card-meta { display: flex; flex-direction: column; gap: 5px; }
.meta-item { font-size: 12px; color: #999; display: flex; align-items: center; gap: 6px; }
.meta-item i { color: #b73f2a; font-size: 11px; }

.card-footer-row {
  display: flex; justify-content: space-between; align-items: center;
  padding-top: 10px; border-top: 1px solid #f0f0f0; margin-top: auto;
}
.price-block  { display: flex; align-items: baseline; gap: 3px; }
.price-amount { font-family: 'Cormorant Garamond', serif; font-size: 20px; font-weight: 600; color: #b73f2a; }
.price-per    { font-size: 12px; color: #aaa; }
.views-chip   { display: flex; align-items: center; gap: 5px; font-size: 12px; color: #aaa; background: #f5f5f5; padding: 4px 10px; border-radius: 20px; }

/* ─── Empty State ─────────────────────── */
.empty-state { text-align: center; padding: 80px 24px; background: #fff; border-radius: 20px; box-shadow: 0 2px 12px rgba(0,0,0,0.05); }
.empty-icon  { width: 70px; height: 70px; border-radius: 20px; background: rgba(183,63,42,0.08); color: #b73f2a; font-size: 28px; display: flex; align-items: center; justify-content: center; margin: 0 auto 20px; }
.empty-state h3 { font-family: 'Cormorant Garamond', serif; font-size: 26px; font-weight: 600; margin: 0 0 8px; }
.empty-state p  { font-size: 14px; color: #888; margin: 0 0 24px; }

/* ─── Modal ───────────────────────────── */
.modal-overlay {
  position: fixed; inset: 0; background: rgba(0,0,0,0.45); backdrop-filter: blur(4px);
  display: flex; align-items: flex-start; justify-content: center;
  z-index: 1050; padding: 24px 16px; overflow-y: auto;
}
.modal-card {
  background: #fff; width: 100%; max-width: 720px; border-radius: 20px; overflow: hidden;
  box-shadow: 0 24px 80px rgba(0,0,0,0.2); animation: slideUp 0.3s ease; margin: auto;
}
@keyframes slideUp { from { transform: translateY(30px); opacity: 0; } to { transform: translateY(0); opacity: 1; } }

.modal-head {
  display: flex; justify-content: space-between; align-items: flex-start;
  padding: 28px 32px 20px; border-bottom: 1px solid #f0f0f0;
}
.modal-eyebrow { font-size: 10px; letter-spacing: 3px; font-weight: 600; color: #b73f2a; margin: 0 0 6px; }
.modal-title   { font-family: 'Cormorant Garamond', serif; font-size: 26px; font-weight: 600; color: #111; margin: 0; }
.modal-close   { width: 36px; height: 36px; background: #f5f4f2; border: none; border-radius: 50%; display: flex; align-items: center; justify-content: center; cursor: pointer; font-size: 14px; color: #555; flex-shrink: 0; transition: background 0.2s; }
.modal-close:hover { background: #ede9e4; color: #111; }
.modal-body    { padding: 28px 32px 32px; }

.form-alert { padding: 12px 16px; border-radius: 10px; background: #fff5f5; color: #b73f2a; border: 1px solid rgba(183,63,42,0.2); font-size: 13.5px; display: flex; align-items: center; gap: 10px; margin-bottom: 20px; }

/* ─── Upload zone ─────────────────────── */
.section-label  { font-size: 10px; letter-spacing: 2.5px; font-weight: 600; color: #aaa; margin: 0 0 10px; }
.upload-section { margin-bottom: 0; }
.upload-zone    { border: 2px dashed #ddd; border-radius: 14px; cursor: pointer; transition: border-color 0.2s, background 0.2s; overflow: hidden; min-height: 160px; display: flex; align-items: center; justify-content: center; }
.upload-zone:hover, .upload-zone.dragging { border-color: #b73f2a; background: rgba(183,63,42,0.03); }
.upload-zone.has-images { min-height: auto; align-items: stretch; }
.hidden-input   { display: none; }
.upload-placeholder { text-align: center; padding: 32px 24px; pointer-events: none; }
.upload-placeholder i { font-size: 36px; color: #ccc; margin-bottom: 12px; display: block; }
.upload-text    { font-size: 14px; color: #555; font-weight: 500; margin: 0 0 6px; }
.upload-sub     { font-size: 12px; color: #aaa; margin: 0; }
.preview-grid   { display: grid; grid-template-columns: repeat(auto-fill, minmax(120px, 1fr)); gap: 8px; padding: 12px; width: 100%; }
.preview-item   { position: relative; border-radius: 10px; overflow: hidden; aspect-ratio: 4/3; border: 2px solid transparent; transition: border-color 0.2s; }
.preview-item.primary { border-color: #b73f2a; }
.preview-item img { width: 100%; height: 100%; object-fit: cover; display: block; }
.primary-tag    { position: absolute; bottom: 6px; left: 6px; background: #b73f2a; color: #fff; font-size: 10px; font-weight: 700; padding: 2px 8px; border-radius: 10px; }
.remove-img     { position: absolute; top: 5px; right: 5px; width: 22px; height: 22px; background: rgba(0,0,0,0.6); color: #fff; border: none; border-radius: 50%; font-size: 10px; cursor: pointer; display: flex; align-items: center; justify-content: center; transition: background 0.2s; }
.remove-img:hover { background: #e53e3e; }
.add-more       { border: 2px dashed #ddd; border-radius: 10px; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 6px; aspect-ratio: 4/3; cursor: pointer; color: #bbb; font-size: 11px; transition: border-color 0.2s, color 0.2s; }
.add-more:hover { border-color: #b73f2a; color: #b73f2a; }
.add-more i     { font-size: 18px; }

/* ─── Form grid ───────────────────────── */
.form-grid      { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-top: 20px; }
.field-group    { display: flex; flex-direction: column; gap: 6px; }
.field-group.full { grid-column: 1 / -1; }
.field-label    { font-size: 10.5px; letter-spacing: 1.5px; text-transform: uppercase; font-weight: 600; color: #888; }
.field-wrap     { position: relative; display: flex; align-items: center; }
.field-icon     { position: absolute; left: 13px; font-size: 13px; color: #ccc; pointer-events: none; transition: color 0.2s; z-index: 1; }
.field-input {
  width: 100%; padding: 11px 14px 11px 38px; border: 1.5px solid #e0dcd8;
  border-radius: 10px; font-family: 'DM Sans', sans-serif; font-size: 14px; color: #1c1c1c;
  background: #fff; outline: none; transition: border-color 0.2s, box-shadow 0.2s; -webkit-appearance: none;
}
.field-input::placeholder { color: #c0bbb6; }
.field-input:focus { border-color: #b73f2a; box-shadow: 0 0 0 3px rgba(183,63,42,0.1); }
.field-wrap:focus-within .field-icon { color: #b73f2a; }
.field-group.error .field-input { border-color: #e53e3e; }
.field-error    { font-size: 12px; color: #e53e3e; font-weight: 500; }
.field-hint     { font-size: 11.5px; color: #b0a99f; }

/* Select */
.select-wrap  { position: relative; }
.field-select { appearance: none; -webkit-appearance: none; padding-right: 36px; cursor: pointer; }
.select-arrow { position: absolute; right: 12px; font-size: 11px; color: #aaa; pointer-events: none; }

/* Price prefix */
.field-prefix { position: absolute; left: 13px; font-size: 13px; font-weight: 600; color: #aaa; pointer-events: none; z-index: 1; }
.prefix-input { padding-left: 46px !important; }

/* Textarea */
.field-textarea { resize: vertical; padding: 11px 14px; line-height: 1.6; min-height: 100px; }
.char-count     { font-size: 11px; color: #bbb; text-align: right; margin-top: -2px; }
.char-count.warn { color: #e53e3e; }

/* Date field */
.date-wrap         { flex-direction: column; align-items: flex-start; gap: 8px; }
.date-input        { width: 100%; }
.date-preview-pill {
  display: inline-flex; align-items: center; gap: 6px;
  padding: 4px 12px; border-radius: 20px;
  background: rgba(183,63,42,0.08); border: 1px solid rgba(183,63,42,0.22);
  color: #b73f2a; font-size: 12px; font-weight: 600;
}
.date-preview-pill i { font-size: 9px; }

/* ─── Amenities section ───────────────── */
.amenities-section { margin-top: 24px; }
.amenities-header  { display: flex; align-items: center; gap: 12px; margin-bottom: 10px; }
.amenity-count-badge {
  font-size: 11.5px; font-weight: 600; color: #b73f2a;
  background: rgba(183,63,42,0.08); border: 1px solid rgba(183,63,42,0.2);
  padding: 3px 10px; border-radius: 20px;
}
.amenities-grid    { display: flex; flex-wrap: wrap; gap: 8px; }
.amenity-chip {
  display: flex; align-items: center; gap: 7px;
  padding: 8px 14px; border: 1.5px solid #e0dcd8; border-radius: 20px;
  font-size: 13px; color: #555; cursor: pointer;
  transition: all 0.18s; user-select: none; background: #fff; position: relative;
}
.amenity-chip input[type="checkbox"] { display: none; }
.amenity-chip i { font-size: 12px; color: #bbb; transition: color 0.2s; }
.amenity-chip:hover { border-color: #b73f2a; color: #b73f2a; }
.amenity-chip:hover i { color: #b73f2a; }
.amenity-chip.selected { border-color: #b73f2a; background: rgba(183,63,42,0.06); color: #b73f2a; font-weight: 500; }
.amenity-chip.selected i { color: #b73f2a; }
.check-mark { font-size: 10px !important; margin-left: 2px; color: #b73f2a !important; }
/* Skeleton shimmer for amenity chips while loading */
.skeleton-chip { width: 100px; height: 38px; background: linear-gradient(90deg,#ececec 25%,#f5f5f5 50%,#ececec 75%); background-size: 200% 100%; animation: shimmer 1.4s infinite; border: none; cursor: default; pointer-events: none; }

/* Live amenity preview */
.amenity-preview {
  margin-top: 14px; padding: 12px 14px;
  background: #faf8f6; border: 1px solid #ede9e4; border-radius: 10px;
}
.preview-label {
  font-size: 10.5px; letter-spacing: 1px; text-transform: uppercase; font-weight: 600;
  color: #b0a99f; margin: 0 0 10px; display: flex; align-items: center; gap: 6px;
}
.preview-pills { display: flex; flex-wrap: wrap; gap: 6px; }
.preview-pill  {
  display: inline-flex; align-items: center; gap: 5px;
  padding: 4px 10px; border-radius: 20px;
  background: #fff; border: 1px solid #e0dcd8;
  font-size: 12px; color: #555; font-weight: 500;
}
.preview-pill i { font-size: 10px; color: #b73f2a; }
.preview-pill.pill-more { background: #1c1c1c; border-color: #1c1c1c; color: #fff; font-weight: 600; }

/* ─── Modal footer ────────────────────── */
.modal-footer { display: flex; justify-content: flex-end; gap: 12px; margin-top: 28px; padding-top: 20px; border-top: 1px solid #f0f0f0; }
.btn-cancel   { padding: 11px 22px; border: 1.5px solid #ddd; border-radius: 10px; background: none; font-family: 'DM Sans', sans-serif; font-size: 14px; color: #555; cursor: pointer; transition: all 0.2s; }
.btn-cancel:hover { border-color: #999; color: #333; }
.btn-submit   { padding: 11px 24px; background: #b73f2a; color: #fff; border: none; border-radius: 10px; font-family: 'DM Sans', sans-serif; font-size: 14px; font-weight: 600; cursor: pointer; display: flex; align-items: center; gap: 8px; transition: background 0.2s, transform 0.2s, box-shadow 0.2s; }
.btn-submit:hover:not(:disabled) { background: #9a3523; transform: translateY(-1px); box-shadow: 0 8px 20px rgba(183,63,42,0.25); }
.btn-submit:disabled { opacity: 0.6; cursor: not-allowed; }

/* ─── Confirm delete card ─────────────── */
.confirm-card    { background: #fff; border-radius: 20px; padding: 36px; width: 100%; max-width: 420px; text-align: center; box-shadow: 0 24px 80px rgba(0,0,0,0.2); animation: slideUp 0.3s ease; margin: auto; }
.confirm-icon    { width: 60px; height: 60px; background: #fff5f5; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 22px; color: #e53e3e; margin: 0 auto 18px; }
.confirm-title   { font-family: 'Cormorant Garamond', serif; font-size: 24px; font-weight: 600; margin: 0 0 10px; }
.confirm-sub     { font-size: 14px; color: #777; line-height: 1.6; margin: 0 0 24px; }
.confirm-actions { display: flex; gap: 10px; justify-content: center; }
.btn-delete      { padding: 11px 22px; background: #e53e3e; color: #fff; border: none; border-radius: 10px; font-family: 'DM Sans', sans-serif; font-size: 14px; font-weight: 600; cursor: pointer; display: flex; align-items: center; gap: 8px; transition: background 0.2s; }
.btn-delete:hover:not(:disabled) { background: #c0392b; }
.btn-delete:disabled { opacity: 0.6; cursor: not-allowed; }

/* ─── Toast ───────────────────────────── */
.notification-toast   { position: fixed; top: 24px; right: 24px; padding: 14px 20px; border-radius: 10px; display: flex; align-items: center; gap: 10px; font-size: 14px; z-index: 9999; max-width: 320px; box-shadow: 0 8px 24px rgba(0,0,0,0.18); }
.notification-toast.success   { background: #1c1c1c; color: #fff; }
.notification-toast.success i { color: #4caf50; }
.notification-toast.error     { background: #fff5f5; color: #b73f2a; border: 1px solid rgba(183,63,42,0.2); }

/* ─── Skeleton ────────────────────────── */
.skeleton-card { background: #fff; border-radius: 16px; overflow: hidden; }
.skeleton-img  { height: 210px; background: linear-gradient(90deg,#ececec 25%,#f5f5f5 50%,#ececec 75%); background-size: 200% 100%; animation: shimmer 1.4s infinite; }
.skeleton-body { padding: 16px 18px; display: flex; flex-direction: column; gap: 10px; }
.skeleton-line { height: 12px; border-radius: 6px; background: linear-gradient(90deg,#ececec 25%,#f5f5f5 50%,#ececec 75%); background-size: 200% 100%; animation: shimmer 1.4s infinite; }
.skeleton-line.short  { width: 40%; }
.skeleton-line.long   { width: 85%; }
.skeleton-line.medium { width: 60%; }
@keyframes shimmer { 0% { background-position: 200% 0; } 100% { background-position: -200% 0; } }

/* ─── Transitions ─────────────────────── */
.toast-enter-active, .toast-leave-active { transition: all 0.3s ease; }
.toast-enter-from,   .toast-leave-to     { opacity: 0; transform: translateX(30px); }
.panel-enter-active, .panel-leave-active { transition: opacity 0.3s ease; }
.panel-enter-from,   .panel-leave-to     { opacity: 0; }
.fade-enter-active,  .fade-leave-active  { transition: opacity 0.2s; }
.fade-enter-from,    .fade-leave-to      { opacity: 0; }

/* ─── Responsive ──────────────────────── */
@media (max-width: 900px) {
  .stats-strip { grid-template-columns: 1fr 1fr; }
  .form-grid   { grid-template-columns: 1fr; }
  .field-group.full { grid-column: 1; }
}
@media (max-width: 600px) {
  .agent-page  { padding: 24px 16px 48px; }
  .page-title  { font-size: 30px; }
  .page-header { flex-direction: column; align-items: flex-start; }
  .stats-strip { grid-template-columns: 1fr 1fr; gap: 10px; }
  .modal-body  { padding: 20px 18px 24px; }
  .modal-head  { padding: 20px 18px 16px; }
  .properties-grid { grid-template-columns: 1fr; }
  .pill-label  { display: none; }
  .amenity-pill { padding: 4px 7px; }
}
</style>