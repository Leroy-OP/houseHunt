<template>
  <div class="register-page">

    <!-- Left Panel — Form -->
    <div class="form-panel">
      <div class="form-panel-inner">

        <!-- Brand -->
        <router-link to="/" class="brand">
          <span class="brand-icon"><i class="fas fa-home"></i></span>
          <span class="brand-text">Hunter<em>Street</em></span>
        </router-link>

        <!-- ── Account Switcher ─────────────────────────────── -->
        <div class="account-switcher" v-if="storedAccounts.length > 0">
          <div class="switcher-header">
            <span class="switcher-label">
              <i class="fas fa-users"></i> Saved Accounts
            </span>
            <button class="switcher-add" @click="showNewForm = !showNewForm" :title="showNewForm ? 'Cancel' : 'Add new account'">
              <i :class="showNewForm ? 'fas fa-times' : 'fas fa-plus'"></i>
            </button>
          </div>

          <transition name="slide">
            <div class="account-list" v-if="!showNewForm">
              <div
                v-for="acc in storedAccounts"
                :key="acc.id"
                class="account-item"
                :class="{ active: acc.id === activeAccountId }"
              >
                <button class="account-info" @click="switchAccount(acc)">
                  <span class="account-avatar" :style="{ background: acc.avatarColor }">
                    {{ acc.initials }}
                  </span>
                  <span class="account-meta">
                    <strong>{{ acc.name }}</strong>
                    <small>{{ acc.email }}</small>
                  </span>
                  <span class="account-badge" :class="acc.accountType">
                    {{ acc.accountType }}
                  </span>
                  <span class="account-active-dot" v-if="acc.id === activeAccountId">
                    <i class="fas fa-check-circle"></i>
                  </span>
                </button>
                <button class="account-remove" @click.stop="removeAccount(acc.id)" title="Remove account">
                  <i class="fas fa-trash-alt"></i>
                </button>
              </div>

              <!-- Add another account nudge -->
              <button class="account-add-row" @click="showNewForm = true">
                <span class="add-icon"><i class="fas fa-user-plus"></i></span>
                <span>Register another account</span>
              </button>
            </div>
          </transition>
        </div>
        <!-- ─────────────────────────────────────────────────── -->

        <!-- Show form only if no accounts yet OR user wants to add another -->
        <transition name="fade">
          <div v-if="storedAccounts.length === 0 || showNewForm">

            <!-- Heading -->
            <div class="form-heading">
              <p class="form-eyebrow">GET STARTED</p>
              <h1 class="form-title">
                {{ storedAccounts.length > 0 ? 'Add another account' : 'Create your account' }}
              </h1>
              <p class="form-sub">Join thousands finding their perfect home in Nairobi.</p>
            </div>

            <!-- Alerts -->
            <transition name="fade">
              <div v-if="apiError" class="alert alert-error" style="margin-top: 16px;">
                <i class="fas fa-exclamation-circle"></i> {{ apiError }}
              </div>
            </transition>
            <transition name="fade">
              <div v-if="successMessage" class="alert alert-success" style="margin-top: 16px;">
                <i class="fas fa-check-circle"></i> {{ successMessage }}
              </div>
            </transition>

            <!-- Form -->
            <form @submit.prevent="handleRegister" class="reg-form" novalidate style="margin-top: 16px;">

              <!-- Full name -->
              <div class="field-row two-col">
                <div class="field-group" :class="{ error: errors.fullName }">
                  <label class="field-label">Full Name</label>
                  <div class="field-wrap">
                    <i class="fas fa-user field-icon"></i>
                    <input type="text" v-model="form.fullName" placeholder="Jane Wanjiku" class="field-input" />
                  </div>
                  <span class="field-error" v-if="errors.fullName">{{ errors.fullName }}</span>
                </div>

                <div class="field-group" :class="{ error: errors.phone }">
                  <label class="field-label">Phone Number</label>
                  <div class="field-wrap">
                    <i class="fas fa-phone field-icon"></i>
                    <input type="tel" v-model="form.phone" placeholder="+254 7XX XXX XXX" class="field-input" />
                  </div>
                  <span class="field-error" v-if="errors.phone">{{ errors.phone }}</span>
                </div>
              </div>

              <!-- Email -->
              <div class="field-group" :class="{ error: errors.email }">
                <label class="field-label">Email Address</label>
                <div class="field-wrap">
                  <i class="fas fa-envelope field-icon"></i>
                  <input type="email" v-model="form.email" placeholder="you@example.com" class="field-input" />
                </div>
                <span class="field-error" v-if="errors.email">{{ errors.email }}</span>
              </div>

              <!-- Password -->
              <div class="field-row two-col">
                <div class="field-group" :class="{ error: errors.password }">
                  <label class="field-label">Password</label>
                  <div class="field-wrap">
                    <i class="fas fa-lock field-icon"></i>
                    <input
                      :type="showPassword ? 'text' : 'password'"
                      v-model="form.password"
                      placeholder="Min. 8 characters"
                      class="field-input"
                    />
                    <button type="button" class="eye-btn" @click="showPassword = !showPassword">
                      <i :class="showPassword ? 'fas fa-eye-slash' : 'fas fa-eye'"></i>
                    </button>
                  </div>
                  <!-- Strength bar -->
                  <div class="strength-wrap" v-if="form.password">
                    <div class="strength-bar">
                      <div class="strength-fill" :class="passwordStrength" :style="strengthWidth"></div>
                    </div>
                    <span class="strength-label" :class="passwordStrength">{{ passwordStrengthText }}</span>
                  </div>
                  <span class="field-error" v-if="errors.password">{{ errors.password }}</span>
                </div>

                <div class="field-group" :class="{ error: errors.confirmPassword }">
                  <label class="field-label">Confirm Password</label>
                  <div class="field-wrap">
                    <i class="fas fa-lock field-icon"></i>
                    <input
                      :type="showConfirmPassword ? 'text' : 'password'"
                      v-model="form.confirmPassword"
                      placeholder="Repeat password"
                      class="field-input"
                    />
                    <button type="button" class="eye-btn" @click="showConfirmPassword = !showConfirmPassword">
                      <i :class="showConfirmPassword ? 'fas fa-eye-slash' : 'fas fa-eye'"></i>
                    </button>
                  </div>
                  <span class="field-error" v-if="errors.confirmPassword">{{ errors.confirmPassword }}</span>
                </div>
              </div>

              <!-- Account type -->
              <div class="field-group" :class="{ error: errors.accountType }">
                <label class="field-label">I am a…</label>
                <div class="type-group">
                  <label class="type-option" :class="{ selected: form.accountType === 'tenant' }">
                    <input type="radio" v-model="form.accountType" value="tenant" />
                    <span class="type-icon"><i class="fas fa-search"></i></span>
                    <span class="type-info">
                      <strong>Tenant</strong>
                      <small>Looking for a rental property</small>
                    </span>
                    <span class="type-check"><i class="fas fa-check"></i></span>
                  </label>
                  <label class="type-option" :class="{ selected: form.accountType === 'agent' }">
                    <input type="radio" v-model="form.accountType" value="agent" />
                    <span class="type-icon"><i class="fas fa-briefcase"></i></span>
                    <span class="type-info">
                      <strong>Agent</strong>
                      <small>Listing properties</small>
                    </span>
                    <span class="type-check"><i class="fas fa-check"></i></span>
                  </label>
                </div>
                <span class="field-error" v-if="errors.accountType">{{ errors.accountType }}</span>
              </div>

              <!-- Terms -->
              <div class="field-group" :class="{ error: errors.agreeTerms }">
                <label class="terms-row">
                  <span class="custom-check" :class="{ checked: form.agreeTerms }">
                    <input type="checkbox" v-model="form.agreeTerms" />
                    <i class="fas fa-check"></i>
                  </span>
                  <span class="terms-text">
                    I agree to the
                    <a href="#" @click.prevent>Terms &amp; Conditions</a>
                    and
                    <a href="#" @click.prevent>Privacy Policy</a>
                  </span>
                </label>
                <span class="field-error" v-if="errors.agreeTerms">{{ errors.agreeTerms }}</span>
              </div>

              <!-- Submit -->
              <button type="submit" class="submit-btn" :disabled="loading">
                <span v-if="loading"><i class="fas fa-spinner fa-spin"></i>&nbsp; Creating Account…</span>
                <span v-else>Create Account <i class="fas fa-arrow-right"></i></span>
              </button>

            </form>

            <!-- Divider -->
            <div class="or-divider" style="margin-top: 20px;"><span>or sign up with</span></div>

            <!-- Social -->
            <div class="social-row" style="margin-top: 12px;">
              <button class="social-btn" @click="registerWithGoogle" title="Google">
                <i class="fab fa-google"></i><span>Google</span>
              </button>
              <button class="social-btn" @click="registerWithFacebook" title="Facebook">
                <i class="fab fa-facebook-f"></i><span>Facebook</span>
              </button>
              <button class="social-btn" @click="registerWithGithub" title="GitHub">
                <i class="fab fa-github"></i><span>GitHub</span>
              </button>
            </div>

            <!-- Login link -->
            <p class="login-cta" style="margin-top: 16px;">
              Already have an account?
              <router-link to="/login">Sign in here</router-link>
            </p>

          </div>
        </transition>

      </div>
    </div>

    <!-- Right Panel — Visual -->
    <div class="visual-panel">
      <div class="visual-overlay"></div>
      <div class="visual-content">
        <p class="visual-eyebrow">HUNTER STREET</p>
        <h2 class="visual-title">Your home<br/><em>awaits.</em></h2>
        <p class="visual-sub">
          Trusted by thousands of Nairobians finding<br/>their perfect space.
        </p>

        <div class="benefit-list">
          <div class="benefit-item" v-for="b in benefits" :key="b.text">
            <span class="benefit-icon"><i :class="b.icon"></i></span>
            <span>{{ b.text }}</span>
          </div>
        </div>

        <!-- Floating stat cards -->
        <div class="stat-cards">
          <div class="stat-card">
            <span class="stat-num">500+</span>
            <span class="stat-label">Active Listings</span>
          </div>
          <div class="stat-card">
            <span class="stat-num">98%</span>
            <span class="stat-label">Satisfaction Rate</span>
          </div>
          <div class="stat-card">
            <span class="stat-num">180+</span>
            <span class="stat-label">Trusted Agencies</span>
          </div>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';

