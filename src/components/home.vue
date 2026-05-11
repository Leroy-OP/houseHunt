<template>
  <div class="home-page">

    <!-- ── HERO ──────────────────────────────────────────────────────── -->
    <section class="hero-section">
      <img src="/hero.jpeg" class="hero-bg" alt="Hero" />
      <div class="hero-grain"></div>
      <div class="hero-overlay"></div>

      <div class="hero-content">
        <!-- eyebrow -->
        <p class="hero-eyebrow">NAIROBI'S GREATEST SPACES</p>

        <h1 class="hero-title">
          Find <em>your</em><br/>perfect space.
        </h1>

        <p class="hero-subtitle">
          Comfortable, reliable and affordable homes —<br class="hide-sm"/>tailored to your lifestyle.
        </p>

        <!-- Search pill -->
        <div class="search-pill">
          <div class="search-field">
            <span class="search-field-label">LOCATION</span>
            <input
              type="text"
              v-model="location"
              placeholder="e.g. Masai Lodge, Tumaini…"
              class="search-input"
            />
          </div>

          <div class="search-divider"></div>

          <div class="search-field search-field--rel">
            <span class="search-field-label">TYPE</span>
            <input
              type="text"
              v-model="type"
              placeholder="Bedsitter, Studio…"
              class="search-input"
              @focus="showTypeDrop = true"
              @blur="delayClose('type')"
            />
            <div v-if="showTypeDrop && filteredTypeSuggestions.length" class="suggest-drop">
              <button
                v-for="s in filteredTypeSuggestions"
                :key="s"
                class="suggest-item"
                @mousedown.prevent="type = s; showTypeDrop = false"
              >{{ s }}</button>
            </div>
          </div>

          <div class="search-divider"></div>

          <div class="search-field search-field--rel">
            <span class="search-field-label">CATEGORY</span>
            <input
              type="text"
              v-model="category"
              placeholder="Hostel, Apartment…"
              class="search-input"
              @focus="showCatDrop = true"
              @blur="delayClose('cat')"
            />
            <div v-if="showCatDrop && filteredCategorySuggestions.length" class="suggest-drop">
              <button
                v-for="s in filteredCategorySuggestions"
                :key="s"
                class="suggest-item"
                @mousedown.prevent="category = s; showCatDrop = false"
              >{{ s }}</button>
            </div>
          </div>

          <button class="search-btn" @click="search">
            <i class="fas fa-search"></i>
          </button>
        </div>

        <!-- Trust strip -->
        <div class="trust-strip">
          <span class="trust-item"><i class="fas fa-shield-alt"></i> Verified listings</span>
          <span class="trust-sep">·</span>
          <span class="trust-item"><i class="fas fa-star"></i> Top-rated agencies</span>
          <span class="trust-sep">·</span>
          <span class="trust-item"><i class="fas fa-map-marker-alt"></i> Nairobi &amp; beyond</span>
        </div>
      </div>
    </section>
