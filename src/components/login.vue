<template>
  <div class="login-page">

    <!-- Left Panel — Visual -->
    <div class="visual-panel">
      <div class="visual-overlay"></div>
      <div class="visual-content">
        <router-link to="/" class="visual-brand">
          <span class="brand-icon"><i class="fas fa-home"></i></span>
          <span class="brand-text">Hunter<em>Street</em></span>
        </router-link>

        <div class="visual-copy">
          <p class="visual-eyebrow">WELCOME BACK</p>
          <h2 class="visual-title">Your next<br/><em>home awaits.</em></h2>
          <p class="visual-sub">
            Sign in to access your saved properties,<br/>
            bookings and personalised listings.
          </p>
        </div>

        <div class="testimonial-card">
          <p class="testimonial-text">
            "Found my dream apartment in Masai Lodge within a week. The process was seamless."
          </p>
          <div class="testimonial-author">
            <div class="testimonial-avatar">DR</div>
            <div>
              <p class="testimonial-name">Deborah Rotich</p>
              <p class="testimonial-role">Verified Tenant</p>
            </div>
          </div>
          <div class="testimonial-stars">
            <i class="fas fa-star" v-for="n in 5" :key="n"></i>
          </div>
        </div>

        <div class="visual-stats">
          <div class="vstat">
            <span class="vstat-num">1,000+</span>
            <span class="vstat-label">Listings</span>
          </div>
          <div class="vstat-divider"></div>
          <div class="vstat">
            <span class="vstat-num">180+</span>
            <span class="vstat-label">Agencies</span>
          </div>
          <div class="vstat-divider"></div>
          <div class="vstat">
            <span class="vstat-num">98%</span>
            <span class="vstat-label">Satisfaction</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Right Panel — Form -->
    <div class="form-panel">
      <div class="form-inner">

        <!-- Mobile brand (hidden on desktop) -->
        <router-link to="/" class="brand-mobile">
          <span class="brand-icon-sm"><i class="fas fa-home"></i></span>
          <span class="brand-text-sm">Hunter<em>Street</em></span>
        </router-link>

        <!-- Heading -->
        <div class="form-heading">
          <p class="form-eyebrow">SIGN IN</p>
          <h1 class="form-title">Good to see<br/><em>you again.</em></h1>
          <p class="form-sub">Enter your credentials to continue.</p>
        </div>

        <!-- Alert -->
        <transition name="fade">
          <div v-if="apiError" class="alert">
            <i class="fas fa-exclamation-circle"></i>
            <span>{{ apiError }}</span>
          </div>
        </transition>

        <!-- Form -->
        <form @submit.prevent="handleLogin" novalidate class="login-form">

          <!-- Email -->
          <div class="field-group" :class="{ error: errors.email }">
            <label class="field-label">Email Address</label>
            <div class="field-wrap">
              <i class="fas fa-envelope field-icon"></i>
              <input
                type="email"
                v-model="form.email"
                placeholder="you@example.com"
                class="field-input"
                autocomplete="email"
              />
            </div>
            <span class="field-error" v-if="errors.email">{{ errors.email }}</span>
          </div>

          <!-- Password -->
          <div class="field-group" :class="{ error: errors.password }">
            <label class="field-label">Password</label>
            <div class="field-wrap">
              <i class="fas fa-lock field-icon"></i>
              <input
                :type="showPassword ? 'text' : 'password'"
                v-model="form.password"
                placeholder="••••••••"
                class="field-input"
                autocomplete="current-password"
              />
              <button type="button" class="eye-btn" @click="showPassword = !showPassword">
                <i :class="showPassword ? 'fas fa-eye-slash' : 'fas fa-eye'"></i>
              </button>
            </div>
            <span class="field-error" v-if="errors.password">{{ errors.password }}</span>
          </div>

          <!-- Options row -->
          <div class="options-row">
            <label class="remember-label">
              <span class="custom-check" :class="{ checked: form.rememberMe }">
                <input type="checkbox" v-model="form.rememberMe" />
                <i class="fas fa-check"></i>
              </span>
              <span>Remember me</span>
            </label>
            <a href="#" class="forgot-link" @click.prevent>Forgot password?</a>
          </div>

          <!-- Submit -->
          <button type="submit" class="submit-btn" :disabled="loading">
            <span v-if="loading">
              <i class="fas fa-spinner fa-spin"></i>&nbsp; Signing in…
            </span>
            <span v-else>
              Sign In <i class="fas fa-arrow-right"></i>
            </span>
          </button>

        </form>

        <!-- Divider -->
        <div class="or-divider"><span>or continue with</span></div>

        <!-- Social -->
        <div class="social-row">
          <button class="social-btn" @click="loginWithGoogle" type="button">
            <i class="fab fa-google"></i><span>Google</span>
          </button>
          <button class="social-btn" @click="loginWithFacebook" type="button">
            <i class="fab fa-facebook-f"></i><span>Facebook</span>
          </button>
          <button class="social-btn" @click="loginWithGithub" type="button">
            <i class="fab fa-github"></i><span>GitHub</span>
          </button>
        </div>

        <!-- Sign up link -->
        <p class="signup-cta">
          Don't have an account?
          <router-link to="/register">Create one here</router-link>
        </p>

      </div>
    </div>

  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';