// ─────────────────────────────────────────────────────────────────
//  Constants
// ─────────────────────────────────────────────────────────────────
const LS_ACCOUNTS    = 'hs_accounts';   // array of all stored accounts
const LS_ACTIVE      = 'hs_active_id';  // id of the currently active account

/*
 * FLAT KEYS — these are the keys that every other page in the app reads with
 * localStorage.getItem(). We write to them every time an account becomes active
 * so those pages always find a valid token and user object, never null.
 */
const LS_TOKEN        = 'authToken';         // flat access token  (read by buildAuthHeaders)
const LS_ACCESS_TOKEN = 'access_token';  // alias              (read by buildAuthHeaders)
const LS_REFRESH      = 'refresh_token'; // flat refresh token
const LS_CURRENT_USER = 'currentUser';   // flat user object   (read by agent page)

const AVATAR_COLORS = [
  '#b73f2a','#2d6a4f','#2b5a9e','#7b3fa0',
  '#c07a1b','#1a6d7a','#8b2252','#3d6b32',
];

const router  = useRouter();
const benefits = [
  { icon: 'fas fa-search',         text: 'Smart property search'   },
  { icon: 'fas fa-heart',          text: 'Save your favourites'    },
  { icon: 'fas fa-calendar-check', text: 'Book viewings instantly' },
  { icon: 'fas fa-headset',        text: '24/7 customer support'   },
];