<
    <!--DISCOVER -->
    <section class="content-section">
      <div class="section-head">
        <div>
          <p class="section-eyebrow">FEATURED</p>
          <h2 class="section-title">Discover</h2>
        </div>
        <router-link to="/properties" class="see-all-btn">
          See all <i class="fas fa-arrow-right"></i>
        </router-link>
      </div>

      <!-- Skeleton -->
      <div class="cards-grid" v-if="loadingProperties">
        <div v-for="n in 3" :key="n" class="skeleton-card">
          <div class="skeleton-img"></div>
          <div class="skeleton-body">
            <div class="skeleton-line short"></div>
            <div class="skeleton-line long"></div>
            <div class="skeleton-line medium"></div>
          </div>
        </div>
      </div>

      <!-- Error -->
      <div v-else-if="propError" class="inline-error">
        <i class="fas fa-exclamation-triangle"></i> {{ propError }}
      </div>

      <!-- Cards -->
      <div class="cards-grid" v-else>
        <div
          v-for="property in discoverProperties"
          :key="property.id"
          class="prop-card"
          @click="goToProperties"
        >
          <div class="card-img-wrap">
            <img
              :src="getPrimaryImage(property)"
              :alt="property.title"
              class="card-img"
              @error="onImgError($event)"
            />
            <div class="card-overlay"></div>
            <span class="status-badge">{{ property.property_type ? formatType(property.property_type) : 'Available' }}</span>
            <button class="heart-btn" @click.stop="toggleSave(property)">
              <i :class="isSaved(property) ? 'fas fa-heart saved' : 'far fa-heart'"></i>
            </button>
          </div>
          <div class="card-body">
            <h4 class="card-title">{{ property.title }}</h4>
            <p class="card-desc">{{ property.description }}</p>
            <div class="card-footer-row">
       <span class="card-location"><i class="fas fa-map-marker-alt"></i> {{ property.location }}</span>
              <span class="card-price">KES {{ formatPrice(property.price) }}<span class="mo">/mo</span></span>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- ── RELIABLE AGENCIES ──────────────────────────────────────────── -->
    <section class="content-section agencies-section">
      <div class="section-head">
        <div>
          <p class="section-eyebrow">TRUSTED</p>
          <h2 class="section-title">Reliable Agencies</h2>
        </div>
        <router-link to="/properties" class="see-all-btn">
          See all <i class="fas fa-arrow-right"></i>
        </router-link>
      </div>

      <!-- Skeleton -->
      <div class="cards-grid" v-if="loadingAgencies">
        <div v-for="n in 3" :key="n" class="skeleton-card">
          <div class="skeleton-img"></div>
          <div class="skeleton-body">
            <div class="skeleton-line short"></div>
            <div class="skeleton-line long"></div>
          </div>
        </div>
      </div>

      <!-- Error -->
      <div v-else-if="agencyError" class="inline-error">
        <i class="fas fa-exclamation-triangle"></i> {{ agencyError }}
      </div>

      <!-- Agency cards -->
      <div class="cards-grid" v-else>
        <div
          v-for="agency in agencies"
          :key="agency.id"
          class="agency-card"
        >
          <div class="agency-logo-wrap">
            <img
              v-if="agency.logo || agency.logo_url"
              :src="agency.logo || agency.logo_url"
              :alt="agency.name"
              class="agency-logo"
              @error="onImgError($event)"
            />
            <div v-else class="agency-logo-placeholder">
              <i class="fas fa-building"></i>
            </div>
          </div>
          <div class="agency-body">
            <h4 class="agency-name">{{ agency.name }}</h4>
            <p class="agency-desc">{{ agency.description || agency.bio || 'Trusted real-estate agency.' }}</p>
            <div class="agency-meta">
              <span v-if="agency.phone" class="agency-chip">
                <i class="fas fa-phone"></i> {{ agency.phone }}
              </span>
              <span v-if="agency.email" class="agency-chip">
                <i class="fas fa-envelope"></i> {{ agency.email }}
              </span>
              <span v-if="agency.location" class="agency-chip">
                <i class="fas fa-map-marker-alt"></i> {{ agency.location }}
              </span>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- ── FOOTER ────────────────────────────────────────────────────── -->
    <footer class="site-footer">
      <div class="footer-inner">
        <div class="footer-brand">
          <p class="footer-brand-label">HUNTER STREET</p>
          <p class="footer-brand-desc">
            Connecting people to homes they love across Nairobi and beyond.
          </p>
          <div class="footer-socials">
            <a href="#" class="social-icon"><i class="fab fa-facebook-f"></i></a>
            <a href="#" class="social-icon"><i class="fab fa-twitter"></i></a>
            <a href="#" class="social-icon"><i class="fab fa-instagram"></i></a>
            <a href="#" class="social-icon"><i class="fab fa-linkedin-in"></i></a>
          </div>
        </div>

        <div class="footer-col">
          <p class="footer-col-label">LINKS</p>
          <a href="#" class="footer-link">Properties</a>
          <a href="#" class="footer-link">Agencies</a>
          <a href="#" class="footer-link">Saved</a>
          <a href="#" class="footer-link">Help</a>
        </div>

        <div class="footer-col">
          <p class="footer-col-label">CONTACT</p>
          <p class="footer-contact-line"><i class="fas fa-map-marker-alt"></i> Nairobi, Kenya</p>
          <p class="footer-contact-line"><i class="fas fa-envelope"></i> info@hunterstreet.co.ke</p>
          <p class="footer-contact-line"><i class="fas fa-phone"></i> +254 700 000 000</p>
        </div>
      </div>

      <div class="footer-bottom">
        <span>© {{ new Date().getFullYear() }} Hunter Street. All rights reserved.</span>
      </div>
    </footer>

  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';

