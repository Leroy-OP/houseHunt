<template>
  <nav class="navbar" :class="{ scrolled: isScrolled }">
    <div class="navbar-inner">

      <!-- Brand -->
      <router-link to="/" class="brand">
        <span class="brand-icon"><i class="fas fa-home"></i></span>
        <span class="brand-text">Hunter<em>Street</em></span>
      </router-link>

      <!-- Center nav links (desktop) -->
      <div class="nav-links" :class="{ 'mobile-open': mobileOpen }">
        <router-link to="/" class="nav-link" @click="mobileOpen = false">Home</router-link>
        <router-link to="/properties" class="nav-link" @click="mobileOpen = false">Properties</router-link>
        <router-link to="/about" class="nav-link" @click="mobileOpen = false">About Us</router-link>
        <router-link to="/support" class="nav-link" @click="mobileOpen = false">Support</router-link>
      </div>

      <!-- Right actions -->
      <div class="nav-actions">

        <!-- Notification bell -->
        <button
          class="icon-btn"
          @click="drawerOpen = true; drawerTab = 'notifications'"
          aria-label="Notifications"
        >
          <i class="fas fa-bell"></i>
          <span class="badge" v-if="notificationCount > 0">{{ notificationCount }}</span>
        </button>

        <!-- Saved -->
        <router-link to="/saved" class="icon-btn" aria-label="Saved properties">
          <i class="fas fa-heart"></i>
          <span class="badge saved-badge" v-if="savedCount > 0">{{ savedCount }}</span>
        </router-link>

        <!-- Avatar / Login -->
        <div class="avatar-wrap" @click="toggleUserMenu" ref="avatarRef">
          <img
            v-if="user && user.avatar"
            :src="user.avatar"
            :alt="userName"
            class="avatar-img"
            @error="onAvatarError"
          />
          <div v-else-if="user && userName" class="avatar-initials">
            {{ getInitials(userName) }}
          </div>
          <div v-else class="avatar-guest">
            <i class="fas fa-user"></i>
          </div>
          <span class="avatar-chevron"><i class="fas fa-chevron-down"></i></span>

          <!-- User dropdown -->
          <transition name="drop">
            <div class="user-drop" v-if="userMenuOpen" @click.stop>
              <div class="drop-profile" v-if="user">
                <div class="drop-avatar">
                  <img v-if="user.avatar" :src="user.avatar" :alt="userName" @error="onAvatarError" />
                  <div v-else class="drop-initials">{{ getInitials(userName) }}</div>
                </div>
                <div class="drop-info">
                  <p class="drop-name">{{ userName }}</p>
                  <p class="drop-email">{{ user.email }}</p>
                </div>
              </div>
              <div class="drop-guest" v-else>
                <p class="drop-greeting">Welcome back</p>
                <p class="drop-sub">Sign in to access your saved properties and bookings.</p>
              </div>

              <div class="drop-divider"></div>

              <template v-if="user">
                <router-link to="/profile" class="drop-item" @click="userMenuOpen = false">
                  <i class="fas fa-user-circle"></i> My Profile
                </router-link>
                <router-link to="/saved" class="drop-item" @click="userMenuOpen = false">
                  <i class="fas fa-heart"></i> Saved Properties
                </router-link>
                <router-link to="/bookings" class="drop-item" @click="userMenuOpen = false">
                  <i class="fas fa-calendar-check"></i> My Bookings
                </router-link>
                <router-link to="/settings" class="drop-item" @click="userMenuOpen = false">
                  <i class="fas fa-cog"></i> Settings
                </router-link>
                <div class="drop-divider"></div>
                <button class="drop-item drop-logout" @click="logout">
                  <i class="fas fa-sign-out-alt"></i> Sign Out
                </button>
              </template>
              <template v-else>
                <router-link to="/login" class="drop-item" @click="userMenuOpen = false">
                  <i class="fas fa-sign-in-alt"></i> Sign In
                </router-link>
                <router-link to="/register" class="drop-item" @click="userMenuOpen = false">
                  <i class="fas fa-user-plus"></i> Create Account
                </router-link>
              </template>
            </div>
          </transition>
        </div>

        <!-- Drawer trigger -->
        <button class="icon-btn drawer-btn" @click="drawerOpen = true; drawerTab = 'menu'" aria-label="Open menu">
          <i class="fas fa-bars"></i>
        </button>

        <!-- Mobile hamburger -->
        <button class="mobile-toggle" @click="mobileOpen = !mobileOpen" aria-label="Toggle navigation">
          <span :class="{ open: mobileOpen }"></span>
          <span :class="{ open: mobileOpen }"></span>
          <span :class="{ open: mobileOpen }"></span>
        </button>
      </div>
    </div>
  </nav>

  <!-- ── DRAWER ─────────────────────────────────────────────────────── -->
  <transition name="backdrop">
    <div v-if="drawerOpen" class="drawer-backdrop" @click="drawerOpen = false"></div>
  </transition>

  <transition name="drawer">
    <aside v-if="drawerOpen" class="drawer">

      <!-- Drawer header -->
      <div class="drawer-head">
        <span class="drawer-brand">Hunter<em>Street</em></span>
        <button class="drawer-close" @click="drawerOpen = false">
          <i class="fas fa-times"></i>
        </button>
      </div>

      <!-- Tabs -->
      <div class="drawer-tabs">
        <button
          class="drawer-tab"
          :class="{ active: drawerTab === 'menu' }"
          @click="drawerTab = 'menu'"
        >Menu</button>
        <button
          class="drawer-tab"
          :class="{ active: drawerTab === 'notifications' }"
          @click="drawerTab = 'notifications'"
        >
          Notifications
          <span class="tab-badge" v-if="notificationCount > 0">{{ notificationCount }}</span>
        </button>
      </div>

      <!-- ── Tab: Menu ── -->
      <div class="drawer-body" v-if="drawerTab === 'menu'">
        <div class="drawer-user-card" v-if="user">
          <div class="drawer-user-avatar">
            <img v-if="user.avatar" :src="user.avatar" :alt="userName" @error="onAvatarError" />
            <div v-else class="drawer-user-initials">{{ getInitials(userName) }}</div>
          </div>
          <div class="drawer-user-info">
            <p class="drawer-user-name">{{ userName }}</p>
            <p class="drawer-user-email">{{ user.email }}</p>
          </div>
        </div>
        <div class="drawer-guest-card" v-else>
          <div class="drawer-guest-icon"><i class="fas fa-user"></i></div>
          <div>
            <p class="drawer-user-name">Guest User</p>
            <div class="drawer-auth-btns">
              <router-link to="/login" class="auth-btn auth-btn--primary" @click="drawerOpen = false">Sign In</router-link>
              <router-link to="/register" class="auth-btn auth-btn--outline" @click="drawerOpen = false">Register</router-link>
            </div>
          </div>
        </div>

        <div class="drawer-divider"></div>

        <p class="drawer-section-label">NAVIGATION</p>
        <nav class="drawer-nav">
          <router-link to="/" class="drawer-nav-item" @click="drawerOpen = false">
            <span class="dnav-icon"><i class="fas fa-home"></i></span>
            <span>Home</span>
            <i class="fas fa-chevron-right dnav-arrow"></i>
          </router-link>
          <router-link to="/properties" class="drawer-nav-item" @click="drawerOpen = false">
            <span class="dnav-icon"><i class="fas fa-building"></i></span>
            <span>Properties</span>
            <i class="fas fa-chevron-right dnav-arrow"></i>
          </router-link>
          <router-link to="/saved" class="drawer-nav-item" @click="drawerOpen = false">
            <span class="dnav-icon"><i class="fas fa-heart"></i></span>
            <span>Saved Properties</span>
            <i class="fas fa-chevron-right dnav-arrow"></i>
          </router-link>
          <router-link to="/about" class="drawer-nav-item" @click="drawerOpen = false">
            <span class="dnav-icon"><i class="fas fa-info-circle"></i></span>
            <span>About Us</span>
            <i class="fas fa-chevron-right dnav-arrow"></i>
          </router-link>
          <router-link to="/support" class="drawer-nav-item" @click="drawerOpen = false">
            <span class="dnav-icon"><i class="fas fa-headset"></i></span>
            <span>Support</span>
            <i class="fas fa-chevron-right dnav-arrow"></i>
          </router-link>
        </nav>

        <div class="drawer-divider"></div>

        <p class="drawer-section-label">ACCOUNT</p>
        <nav class="drawer-nav" v-if="user">
          <router-link to="/profile" class="drawer-nav-item" @click="drawerOpen = false">
            <span class="dnav-icon"><i class="fas fa-user-circle"></i></span>
            <span>My Profile</span>
            <i class="fas fa-chevron-right dnav-arrow"></i>
          </router-link>
          <router-link to="/bookings" class="drawer-nav-item" @click="drawerOpen = false">
            <span class="dnav-icon"><i class="fas fa-calendar-check"></i></span>
            <span>My Bookings</span>
            <i class="fas fa-chevron-right dnav-arrow"></i>
          </router-link>
          <router-link to="/settings" class="drawer-nav-item" @click="drawerOpen = false">
            <span class="dnav-icon"><i class="fas fa-cog"></i></span>
            <span>Settings</span>
            <i class="fas fa-chevron-right dnav-arrow"></i>
          </router-link>
          <button class="drawer-nav-item drawer-logout" @click="logout">
            <span class="dnav-icon"><i class="fas fa-sign-out-alt"></i></span>
            <span>Sign Out</span>
          </button>
        </nav>

        <div class="drawer-footer">
          <p class="drawer-footer-text">© {{ new Date().getFullYear() }} Hunter Street</p>
          <div class="drawer-socials">
            <a href="#" class="dsocial"><i class="fab fa-instagram"></i></a>
            <a href="#" class="dsocial"><i class="fab fa-twitter"></i></a>
            <a href="#" class="dsocial"><i class="fab fa-facebook-f"></i></a>
          </div>
        </div>
      </div>

      <!-- ── Tab: Notifications ── -->
      <div class="drawer-body" v-if="drawerTab === 'notifications'">

        <!-- Loading skeleton -->
        <div class="notif-skeleton" v-if="notifLoading && notifications.length === 0">
          <div class="skeleton-item" v-for="i in 3" :key="i">
            <div class="skeleton-icon"></div>
            <div class="skeleton-lines">
              <div class="skeleton-line short"></div>
              <div class="skeleton-line long"></div>
              <div class="skeleton-line tiny"></div>
            </div>
          </div>
        </div>

        <!-- Error state -->
        <div class="notif-error" v-else-if="notifError && notifications.length === 0">
          <i class="fas fa-exclamation-circle"></i>
          <p>{{ notifError }}</p>
          <button class="retry-btn" @click="fetchNotifications">Retry</button>
        </div>

        <!-- Not logged in state -->
        <div class="notif-empty" v-else-if="!user">
          <i class="fas fa-lock"></i>
          <p>Sign in to see your notifications</p>
        </div>

        <!-- Empty state -->
        <div class="notif-empty" v-else-if="!notifLoading && notifications.length === 0">
          <i class="fas fa-bell-slash"></i>
          <p>No notifications yet</p>
        </div>

        <!-- Notification list -->
        <div class="notif-list" v-else>
          <transition-group name="notif-slide">
            <div
              v-for="n in notifications"
              :key="n.id"
              class="notif-item"
              :class="{ unread: !n.read }"
              @click="markRead(n)"
            >
              <div class="notif-dot" v-if="!n.read"></div>
              <div class="notif-icon" :class="`notif-icon--${n.type}`">
                <i :class="notifIcon(n.type)"></i>
              </div>
              <div class="notif-content">
                <p class="notif-title">{{ n.title }}</p>
                <p class="notif-body">{{ n.body }}</p>
                <p class="notif-time">{{ n.time }}</p>
              </div>
            </div>
          </transition-group>
        </div>

        <button class="clear-notifs" v-if="notifications.length" @click="clearNotifications">
          Clear all
        </button>
      </div>

    </aside>
  </transition>