// ─────────────────────────────────────────────────────────────────
//  Multi-account state (persisted in localStorage)
// ─────────────────────────────────────────────────────────────────
const storedAccounts  = ref([]);
const activeAccountId = ref(null);
const showNewForm     = ref(false);

onMounted(() => {
  storedAccounts.value  = readAccounts();
  activeAccountId.value = localStorage.getItem(LS_ACTIVE) || null;
  applyActiveSession();   // restore token + currentUser for this page load
});

// ─────────────────────────────────────────────────────────────────
//  localStorage helpers
// ─────────────────────────────────────────────────────────────────
function readAccounts() {
  try { return JSON.parse(localStorage.getItem(LS_ACCOUNTS) || '[]'); }
  catch { return []; }
}

function saveAccounts(list) {
  localStorage.setItem(LS_ACCOUNTS, JSON.stringify(list));
  storedAccounts.value = list;
}

function getInitials(name = '') {
  return name.trim().split(/\s+/).slice(0, 2)
    .map(w => w[0]?.toUpperCase() ?? '').join('');
}

function pickColor(email = '') {
  let h = 0;
  for (let i = 0; i < email.length; i++) h = (h * 31 + email.charCodeAt(i)) | 0;
  return AVATAR_COLORS[Math.abs(h) % AVATAR_COLORS.length];
}

/**
 * Write ALL the flat keys that the rest of the app expects.
 *
 * This is the single most important function for fixing the null problem:
 * every page that calls localStorage.getItem('token'), getItem('access_token'),
 * or getItem('currentUser') will now always find a value after login/register.
 */
function writeFlatSession(acc) {
  if (!acc) {
    // Clear everything on logout / last account removed
    localStorage.removeItem(LS_TOKEN);
    localStorage.removeItem(LS_ACCESS_TOKEN);
    localStorage.removeItem(LS_REFRESH);
    localStorage.removeItem(LS_CURRENT_USER);
    delete axios.defaults.headers.common['Authorization'];
    return;
  }

  // Write token under both common key names so any page finds it
  localStorage.setItem(LS_TOKEN,        acc.token);
  localStorage.setItem(LS_ACCESS_TOKEN, acc.token);

  if (acc.refreshToken) {
    localStorage.setItem(LS_REFRESH, acc.refreshToken);
  }

  // Write the user object that pages read via JSON.parse(localStorage.getItem('currentUser'))
  const userPayload = {
    id:          acc.id,
    name:        acc.name,
    email:       acc.email,
    phone:       acc.phone,
    accountType: acc.accountType,
  };
  localStorage.setItem(LS_CURRENT_USER, JSON.stringify(userPayload));

  // Also set axios default header for any requests made from this page
  axios.defaults.headers.common['Authorization'] = `Bearer ${acc.token}`;
}