const router = useRouter();

const form = ref({ email: '', password: '', rememberMe: false });
const errors = ref({ email: '', password: '' });
const loading = ref(false);
const apiError = ref('');
const showPassword = ref(false);

const validateForm = () => {
  errors.value = { email: '', password: '' };
  let ok = true;
  if (!form.value.email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.value.email)) {
    errors.value.email = 'Please enter a valid email address.';
    ok = false;
  }
  if (!form.value.password || form.value.password.length < 6) {
    errors.value.password = 'Password must be at least 6 characters.';
    ok = false;
  }
  return ok;
};

const handleLogin = async () => {
  if (!validateForm()) return;
  loading.value = true;
  apiError.value = '';
  try {
    const res = await axios.post('http://127.0.0.1:8000/api/login/', {
      email: form.value.email,
      password: form.value.password,
    });
    localStorage.setItem('authToken', res.data.token);
    localStorage.setItem('currentUser', JSON.stringify(res.data.user));
    if (form.value.rememberMe) localStorage.setItem('rememberMe', 'true');
    router.push({ name: 'properties' });
  } catch (e) {
    if (e.response?.status === 401) apiError.value = 'Invalid email or password.';
    else if (e.response?.status === 404) apiError.value = 'No account found with that email.';
    else apiError.value = 'Something went wrong. Please try again.';
  } finally {
    loading.value = false;
  }
};

const loginWithGoogle   = () => { apiError.value = 'Google login coming soon.'; };
const loginWithFacebook = () => { apiError.value = 'Facebook login coming soon.'; };
const loginWithGithub   = () => { apiError.value = 'GitHub login coming soon.'; };
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,300;1,400;1,600&family=DM+Sans:wght@300;400;500;600&display=swap');

/* ─── Layout ────────────────────────────────── */
.login-page {
  display: flex;
  min-height: 100vh;
  font-family: 'DM Sans', sans-serif;
}