export default {
  setup() {
    const router = useRouter();

    // ── Search state ─────────────────────────────────────────────────
    const location = ref('');
    const type = ref('');
    const category = ref('');
    const showTypeDrop = ref(false);
    const showCatDrop  = ref(false);

    const typeSuggestions     = ['Bedsitters', 'Single Room', 'Studio Apartment'];
    const categorySuggestions = ['Apartments', 'Bedsitters', 'studio'];

    const filteredTypeSuggestions = computed(() =>
      !type.value ? [] : typeSuggestions.filter(s => s.toLowerCase().includes(type.value.toLowerCase()))
    );
    const filteredCategorySuggestions = computed(() =>
      !category.value ? [] : categorySuggestions.filter(s => s.toLowerCase().includes(category.value.toLowerCase()))
    );

    const delayClose = (which) => {
      setTimeout(() => {
        if (which === 'type') showTypeDrop.value = false;
        else showCatDrop.value = false;
      }, 150);
    };

    const search = () => {
      router.push({ path: '/properties', query: { location: location.value, type: type.value, category: category.value } });
    };

    // ── Properties ───────────────────────────────────────────────────
    const allProperties     = ref([]);
    const loadingProperties = ref(false);
    const propError         = ref('');

    const PLACEHOLDER = 'https://placehold.co/600x400/1a1a2e/ffffff?text=No+Image';

    const normalizeImages = (p) => {  
      const raw = p.images;
      if (!raw || !Array.isArray(raw) || raw.length === 0) return [];
      return raw.map(img => {
        if (typeof img === 'string') return img;
        if (img && img.image_url) return img.image_url;
        if (img && img.url) return img.url;
        return null;
      }).filter(Boolean);
    };

    const getPrimaryImage = (p) => {
      const imgs = normalizeImages(p);
      return imgs.length > 0 ? imgs[0] : PLACEHOLDER;
    };

    const onImgError = (e) => { e.target.src = PLACEHOLDER; };

    const formatPrice = (price) => Number(parseFloat(price)).toLocaleString();
    const formatType  = (type) => ({ apartment: 'Apartment', house: 'House', condo: 'Condo' }[type] || type);

    // Show only first 3
    const discoverProperties = computed(() => allProperties.value.slice(0, 3));

    const fetchProperties = async () => {
      loadingProperties.value = true;
      propError.value = '';
      try {
        const res = await axios.get('http://127.0.0.1:8000/api/properties/');
        allProperties.value = res.data.map(p => ({
          id: p.id,
          title: p.title || 'No Title',
          description: p.description || '',
          location: p.location || 'Unknown',
          price: parseFloat(p.price) || 0,
          property_type: p.property_type || 'apartment',
          images: p.images && Array.isArray(p.images) ? p.images : [],
        }));
      } catch (e) {
        propError.value = 'Could not load properties.';
      } finally {
        loadingProperties.value = false;
      }
    };

    // ── Save / unsave ────────────────────────────────────────────────
    const getSaved = () => {
      try { return JSON.parse(localStorage.getItem('savedProperties') || '[]'); } catch { return []; }
    };
    const isSaved = (property) => getSaved().some(p => p.id === property.id);

    const toggleSave = (property) => {
      let saved = getSaved();
      const idx = saved.findIndex(p => p.id === property.id);
      if (idx > -1) saved.splice(idx, 1);
      else saved.push(property);
      localStorage.setItem('savedProperties', JSON.stringify(saved));
    };

    // ── Agencies ─────────────────────────────────────────────────────
    const agencies       = ref([]);
    const loadingAgencies = ref(false);
    const agencyError    = ref('');

    const fetchAgencies = async () => {
      loadingAgencies.value = true;
      agencyError.value = '';
      try {
        const res = await axios.get('http://127.0.0.1:8000/api/agents/');
        agencies.value = res.data.slice(0, 3).map(a => ({
          id: a.id,
          name: a.name || 'Agency',
          description: a.description || a.bio || '',
          phone: a.phone || '',
          email: a.email || '',
          location: a.location || '',
          logo: a.logo || a.logo_url || '',
        }));
      } catch (e) {
        // Fallback: extract agencies from properties if endpoint unavailable
        agencyError.value = 'Could not load agencies.';
      } finally {
        loadingAgencies.value = false;
      }
    };

    const goToProperties = () => router.push('/properties');

    onMounted(() => {
      fetchProperties();
      fetchAgencies();
    });

    return {
      location, type, category,
      showTypeDrop, showCatDrop,
      filteredTypeSuggestions, filteredCategorySuggestions,
      delayClose, search,
      loadingProperties, propError, discoverProperties,
      getPrimaryImage, onImgError, formatPrice, formatType,
      isSaved, toggleSave,
      agencies, loadingAgencies, agencyError,
      goToProperties,
    };
  }
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,300;1,400;1,600&family=DM+Sans:wght@300;400;500;600&display=swap');

/* ─── Reset / Base ──────────────────────────── */
.home-page {
  font-family: 'DM Sans', sans-serif;
  background: #f6f4f1;
  min-height: 100vh;
  color: #1c1c1c;
}

/* ─── HERO ──────────────────────────────────── */
.hero-section {
  position: relative;
  height: 92vh;
  min-height: 580px;
  overflow: hidden;
  margin: 0px 24px;
  border-radius: 30px;
}

.hero-bg {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center;
  filter: brightness(0.75);
}

/* Subtle grain overlay for luxury texture */
.hero-grain {
  position: absolute;
  inset: 0;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)' opacity='0.04'/%3E%3C/svg%3E");
  pointer-events: none;
  z-index: 1;
}

