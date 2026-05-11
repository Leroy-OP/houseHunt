<template>
  <div class="hs-settings-page">

    <!-- ── PAGE HEADER ──────────────────────────────────────────────── -->
    <div class="hs-page-header">
      <div class="hs-page-header-inner">
        <div class="hs-breadcrumb">
          <router-link to="/" class="hs-breadcrumb-link">
            <i class="fas fa-home"></i>
          </router-link>
          <span class="hs-breadcrumb-sep"><i class="fas fa-chevron-right"></i></span>
          <span class="hs-breadcrumb-current">Settings</span>
        </div>
        <h1 class="hs-page-title">Account Settings</h1>
        <p class="hs-page-sub">Manage your profile, security, and role preferences.</p>
      </div>
    </div>

    <!-- ── FULL-PAGE SKELETON (initial load) ─────────────────────────── -->
    <div v-if="appLoading" class="hs-settings-wrap">
      <div class="hs-sidebar hs-skeleton-sidebar">
        <div class="hs-sk hs-sk--block" style="height:68px;margin:16px 14px 8px;border-radius:10px"></div>
        <div v-for="n in 7" :key="n" class="hs-sk hs-sk--line" :style="`margin:8px 14px;width:${70+n*3}%`"></div>
        <div class="hs-sk hs-sk--circle" style="margin:16px 14px"></div>
      </div>
      <div class="hs-main">
        <div class="hs-sk hs-sk--block" style="height:32px;width:200px;margin-bottom:8px"></div>
        <div class="hs-sk hs-sk--line" style="width:360px;margin-bottom:24px"></div>
        <div class="hs-card hs-skeleton-card">
          <div v-for="n in 5" :key="n" class="hs-sk hs-sk--line" :style="`width:${40+n*10}%`"></div>
        </div>
        <div class="hs-card hs-skeleton-card">
          <div v-for="n in 4" :key="n" class="hs-sk hs-sk--line" :style="`width:${50+n*8}%`"></div>
        </div>
      </div>
    </div>

    <!-- ── MAIN LAYOUT ───────────────────────────────────────────────── -->
    <div v-else class="hs-settings-wrap">

      <!-- ── SIDEBAR ──────────────────────────────────────────────────── -->
      <aside class="hs-sidebar">

        <!-- Role switcher -->
        <div class="hs-sb-section hs-sb-top">
          <p class="hs-sb-label">Active role</p>
          <div class="hs-role-switch" :class="{ 'hs-role-switch--loading': roleSwitching }">
            <button
              class="hs-role-btn"
              :class="{ active: activeRole === 'agent' }"
              :disabled="roleSwitching || !availableRoles.includes('agent')"
              @click="switchRole('agent')"
            >
              <i class="fas fa-user-tie"></i> Agent
            </button>
            <button
              class="hs-role-btn"
              :class="{ active: activeRole === 'tenant' }"
              :disabled="roleSwitching || !availableRoles.includes('tenant')"
              @click="switchRole('tenant')"
            >
              <i class="fas fa-key"></i> Tenant
            </button>
          </div>
          <div class="hs-role-status">
            <span v-if="roleSwitching" class="hs-spinner-xs"></span>
            <span v-else class="hs-status-dot" :class="roleConfig.statusColor"></span>
            {{ roleSwitching ? 'Switching role…' : roleConfig.statusLabel }}
          </div>
        </div>

        <!-- Nav: Account -->
        <div class="hs-sb-section">
          <p class="hs-sb-label">Account</p>
          <nav class="hs-sb-nav">
            <button
              v-for="item in accountNav"
              :key="item.id"
              class="hs-nav-item"
              :class="{ active: activePanel === item.id }"
              @click="navigateTo(item.id)"
            >
              <span class="hs-ni-icon"><i :class="item.icon"></i></span>
              {{ item.label }}
              <span v-if="item.badge" class="hs-ni-badge">{{ item.badge }}</span>
            </button>
          </nav>
        </div>

        <!-- Nav: Role-specific -->
        <div class="hs-sb-section">
          <p class="hs-sb-label">{{ roleConfig.navHeading }}</p>
          <nav class="hs-sb-nav">
            <button
              v-for="item in roleConfig.nav"
              :key="item.id"
              class="hs-nav-item"
              :class="{ active: activePanel === item.id }"
              @click="navigateTo(item.id)"
            >
              <span class="hs-ni-icon"><i :class="item.icon"></i></span>
              {{ item.label }}
            </button>
          </nav>
        </div>

        <!-- User footer -->
        <div class="hs-sb-footer">
          <div class="hs-sb-user">
            <div class="hs-sb-avatar">
              <img v-if="user?.avatar" :src="user.avatar" :alt="user.name" @error="onAvatarError" />
              <span v-else>{{ getInitials(user?.name || 'Guest User') }}</span>
            </div>
            <div class="hs-sb-user-info">
              <p class="hs-sb-user-name">{{ user?.name || 'Guest User' }}</p>
              <p class="hs-sb-user-email">{{ user?.email || 'Not signed in' }}</p>
            </div>
          </div>
        </div>

      </aside>

      <!-- ── MAIN CONTENT ─────────────────────────────────────────────── -->
      <main class="hs-main">

        <!-- ── PROFILE ──────────────────────────────────────────────────── -->
        <section v-if="activePanel === 'profile'" class="hs-panel">
          <div class="hs-panel-header">
            <h2>Profile</h2>
            <p>Manage your personal details and public-facing information.</p>
          </div>

          <!-- Section skeleton -->
          <template v-if="loadingStates.profile">
            <div class="hs-card hs-skeleton-card">
              <div class="hs-sk hs-sk--circle" style="width:72px;height:72px"></div>
              <div v-for="n in 4" :key="n" class="hs-sk hs-sk--line" :style="`width:${40+n*12}%`"></div>
            </div>
            <div class="hs-card hs-skeleton-card">
              <div v-for="n in 5" :key="n" class="hs-sk hs-sk--line" :style="`width:${50+n*8}%`"></div>
            </div>
          </template>

          <template v-else>
            <!-- Photo & identity -->
            <div class="hs-card">
              <div class="hs-card-title"><i class="fas fa-camera"></i> Photo & identity</div>
              <div class="hs-photo-row">
                <div class="hs-photo-avatar">
                  <img v-if="user?.avatar" :src="user.avatar" :alt="user.name" @error="onAvatarError" />
                  <span v-else>{{ getInitials(profileForm.firstName + ' ' + profileForm.lastName) }}</span>
                  <label class="hs-avatar-overlay" title="Change photo">
                    <i class="fas fa-camera"></i>
                    <input type="file" accept="image/*" style="display:none" @change="uploadAvatar" />
                  </label>
                </div>
                <div class="hs-photo-meta">
                  <p class="hs-photo-name">{{ profileForm.firstName }} {{ profileForm.lastName }}</p>
                  <p class="hs-photo-role">{{ roleConfig.statusLabel }}</p>
                  <div class="hs-photo-actions">
                    <label class="hs-btn" :class="{ 'hs-btn--loading': savingStates.avatar }">
                      <i class="fas fa-upload"></i>
                      {{ savingStates.avatar ? 'Uploading…' : 'Upload photo' }}
                      <input v-if="!savingStates.avatar" type="file" accept="image/*" style="display:none" @change="uploadAvatar" />
                    </label>
                    <button class="hs-btn hs-btn--danger-ghost" :disabled="savingStates.avatar" @click="removeAvatar">
                      Remove
                    </button>
                  </div>
                </div>
                <div class="hs-verify-pills">
                  <span class="hs-verify-pill" :class="user?.emailVerified ? 'green' : 'grey'">
                    <i :class="user?.emailVerified ? 'fas fa-check-circle' : 'fas fa-clock'"></i>
                    {{ user?.emailVerified ? 'Email verified' : 'Email unverified' }}
                  </span>
                  <span class="hs-verify-pill" :class="user?.phoneVerified ? 'blue' : 'grey'">
                    <i :class="user?.phoneVerified ? 'fas fa-check-circle' : 'fas fa-clock'"></i>
                    {{ user?.phoneVerified ? 'Phone verified' : 'Phone unverified' }}
                  </span>
                </div>
              </div>

              <div class="hs-field-row">
                <div class="hs-field">
                  <label>First name</label>
                  <input v-model="profileForm.firstName" type="text" :disabled="savingStates.profile" />
                </div>
                <div class="hs-field">
                  <label>Last name</label>
                  <input v-model="profileForm.lastName" type="text" :disabled="savingStates.profile" />
                </div>
              </div>
              <div class="hs-field-row">
                <div class="hs-field">
                  <label>Email address</label>
                  <div class="hs-field-with-action">
                    <input v-model="profileForm.email" type="email" :disabled="savingStates.profile" />
                    <button
                      v-if="profileForm.email !== user?.email"
                      class="hs-field-action"
                      @click="requestEmailVerification"
                    >Verify</button>
                  </div>
                </div>
                <div class="hs-field">
                  <label>Phone number</label>
                  <input v-model="profileForm.phone" type="tel" :disabled="savingStates.profile" />
                </div>
              </div>
            </div>

            <!-- Role-specific profile card -->
            <div class="hs-card">
              <div class="hs-card-title">
                <i class="fas fa-id-badge"></i> {{ roleConfig.profile.cardTitle }}
              </div>
              <div class="hs-field-row hs-field-row--full">
                <div class="hs-field">
                  <label>{{ roleConfig.profile.bioLabel }}</label>
                  <textarea v-model="profileForm.bio" rows="4" :disabled="savingStates.profile"></textarea>
                </div>
              </div>
              <div v-if="activeRole === 'agent'" class="hs-field-row">
                <div class="hs-field">
                  <label>License number</label>
                  <input v-model="profileForm.licenseNumber" type="text" :disabled="savingStates.profile" />
                </div>
                <div class="hs-field">
                  <label>Years of experience</label>
                  <input v-model="profileForm.experience" type="number" min="0" :disabled="savingStates.profile" />
                </div>
              </div>
              <div v-if="activeRole === 'tenant'" class="hs-field-row">
                <div class="hs-field">
                  <label>Occupation</label>
                  <input v-model="profileForm.occupation" type="text" placeholder="e.g. Software Engineer" :disabled="savingStates.profile" />
                </div>
                <div class="hs-field">
                  <label>Emergency contact</label>
                  <input v-model="profileForm.emergencyContact" type="tel" placeholder="+254 7XX XXX XXX" :disabled="savingStates.profile" />
                </div>
              </div>
            </div>

            <div class="hs-btn-row">
              <button class="hs-btn" :disabled="savingStates.profile" @click="resetProfileForm">Discard</button>
              <button
                class="hs-btn hs-btn--primary"
                :class="{ 'hs-btn--loading': savingStates.profile }"
                :disabled="savingStates.profile"
                @click="saveProfile"
              >
                <i v-if="!savingStates.profile" class="fas fa-check"></i>
                <span v-if="savingStates.profile" class="hs-spinner-sm"></span>
                {{ savingStates.profile ? 'Saving…' : 'Save changes' }}
              </button>
            </div>
          </template>
        </section>

        <!-- ── SECURITY ─────────────────────────────────────────────────── -->
        <section v-if="activePanel === 'security'" class="hs-panel">
          <div class="hs-panel-header">
            <h2>Security</h2>
            <p>Control your password, two-factor authentication and active sessions.</p>
          </div>

          <template v-if="loadingStates.security">
            <div class="hs-card hs-skeleton-card"><div v-for="n in 4" :key="n" class="hs-sk hs-sk--line"></div></div>
            <div class="hs-card hs-skeleton-card"><div v-for="n in 3" :key="n" class="hs-sk hs-sk--line"></div></div>
          </template>

          <template v-else>
            <div class="hs-card">
              <div class="hs-card-title"><i class="fas fa-key"></i> Password</div>
              <div class="hs-field-row hs-field-row--full">
                <div class="hs-field">
                  <label>Current password</label>
                  <input v-model="passwordForm.current" type="password" placeholder="Enter current password" :disabled="savingStates.password" />
                </div>
              </div>
              <div class="hs-field-row">
                <div class="hs-field">
                  <label>New password</label>
                  <input v-model="passwordForm.newPass" type="password" placeholder="Min. 10 characters" :disabled="savingStates.password" />
                </div>
                <div class="hs-field">
                  <label>Confirm new password</label>
                  <input v-model="passwordForm.confirm" type="password" placeholder="Repeat new password" :disabled="savingStates.password" />
                </div>
              </div>
              <p v-if="passwordError" class="hs-field-error">{{ passwordError }}</p>
              <div class="hs-btn-row">
                <button
                  class="hs-btn hs-btn--primary"
                  :class="{ 'hs-btn--loading': savingStates.password }"
                  :disabled="savingStates.password"
                  @click="updatePassword"
                >
                  <i v-if="!savingStates.password" class="fas fa-lock"></i>
                  <span v-else class="hs-spinner-sm"></span>
                  {{ savingStates.password ? 'Updating…' : 'Update password' }}
                </button>
              </div>
            </div>

            <div class="hs-card">
              <div class="hs-card-title"><i class="fas fa-mobile-alt"></i> Two-factor authentication</div>
              <div class="hs-toggle-row" v-for="tfa in tfaOptions" :key="tfa.id">
                <div class="hs-tgl-info">
                  <p class="hs-tgl-label">{{ tfa.label }}</p>
                  <p class="hs-tgl-desc">{{ tfa.desc }}</p>
                </div>
                <button
                  class="hs-toggle"
                  :class="{ on: tfa.enabled, 'hs-toggle--loading': tfa.saving }"
                  :disabled="tfa.saving"
                  :aria-label="'Toggle ' + tfa.label"
                  @click="toggleTFA(tfa)"
                ></button>
              </div>
            </div>

            <div class="hs-card">
              <div class="hs-card-title"><i class="fas fa-desktop"></i> Active sessions</div>
              <div v-if="loadingStates.sessions" class="hs-skeleton-card">
                <div v-for="n in 3" :key="n" class="hs-sk hs-sk--line"></div>
              </div>
              <template v-else>
                <div class="hs-session-row" v-for="session in sessions" :key="session.id">
                  <div class="hs-session-left">
                    <div class="hs-session-icon"><i :class="session.icon"></i></div>
                    <div>
                      <p class="hs-session-label">
                        {{ session.label }}
                        <span v-if="session.current" class="hs-badge hs-badge--green">Current</span>
                      </p>
                      <p class="hs-session-meta">{{ session.location }} · {{ session.time }}</p>
                    </div>
                  </div>
                  <button
                    v-if="!session.current"
                    class="hs-btn hs-btn--danger-ghost hs-btn--sm"
                    :class="{ 'hs-btn--loading': session.revoking }"
                    :disabled="session.revoking"
                    @click="revokeSession(session.id)"
                  >
                    {{ session.revoking ? '…' : 'Revoke' }}
                  </button>
                </div>
                <div class="hs-btn-row">
                  <button
                    class="hs-btn hs-btn--danger-ghost"
                    :class="{ 'hs-btn--loading': savingStates.revokeAll }"
                    :disabled="savingStates.revokeAll"
                    @click="revokeAllSessions"
                  >
                    <i v-if="!savingStates.revokeAll" class="fas fa-sign-out-alt"></i>
                    <span v-else class="hs-spinner-sm"></span>
                    {{ savingStates.revokeAll ? 'Revoking…' : 'Revoke all other sessions' }}
                  </button>
                </div>
              </template>
            </div>
          </template>
        </section>

        <!-- ── NOTIFICATIONS ──────────────────────────────────────────────── -->
        <section v-if="activePanel === 'notifications'" class="hs-panel">
          <div class="hs-panel-header">
            <h2>Notifications</h2>
            <p>Choose when and how you want to be notified across HunterStreet.</p>
          </div>

          <template v-if="loadingStates.notifications">
            <div class="hs-card hs-skeleton-card" v-for="n in 2" :key="n">
              <div v-for="m in 4" :key="m" class="hs-sk hs-sk--line"></div>
            </div>
          </template>

          <template v-else>
            <div class="hs-card" v-for="group in notifGroups" :key="group.id">
              <div class="hs-card-title"><i :class="group.icon"></i> {{ group.label }}</div>
              <div class="hs-toggle-row" v-for="item in group.items" :key="item.id">
                <div class="hs-tgl-info">
                  <p class="hs-tgl-label">{{ item.label }}</p>
                  <p class="hs-tgl-desc">{{ item.desc }}</p>
                </div>
                <button
                  class="hs-toggle"
                  :class="{ on: item.enabled, 'hs-toggle--loading': item.saving }"
                  :disabled="item.saving"
                  :aria-label="'Toggle ' + item.label"
                  @click="toggleNotification(item)"
                ></button>
              </div>
            </div>

            <div class="hs-btn-row">
              <button class="hs-btn" :disabled="savingStates.notifications" @click="resetNotifications">Reset to defaults</button>
              <button
                class="hs-btn hs-btn--primary"
                :class="{ 'hs-btn--loading': savingStates.notifications }"
                :disabled="savingStates.notifications"
                @click="saveNotifications"
              >
                <i v-if="!savingStates.notifications" class="fas fa-check"></i>
                <span v-else class="hs-spinner-sm"></span>
                {{ savingStates.notifications ? 'Saving…' : 'Save preferences' }}
              </button>
            </div>
          </template>
        </section>

        <!-- ── PRIVACY ───────────────────────────────────────────────────── -->
        <section v-if="activePanel === 'privacy'" class="hs-panel">
          <div class="hs-panel-header">
            <h2>Privacy & data</h2>
            <p>Control what you share and how your data is used across HunterStreet.</p>
          </div>

          <template v-if="loadingStates.privacy">
            <div class="hs-card hs-skeleton-card"><div v-for="n in 4" :key="n" class="hs-sk hs-sk--line"></div></div>
          </template>

          <template v-else>
            <div class="hs-card">
              <div class="hs-card-title"><i class="fas fa-eye"></i> Profile visibility</div>
              <div class="hs-toggle-row" v-for="item in privacyOptions" :key="item.id">
                <div class="hs-tgl-info">
                  <p class="hs-tgl-label">{{ item.label }}</p>
                  <p class="hs-tgl-desc">{{ item.desc }}</p>
                </div>
                <button
                  class="hs-toggle"
                  :class="{ on: item.enabled, 'hs-toggle--loading': item.saving }"
                  :disabled="item.saving"
                  :aria-label="'Toggle ' + item.label"
                  @click="togglePrivacy(item)"
                ></button>
              </div>
            </div>

            <div class="hs-card hs-card--danger">
              <div class="hs-card-title">
                <i class="fas fa-exclamation-triangle" style="color:#e53e3e"></i> Danger zone
              </div>
              <div class="hs-danger-item">
                <div>
                  <p class="hs-danger-label">Export my data</p>
                  <p class="hs-danger-desc">Download a full copy of your HunterStreet account data as CSV</p>
                </div>
                <button
                  class="hs-btn"
                  :class="{ 'hs-btn--loading': savingStates.export }"
                  :disabled="savingStates.export"
                  @click="exportData"
                >
                  <i v-if="!savingStates.export" class="fas fa-download"></i>
                  <span v-else class="hs-spinner-sm"></span>
                  {{ savingStates.export ? 'Preparing…' : 'Export' }}
                </button>
              </div>
              <div class="hs-danger-item">
                <div>
                  <p class="hs-danger-label hs-danger-label--red">Delete account</p>
                  <p class="hs-danger-desc">Permanently remove your account and all associated data</p>
                </div>
                <button class="hs-btn hs-btn--danger-ghost" @click="confirmDeleteAccount">
                  <i class="fas fa-trash-alt"></i> Delete
                </button>
              </div>
            </div>
          </template>
        </section>

        <!-- ── AGENT: AGENCY PROFILE ──────────────────────────────────────── -->
        <section v-if="activePanel === 'agency' && activeRole === 'agent'" class="hs-panel">
          <div class="hs-panel-header">
            <h2>Agency profile</h2>
            <p>Your professional details displayed to clients and on all listings.</p>
          </div>

          <template v-if="loadingStates.agency">
            <div class="hs-card hs-skeleton-card"><div v-for="n in 5" :key="n" class="hs-sk hs-sk--line"></div></div>
          </template>

          <template v-else>
            <div class="hs-card">
              <div class="hs-card-title"><i class="fas fa-building"></i> Company details</div>
              <div class="hs-field-row">
                <div class="hs-field">
                  <label>Agency name</label>
                  <input v-model="agencyForm.name" type="text" :disabled="savingStates.agency" />
                </div>
                <div class="hs-field">
                  <label>Registration no.</label>
                  <input v-model="agencyForm.regNo" type="text" :disabled="savingStates.agency" />
                </div>
              </div>
              <div class="hs-field-row">
                <div class="hs-field">
                  <label>Website</label>
                  <input v-model="agencyForm.website" type="url" :disabled="savingStates.agency" />
                </div>
                <div class="hs-field">
                  <label>Service areas</label>
                  <input v-model="agencyForm.areas" type="text" placeholder="e.g. Westlands, Kilimani" :disabled="savingStates.agency" />
                </div>
              </div>
              <div class="hs-field-row hs-field-row--full">
                <div class="hs-field">
                  <label>Agency description</label>
                  <textarea v-model="agencyForm.description" rows="4" :disabled="savingStates.agency"></textarea>
                </div>
              </div>
            </div>

            <div class="hs-card">
              <div class="hs-card-title"><i class="fas fa-award"></i> Specialisations & availability</div>
              <div class="hs-tags-row">
                <span class="hs-tag" v-for="(tag, i) in agencyForm.specialisations" :key="i">
                  {{ tag }}
                  <button class="hs-tag-remove" @click="agencyForm.specialisations.splice(i,1)">
                    <i class="fas fa-times"></i>
                  </button>
                </span>
                <button class="hs-btn hs-btn--sm" @click="addSpecialisation">
                  <i class="fas fa-plus"></i> Add
                </button>
              </div>
              <div class="hs-field-row" style="margin-top:14px">
                <div class="hs-field">
                  <label>Languages</label>
                  <input v-model="agencyForm.languages" type="text" :disabled="savingStates.agency" />
                </div>
                <div class="hs-field">
                  <label>Operating hours</label>
                  <input v-model="agencyForm.hours" type="text" :disabled="savingStates.agency" />
                </div>
              </div>
            </div>

            <div class="hs-btn-row">
              <button class="hs-btn" :disabled="savingStates.agency" @click="fetchAgency">Discard</button>
              <button
                class="hs-btn hs-btn--primary"
                :class="{ 'hs-btn--loading': savingStates.agency }"
                :disabled="savingStates.agency"
                @click="saveAgency"
              >
                <i v-if="!savingStates.agency" class="fas fa-check"></i>
                <span v-else class="hs-spinner-sm"></span>
                {{ savingStates.agency ? 'Saving…' : 'Save agency profile' }}
              </button>
            </div>
          </template>
        </section>

        <!-- ── AGENT: LISTINGS ─────────────────────────────────────────────── -->
        <section v-if="activePanel === 'listings' && activeRole === 'agent'" class="hs-panel">
          <div class="hs-panel-header">
            <h2>Listings</h2>
            <p>Default settings applied to all new property listings.</p>
          </div>

          <template v-if="loadingStates.listings">
            <div class="hs-stat-grid"><div v-for="n in 3" :key="n" class="hs-sk hs-sk--block" style="height:80px;border-radius:12px"></div></div>
            <div class="hs-card hs-skeleton-card"><div v-for="n in 4" :key="n" class="hs-sk hs-sk--line"></div></div>
          </template>

          <template v-else>
            <div class="hs-stat-grid">
              <div class="hs-stat-card" v-for="stat in listingStats" :key="stat.label">
                <p class="hs-stat-val">{{ stat.value }}</p>
                <p class="hs-stat-lbl">{{ stat.label }}</p>
              </div>
            </div>

            <div class="hs-card">
              <div class="hs-card-title"><i class="fas fa-home"></i> Listing defaults</div>
              <div class="hs-field-row">
                <div class="hs-field">
                  <label>Default currency</label>
                  <select v-model="listingForm.currency" :disabled="savingStates.listings">
                    <option value="KES">KES – Kenyan Shilling</option>
                    <option value="USD">USD – US Dollar</option>
                    <option value="GBP">GBP – British Pound</option>
                  </select>
                </div>
                <div class="hs-field">
                  <label>Price display</label>
                  <select v-model="listingForm.priceDisplay" :disabled="savingStates.listings">
                    <option>Per month</option>
                    <option>Per year</option>
                    <option>Total price</option>
                  </select>
                </div>
              </div>
              <div class="hs-toggle-row" v-for="item in listingToggles" :key="item.id">
                <div class="hs-tgl-info">
                  <p class="hs-tgl-label">{{ item.label }}</p>
                  <p class="hs-tgl-desc">{{ item.desc }}</p>
                </div>
                <button
                  class="hs-toggle"
                  :class="{ on: item.enabled, 'hs-toggle--loading': item.saving }"
                  :disabled="item.saving"
                  :aria-label="'Toggle ' + item.label"
                  @click="item.enabled = !item.enabled"
                ></button>
              </div>
            </div>

            <div class="hs-btn-row">
              <button
                class="hs-btn hs-btn--primary"
                :class="{ 'hs-btn--loading': savingStates.listings }"
                :disabled="savingStates.listings"
                @click="saveListingSettings"
              >
                <i v-if="!savingStates.listings" class="fas fa-check"></i>
                <span v-else class="hs-spinner-sm"></span>
                {{ savingStates.listings ? 'Saving…' : 'Save listing settings' }}
              </button>
            </div>
          </template>
        </section>

        <!-- ── AGENT: COMMISSION & PAYMENTS ───────────────────────────────── -->
        <section v-if="activePanel === 'commission' && activeRole === 'agent'" class="hs-panel">
          <div class="hs-panel-header">
            <h2>Commission & payments</h2>
            <p>Configure your commission rates and payout preferences.</p>
          </div>

          <template v-if="loadingStates.commission">
            <div class="hs-card hs-skeleton-card"><div v-for="n in 4" :key="n" class="hs-sk hs-sk--line"></div></div>
            <div class="hs-card hs-skeleton-card"><div v-for="n in 3" :key="n" class="hs-sk hs-sk--line"></div></div>
          </template>

          <template v-else>
            <div class="hs-card">
              <div class="hs-card-title"><i class="fas fa-percentage"></i> Commission rates</div>
              <div class="hs-field-row">
                <div class="hs-field">
                  <label>Residential sales (%)</label>
                  <input v-model.number="commissionForm.residential" type="number" min="0" max="100" step="0.5" :disabled="savingStates.commission" />
                </div>
                <div class="hs-field">
                  <label>Commercial sales (%)</label>
                  <input v-model.number="commissionForm.commercial" type="number" min="0" max="100" step="0.5" :disabled="savingStates.commission" />
                </div>
              </div>
              <div class="hs-field-row">
                <div class="hs-field">
                  <label>Rental (% of annual)</label>
                  <input v-model.number="commissionForm.rental" type="number" min="0" max="100" step="0.5" :disabled="savingStates.commission" />
                </div>
                <div class="hs-field">
                  <label>Off-plan (%)</label>
                  <input v-model.number="commissionForm.offplan" type="number" min="0" max="100" step="0.5" :disabled="savingStates.commission" />
                </div>
              </div>
            </div>

            <div class="hs-card">
              <div class="hs-card-title"><i class="fas fa-university"></i> Payout account</div>
              <div class="hs-field-row">
                <div class="hs-field">
                  <label>Bank name</label>
                  <input v-model="commissionForm.bankName" type="text" :disabled="savingStates.commission" />
                </div>
                <div class="hs-field">
                  <label>Account number</label>
                  <input v-model="commissionForm.accountNumber" type="text" :disabled="savingStates.commission" />
                </div>
              </div>
              <div class="hs-field-row">
                <div class="hs-field">
                  <label>Payout frequency</label>
                  <select v-model="commissionForm.frequency" :disabled="savingStates.commission">
                    <option>Monthly</option>
                    <option>Bi-weekly</option>
                    <option>Weekly</option>
                  </select>
                </div>
                <div class="hs-field">
                  <label>M-Pesa number</label>
                  <input v-model="commissionForm.mpesa" type="tel" :disabled="savingStates.commission" />
                </div>
              </div>
            </div>

            <div class="hs-btn-row">
              <button class="hs-btn" :disabled="savingStates.commission" @click="fetchCommission">Discard</button>
              <button
                class="hs-btn hs-btn--primary"
                :class="{ 'hs-btn--loading': savingStates.commission }"
                :disabled="savingStates.commission"
                @click="saveCommission"
              >
                <i v-if="!savingStates.commission" class="fas fa-check"></i>
                <span v-else class="hs-spinner-sm"></span>
                {{ savingStates.commission ? 'Saving…' : 'Save payment settings' }}
              </button>
            </div>
          </template>
        </section>

        <!-- ── TENANT: RENTAL PREFERENCES ─────────────────────────────────── -->
        <section v-if="activePanel === 'preferences' && activeRole === 'tenant'" class="hs-panel">
          <div class="hs-panel-header">
            <h2>Rental preferences</h2>
            <p>Set your property search criteria and wishlist filters.</p>
          </div>

          <template v-if="loadingStates.preferences">
            <div class="hs-card hs-skeleton-card"><div v-for="n in 5" :key="n" class="hs-sk hs-sk--line"></div></div>
          </template>

          <template v-else>
            <div class="hs-card">
              <div class="hs-card-title"><i class="fas fa-search"></i> Search preferences</div>
              <div class="hs-field-row">
                <div class="hs-field">
                  <label>Preferred location</label>
                  <input v-model="tenantPrefForm.location" type="text" placeholder="e.g. Kilimani, Lavington" :disabled="savingStates.preferences" />
                </div>
                <div class="hs-field">
                  <label>Property type</label>
                  <select v-model="tenantPrefForm.propertyType" :disabled="savingStates.preferences">
                    <option>Apartment</option>
                    <option>House</option>
                    <option>Studio</option>
                    <option>Townhouse</option>
                    <option>Penthouse</option>
                  </select>
                </div>
              </div>
              <div class="hs-field-row">
                <div class="hs-field">
                  <label>Min budget (KES/mo)</label>
                  <input v-model.number="tenantPrefForm.minBudget" type="number" min="0" step="1000" :disabled="savingStates.preferences" />
                </div>
                <div class="hs-field">
                  <label>Max budget (KES/mo)</label>
                  <input v-model.number="tenantPrefForm.maxBudget" type="number" min="0" step="1000" :disabled="savingStates.preferences" />
                </div>
              </div>
              <div class="hs-field-row">
                <div class="hs-field">
                  <label>Bedrooms</label>
                  <select v-model="tenantPrefForm.bedrooms" :disabled="savingStates.preferences">
                    <option>Any</option>
                    <option>Studio</option>
                    <option>1</option>
                    <option>2</option>
                    <option>3</option>
                    <option>4+</option>
                  </select>
                </div>
                <div class="hs-field">
                  <label>Move-in date</label>
                  <input v-model="tenantPrefForm.moveIn" type="date" :disabled="savingStates.preferences" />
                </div>
              </div>
            </div>

            <div class="hs-card">
              <div class="hs-card-title"><i class="fas fa-list-ul"></i> Must-have amenities</div>
              <div class="hs-tags-row">
                <span class="hs-tag" v-for="(tag, i) in tenantPrefForm.amenities" :key="i">
                  {{ tag }}
                  <button class="hs-tag-remove" @click="tenantPrefForm.amenities.splice(i,1)"><i class="fas fa-times"></i></button>
                </span>
                <button class="hs-btn hs-btn--sm" @click="addAmenity">
                  <i class="fas fa-plus"></i> Add
                </button>
              </div>
            </div>

            <div class="hs-btn-row">
              <button class="hs-btn" :disabled="savingStates.preferences" @click="fetchTenantPreferences">Discard</button>
              <button
                class="hs-btn hs-btn--primary"
                :class="{ 'hs-btn--loading': savingStates.preferences }"
                :disabled="savingStates.preferences"
                @click="saveTenantPreferences"
              >
                <i v-if="!savingStates.preferences" class="fas fa-check"></i>
                <span v-else class="hs-spinner-sm"></span>
                {{ savingStates.preferences ? 'Saving…' : 'Save preferences' }}
              </button>
            </div>
          </template>
        </section>

        <!-- ── TENANT: LEASE & DOCUMENTS ──────────────────────────────────── -->
        <section v-if="activePanel === 'lease' && activeRole === 'tenant'" class="hs-panel">
          <div class="hs-panel-header">
            <h2>Lease & documents</h2>
            <p>View and manage your lease agreements and uploaded files.</p>
          </div>

          <template v-if="loadingStates.lease">
            <div class="hs-stat-grid"><div v-for="n in 3" :key="n" class="hs-sk hs-sk--block" style="height:80px;border-radius:12px"></div></div>
            <div class="hs-card hs-skeleton-card"><div v-for="n in 3" :key="n" class="hs-sk hs-sk--line"></div></div>
          </template>

          <template v-else>
            <div class="hs-stat-grid">
              <div class="hs-stat-card" v-for="stat in leaseStats" :key="stat.label">
                <p class="hs-stat-val">{{ stat.value }}</p>
                <p class="hs-stat-lbl">{{ stat.label }}</p>
              </div>
            </div>

            <div class="hs-card">
              <div class="hs-card-title"><i class="fas fa-file-contract"></i> Current lease</div>
              <div class="hs-doc-item" v-for="doc in leaseDocuments" :key="doc.id">
                <div class="hs-doc-icon"><i :class="doc.icon"></i></div>
                <div class="hs-doc-info">
                  <p class="hs-doc-name">{{ doc.name }}</p>
                  <p class="hs-doc-meta">{{ doc.meta }}</p>
                </div>
                <button class="hs-btn hs-btn--sm" @click="downloadDocument(doc)">
                  <i class="fas fa-download"></i> Download
                </button>
              </div>
            </div>

            <div class="hs-card">
              <div class="hs-card-title"><i class="fas fa-upload"></i> Upload a document</div>
              <div
                class="hs-upload-zone"
                :class="{ 'hs-upload-zone--over': dragOver, 'hs-upload-zone--uploading': savingStates.upload }"
                @dragover.prevent="dragOver = true"
                @dragleave="dragOver = false"
                @drop.prevent="handleDrop"
                @click="$refs.fileInput.click()"
              >
                <i v-if="!savingStates.upload" class="fas fa-cloud-upload-alt"></i>
                <span v-else class="hs-spinner-lg"></span>
                <p>{{ savingStates.upload ? 'Uploading…' : 'Drag & drop or' }}
                  <span v-if="!savingStates.upload" class="hs-upload-link">browse files</span>
                </p>
                <p class="hs-upload-hint">PDF, JPG, PNG up to 10 MB</p>
              </div>
              <input ref="fileInput" type="file" accept=".pdf,.jpg,.jpeg,.png" style="display:none" @change="uploadDocument" />
            </div>
          </template>
        </section>

        <!-- ── TENANT: RENT & PAYMENTS ─────────────────────────────────────── -->
        <section v-if="activePanel === 'rent' && activeRole === 'tenant'" class="hs-panel">
          <div class="hs-panel-header">
            <h2>Rent & payments</h2>
            <p>Manage payment methods and view your rent history.</p>
          </div>

          <template v-if="loadingStates.rent">
            <div class="hs-stat-grid"><div v-for="n in 3" :key="n" class="hs-sk hs-sk--block" style="height:80px;border-radius:12px"></div></div>
            <div class="hs-card hs-skeleton-card"><div v-for="n in 4" :key="n" class="hs-sk hs-sk--line"></div></div>
          </template>

          <template v-else>
            <div class="hs-stat-grid">
              <div class="hs-stat-card" v-for="stat in rentStats" :key="stat.label">
                <p class="hs-stat-val">{{ stat.value }}</p>
                <p class="hs-stat-lbl">{{ stat.label }}</p>
              </div>
            </div>

            <div class="hs-card">
              <div class="hs-card-title"><i class="fas fa-coins"></i> Payment settings</div>
              <div class="hs-field-row">
                <div class="hs-field">
                  <label>Payment method</label>
                  <select v-model="rentForm.method" :disabled="savingStates.rent">
                    <option v-for="m in paymentMethods" :key="m.id" :value="m.id">{{ m.label }}</option>
                  </select>
                </div>
                <div class="hs-field">
                  <label>Auto-pay date</label>
                  <select v-model="rentForm.autoPayDate" :disabled="savingStates.rent">
                    <option>1st of month</option>
                    <option>5th of month</option>
                    <option>Manual only</option>
                  </select>
                </div>
              </div>
              <div class="hs-toggle-row">
                <div class="hs-tgl-info">
                  <p class="hs-tgl-label">Auto-pay enabled</p>
                  <p class="hs-tgl-desc">Automatically pay rent on the due date via your chosen method</p>
                </div>
                <button
                  class="hs-toggle"
                  :class="{ on: rentForm.autoPay }"
                  aria-label="Toggle auto-pay"
                  @click="rentForm.autoPay = !rentForm.autoPay"
                ></button>
              </div>
              <div class="hs-btn-row">
                <button
                  class="hs-btn hs-btn--primary"
                  :class="{ 'hs-btn--loading': savingStates.rent }"
                  :disabled="savingStates.rent"
                  @click="saveRentSettings"
                >
                  <i v-if="!savingStates.rent" class="fas fa-check"></i>
                  <span v-else class="hs-spinner-sm"></span>
                  {{ savingStates.rent ? 'Saving…' : 'Save payment settings' }}
                </button>
              </div>
            </div>

            <div class="hs-card">
              <div class="hs-card-title"><i class="fas fa-tools"></i> Maintenance requests</div>
              <div v-if="loadingStates.maintenance" class="hs-skeleton-card">
                <div v-for="n in 2" :key="n" class="hs-sk hs-sk--line"></div>
              </div>
              <template v-else>
                <div class="hs-maint-item" v-for="req in maintenanceRequests" :key="req.id">
                  <div class="hs-doc-icon"><i :class="req.icon"></i></div>
                  <div class="hs-doc-info">
                    <p class="hs-doc-name">{{ req.title }}</p>
                    <p class="hs-doc-meta">Submitted {{ req.date }}</p>
                  </div>
                  <span class="hs-badge" :class="`hs-badge--${req.statusColor}`">{{ req.status }}</span>
                </div>
                <div class="hs-btn-row">
                  <button class="hs-btn hs-btn--primary" @click="openNewMaintenanceRequest">
                    <i class="fas fa-plus"></i> New request
                  </button>
                </div>
              </template>
            </div>
          </template>
        </section>

      </main>
    </div>

    <!-- ── TOAST ────────────────────────────────────────────────────────── -->
    <transition name="hs-toast">
      <div v-if="toast.visible" class="hs-toast" :class="`hs-toast--${toast.type}`">
        <i :class="toast.type === 'success' ? 'fas fa-check-circle' : toast.type === 'error' ? 'fas fa-exclamation-circle' : 'fas fa-info-circle'"></i>
        {{ toast.message }}
      </div>
    </transition>

  </div>