</template>

<script>
import { ref, computed, onMounted, onBeforeUnmount, watch } from 'vue';
import { useRouter } from 'vue-router';

const API_BASE      = 'http://127.0.0.1:8000/api/notifications/notifications/';
const POLL_INTERVAL = 30_000;

const getToken = () => localStorage.getItem('authToken') || '';

function relativeTime(iso) {
  if (!iso) return '';
  const diff = Math.floor((Date.now() - new Date(iso).getTime()) / 1000);
  if (diff < 60)    return 'just now';
  if (diff < 3600)  return `${Math.floor(diff / 60)}m ago`;
  if (diff < 86400) return `${Math.floor(diff / 3600)}h ago`;
  return `${Math.floor(diff / 86400)}d ago`;
}

function normalise(raw) {
  return {
    id:    raw.id    ?? Date.now(),
    type:  raw.type  || 'info',
    read:  raw.read  ?? false,
    title: raw.title || 'Notification',
    body:  raw.body  || '',
    time:  relativeTime(raw.created_at),
  };
}

async function authFetch(url, options = {}) {
  const token = getToken();
  const res = await fetch(url, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      'Accept':       'application/json',
      ...options.headers,
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
    },
  });

  if (res.status === 401) {
    const err  = new Error('Unauthorized');
    err.status = 401;
    throw err;
  }

  return res;
}