.hero-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(
    160deg,
    rgba(0,0,0,0.55) 0%,
    rgba(0,0,0,0.2)  50%,
    rgba(0,0,0,0.5)  100%
  );
  z-index: 2;
}

.hero-content {
  position: relative;
  z-index: 3;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
  padding: 40px 24px;
  color: #fff;
}

.hero-eyebrow {
  font-size: 11px;
  letter-spacing: 4px;
  font-weight: 600;
  color: rgba(255,255,255,0.7);
  margin-bottom: 18px;
  animation: fadeUp 0.8s ease both;
}

.hero-title {
  font-family: 'Cormorant Garamond', serif;
  font-size: clamp(52px, 8vw, 96px);
  font-weight: 300;
  line-height: 1.05;
  letter-spacing: -1px;
  color: #fff;
  margin: 0 0 20px;
  animation: fadeUp 0.9s ease 0.1s both;
}

.hero-title em {
  font-style: italic;
  font-weight: 300;
  color: #f2c4b8;
}

.hero-subtitle {
  font-size: 16px;
  font-weight: 300;
  color: rgba(255,255,255,0.82);
  line-height: 1.6;
  margin: 0 0 40px;
  animation: fadeUp 1s ease 0.2s both;
}

/* Search pill */
.search-pill {
  display: flex;
  align-items: center;
  background: rgba(255,255,255,0.97);
  border-radius: 60px;
  padding: 8px 8px 8px 20px;
  gap: 0;
  width: 100%;
  max-width: 840px;
  box-shadow: 0 20px 60px rgba(0,0,0,0.3);
  animation: fadeUp 1.1s ease 0.3s both;
}