</template>

<script>
import { ref, computed, reactive, onMounted, watch } from 'vue';

// ──
const API_BASE = import.meta.env?.VITE_API_BASE_URL || '/api';

function getAuthToken() {

  return localStorage.getItem('auth_token') || sessionStorage.getItem('auth_token') || '';
}

async function apiFetch(method, endpoint, body = null) {
  const token = getAuthToken();
  const opts = {
    method,
    headers: {
      'Content-Type': 'application/json',
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
    },
  };
  if (body !== null) opts.body = JSON.stringify(body);

  const res = await fetch(`${API_BASE}${endpoint}`, opts);

  if (res.status === 401) {
    // Token expired — redirect to login
    localStorage.removeItem('auth_token');
    window.location.href = '/login?redirect=/settings';
    throw new Error('Unauthorised');
  }

  const data = await res.json().catch(() => ({}));

  if (!res.ok) {
    throw new Error(data.message || data.error || `HTTP ${res.status}`);
  }

  return data;
}

async function apiUpload(endpoint, file, extraFields = {}) {
  const token = getAuthToken();
  const form = new FormData();
  form.append('file', file);
  Object.entries(extraFields).forEach(([k, v]) => form.append(k, v));

  const res = await fetch(`${API_BASE}${endpoint}`, {
    method: 'POST',
    headers: token ? { Authorization: `Bearer ${token}` } : {},
    body: form,
  });

  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(data.message || `HTTP ${res.status}`);
  return data;
}