export default {
  name: 'AppNavbar',

  setup() {
    const router = useRouter();

    // ── Scroll
    const isScrolled = ref(false);
    const onScroll   = () => { isScrolled.value = window.scrollY > 20; };
    onMounted(()       => window.addEventListener('scroll', onScroll));
    onBeforeUnmount(() => window.removeEventListener('scroll', onScroll));

    // ── Mobile nav
    const mobileOpen = ref(false);

    // ── Drawer
    const drawerOpen = ref(false);
    const drawerTab  = ref('menu');

    // ── User
    const user = ref(null);

    const loadUser = () => {
      try {
        const raw  = localStorage.getItem('currentUser');
        user.value = raw ? JSON.parse(raw) : null;
      } catch (_) {
        user.value = null;
      }
    };

    onMounted(loadUser);

    // ── Derived full name from first_name + last_name (or fallback to name)
    const userName = computed(() => {
      if (!user.value) return '';
      if (user.value.name) return user.value.name;
      return [user.value.first_name, user.value.last_name].filter(Boolean).join(' ');
    });

    const getInitials = (name) => {
      if (!name) return '?';
      return name.split(' ').slice(0, 2).map(w => w[0]).join('').toUpperCase();
    };

    const onAvatarError = (e) => { e.target.style.display = 'none'; };

    // ── Notifications
    const notifications = ref([]);
    const notifLoading  = ref(false);
    const notifError    = ref(null);

    let pollTimer = null;

    const stopPolling = () => {
      if (pollTimer !== null) { clearInterval(pollTimer); pollTimer = null; }
    };

    // ── Handle 401
    const handleUnauthorized = () => {
      localStorage.removeItem('authToken');
      localStorage.removeItem('currentUser');
      user.value          = null;
      drawerOpen.value    = false;
      userMenuOpen.value  = false;
      stopPolling();
      notifications.value = [];
      router.push('/login');
    };

    // ── Logout
    const logout = () => {
      localStorage.removeItem('currentUser');
      localStorage.removeItem('authToken');
      user.value          = null;
      drawerOpen.value    = false;
      userMenuOpen.value  = false;
      stopPolling();
      notifications.value = [];
      router.push('/');
    };

    // ── User dropdown
    const userMenuOpen = ref(false);
    const avatarRef    = ref(null);
    const toggleUserMenu = () => { userMenuOpen.value = !userMenuOpen.value; };

    const onClickOutside = (e) => {
      if (avatarRef.value && !avatarRef.value.contains(e.target)) {
        userMenuOpen.value = false;
      }
    };

    onMounted(()       => document.addEventListener('click', onClickOutside));
    onBeforeUnmount(() => document.removeEventListener('click', onClickOutside));

    // ── Saved count
    const savedCount = computed(() => {
      try { return JSON.parse(localStorage.getItem('savedProperties') || '[]').length; }
      catch { return 0; }
    });

    // ── Fetch notifications
    const fetchNotifications = async () => {
      if (!getToken()) return;

      if (notifications.value.length === 0) notifLoading.value = true;
      notifError.value = null;

      try {
        const res = await authFetch(API_BASE);
        if (!res.ok) throw new Error(`${res.status} ${res.statusText}`);

        const json     = await res.json();
        const raw      = Array.isArray(json) ? json : (json.data ?? []);
        const incoming = raw.map(normalise).sort((a, b) => b.id - a.id);

        const existingMap = new Map(notifications.value.map(n => [n.id, n]));
        const newItems    = incoming.filter(n => !existingMap.has(n.id));

        incoming.forEach(n => {
          if (existingMap.has(n.id)) {
            const existing = existingMap.get(n.id);
            if (!existing.read) existing.read = n.read;
            existing.time = n.time;
          }
        });

        notifications.value = [...newItems, ...notifications.value].slice(0, 50);

      } catch (err) {
        if (err.status === 401) { handleUnauthorized(); return; }
        console.error('[AppNavbar] fetchNotifications:', err);
        if (notifications.value.length === 0) {
          notifError.value = 'Could not load notifications. Tap to retry.';
        }
      } finally {
        notifLoading.value = false;
      }
    };

    const startPolling = () => {
      stopPolling();
      if (!getToken()) return;
      pollTimer = setInterval(fetchNotifications, POLL_INTERVAL);
    };

    onMounted(async () => {
      if (getToken()) {
        await fetchNotifications();
        startPolling();
      }
    });

    onBeforeUnmount(stopPolling);

    watch(user, (newVal, oldVal) => {
      if (newVal && !oldVal && getToken()) {
        fetchNotifications();
        startPolling();
      } else if (!newVal && oldVal) {
        stopPolling();
        notifications.value = [];
      }
    });

    // ── Cross-tab sync
    const onStorageChange = (e) => {
      if (e.key === 'currentUser') {
        loadUser();
      }
      if (e.key === 'authToken') {
        if (getToken()) {
          fetchNotifications();
          startPolling();
        } else {
          stopPolling();
          notifications.value = [];
        }
      }
    };

    onMounted(()       => window.addEventListener('storage', onStorageChange));
    onBeforeUnmount(() => window.removeEventListener('storage', onStorageChange));

    // ── Derived state
    const notificationCount = computed(() =>
      notifications.value.filter(n => !n.read).length
    );

    // ── Mark read
    const markRead = async (n) => {
      if (n.read) return;
      n.read = true;

      try {
        const res = await authFetch(`${API_BASE}${n.id}/`, {
          method: 'PATCH',
          body:   JSON.stringify({ read: true }),
        });
        if (!res.ok) throw new Error(res.statusText);
      } catch (err) {
        if (err.status === 401) { handleUnauthorized(); return; }
        console.warn('[AppNavbar] markRead failed:', err);
        n.read = false;
      }
    };

    // ── Clear all
    const clearNotifications = async () => {
      const backup        = [...notifications.value];
      notifications.value = [];

      try {
        const res = await authFetch('http://127.0.0.1:8000/api/notifications/notifications/clear/', { method: 'DELETE' });
        if (!res.ok) throw new Error(res.statusText);
      } catch (err) {
        if (err.status === 401) { handleUnauthorized(); return; }
        console.warn('[AppNavbar] clearNotifications failed:', err);
        notifications.value = backup;
      }
    };

    const notifIcon = (type) => ({
      listing:   'fas fa-home',
      booking:   'fas fa-calendar-alt',
      confirmed: 'fas fa-check-circle',
      cancelled: 'fas fa-times-circle',
    }[type] || 'fas fa-info-circle');

    return {
      isScrolled, mobileOpen,
      drawerOpen, drawerTab,
      user, userName, getInitials, onAvatarError, logout,
      userMenuOpen, avatarRef, toggleUserMenu,
      savedCount,
      notifications, notifLoading, notifError,
      notificationCount,
      fetchNotifications,
      markRead, clearNotifications,
      notifIcon,
    };
  },
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,600;1,400&family=DM+Sans:wght@300;400;500;600&display=swap');

/* ─── Navbar shell ──────────────────────────── */
.navbar {
  position: sticky;
  top: 0;
  z-index: 900;
  font-family: 'DM Sans', sans-serif;
  background: rgba(246, 244, 241, 0.85);
  backdrop-filter: blur(14px);
  -webkit-backdrop-filter: blur(14px);
  border-bottom: 1px solid transparent;
  transition: background 0.3s, border-color 0.3s, box-shadow 0.3s;
}

.navbar.scrolled {
  background: rgba(246, 244, 241, 0.97);
  border-bottom-color: rgba(0,0,0,0.06);
  box-shadow: 0 2px 20px rgba(0,0,0,0.06);
}

.navbar-inner {
  max-width: 1280px;
  margin: 0 auto;
  padding: 0 28px;
  height: 68px;
  display: flex;
  align-items: center;
  gap: 32px;
}

/* ─── Brand ─────────────────────────────────── */
.brand { display: flex; align-items: center; gap: 9px; text-decoration: none; flex-shrink: 0; }

.brand-icon {
  width: 34px; height: 34px;
  background: #b73f2a;
  border-radius: 8px;
  display: flex; align-items: center; justify-content: center;
  color: #fff; font-size: 14px;
}

.brand-text {
  font-family: 'Cormorant Garamond', serif;
  font-size: 22px;
  font-weight: 600;
  color: #1c1c1c;
  letter-spacing: -0.3px;
}

.brand-text em { font-style: italic; color: #b73f2a; }

/* ─── Center nav links ──────────────────────── */
.nav-links { display: flex; align-items: center; gap: 4px; flex: 1; justify-content: center; }

.nav-link {
  font-size: 14px; font-weight: 500; color: #555;
  text-decoration: none; padding: 6px 14px;
  border-radius: 8px; position: relative;
  transition: color 0.2s, background 0.2s;
}

.nav-link:hover { color: #1c1c1c; background: rgba(0,0,0,0.04); }

.nav-link.router-link-active,
.nav-link.router-link-exact-active { color: #b73f2a; font-weight: 600; }

.nav-link.router-link-exact-active::after {
  content: '';
  position: absolute;
  bottom: -2px; left: 14px; right: 14px;
  height: 2px; background: #b73f2a; border-radius: 2px;
}

/* ─── Right actions ─────────────────────────── */
.nav-actions { display: flex; align-items: center; gap: 6px; margin-left: auto; flex-shrink: 0; }

.icon-btn {
  position: relative;
  width: 40px; height: 40px;
  border: none; background: none;
  border-radius: 10px;
  display: flex; align-items: center; justify-content: center;
  color: #555; font-size: 16px;
  cursor: pointer; text-decoration: none;
  transition: background 0.2s, color 0.2s;
}

.icon-btn:hover { background: rgba(0,0,0,0.06); color: #1c1c1c; }

.badge {
  position: absolute;
  top: 3px; right: 3px;
  background: #b73f2a; color: #fff;
  font-size: 9px; font-weight: 700;
  min-width: 16px; height: 16px;
  border-radius: 8px;
  display: flex; align-items: center; justify-content: center;
  padding: 0 3px;
  border: 2px solid #f6f4f1;
}

.saved-badge { background: #e53e3e; }

.drawer-btn { background: rgba(0,0,0,0.05); }
.drawer-btn:hover { background: rgba(0,0,0,0.1); }

/* ─── Avatar ────────────────────────────────── */
.avatar-wrap {
  position: relative;
  display: flex; align-items: center; gap: 6px;
  cursor: pointer;
  padding: 4px 10px 4px 4px;
  border-radius: 50px;
  border: 1.5px solid rgba(0,0,0,0.08);
  background: #fff;
  transition: border-color 0.2s, box-shadow 0.2s;
  user-select: none;
}

.avatar-wrap:hover {
  border-color: #b73f2a;
  box-shadow: 0 2px 12px rgba(183,63,42,0.12);
}

.avatar-img, .avatar-initials, .avatar-guest {
  width: 32px; height: 32px; border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  flex-shrink: 0;
}

.avatar-img { object-fit: cover; }

.avatar-initials {
  background: linear-gradient(135deg, #b73f2a, #d4614a);
  color: #fff; font-size: 12px; font-weight: 700; letter-spacing: 0.5px;
}

.avatar-guest { background: #e8e4df; color: #888; font-size: 14px; }
.avatar-chevron { font-size: 10px; color: #999; transition: transform 0.2s; }

/* ─── User dropdown ─────────────────────────── */
.user-drop {
  position: absolute;
  top: calc(100% + 10px); right: 0;
  background: #fff;
  border-radius: 14px;
  min-width: 240px;
  box-shadow: 0 12px 40px rgba(0,0,0,0.14);
  overflow: hidden;
  border: 1px solid rgba(0,0,0,0.06);
  z-index: 200;
}

.drop-profile { display: flex; align-items: center; gap: 12px; padding: 16px; }

.drop-avatar { width: 44px; height: 44px; border-radius: 50%; overflow: hidden; flex-shrink: 0; }
.drop-avatar img { width: 100%; height: 100%; object-fit: cover; }

.drop-initials {
  width: 100%; height: 100%;
  background: linear-gradient(135deg, #b73f2a, #d4614a);
  color: #fff;
  display: flex; align-items: center; justify-content: center;
  font-size: 15px; font-weight: 700;
}

.drop-name  { font-size: 14px; font-weight: 600; color: #111; margin: 0 0 2px; }
.drop-email { font-size: 12px; color: #999; margin: 0; }

.drop-guest    { padding: 16px; }
.drop-greeting { font-size: 15px; font-weight: 600; color: #111; margin: 0 0 4px; }
.drop-sub      { font-size: 12px; color: #888; margin: 0; line-height: 1.5; }

.drop-divider { height: 1px; background: #f0f0f0; margin: 0; }

.drop-item {
  display: flex; align-items: center; gap: 10px;
  padding: 11px 16px;
  font-size: 13.5px; color: #333;
  text-decoration: none;
  transition: background 0.15s, color 0.15s;
  border: none; background: none;
  width: 100%; text-align: left;
  cursor: pointer;
  font-family: 'DM Sans', sans-serif;
}

.drop-item i { font-size: 14px; color: #aaa; width: 18px; text-align: center; transition: color 0.15s; }
.drop-item:hover { background: #f9f7f5; color: #b73f2a; }
.drop-item:hover i { color: #b73f2a; }

.drop-logout { color: #e53e3e; }
.drop-logout i { color: #e53e3e; }
.drop-logout:hover { background: #fff5f5; color: #c0392b; }

.drop-enter-active, .drop-leave-active { transition: all 0.2s ease; }
.drop-enter-from, .drop-leave-to { opacity: 0; transform: translateY(-8px) scale(0.97); }

/* ─── Mobile toggle ─────────────────────────── */
.mobile-toggle {
  display: none;
  flex-direction: column; gap: 5px;
  background: none; border: none; cursor: pointer; padding: 4px;
}

.mobile-toggle span {
  display: block; width: 22px; height: 2px;
  background: #333; border-radius: 2px; transition: all 0.3s;
}

.mobile-toggle span:nth-child(1).open { transform: translateY(7px) rotate(45deg); }
.mobile-toggle span:nth-child(2).open { opacity: 0; }
.mobile-toggle span:nth-child(3).open { transform: translateY(-7px) rotate(-45deg); }

/* ─── DRAWER ────────────────────────────────── */
.drawer-backdrop {
  position: fixed; inset: 0;
  background: rgba(0,0,0,0.35);
  backdrop-filter: blur(2px);
  z-index: 1000;
}

.drawer {
  position: fixed; top: 0; right: 0;
  width: 320px; height: 100%;
  background: #fff;
  z-index: 1010;
  display: flex; flex-direction: column;
  box-shadow: -12px 0 40px rgba(0,0,0,0.12);
  overflow: hidden;
}

.drawer-head {
  display: flex; justify-content: space-between; align-items: center;
  padding: 20px 24px;
  border-bottom: 1px solid #f0f0f0;
  flex-shrink: 0;
}

.drawer-brand { font-family: 'Cormorant Garamond', serif; font-size: 20px; font-weight: 600; color: #1c1c1c; }
.drawer-brand em { font-style: italic; color: #b73f2a; }

.drawer-close {
  width: 34px; height: 34px; background: #f5f4f2;
  border: none; border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  cursor: pointer; font-size: 14px; color: #555;
  transition: background 0.2s, color 0.2s;
}

.drawer-close:hover { background: #ede9e4; color: #111; }

.drawer-tabs { display: flex; border-bottom: 1px solid #f0f0f0; flex-shrink: 0; }

.drawer-tab {
  flex: 1; padding: 12px;
  border: none; background: none;
  font-family: 'DM Sans', sans-serif;
  font-size: 13px; font-weight: 500; color: #888;
  cursor: pointer;
  display: flex; align-items: center; justify-content: center; gap: 6px;
  border-bottom: 2px solid transparent;
  transition: color 0.2s, border-color 0.2s;
}

.drawer-tab.active { color: #b73f2a; border-bottom-color: #b73f2a; }

.tab-badge {
  background: #b73f2a; color: #fff;
  font-size: 10px; font-weight: 700;
  min-width: 16px; height: 16px;
  border-radius: 8px;
  display: flex; align-items: center; justify-content: center;
  padding: 0 4px;
}

.drawer-body {
  flex: 1; overflow-y: auto;
  padding: 20px 20px 0;
  display: flex; flex-direction: column;
}

/* ─── Skeleton loader ───────────────────────── */
.notif-skeleton { display: flex; flex-direction: column; gap: 12px; }

.skeleton-item { display: flex; align-items: flex-start; gap: 12px; padding: 4px 0; }

.skeleton-icon {
  width: 36px; height: 36px; border-radius: 10px;
  background: #ede9e4; flex-shrink: 0;
  animation: shimmer 1.4s ease-in-out infinite;
}

.skeleton-lines { flex: 1; display: flex; flex-direction: column; gap: 7px; padding-top: 4px; }

.skeleton-line {
  height: 10px; border-radius: 6px; background: #ede9e4;
  animation: shimmer 1.4s ease-in-out infinite;
}

.skeleton-line.short { width: 55%; }
.skeleton-line.long  { width: 90%; }
.skeleton-line.tiny  { width: 30%; height: 8px; }

@keyframes shimmer {
  0%, 100% { opacity: 1; }
  50%       { opacity: 0.4; }
}

/* ─── Error / empty states ──────────────────── */
.notif-error,
.notif-empty {
  flex: 1;
  display: flex; flex-direction: column;
  align-items: center; justify-content: center;
  gap: 12px; padding: 40px 0;
}

.notif-error i { font-size: 36px; color: #ef4444; }
.notif-error p { font-size: 13.5px; color: #888; margin: 0; text-align: center; }

.retry-btn {
  padding: 8px 20px;
  border: 1.5px solid #b73f2a; border-radius: 8px;
  background: none; color: #b73f2a;
  font-family: 'DM Sans', sans-serif; font-size: 13px;
  cursor: pointer; transition: all 0.2s;
}

.retry-btn:hover { background: #b73f2a; color: #fff; }

.notif-empty i { font-size: 40px; color: #ccc; }
.notif-empty p { font-size: 14px; color: #bbb; margin: 0; }

/* ─── Notification list ─────────────────────── */
.notif-list { display: flex; flex-direction: column; gap: 4px; }

.notif-item {
  display: flex; align-items: flex-start; gap: 12px;
  padding: 13px 12px;
  border-radius: 10px; cursor: pointer; position: relative;
  transition: background 0.15s;
}

.notif-item:hover { background: #f9f8f6; }
.notif-item.unread { background: rgba(183,63,42,0.04); }

.notif-dot {
  position: absolute; top: 17px; left: 4px;
  width: 6px; height: 6px; border-radius: 50%; background: #b73f2a;
}

.notif-icon {
  width: 36px; height: 36px; border-radius: 10px;
  background: #f0ede9;
  display: flex; align-items: center; justify-content: center;
  font-size: 14px; color: #b73f2a; flex-shrink: 0;
}

/* Per-type icon tints */
.notif-icon--listing   { background: #fef3c7; color: #d97706; }
.notif-icon--booking   { background: #dbeafe; color: #2563eb; }
.notif-icon--confirmed { background: #dcfce7; color: #16a34a; }
.notif-icon--cancelled { background: #fee2e2; color: #dc2626; }

.notif-title { font-size: 13.5px; font-weight: 600; color: #111; margin: 0 0 3px; }
.notif-body  { font-size: 12.5px; color: #666; margin: 0 0 4px; line-height: 1.4; }
.notif-time  { font-size: 11px; color: #bbb; margin: 0; }

.clear-notifs {
  margin: 16px auto;
  display: block; padding: 9px 20px;
  border: 1.5px solid #eee; border-radius: 8px;
  background: none;
  font-family: 'DM Sans', sans-serif; font-size: 13px; color: #888;
  cursor: pointer; transition: all 0.2s;
}

.clear-notifs:hover { border-color: #b73f2a; color: #b73f2a; }

/* ─── Drawer user / guest cards ─────────────── */
.drawer-user-card, .drawer-guest-card {
  display: flex; align-items: center; gap: 14px;
  padding: 14px 16px;
  background: #f9f8f6; border-radius: 14px; margin-bottom: 4px;
}

.drawer-user-avatar { width: 50px; height: 50px; border-radius: 50%; overflow: hidden; flex-shrink: 0; }
.drawer-user-avatar img { width: 100%; height: 100%; object-fit: cover; }

.drawer-user-initials {
  width: 100%; height: 100%;
  background: linear-gradient(135deg, #b73f2a, #d4614a);
  color: #fff;
  display: flex; align-items: center; justify-content: center;
  font-size: 18px; font-weight: 700;
}

.drawer-guest-icon {
  width: 50px; height: 50px; border-radius: 50%;
  background: #e8e4df;
  display: flex; align-items: center; justify-content: center;
  font-size: 20px; color: #aaa; flex-shrink: 0;
}

.drawer-user-name  { font-size: 14px; font-weight: 600; color: #111; margin: 0 0 2px; }
.drawer-user-email { font-size: 12px; color: #999; margin: 0; }

.drawer-auth-btns { display: flex; gap: 8px; margin-top: 8px; }

.auth-btn {
  padding: 7px 14px; border-radius: 8px;
  font-family: 'DM Sans', sans-serif; font-size: 12.5px; font-weight: 500;
  text-decoration: none; transition: all 0.2s;
}

.auth-btn--primary { background: #b73f2a; color: #fff; }
.auth-btn--primary:hover { background: #9a3523; }
.auth-btn--outline { border: 1.5px solid #ddd; color: #333; }
.auth-btn--outline:hover { border-color: #b73f2a; color: #b73f2a; }

.drawer-divider { height: 1px; background: #f0f0f0; margin: 16px 0 12px; }

.drawer-section-label {
  font-size: 9.5px; letter-spacing: 2.5px; font-weight: 600; color: #bbb;
  margin: 0 0 8px 4px;
}

.drawer-nav { display: flex; flex-direction: column; gap: 2px; }

.drawer-nav-item {
  display: flex; align-items: center; gap: 12px;
  padding: 11px 12px; border-radius: 10px;
  font-size: 14px; color: #333; text-decoration: none;
  border: none; background: none; width: 100%; text-align: left;
  cursor: pointer;
  font-family: 'DM Sans', sans-serif;
  transition: background 0.15s, color 0.15s;
}

.drawer-nav-item:hover { background: #f5f2ef; color: #b73f2a; }
.drawer-nav-item.router-link-exact-active { background: rgba(183,63,42,0.08); color: #b73f2a; font-weight: 600; }

.dnav-icon {
  width: 34px; height: 34px; background: #f0ede9; border-radius: 8px;
  display: flex; align-items: center; justify-content: center;
  font-size: 14px; color: #777; flex-shrink: 0;
  transition: background 0.15s, color 0.15s;
}

.drawer-nav-item:hover .dnav-icon,
.drawer-nav-item.router-link-exact-active .dnav-icon { background: rgba(183,63,42,0.12); color: #b73f2a; }

.dnav-arrow { margin-left: auto; font-size: 11px; color: #ccc; }

.drawer-logout { color: #e53e3e; }
.drawer-logout:hover { background: #fff5f5; color: #c0392b; }
.drawer-logout .dnav-icon { color: #e53e3e; }
.drawer-logout:hover .dnav-icon { background: #fff0f0; }

.drawer-footer {
  display: flex; justify-content: space-between; align-items: center;
  padding: 16px 4px 20px; margin-top: auto;
  border-top: 1px solid #f0f0f0;
}

.drawer-footer-text { font-size: 11px; color: #bbb; margin: 0; }
.drawer-socials { display: flex; gap: 8px; }

.dsocial {
  width: 30px; height: 30px; border-radius: 50%;
  border: 1px solid #e5e5e5;
  display: flex; align-items: center; justify-content: center;
  color: #aaa; font-size: 12px; text-decoration: none;
  transition: all 0.2s;
}

.dsocial:hover { border-color: #b73f2a; color: #b73f2a; }

/* ─── Notification slide animation ─────────── */
.notif-slide-enter-active { transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1); }
.notif-slide-enter-from   { opacity: 0; transform: translateY(-12px) scale(0.96); }
.notif-slide-leave-active { transition: all 0.2s ease; }
.notif-slide-leave-to     { opacity: 0; transform: translateX(20px); }

/* ─── Backdrop / drawer transitions ─────────── */
.backdrop-enter-active, .backdrop-leave-active { transition: opacity 0.3s ease; }
.backdrop-enter-from,  .backdrop-leave-to      { opacity: 0; }

.drawer-enter-active, .drawer-leave-active { transition: transform 0.3s cubic-bezier(0.4,0,0.2,1); }
.drawer-enter-from,  .drawer-leave-to      { transform: translateX(100%); }

/* ─── Responsive ────────────────────────────── */
@media (max-width: 900px) {
  .nav-links {
    position: fixed;
    top: 68px; left: 0; right: 0;
    background: rgba(246,244,241,0.98);
    backdrop-filter: blur(14px);
    flex-direction: column; align-items: flex-start;
    padding: 16px 24px 24px; gap: 4px;
    border-bottom: 1px solid rgba(0,0,0,0.06);
    box-shadow: 0 8px 24px rgba(0,0,0,0.08);
    transform: translateY(-120%); opacity: 0; pointer-events: none;
    transition: transform 0.3s ease, opacity 0.3s ease;
  }

  .nav-links.mobile-open { transform: translateY(0); opacity: 1; pointer-events: auto; }

  .nav-link { width: 100%; padding: 12px 14px; font-size: 15px; }
  .mobile-toggle { display: flex; }
  .drawer-btn { display: none; }
}

@media (max-width: 480px) {
  .navbar-inner { padding: 0 16px; gap: 12px; }
  .drawer { width: 100%; }
}
</style>