.search-field {
  flex: 1;
  padding: 8px 16px;
  min-width: 0;
  text-align: left;
}

.search-field-label {
  display: block;
  font-size: 9px;
  letter-spacing: 2px;
  font-weight: 700;
  color: #b73f2a;
  margin-bottom: 3px;
}

.search-input {
  border: none;
  outline: none;
  background: transparent;
  font-family: 'DM Sans', sans-serif;
  font-size: 14px;
  color: #1c1c1c;
  width: 100%;
}

.search-input::placeholder { color: #bbb; }

.search-field--rel { position: relative; }

.suggest-drop {
  position: absolute;
  top: calc(100% + 10px);
  left: -8px;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 8px 30px rgba(0,0,0,0.12);
  overflow: hidden;
  z-index: 100;
  min-width: 200px;
}

.suggest-item {
  display: block;
  width: 100%;
  padding: 11px 16px;
  text-align: left;
  background: none;
  border: none;
  font-family: 'DM Sans', sans-serif;
  font-size: 14px;
  color: #333;
  cursor: pointer;
  transition: background 0.15s;
}

.suggest-item:hover { background: #f5f0ee; color: #b73f2a; }

.search-divider {
  width: 1px;
  height: 36px;
  background: #e5e5e5;
  flex-shrink: 0;
}

.search-btn {
  background: #b73f2a;
  color: #fff;
  border: none;
  border-radius: 50px;
  width: 52px;
  height: 52px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
  cursor: pointer;
  flex-shrink: 0;
  transition: background 0.2s, transform 0.2s;
}

.search-btn:hover { background: #9a3523; transform: scale(1.06); }

/* Trust strip */
.trust-strip {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-top: 28px;
  color: rgba(255,255,255,0.7);
  font-size: 13px;
  animation: fadeUp 1.2s ease 0.4s both;
}

.trust-item { display: flex; align-items: center; gap: 6px; }
.trust-item i { color: #f2c4b8; font-size: 12px; }
.trust-sep { color: rgba(255,255,255,0.3); }

@keyframes fadeUp {
  from { opacity: 0; transform: translateY(24px); }
  to   { opacity: 1; transform: translateY(0); }
}

/* ─── CONTENT SECTIONS ──────────────────────── */
.content-section {
  padding: 56px 32px;
}

.agencies-section {
  background: #fff;
}

.section-head {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  margin-bottom: 32px;
}

.section-eyebrow {
  font-size: 10px;
  letter-spacing: 3px;
  font-weight: 600;
  color: #b73f2a;
  margin: 0 0 6px;
}

.section-title {
  font-family: 'Cormorant Garamond', serif;
  font-size: 36px;
  font-weight: 600;
  color: #111;
  margin: 0;
}

.see-all-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  font-weight: 500;
  color: #1c1c1c;
  text-decoration: none;
  border-bottom: 1px solid #1c1c1c;
  padding-bottom: 2px;
  transition: color 0.2s, border-color 0.2s;
  white-space: nowrap;
}

.see-all-btn i { font-size: 11px; transition: transform 0.2s; }
.see-all-btn:hover { color: #b73f2a; border-color: #b73f2a; }
.see-all-btn:hover i { transform: translateX(4px); }

/* ─── Cards Grid ────────────────────────────── */
.cards-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
}

/* ─── Property Card ─────────────────────────── */
.prop-card {
  background: #fff;
  border-radius: 16px;
  overflow: hidden;
  cursor: pointer;
  transition: transform 0.25s, box-shadow 0.25s;
  box-shadow: 0 2px 12px rgba(0,0,0,0.06);
  display: flex;
  flex-direction: column;
}

.prop-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 16px 40px rgba(0,0,0,0.12);
}

.card-img-wrap {
  position: relative;
  height: 220px;
  overflow: hidden;
  background: #e8e4df;
}

.card-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
  transition: transform 0.4s ease;
}

.prop-card:hover .card-img { transform: scale(1.05); }

.card-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(to top, rgba(0,0,0,0.4) 0%, transparent 55%);
  pointer-events: none;
}