export default {
  name: 'SettingsPage',

  setup() {
    // ── App-level loading ──────────────────────────────────────────────
    const appLoading = ref(true);

    // ── Per-section loading flags ──────────────────────────────────────
    const loadingStates = reactive({
      profile:      false,
      security:     false,
      sessions:     false,
      notifications:false,
      privacy:      false,
      agency:       false,
      listings:     false,
      commission:   false,
      preferences:  false,
      lease:        false,
      rent:         false,
      maintenance:  false,
    });

    // ── Per-action saving flags ────────────────────────────────────────
    const savingStates = reactive({
      profile:      false,
      avatar:       false,
      password:     false,
      revokeAll:    false,
      notifications:false,
      privacy:      false,
      export:       false,
      agency:       false,
      listings:     false,
      commission:   false,
      preferences:  false,
      upload:       false,
      rent:         false,
    });

    // ── Toast ──────────────────────────────────────────────────────────
    const toast = reactive({ visible: false, message: '', type: 'success' });
    let toastTimer = null;

    const showToast = (message, type = 'success') => {
      clearTimeout(toastTimer);
      toast.message = message;
      toast.type    = type;
      toast.visible = true;
      toastTimer = setTimeout(() => { toast.visible = false; }, 3500);
    };

    // ── User ───────────────────────────────────────────────────────────
    const user = ref(null);

    const getInitials = (name) => {
      if (!name) return '?';
      return name.split(' ').slice(0, 2).map(w => w[0]).join('').toUpperCase();
    };
    const onAvatarError = (e) => { e.target.style.display = 'none'; };

    // ── Role & panel ───────────────────────────────────────────────────
    const activeRole    = ref('agent');
    const activePanel   = ref('profile');
    const availableRoles= ref([]);
    const roleSwitching = ref(false);

    const roleConfigs = {
      agent: {
        statusLabel: 'Agent · Verified ✦',
        statusColor: 'green',
        navHeading:  'Agent tools',
        profile: { cardTitle: 'Agent bio', bioLabel: 'Professional bio' },
        nav: [
          { id: 'agency',     label: 'Agency profile',   icon: 'fas fa-building'    },
          { id: 'listings',   label: 'Listings',         icon: 'fas fa-home'        },
          { id: 'commission', label: 'Commission & pay', icon: 'fas fa-credit-card' },
        ],
      },
      tenant: {
        statusLabel: 'Tenant · Active lease',
        statusColor: 'blue',
        navHeading:  'Tenant tools',
        profile: { cardTitle: 'Tenant profile', bioLabel: 'About me (optional)' },
        nav: [
          { id: 'preferences', label: 'Rental preferences', icon: 'fas fa-search'        },
          { id: 'lease',       label: 'Lease & documents',  icon: 'fas fa-file-contract' },
          { id: 'rent',        label: 'Rent & payments',    icon: 'fas fa-coins'         },
        ],
      },
    };

    const roleConfig = computed(() => roleConfigs[activeRole.value]);

    const accountNav = [
      { id: 'profile',       label: 'Profile',        icon: 'fas fa-user-circle' },
      { id: 'security',      label: 'Security',       icon: 'fas fa-lock'        },
      { id: 'notifications', label: 'Notifications',  icon: 'fas fa-bell', badge: 0 },
      { id: 'privacy',       label: 'Privacy & data', icon: 'fas fa-shield-alt'  },
    ];

    // Navigate to a panel and lazy-fetch its data if needed
    const navigateTo = (panelId) => {
      activePanel.value = panelId;
      fetchPanelData(panelId);
    };

    // ── Switch role ────────────────────────────────────────────────────
    const switchRole = async (role) => {
      if (role === activeRole.value || roleSwitching.value) return;
      roleSwitching.value = true;
      try {
        await apiFetch('PUT', '/me/active-role', { role });
        activeRole.value  = role;
        activePanel.value = 'profile';
        await fetchProfile();
        showToast(`Switched to ${role} view.`);
      } catch (err) {
        showToast(err.message || 'Could not switch role.', 'error');
      } finally {
        roleSwitching.value = false;
      }
    };

    // ── Profile ────────────────────────────────────────────────────────
    const profileFormDefaults = {
      firstName: '', lastName: '', email: '', phone: '',
      bio: '', licenseNumber: '', experience: 0,
      occupation: '', emergencyContact: '',
    };
    const profileForm = reactive({ ...profileFormDefaults });
    let   profileSnapshot = { ...profileFormDefaults };

    const fetchProfile = async () => {
      loadingStates.profile = true;
      try {
        const data = await apiFetch('GET', '/me');
        user.value = {
          name:          `${data.firstName} ${data.lastName}`,
          email:         data.email,
          avatar:        data.avatar || null,
          emailVerified: data.emailVerified || false,
          phoneVerified: data.phoneVerified || false,
        };
        Object.assign(profileForm, {
          firstName:        data.firstName       || '',
          lastName:         data.lastName        || '',
          email:            data.email           || '',
          phone:            data.phone           || '',
          bio:              data.bio             || '',
          licenseNumber:    data.licenseNumber   || '',
          experience:       data.experience      || 0,
          occupation:       data.occupation      || '',
          emergencyContact: data.emergencyContact|| '',
        });
        profileSnapshot = { ...profileForm };

        // Update role info from server
        if (data.activeRole && roleConfigs[data.activeRole]) {
          activeRole.value = data.activeRole;
        }
        availableRoles.value = data.roles || [data.activeRole || 'agent'];
        // Update unread notification badge
        const notifNav = accountNav.find(n => n.id === 'notifications');
        if (notifNav) notifNav.badge = data.unreadNotifications || 0;
      } catch (err) {
        showToast(err.message || 'Could not load profile.', 'error');
      } finally {
        loadingStates.profile = false;
      }
    };

    const resetProfileForm = () => Object.assign(profileForm, profileSnapshot);

    const saveProfile = async () => {
      savingStates.profile = true;
      try {
        const updated = await apiFetch('PUT', '/me/profile', {
          firstName:        profileForm.firstName,
          lastName:         profileForm.lastName,
          email:            profileForm.email,
          phone:            profileForm.phone,
          bio:              profileForm.bio,
          licenseNumber:    profileForm.licenseNumber,
          experience:       profileForm.experience,
          occupation:       profileForm.occupation,
          emergencyContact: profileForm.emergencyContact,
        });
        // Sync user display name
        user.value.name  = `${profileForm.firstName} ${profileForm.lastName}`;
        user.value.email = profileForm.email;
        if (updated.emailVerified !== undefined) user.value.emailVerified = updated.emailVerified;
        profileSnapshot = { ...profileForm };
        showToast('Profile updated successfully.');
      } catch (err) {
        showToast(err.message || 'Could not save profile.', 'error');
      } finally {
        savingStates.profile = false;
      }
    };

    const uploadAvatar = async (e) => {
      const file = e.target.files?.[0];
      if (!file) return;
      if (file.size > 5 * 1024 * 1024) {
        showToast('Image must be under 5 MB.', 'error');
        return;
      }
      savingStates.avatar = true;
      try {
        const data = await apiUpload('/me/avatar', file);
        user.value.avatar = data.avatarUrl;
        showToast('Photo updated.');
      } catch (err) {
        showToast(err.message || 'Upload failed.', 'error');
      } finally {
        savingStates.avatar = false;
      }
    };

    const removeAvatar = async () => {
      savingStates.avatar = true;
      try {
        await apiFetch('DELETE', '/me/avatar');
        user.value.avatar = null;
        showToast('Photo removed.');
      } catch (err) {
        showToast(err.message || 'Could not remove photo.', 'error');
      } finally {
        savingStates.avatar = false;
      }
    };

    const requestEmailVerification = async () => {
      try {
        await apiFetch('POST', '/me/email-verification');
        showToast('Verification email sent. Check your inbox.');
      } catch (err) {
        showToast(err.message || 'Could not send verification.', 'error');
      }
    };

    // ── Security: Password ─────────────────────────────────────────────
    const passwordForm  = reactive({ current: '', newPass: '', confirm: '' });
    const passwordError = ref('');

    const updatePassword = async () => {
      passwordError.value = '';
      if (!passwordForm.current) {
        passwordError.value = 'Please enter your current password.'; return;
      }
      if (passwordForm.newPass.length < 10) {
        passwordError.value = 'New password must be at least 10 characters.'; return;
      }
      if (passwordForm.newPass !== passwordForm.confirm) {
        passwordError.value = 'Passwords do not match.'; return;
      }
      savingStates.password = true;
      try {
        await apiFetch('PUT', '/me/password', {
          currentPassword: passwordForm.current,
          newPassword:     passwordForm.newPass,
        });
        passwordForm.current = '';
        passwordForm.newPass = '';
        passwordForm.confirm = '';
        showToast('Password updated successfully.');
      } catch (err) {
        passwordError.value = err.message || 'Could not update password.';
      } finally {
        savingStates.password = false;
      }
    };

   
    const tfaOptions = reactive([]);

    const fetchTFA = async () => {
      try {
        const data = await apiFetch('GET', '/me/2fa');
        tfaOptions.splice(0, tfaOptions.length, ...data.map(t => ({ ...t, saving: false })));
      } catch {
        // Fallback defaults
        tfaOptions.splice(0, tfaOptions.length,
          { id: 'app', label: 'Authenticator app', desc: 'Use Google Authenticator or Authy', enabled: false, saving: false },
          { id: 'sms', label: 'SMS backup code',   desc: 'Receive a login code via text message', enabled: false, saving: false },
        );
      }
    };

    const toggleTFA = async (tfa) => {
      tfa.saving = true;
      const newVal = !tfa.enabled;
      try {
        await apiFetch('PUT', `/me/2fa/${tfa.id}`, { enabled: newVal });
        tfa.enabled = newVal;
        showToast(`${tfa.label} ${newVal ? 'enabled' : 'disabled'}.`);
      } catch (err) {
        showToast(err.message || 'Could not update 2FA.', 'error');
      } finally {
        tfa.saving = false;
      }
    };

    const sessions = reactive([]);

    const fetchSessions = async () => {
      loadingStates.sessions = true;
      try {
        const data = await apiFetch('GET', '/me/sessions');
        sessions.splice(0, sessions.length,
          ...data.map(s => ({ ...s, icon: resolveDeviceIcon(s.device), revoking: false }))
        );
      } catch {
        // Leave empty — non-critical
      } finally {
        loadingStates.sessions = false;
      }
    };

    const resolveDeviceIcon = (device = '') => {
      if (/mobile|iphone|android/i.test(device)) return 'fas fa-mobile-alt';
      if (/tablet|ipad/i.test(device))            return 'fas fa-tablet-alt';
      return 'fas fa-desktop';
    };

    const revokeSession = async (id) => {
      const s = sessions.find(x => x.id === id);
      if (!s) return;
      s.revoking = true;
      try {
        await apiFetch('DELETE', `/me/sessions/${id}`);
        const i = sessions.findIndex(x => x.id === id);
        if (i > -1) sessions.splice(i, 1);
        showToast('Session revoked.');
      } catch (err) {
        showToast(err.message || 'Could not revoke session.', 'error');
        s.revoking = false;
      }
    };

    const revokeAllSessions = async () => {
      savingStates.revokeAll = true;
      try {
        await apiFetch('DELETE', '/me/sessions');
        const current = sessions.find(s => s.current);
        sessions.splice(0, sessions.length, ...(current ? [current] : []));
        showToast('All other sessions revoked.');
      } catch (err) {
        showToast(err.message || 'Could not revoke sessions.', 'error');
      } finally {
        savingStates.revokeAll = false;
      }
    };

    // ── Notifications ──────────────────────────────────────────────────
    const notifGroups = reactive([]);

    const fetchNotifications = async () => {
      loadingStates.notifications = true;
      try {
        const data = await apiFetch('GET', '/me/notifications');
        notifGroups.splice(0, notifGroups.length,
          ...data.map(g => ({
            ...g,
            items: g.items.map(i => ({ ...i, saving: false })),
          }))
        );
      } catch {
        // Fallback defaults
        notifGroups.splice(0, notifGroups.length,
          {
            id: 'email', label: 'Email notifications', icon: 'fas fa-envelope',
            items: [
              { id: 'e1', label: 'New messages',      desc: 'When a client or agent sends you a message',        enabled: true,  saving: false },
              { id: 'e2', label: 'Listing updates',   desc: 'Price changes, availability and status updates',   enabled: true,  saving: false },
              { id: 'e3', label: 'Promotions & tips', desc: 'Platform guides, offers and feature announcements', enabled: false, saving: false },
            ],
          },
          {
            id: 'push', label: 'Push & SMS notifications', icon: 'fas fa-sms',
            items: [
              { id: 'p1', label: 'Enquiry alerts',        desc: 'Instant push when someone enquires on a property',   enabled: true,  saving: false },
              { id: 'p2', label: 'Viewing reminders',     desc: 'SMS reminder 1 hour before a scheduled viewing',     enabled: true,  saving: false },
              { id: 'p3', label: 'Payment confirmations', desc: 'SMS on every successful payment or receipt',         enabled: false, saving: false },
            ],
          }
        );
      } finally {
        loadingStates.notifications = false;
      }
    };

    // Optimistic per-item toggle with server sync
    const toggleNotification = async (item) => {
      item.saving = true;
      const newVal = !item.enabled;
      item.enabled = newVal; // Optimistic
      try {
        await apiFetch('PUT', `/me/notifications/${item.id}`, { enabled: newVal });
      } catch (err) {
        item.enabled = !newVal; // Rollback
        showToast(err.message || 'Could not update notification.', 'error');
      } finally {
        item.saving = false;
      }
    };

    const saveNotifications = async () => {
      savingStates.notifications = true;
      try {
        const payload = notifGroups.flatMap(g => g.items.map(i => ({ id: i.id, enabled: i.enabled })));
        await apiFetch('PUT', '/me/notifications', { preferences: payload });
        showToast('Notification preferences saved.');
      } catch (err) {
        showToast(err.message || 'Could not save preferences.', 'error');
      } finally {
        savingStates.notifications = false;
      }
    };

    const resetNotifications = async () => {
      savingStates.notifications = true;
      try {
        const data = await apiFetch('POST', '/me/notifications/reset');
        notifGroups.forEach(g =>
          g.items.forEach(i => {
            const reset = data.find(d => d.id === i.id);
            if (reset) i.enabled = reset.enabled;
          })
        );
        showToast('Notification preferences reset to defaults.');
      } catch {
        notifGroups.forEach(g => g.items.forEach(i => { i.enabled = true; }));
        showToast('Reset to defaults.');
      } finally {
        savingStates.notifications = false;
      }
    };

    // ── Privacy ────────────────────────────────────────────────────────
    const privacyOptions = reactive([]);

    const fetchPrivacy = async () => {
      loadingStates.privacy = true;
      try {
        const data = await apiFetch('GET', '/me/privacy');
        privacyOptions.splice(0, privacyOptions.length,
          ...data.map(p => ({ ...p, saving: false }))
        );
      } catch {
        privacyOptions.splice(0, privacyOptions.length,
          { id: 'pub',   label: 'Public profile',   desc: 'Allow anyone to view your profile and listings',      enabled: true,  saving: false },
          { id: 'phone', label: 'Show phone number', desc: 'Display your number on public listing pages',         enabled: false, saving: false },
          { id: 'anon',  label: 'Analytics sharing', desc: 'Share anonymised usage data to improve HunterStreet', enabled: true,  saving: false },
        );
      } finally {
        loadingStates.privacy = false;
      }
    };

    const togglePrivacy = async (item) => {
      item.saving = true;
      const newVal = !item.enabled;
      item.enabled = newVal;
      try {
        await apiFetch('PUT', `/me/privacy/${item.id}`, { enabled: newVal });
      } catch (err) {
        item.enabled = !newVal;
        showToast(err.message || 'Could not update privacy setting.', 'error');
      } finally {
        item.saving = false;
      }
    };

    const exportData = async () => {
      savingStates.export = true;
      try {
        const token = getAuthToken();
        const res = await fetch(`${API_BASE}/me/export`, {
          headers: token ? { Authorization: `Bearer ${token}` } : {},
        });
        if (!res.ok) throw new Error('Export failed');
        const blob = await res.blob();
        const url  = URL.createObjectURL(blob);
        const a    = document.createElement('a');
        a.href = url;
        a.download = `hunterstreet-export-${Date.now()}.csv`;
        a.click();
        URL.revokeObjectURL(url);
        showToast('Your data export has started downloading.');
      } catch (err) {
        showToast(err.message || 'Export failed.', 'error');
      } finally {
        savingStates.export = false;
      }
    };

    const confirmDeleteAccount = async () => {
      if (!confirm('Are you sure you want to permanently delete your account? This cannot be undone.')) return;
      try {
        await apiFetch('DELETE', '/me');
        localStorage.removeItem('auth_token');
        showToast('Account deletion requested. You will be signed out shortly.', 'error');
        setTimeout(() => { window.location.href = '/goodbye'; }, 2500);
      } catch (err) {
        showToast(err.message || 'Could not delete account.', 'error');
      }
    };

    // ── Agent: Agency ──────────────────────────────────────────────────
    const agencyForm = reactive({
      name: '', regNo: '', website: '', areas: '',
      description: '', specialisations: [], languages: '', hours: '',
    });

    const fetchAgency = async () => {
      loadingStates.agency = true;
      try {
        const data = await apiFetch('GET', '/agent/agency');
        Object.assign(agencyForm, {
          name:            data.name            || '',
          regNo:           data.regNo           || '',
          website:         data.website         || '',
          areas:           data.areas           || '',
          description:     data.description     || '',
          specialisations: [...(data.specialisations || [])],
          languages:       data.languages       || '',
          hours:           data.hours           || '',
        });
      } catch (err) {
        showToast(err.message || 'Could not load agency profile.', 'error');
      } finally {
        loadingStates.agency = false;
      }
    };

    const saveAgency = async () => {
      savingStates.agency = true;
      try {
        await apiFetch('PUT', '/agent/agency', { ...agencyForm });
        showToast('Agency profile saved.');
      } catch (err) {
        showToast(err.message || 'Could not save agency profile.', 'error');
      } finally {
        savingStates.agency = false;
      }
    };

    const addSpecialisation = () => {
      const val = prompt('Enter specialisation:');
      if (val?.trim()) agencyForm.specialisations.push(val.trim());
    };

    // ── Agent: Listings ────────────────────────────────────────────────
    const listingStats = reactive([
      { value: '—', label: 'Active listings'  },
      { value: '—', label: 'Pending review'   },
      { value: '—', label: 'Total enquiries'  },
    ]);
    const listingForm    = reactive({ currency: 'KES', priceDisplay: 'Per month' });
    const listingToggles = reactive([]);

    const fetchListingSettings = async () => {
      loadingStates.listings = true;
      try {
        const data = await apiFetch('GET', '/agent/listings/settings');
        listingStats[0].value = data.stats?.active  ?? '0';
        listingStats[1].value = data.stats?.pending ?? '0';
        listingStats[2].value = data.stats?.enquiries ?? '0';
        listingForm.currency     = data.currency     || 'KES';
        listingForm.priceDisplay = data.priceDisplay || 'Per month';
        listingToggles.splice(0, listingToggles.length,
          ...(data.toggles || [
            { id: 'pub',     label: 'Auto-publish listings', desc: 'Publish immediately when you submit a listing',         enabled: true  },
            { id: 'contact', label: 'Allow direct contact',  desc: 'Show your phone number on listing pages',               enabled: true  },
            { id: 'vt',      label: 'Virtual tour prompt',   desc: 'Prompt to add a 360° tour when creating a listing',     enabled: false },
          ]).map(t => ({ ...t, saving: false }))
        );
      } catch (err) {
        showToast(err.message || 'Could not load listing settings.', 'error');
      } finally {
        loadingStates.listings = false;
      }
    };

    const saveListingSettings = async () => {
      savingStates.listings = true;
      try {
        await apiFetch('PUT', '/agent/listings/settings', {
          currency:     listingForm.currency,
          priceDisplay: listingForm.priceDisplay,
          toggles:      listingToggles.map(t => ({ id: t.id, enabled: t.enabled })),
        });
        showToast('Listing settings saved.');
      } catch (err) {
        showToast(err.message || 'Could not save listing settings.', 'error');
      } finally {
        savingStates.listings = false;
      }
    };

    // ── Agent: Commission ──────────────────────────────────────────────
    const commissionForm = reactive({
      residential: 3, commercial: 4, rental: 8, offplan: 5,
      bankName: '', accountNumber: '', frequency: 'Monthly', mpesa: '',
    });

    const fetchCommission = async () => {
      loadingStates.commission = true;
      try {
        const data = await apiFetch('GET', '/agent/commission');
        Object.assign(commissionForm, {
          residential:   data.residential   ?? '',
          commercial:    data.commercial    ?? '',
          rental:        data.rental        ?? '',
          offplan:       data.offplan       ?? '',
          bankName:      data.bankName      || '',
          accountNumber: data.accountNumber || '',
          frequency:     data.frequency     || 'Monthly',
          mpesa:         data.mpesa         || '',
        });
      } catch (err) {
        showToast(err.message || 'Could not load commission settings.', 'error');
      } finally {
        loadingStates.commission = false;
      }
    };

    const saveCommission = async () => {
      savingStates.commission = true;
      try {
        await apiFetch('PUT', '/agent/commission', { ...commissionForm });
        showToast('Payment settings saved.');
      } catch (err) {
        showToast(err.message || 'Could not save payment settings.', 'error');
      } finally {
        savingStates.commission = false;
      }
    };

    // ── Tenant: Preferences ────────────────────────────────────────────
    const tenantPrefForm = reactive({
      location: '', propertyType: 'Apartment',
      minBudget: 0, maxBudget: 0,
      bedrooms: 'Any', moveIn: '', amenities: [],
    });

    const fetchTenantPreferences = async () => {
      loadingStates.preferences = true;
      try {
        const data = await apiFetch('GET', '/tenant/preferences');
        Object.assign(tenantPrefForm, {
          location:     data.location     || '',
          propertyType: data.propertyType || 'Apartment',
          minBudget:    data.minBudget    || 0,
          maxBudget:    data.maxBudget    || 0,
          bedrooms:     data.bedrooms     || 'Any',
          moveIn:       data.moveIn       || '',
          amenities:    [...(data.amenities || [])],
        });
      } catch (err) {
        showToast(err.message || 'Could not load rental preferences.', 'error');
      } finally {
        loadingStates.preferences = false;
      }
    };

    const saveTenantPreferences = async () => {
      savingStates.preferences = true;
      try {
        await apiFetch('PUT', '/tenant/preferences', { ...tenantPrefForm });
        showToast('Rental preferences saved.');
      } catch (err) {
        showToast(err.message || 'Could not save preferences.', 'error');
      } finally {
        savingStates.preferences = false;
      }
    };

    const addAmenity = () => {
      const val = prompt('Enter amenity:');
      if (val?.trim()) tenantPrefForm.amenities.push(val.trim());
    };

    // ── Tenant: Lease ──────────────────────────────────────────────────
    const leaseStats     = reactive([
      { value: '—', label: 'Lease end'    },
      { value: '—', label: 'Monthly rent' },
      { value: '—', label: 'Lease status' },
    ]);
    const leaseDocuments = reactive([]);
    const dragOver       = ref(false);

    const fetchLease = async () => {
      loadingStates.lease = true;
      try {
        const data = await apiFetch('GET', '/tenant/lease');
        leaseStats[0].value = data.endDate    || '—';
        leaseStats[1].value = data.monthlyRent ? `KES ${Number(data.monthlyRent).toLocaleString()}` : '—';
        leaseStats[2].value = data.status     || '—';
        leaseDocuments.splice(0, leaseDocuments.length,
          ...(data.documents || []).map(d => ({
            ...d,
            icon: d.type === 'pdf' ? 'fas fa-file-pdf' : 'fas fa-clipboard-check',
          }))
        );
      } catch (err) {
        showToast(err.message || 'Could not load lease information.', 'error');
      } finally {
        loadingStates.lease = false;
      }
    };

    const downloadDocument = async (doc) => {
      try {
        const token = getAuthToken();
        const res = await fetch(`${API_BASE}/tenant/documents/${doc.id}/download`, {
          headers: token ? { Authorization: `Bearer ${token}` } : {},
        });
        if (!res.ok) throw new Error('Download failed');
        const blob = await res.blob();
        const url  = URL.createObjectURL(blob);
        const a    = document.createElement('a');
        a.href     = url;
        a.download = doc.name;
        a.click();
        URL.revokeObjectURL(url);
      } catch (err) {
        showToast(err.message || 'Download failed.', 'error');
      }
    };

    const handleDrop = (e) => {
      dragOver.value = false;
      const file = e.dataTransfer?.files?.[0];
      if (file) processUpload(file);
    };

    const uploadDocument = (e) => {
      const file = e.target.files?.[0];
      if (file) processUpload(file);
    };

    const processUpload = async (file) => {
      const allowed = ['application/pdf', 'image/jpeg', 'image/png'];
      if (!allowed.includes(file.type)) {
        showToast('Only PDF, JPG and PNG files are accepted.', 'error'); return;
      }
      if (file.size > 10 * 1024 * 1024) {
        showToast('File must be under 10 MB.', 'error'); return;
      }
      savingStates.upload = true;
      try {
        const data = await apiUpload('/tenant/documents', file);
        leaseDocuments.push({
          id:   data.id,
          name: data.name,
          meta: data.meta,
          icon: data.type === 'pdf' ? 'fas fa-file-pdf' : 'fas fa-file-image',
        });
        showToast('Document uploaded successfully.');
      } catch (err) {
        showToast(err.message || 'Upload failed.', 'error');
      } finally {
        savingStates.upload = false;
      }
    };

    // ── Tenant: Rent ───────────────────────────────────────────────────
    const rentStats = reactive([
      { value: '—', label: 'Due Jun 1'        },
      { value: '—', label: 'May status'       },
      { value: '—', label: 'On-time payments' },
    ]);
    const rentForm         = reactive({ method: '', autoPayDate: '1st of month', autoPay: false });
    const paymentMethods   = reactive([]);
    const maintenanceRequests = reactive([]);

    const fetchRent = async () => {
      loadingStates.rent = true;
      loadingStates.maintenance = true;
      try {
        const [rentData, maintData] = await Promise.all([
          apiFetch('GET', '/tenant/payments'),
          apiFetch('GET', '/tenant/maintenance'),
        ]);

        rentStats[0].value = rentData.nextDueFormatted  || '—';
        rentStats[1].value = rentData.lastMonthStatus   || '—';
        rentStats[2].value = rentData.onTimeCount       ?? '—';

        paymentMethods.splice(0, paymentMethods.length,
          ...(rentData.paymentMethods || [
            { id: 'mpesa',  label: 'M-Pesa · 0712 345 678' },
            { id: 'bank',   label: 'Bank transfer'          },
            { id: 'card',   label: 'Debit / credit card'    },
          ])
        );

        rentForm.method      = rentData.selectedMethod || (paymentMethods[0]?.id ?? '');
        rentForm.autoPayDate = rentData.autoPayDate    || '1st of month';
        rentForm.autoPay     = rentData.autoPay        ?? false;

        maintenanceRequests.splice(0, maintenanceRequests.length,
          ...maintData.map(r => ({
            ...r,
            icon:        resolveMaintenanceIcon(r.category),
            statusColor: resolveStatusColor(r.status),
          }))
        );
      } catch (err) {
        showToast(err.message || 'Could not load rent information.', 'error');
      } finally {
        loadingStates.rent        = false;
        loadingStates.maintenance = false;
      }
    };

    const resolveMaintenanceIcon = (cat = '') => {
      const map = {
        plumbing:    'fas fa-tint',
        electrical:  'fas fa-plug',
        structural:  'fas fa-hard-hat',
        appliance:   'fas fa-blender',
        pest:        'fas fa-bug',
      };
      return map[cat] || 'fas fa-tools';
    };

    const resolveStatusColor = (status = '') => {
      const map = {
        'In progress': 'amber',
        'Resolved':    'green',
        'Open':        'blue',
        'Rejected':    'red',
      };
      return map[status] || 'blue';
    };

    const saveRentSettings = async () => {
      savingStates.rent = true;
      try {
        await apiFetch('PUT', '/tenant/payments', {
          method:      rentForm.method,
          autoPayDate: rentForm.autoPayDate,
          autoPay:     rentForm.autoPay,
        });
        showToast('Payment settings saved.');
      } catch (err) {
        showToast(err.message || 'Could not save payment settings.', 'error');
      } finally {
        savingStates.rent = false;
      }
    };

    const openNewMaintenanceRequest = () => {
      // Emit to parent router or open modal — adjust to your routing
      showToast('Opening maintenance request form…', 'info');
    };

    // ── Security panel bootstrap ───────────────────────────────────────
    const fetchSecurityData = async () => {
      loadingStates.security = true;
      await Promise.all([fetchTFA(), fetchSessions()]);
      loadingStates.security = false;
    };

    // ── Lazy panel data fetcher ────────────────────────────────────────
    const fetchedPanels = new Set();

    const fetchPanelData = async (panelId) => {
      if (fetchedPanels.has(panelId)) return;
      fetchedPanels.add(panelId);

      const fetchMap = {
        profile:      fetchProfile,
        security:     fetchSecurityData,
        notifications:fetchNotifications,
        privacy:      fetchPrivacy,
        agency:       fetchAgency,
        listings:     fetchListingSettings,
        commission:   fetchCommission,
        preferences:  fetchTenantPreferences,
        lease:        fetchLease,
        rent:         fetchRent,
      };

      await fetchMap[panelId]?.();
    };

    // ── Bootstrap ──────────────────────────────────────────────────────
    onMounted(async () => {
      try {
        await fetchProfile();
        fetchedPanels.add('profile');
      } finally {
        appLoading.value = false;
      }
    });

    // Re-fetch panel when role changes (different data per role)
    watch(activeRole, () => {
      fetchedPanels.clear();
      fetchedPanels.add('profile'); // Already loaded above
    });

    return {
      appLoading,
      loadingStates, savingStates,
      toast,
      user, getInitials, onAvatarError,
      activeRole, activePanel, availableRoles, roleSwitching,
      roleConfig, switchRole, navigateTo, accountNav,
      profileForm, resetProfileForm, saveProfile, uploadAvatar, removeAvatar, requestEmailVerification,
      passwordForm, passwordError, updatePassword,
      tfaOptions, toggleTFA,
      sessions, revokeSession, revokeAllSessions,
      notifGroups, toggleNotification, saveNotifications, resetNotifications,
      privacyOptions, togglePrivacy, exportData, confirmDeleteAccount,
      agencyForm, addSpecialisation, saveAgency, fetchAgency,
      listingStats, listingForm, listingToggles, saveListingSettings,
      commissionForm, saveCommission, fetchCommission,
      tenantPrefForm, addAmenity, saveTenantPreferences, fetchTenantPreferences,
      leaseStats, leaseDocuments, downloadDocument,
      dragOver, handleDrop, uploadDocument,
      rentStats, rentForm, paymentMethods, maintenanceRequests,
      saveRentSettings, openNewMaintenanceRequest,
    };
  },
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,600;1,400&family=DM+Sans:wght@300;400;500;600&display=swap');

/* ─── Page shell ──────────────────────────────────────────────────── */
.hs-settings-page {
  font-family: 'DM Sans', sans-serif;
  background: #f6f4f1;
  min-height: 100vh;
  padding-bottom: 60px;
}

/* ─── Page header ─────────────────────────────────────────────────── */
.hs-page-header {
  background: #fff;
  border-bottom: 1px solid rgba(0,0,0,0.06);
  padding: 28px 0 24px;
  margin-bottom: 32px;
}
.hs-page-header-inner {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 32px;
}
.hs-breadcrumb {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 12px;
}
.hs-breadcrumb-link {
  color: #b73f2a;
  text-decoration: none;
  font-size: 13px;
  display: flex;
  align-items: center;
  gap: 5px;
  transition: opacity 0.15s;
}
.hs-breadcrumb-link:hover { opacity: 0.75; }
.hs-breadcrumb-sep { color: #ccc; font-size: 11px; }
.hs-breadcrumb-current { font-size: 13px; color: #999; }
.hs-page-title {
  font-family: 'Cormorant Garamond', serif;
  font-size: 32px;
  font-weight: 600;
  color: #1c1c1c;
  letter-spacing: -0.4px;
  margin-bottom: 6px;
}
.hs-page-sub { font-size: 14px; color: #999; }

/* ─── Layout ──────────────────────────────────────────────────────── */
.hs-settings-wrap {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 32px;
  display: grid;
  grid-template-columns: 248px 1fr;
  gap: 28px;
  align-items: start;
}

/* ─── SKELETON ────────────────────────────────────────────────────── */
@keyframes hs-shimmer {
  0%   { background-position: -600px 0; }
  100% { background-position: 600px 0; }
}

.hs-sk {
  background: linear-gradient(90deg, #ebe9e5 25%, #f5f3f0 50%, #ebe9e5 75%);
  background-size: 600px 100%;
  animation: hs-shimmer 1.4s infinite linear;
  border-radius: 6px;
}
.hs-sk--line  { height: 14px; margin-bottom: 12px; }
.hs-sk--block { height: 48px; width: 100%; }
.hs-sk--circle{ border-radius: 50%; }

.hs-skeleton-sidebar { padding: 16px; }
.hs-skeleton-card { padding: 22px 24px; }

/* ─── Spinners ────────────────────────────────────────────────────── */
@keyframes hs-spin { to { transform: rotate(360deg); } }

.hs-spinner-xs,
.hs-spinner-sm,
.hs-spinner-lg {
  display: inline-block;
  border-radius: 50%;
  border-style: solid;
  border-color: transparent;
  animation: hs-spin 0.7s linear infinite;
  flex-shrink: 0;
}
.hs-spinner-xs { width:7px;  height:7px;  border-width:1.5px; border-top-color:#b73f2a; }
.hs-spinner-sm { width:13px; height:13px; border-width:2px;   border-top-color:currentColor; }
.hs-spinner-lg { width:30px; height:30px; border-width:3px;   border-top-color:#b73f2a; margin:0 auto 10px; }

/* ─── SIDEBAR ─────────────────────────────────────────────────────── */
.hs-sidebar {
  background: #fff;
  border-radius: 16px;
  border: 1px solid rgba(0,0,0,0.06);
  overflow: hidden;
  position: sticky;
  top: 96px;
  box-shadow: 0 2px 14px rgba(0,0,0,0.04);
}
.hs-sb-section { padding: 16px 14px 4px; }
.hs-sb-top { padding-bottom: 12px; border-bottom: 1px solid rgba(0,0,0,0.05); }
.hs-sb-label {
  font-size: 9.5px;
  letter-spacing: 2.5px;
  font-weight: 600;
  color: #bbb;
  text-transform: uppercase;
  display: block;
  margin-bottom: 10px;
  padding: 0 4px;
}

/* Role switcher */
.hs-role-switch {
  display: flex;
  border: 1.5px solid rgba(0,0,0,0.08);
  border-radius: 10px;
  overflow: hidden;
  background: #f9f8f6;
  margin-bottom: 10px;
  transition: opacity 0.2s;
}
.hs-role-switch--loading { opacity: 0.6; pointer-events: none; }

.hs-role-btn {
  flex: 1;
  padding: 9px 0;
  font-size: 12.5px;
  font-weight: 500;
  background: transparent;
  border: none;
  cursor: pointer;
  color: #999;
  font-family: 'DM Sans', sans-serif;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  transition: background 0.18s, color 0.18s;
}
.hs-role-btn:disabled { cursor: not-allowed; opacity: 0.45; }
.hs-role-btn i { font-size: 11px; }
.hs-role-btn.active { background: #b73f2a; color: #fff; }

.hs-role-status {
  display: flex;
  align-items: center;
  gap: 7px;
  font-size: 12px;
  color: #888;
  padding: 0 4px;
  min-height: 20px;
}
.hs-status-dot {
  width: 7px; height: 7px;
  border-radius: 50%;
  flex-shrink: 0;
}
.hs-status-dot.green { background: #22c55e; }
.hs-status-dot.blue  { background: #3b82f6; }

/* Nav items */
.hs-sb-nav { display: flex; flex-direction: column; gap: 2px; }
.hs-nav-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 12px;
  border-radius: 10px;
  cursor: pointer;
  font-size: 13.5px;
  color: #555;
  transition: background 0.12s, color 0.12s;
  border: none;
  background: transparent;
  width: 100%;
  text-align: left;
  font-family: 'DM Sans', sans-serif;
  font-weight: 400;
}
.hs-ni-icon {
  width: 32px; height: 32px;
  background: #f0ede9;
  border-radius: 8px;
  display: flex; align-items: center; justify-content: center;
  font-size: 13px; color: #888;
  flex-shrink: 0;
  transition: background 0.12s, color 0.12s;
}
.hs-nav-item:hover { background: #f9f8f6; color: #1c1c1c; }
.hs-nav-item:hover .hs-ni-icon { background: rgba(183,63,42,.1); color: #b73f2a; }
.hs-nav-item.active { background: rgba(183,63,42,.07); color: #b73f2a; font-weight: 500; }
.hs-nav-item.active .hs-ni-icon { background: rgba(183,63,42,.12); color: #b73f2a; }
.hs-ni-badge {
  margin-left: auto;
  font-size: 10px;
  background: #b73f2a;
  color: #fff;
  border-radius: 8px;
  padding: 2px 7px;
  font-weight: 700;
}

/* Sidebar footer */
.hs-sb-footer { padding: 14px 16px; border-top: 1px solid rgba(0,0,0,0.06); }
.hs-sb-user { display: flex; align-items: center; gap: 10px; }
.hs-sb-avatar {
  width: 38px; height: 38px;
  border-radius: 50%;
  background: linear-gradient(135deg, #b73f2a, #d4614a);
  color: #fff;
  display: flex; align-items: center; justify-content: center;
  font-size: 13px; font-weight: 700;
  flex-shrink: 0; overflow: hidden;
  box-shadow: 0 2px 8px rgba(183,63,42,.28);
}
.hs-sb-avatar img { width:100%; height:100%; object-fit:cover; }
.hs-sb-user-name  { font-size: 13.5px; font-weight: 600; color: #111; }
.hs-sb-user-email { font-size: 11.5px; color: #aaa; margin-top: 1px; }

/* ─── MAIN ────────────────────────────────────────────────────────── */
.hs-main { min-width: 0; }
.hs-panel-header { margin-bottom: 22px; }
.hs-panel-header h2 {
  font-family: 'Cormorant Garamond', serif;
  font-size: 26px; font-weight: 600;
  color: #1c1c1c; letter-spacing: -0.3px;
  margin-bottom: 4px;
}
.hs-panel-header p { font-size: 13.5px; color: #999; }

/* ─── Cards ───────────────────────────────────────────────────────── */
.hs-card {
  background: #fff;
  border: 1px solid rgba(0,0,0,0.06);
  border-radius: 14px;
  padding: 22px 24px;
  margin-bottom: 14px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.03);
}
.hs-card--danger { border-color: rgba(229,62,62,.2); }
.hs-card-title {
  font-size: 13.5px; font-weight: 600; color: #1c1c1c;
  margin-bottom: 18px;
  display: flex; align-items: center; gap: 9px;
}
.hs-card-title i { color: #b73f2a; font-size: 14px; }

/* ─── Photo row ───────────────────────────────────────────────────── */
.hs-photo-row {
  display: flex;
  align-items: center;
  gap: 20px;
  flex-wrap: wrap;
  margin-bottom: 22px;
}
.hs-photo-avatar {
  width: 72px; height: 72px;
  border-radius: 50%;
  background: linear-gradient(135deg, #b73f2a, #d4614a);
  color: #fff;
  display: flex; align-items: center; justify-content: center;
  font-size: 24px; font-weight: 700;
  flex-shrink: 0; overflow: hidden;
  box-shadow: 0 4px 18px rgba(183,63,42,.28);
  position: relative;
}
.hs-photo-avatar img { width:100%; height:100%; object-fit:cover; }
.hs-avatar-overlay {
  position: absolute; inset: 0;
  background: rgba(0,0,0,0.45);
  display: flex; align-items: center; justify-content: center;
  opacity: 0; cursor: pointer;
  transition: opacity 0.18s;
  font-size: 18px; color: #fff;
  border-radius: 50%;
}
.hs-photo-avatar:hover .hs-avatar-overlay { opacity: 1; }
.hs-photo-name { font-size: 16px; font-weight: 600; color: #1c1c1c; margin-bottom: 3px; }
.hs-photo-role { font-size: 12px; color: #b73f2a; font-weight: 500; margin-bottom: 10px; }
.hs-photo-actions { display: flex; gap: 8px; }
.hs-verify-pills { display: flex; flex-direction: column; gap: 7px; margin-left: auto; }
.hs-verify-pill {
  display: flex; align-items: center; gap: 6px;
  font-size: 12px; font-weight: 500;
  padding: 5px 12px; border-radius: 20px;
}
.hs-verify-pill.green { background: #dcfce7; color: #15803d; }
.hs-verify-pill.blue  { background: #dbeafe; color: #1d4ed8; }
.hs-verify-pill.grey  { background: #f3f4f6; color: #6b7280; }

/* ─── Fields ──────────────────────────────────────────────────────── */
.hs-field-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 14px;
  margin-bottom: 14px;
}
.hs-field-row--full { grid-template-columns: 1fr; }
.hs-field { display: flex; flex-direction: column; gap: 6px; }
.hs-field label {
  font-size: 11px; font-weight: 600; color: #999;
  letter-spacing: 0.06em; text-transform: uppercase;
}
.hs-field input,
.hs-field select,
.hs-field textarea {
  font-size: 13.5px;
  padding: 10px 13px;
  border: 1.5px solid rgba(0,0,0,0.08);
  border-radius: 8px;
  background: #f9f8f6;
  color: #1c1c1c;
  font-family: 'DM Sans', sans-serif;
  width: 100%;
  outline: none;
  transition: border-color 0.18s, background 0.18s;
}
.hs-field input:focus,
.hs-field select:focus,
.hs-field textarea:focus {
  border-color: #b73f2a;
  background: #fff;
  box-shadow: 0 0 0 3px rgba(183,63,42,.08);
}
.hs-field input:disabled,
.hs-field select:disabled,
.hs-field textarea:disabled {
  opacity: 0.55; cursor: not-allowed;
}
.hs-field textarea { resize: vertical; min-height: 90px; }

.hs-field-with-action { position: relative; }
.hs-field-with-action input { padding-right: 64px; }
.hs-field-action {
  position: absolute; right: 8px; top: 50%; transform: translateY(-50%);
  font-size: 11px; font-weight: 600; color: #b73f2a;
  background: rgba(183,63,42,.08); border: none; border-radius: 5px;
  padding: 3px 9px; cursor: pointer;
  font-family: 'DM Sans', sans-serif;
  transition: background 0.15s;
}
.hs-field-action:hover { background: rgba(183,63,42,.15); }

.hs-field-error {
  font-size: 12.5px; color: #e53e3e;
  margin-top: -6px; margin-bottom: 8px;
}

/* ─── Toggles ─────────────────────────────────────────────────────── */
.hs-toggle-row {
  display: flex; align-items: center;
  justify-content: space-between;
  padding: 13px 0;
  border-bottom: 1px solid rgba(0,0,0,0.05);
  gap: 16px;
}
.hs-toggle-row:last-child { border-bottom: none; padding-bottom: 0; }
.hs-tgl-label { font-size: 13.5px; color: #1c1c1c; margin-bottom: 2px; }
.hs-tgl-desc  { font-size: 12px; color: #aaa; }

.hs-toggle {
  width: 40px; height: 22px;
  border-radius: 11px;
  background: #e0ddd9;
  border: none; cursor: pointer;
  position: relative;
  transition: background 0.22s;
  flex-shrink: 0;
}
.hs-toggle.on { background: #b73f2a; }
.hs-toggle--loading { opacity: 0.6; cursor: wait; }
.hs-toggle::after {
  content: '';
  position: absolute;
  width: 16px; height: 16px;
  border-radius: 50%;
  background: #fff;
  top: 3px; left: 3px;
  transition: transform 0.22s;
  box-shadow: 0 1px 4px rgba(0,0,0,0.2);
}
.hs-toggle.on::after { transform: translateX(18px); }

/* ─── Buttons ─────────────────────────────────────────────────────── */
.hs-btn-row {
  display: flex; gap: 9px;
  justify-content: flex-end;
  margin-top: 20px;
}
.hs-btn {
  padding: 10px 20px;
  border-radius: 8px;
  font-size: 13px; font-weight: 500;
  cursor: pointer;
  border: 1.5px solid rgba(0,0,0,0.1);
  background: #fff; color: #333;
  transition: all 0.15s;
  font-family: 'DM Sans', sans-serif;
  display: inline-flex; align-items: center; gap: 7px;
}
.hs-btn:hover { background: #f9f8f6; border-color: rgba(0,0,0,0.18); }
.hs-btn:disabled { opacity: 0.55; cursor: not-allowed; }
.hs-btn--primary {
  background: #b73f2a; color: #fff; border-color: transparent;
  box-shadow: 0 2px 14px rgba(183,63,42,.24);
}
.hs-btn--primary:hover:not(:disabled) { background: #9a3523; box-shadow: 0 2px 18px rgba(183,63,42,.32); }
.hs-btn--danger-ghost { color: #e53e3e; border-color: rgba(229,62,62,.25); background: transparent; }
.hs-btn--danger-ghost:hover:not(:disabled) { background: #fff5f5; border-color: #e53e3e; }
.hs-btn--sm { padding: 6px 14px; font-size: 12px; }
.hs-btn--loading { opacity: 0.8; cursor: wait; }

/* ─── Stats grid ──────────────────────────────────────────────────── */
.hs-stat-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px; margin-bottom: 14px;
}
.hs-stat-card {
  background: #fff;
  border: 1px solid rgba(0,0,0,0.06);
  border-radius: 12px;
  padding: 16px 18px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.03);
}
.hs-stat-val {
  font-family: 'Cormorant Garamond', serif;
  font-size: 24px; font-weight: 600; color: #1c1c1c;
  margin-bottom: 4px;
}
.hs-stat-lbl { font-size: 11.5px; color: #aaa; font-weight: 500; }

/* ─── Badges ──────────────────────────────────────────────────────── */
.hs-badge {
  font-size: 11.5px; padding: 4px 10px;
  border-radius: 20px; font-weight: 600;
  display: inline-flex; align-items: center; gap: 5px;
}
.hs-badge--green { background: #dcfce7; color: #15803d; }
.hs-badge--blue  { background: #dbeafe; color: #1d4ed8; }
.hs-badge--amber { background: #fef3c7; color: #b45309; }
.hs-badge--red   { background: #fee2e2; color: #b91c1c; }

/* ─── Tags ────────────────────────────────────────────────────────── */
.hs-tags-row { display: flex; flex-wrap: wrap; gap: 8px; align-items: center; }
.hs-tag {
  display: inline-flex; align-items: center; gap: 6px;
  background: rgba(183,63,42,.08); color: #b73f2a;
  font-size: 12.5px; font-weight: 500;
  padding: 5px 11px; border-radius: 20px;
}
.hs-tag-remove {
  background: none; border: none; cursor: pointer;
  color: #b73f2a; font-size: 10px;
  padding: 0; line-height: 1; opacity: 0.6;
  transition: opacity 0.15s;
}
.hs-tag-remove:hover { opacity: 1; }

/* ─── Sessions ────────────────────────────────────────────────────── */
.hs-session-row {
  display: flex; align-items: center;
  justify-content: space-between;
  padding: 13px 0;
  border-bottom: 1px solid rgba(0,0,0,0.05);
  gap: 12px;
}
.hs-session-row:last-of-type { border-bottom: none; }
.hs-session-left { display: flex; align-items: center; gap: 12px; }
.hs-session-icon {
  width: 36px; height: 36px;
  border-radius: 9px;
  background: #f0ede9;
  display: flex; align-items: center; justify-content: center;
  font-size: 14px; color: #b73f2a; flex-shrink: 0;
}
.hs-session-label {
  font-size: 13.5px; font-weight: 500; color: #1c1c1c;
  margin-bottom: 3px;
  display: flex; align-items: center; gap: 8px;
}
.hs-session-meta { font-size: 12px; color: #aaa; }

/* ─── Documents ───────────────────────────────────────────────────── */
.hs-doc-item,
.hs-maint-item {
  display: flex; align-items: center;
  gap: 14px; padding: 12px 0;
  border-bottom: 1px solid rgba(0,0,0,0.05);
}
.hs-doc-item:last-child,
.hs-maint-item:last-child { border-bottom: none; }
.hs-doc-icon {
  width: 36px; height: 36px;
  border-radius: 9px;
  background: #f0ede9;
  display: flex; align-items: center; justify-content: center;
  font-size: 14px; color: #b73f2a; flex-shrink: 0;
}
.hs-doc-info { flex: 1; min-width: 0; }
.hs-doc-name {
  font-size: 13.5px; font-weight: 500; color: #1c1c1c;
  margin-bottom: 2px; white-space: nowrap;
  overflow: hidden; text-overflow: ellipsis;
}
.hs-doc-meta { font-size: 12px; color: #aaa; }

/* ─── Upload zone ─────────────────────────────────────────────────── */
.hs-upload-zone {
  border: 1.5px dashed rgba(0,0,0,0.14);
  border-radius: 10px; padding: 32px;
  text-align: center; color: #aaa;
  cursor: pointer;
  transition: border-color 0.18s, background 0.18s;
}
.hs-upload-zone:hover,
.hs-upload-zone--over { border-color: #b73f2a; background: rgba(183,63,42,.02); }
.hs-upload-zone--uploading { pointer-events: none; opacity: 0.7; }
.hs-upload-zone i { font-size: 28px; margin-bottom: 10px; color: #ccc; display: block; }
.hs-upload-zone p { font-size: 13.5px; margin-bottom: 4px; }
.hs-upload-link { color: #b73f2a; font-weight: 500; cursor: pointer; }
.hs-upload-hint { font-size: 12px !important; color: #bbb; }

/* ─── Danger items ────────────────────────────────────────────────── */
.hs-danger-item {
  display: flex; align-items: center;
  justify-content: space-between;
  padding: 14px 0;
  border-bottom: 1px solid rgba(0,0,0,0.05);
  gap: 16px;
}
.hs-danger-item:last-child { border-bottom: none; padding-bottom: 0; }
.hs-danger-label { font-size: 13.5px; font-weight: 500; color: #1c1c1c; margin-bottom: 3px; }
.hs-danger-label--red { color: #e53e3e; }
.hs-danger-desc { font-size: 12px; color: #aaa; }

/* ─── Toast ───────────────────────────────────────────────────────── */
.hs-toast {
  position: fixed;
  bottom: 28px; right: 28px;
  padding: 14px 20px;
  border-radius: 10px;
  font-size: 13.5px; font-weight: 500;
  display: flex; align-items: center; gap: 10px;
  z-index: 9999;
  box-shadow: 0 8px 30px rgba(0,0,0,0.14);
}
.hs-toast--success { background: #1c1c1c; color: #fff; }
.hs-toast--error   { background: #fff5f5; color: #e53e3e; border: 1px solid rgba(229,62,62,.2); }
.hs-toast--info    { background: #eff6ff; color: #1d4ed8; border: 1px solid rgba(29,78,216,.2); }

.hs-toast-enter-active, .hs-toast-leave-active {
  transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
}
.hs-toast-enter-from, .hs-toast-leave-to {
  opacity: 0;
  transform: translateY(12px) scale(0.96);
}

/* ─── Responsive ──────────────────────────────────────────────────── */
@media (max-width: 900px) {
  .hs-settings-wrap {
    grid-template-columns: 1fr;
    padding: 0 16px;
  }
  .hs-sidebar { position: static; top: auto; }
  .hs-page-header-inner { padding: 0 16px; }
  .hs-page-title { font-size: 26px; }
  .hs-photo-row { flex-wrap: wrap; }
  .hs-verify-pills { margin-left: 0; }
}

@media (max-width: 560px) {
  .hs-field-row { grid-template-columns: 1fr; }
  .hs-stat-grid { grid-template-columns: repeat(2, 1fr); }
  .hs-stat-grid .hs-stat-card:last-child { grid-column: span 2; }
  .hs-btn-row { flex-direction: column; }
  .hs-btn { width: 100%; justify-content: center; }
}
</style>