/** Make an account active: update the pointer key + write all flat keys */
function setActive(id) {
  activeAccountId.value = id;
  localStorage.setItem(LS_ACTIVE, id);
  const acc = readAccounts().find(a => a.id === id) || null;
  writeFlatSession(acc);
}

/** On page load, re-apply the active account's session data */
function applyActiveSession() {
  if (!activeAccountId.value) return;
  const acc = storedAccounts.value.find(a => a.id === activeAccountId.value);
  if (acc) writeFlatSession(acc);
}

/** Persist a newly registered account then make it active */
function persistAccount({ id, name, email, phone, accountType, token, refreshToken }) {
  const existing = readAccounts();
  const entry = {
    id,
    name,
    email,
    phone,
    accountType,
    token,
    refreshToken: refreshToken || null,
    initials:     getInitials(name),
    avatarColor:  pickColor(email),
    addedAt:      new Date().toISOString(),
  };

  // Replace if same email already stored, otherwise append
  const idx = existing.findIndex(a => a.email === email);
  if (idx >= 0) existing[idx] = entry;
  else          existing.push(entry);

  saveAccounts(existing);
  setActive(id);   // <-- writes all flat keys + axios header
}

// ─────────────────────────────────────────────────────────────────
//  Public account actions
// ─────────────────────────────────────────────────────────────────

/** Switch active account from the switcher UI */
function switchAccount(acc) {
  setActive(acc.id);   // writes flat keys for the switched-to account
  const dest = acc.accountType === 'agent' ? '/agents' : '/properties';
  router.push(dest);
}

/** Remove a stored account */
function removeAccount(id) {
  const updated = storedAccounts.value.filter(a => a.id !== id);
  saveAccounts(updated);

  if (id === activeAccountId.value) {
    if (updated.length > 0) {
      setActive(updated[0].id);
    } else {
      activeAccountId.value = null;
      localStorage.removeItem(LS_ACTIVE);
      writeFlatSession(null);   // clears all flat keys
    }
  }
}

// ─────────────────────────────────────────────────────────────────
//  Form state
// ─────────────────────────────────────────────────────────────────
const form = ref({
  fullName: '', email: '', phone: '',
  password: '', confirmPassword: '',
  accountType: 'tenant', agreeTerms: false,
});

const errors = ref({
  fullName: '', email: '', phone: '',
  password: '', confirmPassword: '',
  accountType: '', agreeTerms: '',
});

const loading             = ref(false);
const apiError            = ref('');
const successMessage      = ref('');
const showPassword        = ref(false);
const showConfirmPassword = ref(false);