/* ─── Visual Panel (LEFT) ───────────────────── */
.visual-panel {
  width: 48%;
  max-width: 620px;
  position: relative;
  background: #111;
  overflow: hidden;
  display: flex;
  align-items: stretch;
  background-image:
    url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='60' height='60'%3E%3Cpath d='M30 0v60M0 30h60' stroke='rgba(255,255,255,0.025)' stroke-width='1'/%3E%3C/svg%3E"),
    linear-gradient(145deg, #1a0e0b 0%, #2d1510 50%, #1c0e0b 100%);
}

.visual-overlay {
  position: absolute;
  inset: 0;
  background:
    radial-gradient(ellipse at 15% 15%, rgba(183,63,42,0.4) 0%, transparent 55%),
    radial-gradient(ellipse at 85% 85%, rgba(100,25,10,0.3) 0%, transparent 55%);
  pointer-events: none;
}

.visual-content {
  position: relative;
  z-index: 2;
  padding: 52px 56px;
  display: flex;
  flex-direction: column;
  gap: 36px;
  width: 100%;
}

/* Visual brand */
.visual-brand {
  display: inline-flex;
  align-items: center;
  gap: 9px;
  text-decoration: none;
}

.brand-icon {
  width: 34px;
  height: 34px;
  background: #b73f2a;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  font-size: 14px;
}

.brand-text {
  font-family: 'Cormorant Garamond', serif;
  font-size: 22px;
  font-weight: 600;
  color: #fff;
}

.brand-text em { font-style: italic; color: #f2c4b8; }

/* Copy block */
.visual-eyebrow {
  font-size: 10px;
  letter-spacing: 4px;
  font-weight: 600;
  color: rgba(242,196,184,0.7);
  margin: 0 0 10px;
}

.visual-title {
  font-family: 'Cormorant Garamond', serif;
  font-size: clamp(38px, 3.5vw, 56px);
  font-weight: 300;
  line-height: 1.1;
  color: #fff;
  margin: 0 0 14px;
}

.visual-title em { font-style: italic; color: #f2c4b8; font-weight: 300; }

.visual-sub {
  font-size: 14.5px;
  color: rgba(255,255,255,0.55);
  line-height: 1.75;
  margin: 0;
}

/* Testimonial card */
.testimonial-card {
  background: rgba(255,255,255,0.06);
  border: 1px solid rgba(255,255,255,0.09);
  border-radius: 16px;
  padding: 22px 24px;
  backdrop-filter: blur(10px);
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.testimonial-text {
  font-size: 14.5px;
  color: rgba(255,255,255,0.82);
  line-height: 1.65;
  margin: 0;
  font-style: italic;
}

.testimonial-author {
  display: flex;
  align-items: center;
  gap: 12px;
}

.testimonial-avatar {
  width: 38px;
  height: 38px;
  border-radius: 50%;
  background: linear-gradient(135deg, #b73f2a, #d4614a);
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 13px;
  font-weight: 700;
  flex-shrink: 0;
}

.testimonial-name { font-size: 13.5px; font-weight: 600; color: #fff; margin: 0 0 2px; }
.testimonial-role { font-size: 11px; color: rgba(255,255,255,0.4); margin: 0; }

.testimonial-stars { display: flex; gap: 3px; }
.testimonial-stars i { color: #f2c4b8; font-size: 12px; }

/* Stats strip */
.visual-stats {
  display: flex;
  align-items: center;
  gap: 20px;
  padding-top: 4px;
  margin-top: auto;
}

.vstat { display: flex; flex-direction: column; gap: 3px; }
.vstat-num {
  font-family: 'Cormorant Garamond', serif;
  font-size: 26px;
  font-weight: 600;
  color: #f2c4b8;
  line-height: 1;
}

.vstat-label { font-size: 11px; color: rgba(255,255,255,0.35); letter-spacing: 0.5px; }

.vstat-divider { width: 1px; height: 36px; background: rgba(255,255,255,0.1); }

/* ─── Form Panel (RIGHT) ────────────────────── */
.form-panel {
  flex: 1;
  background: #f6f4f1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 48px 32px;
  overflow-y: auto;
}

.form-inner {
  width: 100%;
  max-width: 440px;
  display: flex;
  flex-direction: column;
  gap: 24px;
}

/* Mobile brand */
.brand-mobile {
  display: none;
  align-items: center;
  gap: 9px;
  text-decoration: none;
  margin-bottom: 4px;
}

.brand-icon-sm {
  width: 30px;
  height: 30px;
  background: #b73f2a;
  border-radius: 7px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  font-size: 13px;
}

.brand-text-sm {
  font-family: 'Cormorant Garamond', serif;
  font-size: 20px;
  font-weight: 600;
  color: #1c1c1c;
}

.brand-text-sm em { font-style: italic; color: #b73f2a; }

/* Heading */
.form-eyebrow {
  font-size: 10px;
  letter-spacing: 3px;
  font-weight: 600;
  color: #b73f2a;
  margin: 0 0 8px;
}

.form-title {
  font-family: 'Cormorant Garamond', serif;
  font-size: 40px;
  font-weight: 600;
  color: #111;
  margin: 0 0 8px;
  line-height: 1.1;
}

.form-title em { font-style: italic; color: #b73f2a; }
.form-sub { font-size: 14px; color: #888; margin: 0; }

/* Alert */
.alert {
  padding: 13px 16px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 13.5px;
  background: #fff5f5;
  color: #b73f2a;
  border: 1px solid rgba(183,63,42,0.2);
}

/* Form */
.login-form { display: flex; flex-direction: column; gap: 18px; }

.field-group { display: flex; flex-direction: column; gap: 6px; }

.field-label {
  font-size: 11px;
  letter-spacing: 1.5px;
  text-transform: uppercase;
  font-weight: 600;
  color: #888;
}

.field-wrap {
  position: relative;
  display: flex;
  align-items: center;
}

.field-icon {
  position: absolute;
  left: 14px;
  font-size: 14px;
  color: #ccc;
  pointer-events: none;
  transition: color 0.2s;
}

.field-input {
  width: 100%;
  padding: 13px 42px 13px 40px;
  border: 1.5px solid #e0dcd8;
  border-radius: 10px;
  font-family: 'DM Sans', sans-serif;
  font-size: 14px;
  color: #1c1c1c;
  background: #fff;
  outline: none;
  transition: border-color 0.2s, box-shadow 0.2s;
}

.field-input::placeholder { color: #c0bbb6; }

.field-input:focus {
  border-color: #b73f2a;
  box-shadow: 0 0 0 3px rgba(183,63,42,0.1);
}

.field-wrap:focus-within .field-icon { color: #b73f2a; }

.field-group.error .field-input { border-color: #e53e3e; }
.field-group.error .field-input:focus { box-shadow: 0 0 0 3px rgba(229,62,62,0.1); }

.field-error { font-size: 12px; color: #e53e3e; font-weight: 500; }

.eye-btn {
  position: absolute;
  right: 12px;
  background: none;
  border: none;
  color: #bbb;
  cursor: pointer;
  font-size: 14px;
  padding: 4px;
  transition: color 0.2s;
}

.eye-btn:hover { color: #b73f2a; }

/* Options row */
.options-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: -4px;
}

.remember-label {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  font-size: 13.5px;
  color: #666;
  user-select: none;
}

.custom-check {
  width: 18px;
  height: 18px;
  border: 1.5px solid #ccc;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  transition: all 0.2s;
}

.custom-check input[type="checkbox"] { display: none; }
.custom-check i { font-size: 9px; color: #fff; opacity: 0; transition: opacity 0.15s; }
.custom-check.checked { background: #b73f2a; border-color: #b73f2a; }
.custom-check.checked i { opacity: 1; }

.forgot-link {
  font-size: 13.5px;
  font-weight: 600;
  color: #b73f2a;
  text-decoration: none;
  transition: color 0.2s;
}

.forgot-link:hover { color: #9a3523; text-decoration: underline; }

/* Submit */
.submit-btn {
  padding: 14px;
  background: #b73f2a;
  color: #fff;
  border: none;
  border-radius: 10px;
  font-family: 'DM Sans', sans-serif;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  transition: background 0.2s, transform 0.2s, box-shadow 0.2s;
  letter-spacing: 0.3px;
  margin-top: 4px;
}

.submit-btn:hover:not(:disabled) {
  background: #9a3523;
  transform: translateY(-2px);
  box-shadow: 0 10px 28px rgba(183,63,42,0.28);
}

.submit-btn:disabled { opacity: 0.65; cursor: not-allowed; }

/* Or divider */
.or-divider {
  display: flex;
  align-items: center;
  gap: 12px;
  color: #bbb;
  font-size: 13px;
}

.or-divider::before, .or-divider::after {
  content: '';
  flex: 1;
  height: 1px;
  background: #e0dcd8;
}

/* Social */
.social-row { display: flex; gap: 10px; }

.social-btn {
  flex: 1;
  padding: 11px 14px;
  border: 1.5px solid #e0dcd8;
  border-radius: 10px;
  background: #fff;
  font-family: 'DM Sans', sans-serif;
  font-size: 13px;
  font-weight: 500;
  color: #444;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  transition: all 0.2s;
}

.social-btn:hover {
  border-color: #b73f2a;
  color: #b73f2a;
  background: rgba(183,63,42,0.04);
  transform: translateY(-1px);
}

.social-btn i { font-size: 15px; }

/* Sign up CTA */
.signup-cta {
  text-align: center;
  font-size: 14px;
  color: #888;
  margin: 0;
}

.signup-cta a {
  color: #b73f2a;
  font-weight: 600;
  text-decoration: none;
}

.signup-cta a:hover { text-decoration: underline; }

/* ─── Transition ────────────────────────────── */
.fade-enter-active, .fade-leave-active { transition: opacity 0.3s ease; }
.fade-enter-from,  .fade-leave-to      { opacity: 0; }

/* ─── Responsive ────────────────────────────── */
@media (max-width: 900px) {
  .visual-panel { display: none; }
  .brand-mobile { display: flex; }
  .form-panel   { padding: 32px 20px; align-items: flex-start; }
  .form-inner   { padding-top: 12px; }
}

@media (max-width: 480px) {
  .form-title    { font-size: 32px; }
  .social-row    { flex-direction: column; }
}
</style>