.status-badge {
  position: absolute;
  top: 12px;
  left: 12px;
  background: rgba(183,63,42,0.9);
  color: #fff;
  padding: 4px 10px;
  border-radius: 20px;
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 0.5px;
  text-transform: uppercase;
}

.heart-btn {
  position: absolute;
  top: 12px;
  right: 12px;
  background: rgba(255,255,255,0.92);
  border: none;
  border-radius: 50%;
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  font-size: 14px;
  color: #888;
  transition: all 0.2s;
}

.heart-btn:hover { background: #fff; transform: scale(1.1); }
.heart-btn .saved { color: #e53e3e; }

.card-body {
  padding: 16px 18px 18px;
  display: flex;
  flex-direction: column;
  gap: 8px;
  flex-grow: 1;
}

.card-title {
  font-family: 'Cormorant Garamond', serif;
  font-size: 18px;
  font-weight: 600;
  color: #111;
  margin: 0;
  line-height: 1.3;
}

.card-desc {
  font-size: 13px;
  color: #777;
  margin: 0;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  line-height: 1.5;
  flex-grow: 1;
}

.card-footer-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 10px;
  border-top: 1px solid #f0f0f0;
}

.card-location {
  font-size: 12px;
  color: #888;
  display: flex;
  align-items: center;
  gap: 4px;
}

.card-location i { color: #b73f2a; font-size: 11px; }

.card-price {
  font-family: 'Cormorant Garamond', serif;
  font-size: 18px;
  font-weight: 600;
  color: #b73f2a;
}

.card-price .mo { font-size: 12px; color: #aaa; font-family: 'DM Sans', sans-serif; font-weight: 400; }

/* ─── Agency Cards ──────────────────────────── */
.agency-card {
  background: #f9f8f6;
  border-radius: 16px;
  overflow: hidden;
  padding: 24px;
  display: flex;
  flex-direction: column;
  gap: 14px;
  border: 1px solid #ede9e4;
  transition: box-shadow 0.25s, transform 0.25s;
}

.agency-card:hover {
  box-shadow: 0 12px 36px rgba(0,0,0,0.08);
  transform: translateY(-4px);
}

.agency-logo-wrap {
  width: 64px;
  height: 64px;
  border-radius: 12px;
  overflow: hidden;
  background: #e8e4df;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.agency-logo { width: 100%; height: 100%; object-fit: cover; }

.agency-logo-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #b73f2a 0%, #d4614a 100%);
  color: #fff;
  font-size: 24px;
}

.agency-name {
  font-family: 'Cormorant Garamond', serif;
  font-size: 20px;
  font-weight: 600;
  color: #111;
  margin: 0;
}

.agency-desc {
  font-size: 13px;
  color: #777;
  margin: 0;
  line-height: 1.6;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.agency-meta { display: flex; flex-wrap: wrap; gap: 6px; margin-top: 4px; }

.agency-chip {
  display: flex;
  align-items: center;
  gap: 5px;
  padding: 5px 10px;
  background: #fff;
  border: 1px solid #e5e5e5;
  border-radius: 20px;
  font-size: 11.5px;
  color: #555;
}

.agency-chip i { color: #b73f2a; font-size: 10px; }

/* ─── Skeleton ──────────────────────────────── */
.skeleton-card {
  background: #fff;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 2px 12px rgba(0,0,0,0.06);
}

.skeleton-img {
  height: 220px;
  background: linear-gradient(90deg, #ececec 25%, #f5f5f5 50%, #ececec 75%);
  background-size: 200% 100%;
  animation: shimmer 1.4s infinite;
}

.skeleton-body { padding: 16px 18px; display: flex; flex-direction: column; gap: 10px; }

.skeleton-line {
  height: 12px;
  border-radius: 6px;
  background: linear-gradient(90deg, #ececec 25%, #f5f5f5 50%, #ececec 75%);
  background-size: 200% 100%;
  animation: shimmer 1.4s infinite;
}

.skeleton-line.short  { width: 40%; }
.skeleton-line.long   { width: 85%; }
.skeleton-line.medium { width: 60%; }

@keyframes shimmer {
  0%   { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}

.inline-error {
  padding: 24px;
  background: #fff5f5;
  border-radius: 12px;
  color: #b73f2a;
  font-size: 14px;
  display: flex;
  align-items: center;
  gap: 10px;
}

/* ─── FOOTER ────────────────────────────────── */
.site-footer {
  background: #111;
  color: #fff;
  padding: 60px 32px 0;
}

.footer-inner {
  display: grid;
  grid-template-columns: 2fr 1fr 1fr;
  gap: 48px;
  padding-bottom: 48px;
  border-bottom: 1px solid rgba(255,255,255,0.08);
}

.footer-brand-label {
  font-size: 11px;
  letter-spacing: 3px;
  font-weight: 600;
  color: #b73f2a;
  margin: 0 0 10px;
}

.footer-brand-desc {
  font-size: 14px;
  color: rgba(255,255,255,0.5);
  line-height: 1.7;
  margin: 0 0 20px;
  max-width: 280px;
}

.footer-socials { display: flex; gap: 10px; }

.social-icon {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  border: 1px solid rgba(255,255,255,0.15);
  display: flex;
  align-items: center;
  justify-content: center;
  color: rgba(255,255,255,0.6);
  text-decoration: none;
  font-size: 13px;
  transition: all 0.2s;
}

.social-icon:hover { border-color: #b73f2a; color: #b73f2a; }

.footer-col-label {
  font-size: 10px;
  letter-spacing: 2.5px;
  font-weight: 600;
  color: rgba(255,255,255,0.35);
  margin: 0 0 16px;
}

.footer-link {
  display: block;
  font-size: 14px;
  color: rgba(255,255,255,0.6);
  text-decoration: none;
  margin-bottom: 10px;
  transition: color 0.2s;
}

.footer-link:hover { color: #fff; }

.footer-contact-line {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13.5px;
  color: rgba(255,255,255,0.55);
  margin-bottom: 10px;
}

.footer-contact-line i { color: #b73f2a; font-size: 12px; }

.footer-bottom {
  padding: 20px 0;
  text-align: center;
  font-size: 12.5px;
  color: rgba(255,255,255,0.25);
}

/* ─── Responsive ────────────────────────────── */
.hide-sm { display: inline; }

@media (max-width: 900px) {
  .cards-grid { grid-template-columns: 1fr 1fr; }
  .footer-inner { grid-template-columns: 1fr 1fr; }
  .search-pill { flex-direction: column; border-radius: 20px; padding: 16px; gap: 10px; }
  .search-divider { display: none; }
  .search-field { padding: 4px 0; width: 100%; }
  .search-btn { width: 100%; border-radius: 12px; height: 46px; }
}

@media (max-width: 600px) {
  .hero-section { height: 100vh; margin: 12px; border-radius: 16px; }
  .hero-title { font-size: 42px; }
  .cards-grid { grid-template-columns: 1fr; }
  .footer-inner { grid-template-columns: 1fr; gap: 32px; }
  .content-section { padding: 40px 16px; }
  .section-title { font-size: 28px; }
  .hide-sm { display: none; }
  .trust-strip { flex-direction: column; gap: 8px; }
  .trust-sep { display: none; }
}
</style>