// ── Password strength ─────────────────────────────────────────────
const passwordStrength = computed(() => {
  const p = form.value.password;
  if (!p) return 'weak';
  let s = 0;
  if (p.length >= 8)  s++;
  if (p.length >= 12) s++;
  if (/[a-z]/.test(p) && /[A-Z]/.test(p)) s++;
  if (/\d/.test(p))           s++;
  if (/[!@#$%^&*]/.test(p))  s++;
  if (s <= 2) return 'weak';
  if (s <= 3) return 'fair';
  if (s <= 4) return 'good';
  return 'strong';
});

const passwordStrengthText = computed(() =>
  ({ weak: 'Weak', fair: 'Fair', good: 'Good', strong: 'Strong' }[passwordStrength.value])
);

const strengthWidth = computed(() =>
  ({ weak: 'width:25%', fair: 'width:50%', good: 'width:75%', strong: 'width:100%' }[passwordStrength.value])
);

// ── Validation ────────────────────────────────────────────────────
const validateForm = () => {
  errors.value = {
    fullName: '', email: '', phone: '',
    password: '', confirmPassword: '',
    accountType: '', agreeTerms: '',
  };
  let ok = true;
  const set = (k, msg) => { errors.value[k] = msg; ok = false; };

  if (!form.value.fullName.trim() || form.value.fullName.trim().length < 3)
    set('fullName', 'Please enter your full name (min 3 chars)');
  if (!form.value.email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.value.email))
    set('email', 'Enter a valid email address');
  if (!form.value.phone || !/^\d{10,}$/.test(form.value.phone.replace(/\D/g, '')))
    set('phone', 'Enter a valid phone number');
  if (!form.value.password || form.value.password.length < 8)
    set('password', 'Password must be at least 8 characters');
  if (form.value.password !== form.value.confirmPassword)
    set('confirmPassword', 'Passwords do not match');
  if (!form.value.agreeTerms)
    set('agreeTerms', 'You must accept the terms and conditions');

  // Duplicate email guard
  if (storedAccounts.value.some(a => a.email === form.value.email))
    set('email', 'This email is already saved — switch to it above');

  return ok;
};

// ── Submit ────────────────────────────────────────────────────────
const handleRegister = async () => {
  if (!validateForm()) return;
  loading.value        = true;
  apiError.value       = '';
  successMessage.value = '';

  try {
    const { data } = await axios.post('http://127.0.0.1:8000/api/register/', {
      first_name:   form.value.fullName.split(' ')[0],
      last_name:    form.value.fullName.split(' ').slice(1).join(' '),
      email:        form.value.email,
      phone:        form.value.phone,
      password:     form.value.password,
      account_type: form.value.accountType,
    });

    /*
     * Handle both common Django JWT response shapes:
     *   { access: "eyJ…", refresh: "eyJ…", user: { id, … } }
     *   { token:  "eyJ…", user: { id, … } }
     */
    const token        = data.access  ?? data.token  ?? null;
    const refreshToken = data.refresh ?? null;
    const userId       = data.user?.id ?? data.id ?? crypto.randomUUID();

    if (!token) throw new Error('NO_TOKEN');

    const accountType = form.value.accountType;  // capture before reset

    persistAccount({
      id:           String(userId),
      name:         form.value.fullName,
      email:        form.value.email,
      phone:        form.value.phone,
      accountType,
      token,
      refreshToken,
    });
    // ↑ persistAccount → setActive → writeFlatSession
    //   At this point localStorage now contains:
    //     'token'        → "eyJ…"
    //     'access_token' → "eyJ…"
    //     'refresh_token'→ "eyJ…"  (if returned)
    //     'currentUser'  → JSON with id, name, email, phone, accountType
    //     'hs_active_id' → userId
    //     'hs_accounts'  → full account array

    successMessage.value = 'Account created! Redirecting…';

    setTimeout(() => {
      showNewForm.value = false;
      form.value = {
        fullName: '', email: '', phone: '',
        password: '', confirmPassword: '',
        accountType: 'buyer', agreeTerms: false,
      };
      router.push(accountType === 'agent' ? '/agents' : '/properties');
    }, 1500);

  } catch (e) {
    if (e.message === 'NO_TOKEN') {
      apiError.value = 'Server did not return an auth token. Check your backend.';
    } else if (e.response?.data?.email) {
      apiError.value = 'That email is already registered.';
    } else if (e.response?.data?.phone) {
      apiError.value = 'That phone number is already in use.';
    } else {
      apiError.value = 'Registration failed. Please try again.';
    }
  } finally {
    loading.value = false;
  }
};

const registerWithGoogle   = () => { apiError.value = 'Google sign-up coming soon.';   };
const registerWithFacebook = () => { apiError.value = 'Facebook sign-up coming soon.'; };
const registerWithGithub   = () => { apiError.value = 'GitHub sign-up coming soon.';   };
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,300;1,400;1,600&family=DM+Sans:wght@300;400;500;600&display=swap');

/* ─── Layout ────────────────────────────────── */
.register-page {
  display: flex;
  min-height: 100vh;
  font-family: 'DM Sans', sans-serif;
}

/* ─── Form Panel ────────────────────────────── */
.form-panel {
  flex: 1;
  background: #f6f4f1;
  display: flex;
  align-items: flex-start;
  justify-content: center;
  padding: 48px 32px;
  overflow-y: auto;
}

.form-panel-inner {
  width: 100%;
  max-width: 560px;
  display: flex;
  flex-direction: column;
  gap: 24px;
}

/* Brand */
.brand {
  display: inline-flex;
  align-items: center;
  gap: 9px;
  text-decoration: none;
  margin-bottom: 4px;
}
.brand-icon {
  width: 34px; height: 34px;
  background: #b73f2a;
  border-radius: 8px;
  display: flex; align-items: center; justify-content: center;
  color: #fff; font-size: 14px;
}
.brand-text { font-family: 'Cormorant Garamond', serif; font-size: 22px; font-weight: 600; color: #1c1c1c; }
.brand-text em { font-style: italic; color: #b73f2a; }

/* ─── Account Switcher ──────────────────────── */
.account-switcher {
  background: #fff;
  border: 1.5px solid #e0dcd8;
  border-radius: 14px;
  overflow: hidden;
}

.switcher-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 14px 16px;
  border-bottom: 1px solid #f0ece8;
}

.switcher-label {
  font-size: 11px;
  letter-spacing: 1.5px;
  text-transform: uppercase;
  font-weight: 700;
  color: #aaa;
  display: flex;
  align-items: center;
  gap: 7px;
}

.switcher-add {
  width: 28px; height: 28px;
  border-radius: 7px;
  border: 1.5px solid #e0dcd8;
  background: transparent;
  color: #888;
  cursor: pointer;
  display: flex; align-items: center; justify-content: center;
  font-size: 12px;
  transition: all 0.2s;
}
.switcher-add:hover { border-color: #b73f2a; color: #b73f2a; background: rgba(183,63,42,0.05); }

.account-list { display: flex; flex-direction: column; }

.account-item {
  display: flex;
  align-items: center;
  border-bottom: 1px solid #f6f4f1;
  transition: background 0.15s;
}
.account-item:last-child { border-bottom: none; }
.account-item:hover { background: #fdfcfb; }
.account-item.active { background: rgba(183,63,42,0.03); }

.account-info {
  flex: 1;
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px 16px;
  background: none;
  border: none;
  cursor: pointer;
  text-align: left;
  min-width: 0;
}

.account-avatar {
  width: 38px; height: 38px;
  border-radius: 10px;
  display: flex; align-items: center; justify-content: center;
  font-size: 14px;
  font-weight: 700;
  color: #fff;
  flex-shrink: 0;
  letter-spacing: 0;
}

.account-meta {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-width: 0;
}
.account-meta strong { font-size: 13.5px; color: #111; font-weight: 600; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.account-meta small  { font-size: 12px; color: #999; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }

.account-badge {
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 1px;
  text-transform: uppercase;
  padding: 3px 8px;
  border-radius: 20px;
  flex-shrink: 0;
}
.account-badge.tenant { background: rgba(44,90,160,0.1); color: #2b5a9e; }
.account-badge.agent { background: rgba(45,106,79,0.1); color: #2d6a4f; }

.account-active-dot {
  color: #b73f2a;
  font-size: 15px;
  flex-shrink: 0;
  margin-left: 6px;
}

.account-remove {
  padding: 14px 16px;
  background: none;
  border: none;
  color: #ccc;
  cursor: pointer;
  font-size: 13px;
  transition: color 0.2s;
  flex-shrink: 0;
}
.account-remove:hover { color: #e53e3e; }

.account-add-row {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 13px 16px;
  width: 100%;
  background: none;
  border: none;
  border-top: 1px dashed #e8e4e0;
  color: #b73f2a;
  font-family: 'DM Sans', sans-serif;
  font-size: 13.5px;
  font-weight: 600;
  cursor: pointer;
  text-align: left;
  transition: background 0.2s;
}
.account-add-row:hover { background: rgba(183,63,42,0.04); }
.add-icon {
  width: 28px; height: 28px;
  border-radius: 7px;
  background: rgba(183,63,42,0.1);
  display: flex; align-items: center; justify-content: center;
  font-size: 13px;
}

/* ─── Heading ───────────────────────────────── */
.form-eyebrow {
  font-size: 10px; letter-spacing: 3px; font-weight: 600; color: #b73f2a; margin: 0 0 8px;
}
.form-title {
  font-family: 'Cormorant Garamond', serif;
  font-size: 38px; font-weight: 600; color: #111; margin: 0 0 8px; line-height: 1.1;
}
.form-title em { font-style: italic; color: #b73f2a; }
.form-sub { font-size: 14px; color: #888; margin: 0; }

/* Alerts */
.alert {
  padding: 13px 16px; border-radius: 10px;
  display: flex; align-items: center; gap: 10px; font-size: 13.5px;
}
.alert-error   { background: #fff5f5; color: #b73f2a; border: 1px solid rgba(183,63,42,0.2); }
.alert-success { background: #f0faf4; color: #2d6a4f; border: 1px solid rgba(45,106,79,0.2); }

/* Form */
.reg-form { display: flex; flex-direction: column; gap: 18px; }

.field-row.two-col { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
.field-group { display: flex; flex-direction: column; gap: 6px; }
.field-label {
  font-size: 11px; letter-spacing: 1.5px; text-transform: uppercase; font-weight: 600; color: #888;
}
.field-wrap { position: relative; display: flex; align-items: center; }
.field-icon {
  position: absolute; left: 14px; font-size: 14px; color: #bbb; pointer-events: none; transition: color 0.2s;
}
.field-input {
  width: 100%; padding: 12px 42px 12px 40px;
  border: 1.5px solid #e0dcd8; border-radius: 10px;
  font-family: 'DM Sans', sans-serif; font-size: 14px; color: #1c1c1c;
  background: #fff; outline: none; transition: border-color 0.2s, box-shadow 0.2s;
}
.field-input::placeholder { color: #c0bbb6; }
.field-input:focus { border-color: #b73f2a; box-shadow: 0 0 0 3px rgba(183,63,42,0.1); }
.field-wrap:focus-within .field-icon { color: #b73f2a; }
.field-group.error .field-input { border-color: #e53e3e; }
.field-group.error .field-input:focus { box-shadow: 0 0 0 3px rgba(229,62,62,0.1); }
.field-error { font-size: 12px; color: #e53e3e; font-weight: 500; }

.eye-btn {
  position: absolute; right: 12px; background: none; border: none;
  color: #bbb; cursor: pointer; font-size: 14px; padding: 4px; transition: color 0.2s;
}
.eye-btn:hover { color: #b73f2a; }

/* Strength */
.strength-wrap { display: flex; align-items: center; gap: 10px; margin-top: 2px; }
.strength-bar { flex: 1; height: 4px; background: #e8e4e0; border-radius: 2px; overflow: hidden; }
.strength-fill { height: 100%; border-radius: 2px; transition: width 0.4s ease, background-color 0.4s ease; }
.strength-fill.weak   { background: #e53e3e; }
.strength-fill.fair   { background: #dd9b17; }
.strength-fill.good   { background: #3182ce; }
.strength-fill.strong { background: #38a169; }
.strength-label { font-size: 11px; font-weight: 600; letter-spacing: 0.5px; white-space: nowrap; }
.strength-label.weak   { color: #e53e3e; }
.strength-label.fair   { color: #dd9b17; }
.strength-label.good   { color: #3182ce; }
.strength-label.strong { color: #38a169; }

/* Account type */
.type-group { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
.type-option {
  position: relative; display: flex; align-items: center; gap: 12px;
  padding: 14px 16px; border: 1.5px solid #e0dcd8; border-radius: 12px;
  cursor: pointer; background: #fff; transition: border-color 0.2s, background 0.2s;
}
.type-option input[type="radio"] { display: none; }
.type-option.selected { border-color: #b73f2a; background: rgba(183,63,42,0.04); }
.type-icon {
  width: 38px; height: 38px; border-radius: 8px; background: #f0ede9;
  display: flex; align-items: center; justify-content: center;
  font-size: 15px; color: #b73f2a; flex-shrink: 0; transition: background 0.2s;
}
.type-option.selected .type-icon { background: rgba(183,63,42,0.12); }
.type-info { flex: 1; }
.type-info strong { display: block; font-size: 13.5px; color: #111; font-weight: 600; }
.type-info small  { display: block; font-size: 11.5px; color: #999; margin-top: 2px; }
.type-check {
  width: 20px; height: 20px; border-radius: 50%; background: #b73f2a;
  color: #fff; display: flex; align-items: center; justify-content: center;
  font-size: 10px; opacity: 0; transform: scale(0.5); transition: opacity 0.2s, transform 0.2s;
}
.type-option.selected .type-check { opacity: 1; transform: scale(1); }

/* Terms */
.terms-row { display: flex; align-items: flex-start; gap: 10px; cursor: pointer; }
.custom-check {
  width: 20px; height: 20px; border: 1.5px solid #ccc; border-radius: 5px;
  display: flex; align-items: center; justify-content: center;
  flex-shrink: 0; margin-top: 1px; transition: all 0.2s;
}
.custom-check input[type="checkbox"] { display: none; }
.custom-check i { font-size: 10px; color: #fff; opacity: 0; transition: opacity 0.2s; }
.custom-check.checked { background: #b73f2a; border-color: #b73f2a; }
.custom-check.checked i { opacity: 1; }
.terms-text { font-size: 13.5px; color: #666; line-height: 1.5; }
.terms-text a { color: #b73f2a; text-decoration: none; font-weight: 500; }
.terms-text a:hover { text-decoration: underline; }

/* Submit */
.submit-btn {
  padding: 14px; background: #b73f2a; color: #fff;
  border: none; border-radius: 10px;
  font-family: 'DM Sans', sans-serif; font-size: 15px; font-weight: 600;
  cursor: pointer; display: flex; align-items: center; justify-content: center;
  gap: 8px; transition: background 0.2s, transform 0.2s, box-shadow 0.2s;
  letter-spacing: 0.3px; margin-top: 4px;
}
.submit-btn:hover:not(:disabled) {
  background: #9a3523; transform: translateY(-2px); box-shadow: 0 10px 28px rgba(183,63,42,0.28);
}
.submit-btn:disabled { opacity: 0.65; cursor: not-allowed; }

/* Divider */
.or-divider { display: flex; align-items: center; gap: 12px; color: #bbb; font-size: 13px; }
.or-divider::before, .or-divider::after { content: ''; flex: 1; height: 1px; background: #e0dcd8; }

/* Social */
.social-row { display: flex; gap: 10px; }
.social-btn {
  flex: 1; padding: 11px 14px; border: 1.5px solid #e0dcd8; border-radius: 10px;
  background: #fff; font-family: 'DM Sans', sans-serif; font-size: 13px;
  font-weight: 500; color: #444; cursor: pointer;
  display: flex; align-items: center; justify-content: center; gap: 8px; transition: all 0.2s;
}
.social-btn:hover { border-color: #b73f2a; color: #b73f2a; background: rgba(183,63,42,0.04); transform: translateY(-1px); }
.social-btn i { font-size: 15px; }

/* Login CTA */
.login-cta { text-align: center; font-size: 14px; color: #888; margin: 0; }
.login-cta a { color: #b73f2a; font-weight: 600; text-decoration: none; }
.login-cta a:hover { text-decoration: underline; }

/* ─── Visual Panel ──────────────────────────── */
.visual-panel {
  width: 42%; max-width: 560px; position: relative; background: #111;
  overflow: hidden; display: flex; align-items: center; justify-content: center;
  background-image:
    url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='60' height='60'%3E%3Cpath d='M0 0h60v60H0z' fill='none'/%3E%3Cpath d='M30 0v60M0 30h60' stroke='rgba(255,255,255,0.03)' stroke-width='1'/%3E%3C/svg%3E"),
    linear-gradient(145deg, #1a0e0b 0%, #2d1510 40%, #1c0e0b 100%);
}
.visual-overlay {
  position: absolute; inset: 0;
  background:
    radial-gradient(ellipse at 20% 20%, rgba(183,63,42,0.35) 0%, transparent 60%),
    radial-gradient(ellipse at 80% 80%, rgba(120,30,15,0.25) 0%, transparent 60%);
  pointer-events: none;
}
.visual-content {
  position: relative; z-index: 2; padding: 56px 48px;
  color: #fff; max-width: 420px;
  display: flex; flex-direction: column; gap: 20px;
}
.visual-eyebrow { font-size: 10px; letter-spacing: 4px; font-weight: 600; color: rgba(242,196,184,0.8); margin: 0; }
.visual-title {
  font-family: 'Cormorant Garamond', serif;
  font-size: clamp(40px, 4vw, 58px); font-weight: 300; line-height: 1.1; color: #fff; margin: 0;
}
.visual-title em { font-style: italic; color: #f2c4b8; font-weight: 300; }
.visual-sub { font-size: 14.5px; color: rgba(255,255,255,0.6); line-height: 1.7; margin: 0; }

.benefit-list { display: flex; flex-direction: column; gap: 12px; margin-top: 8px; }
.benefit-item { display: flex; align-items: center; gap: 14px; font-size: 14px; color: rgba(255,255,255,0.82); }
.benefit-icon {
  width: 32px; height: 32px; background: rgba(183,63,42,0.25); border-radius: 8px;
  display: flex; align-items: center; justify-content: center;
  font-size: 13px; color: #f2c4b8; flex-shrink: 0;
}

.stat-cards { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; margin-top: 16px; }
.stat-card {
  background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.1);
  border-radius: 12px; padding: 16px 12px;
  display: flex; flex-direction: column; align-items: center; gap: 4px; backdrop-filter: blur(8px);
}
.stat-num { font-family: 'Cormorant Garamond', serif; font-size: 24px; font-weight: 600; color: #f2c4b8; }
.stat-label { font-size: 11px; color: rgba(255,255,255,0.45); text-align: center; line-height: 1.3; }

/* ─── Transitions ───────────────────────────── */
.fade-enter-active, .fade-leave-active { transition: opacity 0.3s ease; }
.fade-enter-from,  .fade-leave-to      { opacity: 0; }

.slide-enter-active, .slide-leave-active { transition: all 0.25s ease; }
.slide-enter-from  { opacity: 0; transform: translateY(-8px); }
.slide-leave-to    { opacity: 0; transform: translateY(-8px); }

/* ─── Responsive ────────────────────────────── */
@media (max-width: 960px) {
  .visual-panel { display: none; }
  .form-panel   { padding: 32px 20px; }
}
@media (max-width: 540px) {
  .field-row.two-col { grid-template-columns: 1fr; }
  .type-group        { grid-template-columns: 1fr; }
  .stat-cards        { grid-template-columns: 1fr 1fr; }
  .form-title        { font-size: 30px; }
  .social-row        { flex-direction: column; }
}
</style>