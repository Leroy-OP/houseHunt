<template>
  <div class="about-page">

    <!-- ── HERO  -->
    <section class="about-hero">
      <div class="about-hero-bg"></div>
      <div class="about-hero-overlay"></div>
      <div class="about-hero-content">
        <p class="hero-eyebrow">OUR STORY</p>
        <h1 class="hero-title">Built for <em>Nairobi.</em><br/>Made for you.</h1>
        <p class="hero-subtitle">
          We believe finding a home should feel less like a search<br class="hide-sm"/>
          and more like a discovery.
        </p>
      </div>
      <!-- Decorative stat ribbon -->
      <div class="stat-ribbon">
        <div class="stat-item" v-for="stat in stats" :key="stat.label">
          <span class="stat-value">{{ stat.value }}</span>
          <span class="stat-label">{{ stat.label }}</span>
        </div>
      </div>
    </section>

    <!-- ── MISSION  -->
    <section class="mission-section">
      <div class="mission-inner">
        <div class="mission-text">
          <p class="section-eyebrow">WHO WE ARE</p>
          <h2 class="section-title">A smarter way<br/>to find home.</h2>
          <p class="mission-body">
            Hunter Street was born out of frustration — the kind that comes from
            scrolling endless listings, chasing unreliable landlords, and arriving
            at properties that look nothing like their photos.
          </p>
          <p class="mission-body">
            We set out to build something different: a curated, verified platform
            that connects Nairobi residents to spaces they'll genuinely love —
            from cosy bedsitters in Westlands to spacious apartments in Karen.
          </p>
          <div class="mission-values">
            <div class="value-chip" v-for="v in values" :key="v">
              <i class="fas fa-check"></i> {{ v }}
            </div>
          </div>
        </div>
        <div class="mission-visual">
          <div class="visual-card visual-card--top">
            <i class="fas fa-map-marker-alt"></i>
            <div>
              <p class="vc-title">Nairobi-First</p>
              <p class="vc-sub">Hyper-local knowledge you can trust</p>
            </div>
          </div>
          <div class="visual-card visual-card--mid">
            <i class="fas fa-shield-alt"></i>
            <div>
              <p class="vc-title">Verified Listings</p>
              <p class="vc-sub">Every property personally reviewed</p>
            </div>
          </div>
          <div class="visual-card visual-card--bot">
            <i class="fas fa-handshake"></i>
            <div>
              <p class="vc-title">Trusted Agencies</p>
              <p class="vc-sub">Only vetted real-estate partners</p>
            </div>
          </div>
          <div class="visual-accent-ring"></div>
        </div>
      </div>
    </section>

    <!-- ── HOW IT WORKS -->
    <section class="how-section">
      <div class="section-head centered">
        <p class="section-eyebrow">PROCESS</p>
        <h2 class="section-title">How Hunter Street works</h2>
        <p class="section-sub">Three simple steps between you and your next home.</p>
      </div>
      <div class="steps-grid">
        <div class="step-card" v-for="(step, i) in steps" :key="step.title">
          <div class="step-number">0{{ i + 1 }}</div>
          <div class="step-icon-wrap">
            <i :class="'fas ' + step.icon"></i>
          </div>
          <h4 class="step-title">{{ step.title }}</h4>
          <p class="step-desc">{{ step.desc }}</p>
          <div class="step-connector" v-if="i < steps.length - 1"></div>
        </div>
      </div>
    </section>

    <!-- ── TEAM -->
    <section class="team-section">
      <div class="section-head centered">
        <p class="section-eyebrow">THE PEOPLE</p>
        <h2 class="section-title">Meet our team</h2>
        <p class="section-sub">A small, passionate crew driven by one goal — better homes for Nairobi.</p>
      </div>
      <div class="team-grid">
        <div class="team-card" v-for="member in team" :key="member.name">
          <div class="team-avatar">
            <div class="avatar-initials">{{ initials(member.name) }}</div>
          </div>
          <h4 class="team-name">{{ member.name }}</h4>
          <p class="team-role">{{ member.role }}</p>
          <p class="team-bio">{{ member.bio }}</p>
          <div class="team-socials">
            <a href="#" class="tsocial"><i class="fab fa-linkedin-in"></i></a>
            <a href="#" class="tsocial"><i class="fab fa-twitter"></i></a>
          </div>
        </div>
      </div>
    </section>

    <!-- ── CTA BANNER  -->
    <section class="cta-section">
      <div class="cta-inner">
        <p class="section-eyebrow" style="color:#f2c4b8">GET STARTED</p>
        <h2 class="cta-title">Ready to find your<br/><em>perfect space?</em></h2>
        <p class="cta-sub">
          Join thousands of Nairobi residents who found their home through Hunter Street.
        </p>
        <div class="cta-actions">
          <router-link to="/properties" class="cta-btn cta-btn--primary">
            Browse Properties <i class="fas fa-arrow-right"></i>
          </router-link>
          <a href="mailto:info@hunterstreet.co.ke" class="cta-btn cta-btn--ghost">
            Contact Us
          </a>
        </div>
      </div>
      <div class="cta-decoration">
        <div class="deco-circle deco-circle--1"></div>
        <div class="deco-circle deco-circle--2"></div>
      </div>
    </section>

    <!-- ── FOOTER ─────────────────────────────────────────────────────── -->
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
export default {
  name: 'AboutPage',
  data() {
    return {
      stats: [
        { value: '500+', label: 'Active Listings' },
        { value: '140+',   label: 'Verified Agencies' },
        { value: '1,500+', label: 'Happy Tenants' },
        { value: '15+',    label: 'Neighbourhoods' },
      ],
      values: [
        'Transparency first',
        'Verified listings only',
        'Renter-centric design',
        'Local expertise',
      ],
      steps: [
        {
          icon: 'fa-search',
          title: 'Search & Filter',
          desc: 'Browse listings by location, type, and budget. Our smart filters surface only what matters to you.',
        },
        {
          icon: 'fa-home',
          title: 'Explore Spaces',
          desc: 'View detailed photos, pricing, and agency contacts — all verified before they go live.',
        },
        {
          icon: 'fa-key',
          title: 'Move In',
          desc: 'Connect directly with trusted agencies and landlords. No middlemen, no hidden fees.',
        },
      ],
      team: [
        {
          name: 'Leroy Keretts',
          role: 'Co-Founder & CEO',
          bio: 'Former property consultant with 10 years in Nairobi real estate. Passionate about making housing accessible to all.',
        },
        {
          name: 'Victoria Chebet',
          role: 'Co-Founder & CTO',
          bio: 'Full-stack engineer who previously built fintech products across East Africa. Believes great software changes lives.',
        },
        {
          name: 'Mercy Mbingu',
          role: 'Head of Listings',
          bio: 'Meticulous about quality, Zawadi oversees every property verification and agency partnership on the platform.',
        },
        {
          name: 'Frank Obare',
          role: 'Design & UX Lead',
          bio: 'Obsessed with beautiful, intuitive experiences. If it feels effortless, David probably spent weeks on it.',
        },
      ],
    };
  },
  methods: {
    initials(name) {
      return name.split(' ').map(n => n[0]).join('').slice(0, 2).toUpperCase();
    },
  },
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,300;1,400;1,600&family=DM+Sans:wght@300;400;500;600&display=swap');

/* ── Reset / Base  */
.about-page {
  font-family: 'DM Sans', sans-serif;
  background: #f6f4f1;
  color: #1c1c1c;
  min-height: 100vh;
}

/* ── HERO ─────────────────────────────────────────────────────────────── */
.about-hero {
  position: relative;
  min-height: 72vh;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
  margin: 0 24px;
  border-radius: 30px;
  overflow: hidden;
}

.about-hero-bg {
  position: absolute;
  inset: 0;
  background:
    url('https://images.unsplash.com/photo-1486325212027-8081e485255e?w=1400&q=80')
    center / cover no-repeat;
  filter: brightness(0.6);
}

.about-hero-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(160deg, rgba(0,0,0,0.6) 0%, rgba(183,63,42,0.25) 100%);
  z-index: 1;
}

.about-hero-content {
  position: relative;
  z-index: 2;
  padding: 80px 24px 120px;
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
  font-size: clamp(48px, 7vw, 88px);
  font-weight: 300;
  line-height: 1.05;
  color: #fff;
  margin: 0 0 20px;
  animation: fadeUp 0.9s ease 0.1s both;
}

.hero-title em {
  font-style: italic;
  color: #f2c4b8;
}

.hero-subtitle {
  font-size: 16px;
  font-weight: 300;
  color: rgba(255,255,255,0.8);
  line-height: 1.7;
  animation: fadeUp 1s ease 0.2s both;
}

/* Stat ribbon */
.stat-ribbon {
  position: absolute;
  bottom: 0;
  left: 0; right: 0;
  z-index: 3;
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  background: rgba(255,255,255,0.97);
  border-top: 1px solid rgba(0,0,0,0.06);
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 22px 16px;
  border-right: 1px solid #ede9e4;
}

.stat-item:last-child { border-right: none; }

.stat-value {
  font-family: 'Cormorant Garamond', serif;
  font-size: 32px;
  font-weight: 600;
  color: #b73f2a;
  line-height: 1;
  margin-bottom: 4px;
}

.stat-label {
  font-size: 11px;
  letter-spacing: 1.5px;
  color: #888;
  text-transform: uppercase;
  font-weight: 500;
}

/* ── MISSION ──────────────────────────────────────────────────────────── */
.mission-section {
  padding: 96px 48px;
  background: #fff;
}

.mission-inner {
  max-width: 1100px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 72px;
  align-items: center;
}

.section-eyebrow {
  font-size: 10px;
  letter-spacing: 3px;
  font-weight: 600;
  color: #b73f2a;
  margin: 0 0 10px;
  text-transform: uppercase;
}

.section-title {
  font-family: 'Cormorant Garamond', serif;
  font-size: clamp(30px, 3.5vw, 44px);
  font-weight: 600;
  color: #111;
  margin: 0 0 24px;
  line-height: 1.15;
}

.mission-body {
  font-size: 15px;
  color: #555;
  line-height: 1.8;
  margin: 0 0 18px;
}

.mission-values {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-top: 28px;
}

.value-chip {
  display: flex;
  align-items: center;
  gap: 7px;
  padding: 8px 14px;
  background: #fdf5f3;
  border: 1px solid #f0d8d3;
  border-radius: 30px;
  font-size: 13px;
  color: #b73f2a;
  font-weight: 500;
}

.value-chip i { font-size: 10px; }

/* Visual column */
.mission-visual {
  position: relative;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.visual-card {
  display: flex;
  align-items: center;
  gap: 16px;
  background: #f9f8f6;
  border: 1px solid #ede9e4;
  border-radius: 16px;
  padding: 20px 24px;
  transition: box-shadow 0.25s, transform 0.25s;
}

.visual-card:hover {
  box-shadow: 0 10px 30px rgba(0,0,0,0.07);
  transform: translateX(6px);
}

.visual-card--mid { margin-left: 24px; }
.visual-card--bot { margin-left: 0; }

.visual-card > .fas {
  font-size: 22px;
  color: #b73f2a;
  width: 48px;
  height: 48px;
  background: #fdf5f3;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.vc-title {
  font-family: 'Cormorant Garamond', serif;
  font-size: 18px;
  font-weight: 600;
  color: #111;
  margin: 0 0 3px;
}

.vc-sub { font-size: 12.5px; color: #888; margin: 0; }

.visual-accent-ring {
  position: absolute;
  width: 180px;
  height: 180px;
  border-radius: 50%;
  border: 2px dashed #f0d8d3;
  bottom: -40px;
  right: -40px;
  pointer-events: none;
  opacity: 0.5;
}

/* ── HOW IT WORKS ─────────────────────────────────────────────────────── */
.how-section {
  padding: 88px 48px;
  background: #f6f4f1;
}

.section-head.centered { text-align: center; margin-bottom: 56px; }
.section-sub {
  font-size: 15px;
  color: #888;
  margin-top: 10px;
  line-height: 1.7;
}

.steps-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 32px;
  max-width: 1000px;
  margin: 0 auto;
  position: relative;
}

.step-card {
  background: #fff;
  border-radius: 20px;
  padding: 36px 28px;
  position: relative;
  text-align: center;
  box-shadow: 0 2px 16px rgba(0,0,0,0.05);
  border: 1px solid #ede9e4;
  transition: box-shadow 0.25s, transform 0.25s;
}

.step-card:hover {
  box-shadow: 0 16px 40px rgba(0,0,0,0.1);
  transform: translateY(-6px);
}

.step-number {
  font-family: 'Cormorant Garamond', serif;
  font-size: 52px;
  font-weight: 600;
  color: #f0d8d3;
  line-height: 1;
  margin-bottom: 12px;
}

.step-icon-wrap {
  width: 56px;
  height: 56px;
  background: linear-gradient(135deg, #b73f2a, #d4614a);
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 20px;
  color: #fff;
  font-size: 20px;
  box-shadow: 0 8px 20px rgba(183,63,42,0.3);
}

.step-title {
  font-family: 'Cormorant Garamond', serif;
  font-size: 22px;
  font-weight: 600;
  color: #111;
  margin: 0 0 10px;
}

.step-desc {
  font-size: 13.5px;
  color: #777;
  line-height: 1.7;
  margin: 0;
}

/* Dashed connector between steps */
.step-connector {
  display: none; /* shown via pseudo-element on grid parent for simplicity */
}

/* ── TEAM ─────────────────────────────────────────────────────────────── */
.team-section {
  padding: 88px 48px;
  background: #fff;
}

.team-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 24px;
  max-width: 1100px;
  margin: 0 auto;
}

.team-card {
  background: #f9f8f6;
  border: 1px solid #ede9e4;
  border-radius: 20px;
  padding: 32px 24px;
  text-align: center;
  transition: box-shadow 0.25s, transform 0.25s;
}

.team-card:hover {
  box-shadow: 0 12px 36px rgba(0,0,0,0.08);
  transform: translateY(-5px);
}

.team-avatar {
  width: 72px;
  height: 72px;
  border-radius: 50%;
  background: linear-gradient(135deg, #b73f2a, #d4614a);
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 18px;
  box-shadow: 0 6px 20px rgba(183,63,42,0.25);
}

.avatar-initials {
  font-family: 'Cormorant Garamond', serif;
  font-size: 24px;
  font-weight: 600;
  color: #fff;
  letter-spacing: 1px;
}

.team-name {
  font-family: 'Cormorant Garamond', serif;
  font-size: 20px;
  font-weight: 600;
  color: #111;
  margin: 0 0 4px;
}

.team-role {
  font-size: 11px;
  letter-spacing: 1.5px;
  color: #b73f2a;
  text-transform: uppercase;
  font-weight: 600;
  margin: 0 0 14px;
}

.team-bio {
  font-size: 13px;
  color: #777;
  line-height: 1.7;
  margin: 0 0 18px;
}

.team-socials { display: flex; justify-content: center; gap: 8px; }

.tsocial {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  border: 1px solid #e5e5e5;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #888;
  font-size: 12px;
  text-decoration: none;
  transition: all 0.2s;
}

.tsocial:hover { border-color: #b73f2a; color: #b73f2a; background: #fdf5f3; }

/* ── CTA BANNER ───────────────────────────────────────────────────────── */
.cta-section {
  margin: 0 24px 40px;
  border-radius: 30px;
  background: linear-gradient(135deg, #1a0e0c 0%, #2e1210 40%, #b73f2a 100%);
  padding: 80px 48px;
  text-align: center;
  color: #fff;
  position: relative;
  overflow: hidden;
}

.cta-inner { position: relative; z-index: 2; }

.cta-title {
  font-family: 'Cormorant Garamond', serif;
  font-size: clamp(40px, 5vw, 68px);
  font-weight: 300;
  line-height: 1.1;
  color: #fff;
  margin: 10px 0 18px;
}

.cta-title em { font-style: italic; color: #f2c4b8; }

.cta-sub {
  font-size: 15px;
  color: rgba(255,255,255,0.65);
  margin: 0 0 40px;
  line-height: 1.7;
}

.cta-actions { display: flex; justify-content: center; gap: 16px; flex-wrap: wrap; }

.cta-btn {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  padding: 15px 32px;
  border-radius: 50px;
  font-size: 14px;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.25s;
  letter-spacing: 0.3px;
}

.cta-btn--primary {
  background: #fff;
  color: #b73f2a;
}

.cta-btn--primary:hover {
  background: #f2c4b8;
  color: #7a2216;
  transform: translateY(-2px);
  box-shadow: 0 10px 30px rgba(0,0,0,0.2);
}

.cta-btn--ghost {
  background: transparent;
  color: #fff;
  border: 1px solid rgba(255,255,255,0.4);
}

.cta-btn--ghost:hover {
  background: rgba(255,255,255,0.08);
  border-color: #fff;
  transform: translateY(-2px);
}

/* Decorative circles */
.deco-circle {
  position: absolute;
  border-radius: 50%;
  pointer-events: none;
  z-index: 1;
}

.deco-circle--1 {
  width: 400px; height: 400px;
  top: -180px; right: -120px;
  background: rgba(255,255,255,0.04);
}

.deco-circle--2 {
  width: 250px; height: 250px;
  bottom: -100px; left: -60px;
  background: rgba(255,255,255,0.03);
}

/* ── FOOTER ───────────────────────────────────────────────────────────── */
.site-footer { background: #111; color: #fff; padding: 60px 32px 0; }

.footer-inner {
  display: grid;
  grid-template-columns: 2fr 1fr 1fr;
  gap: 48px;
  padding-bottom: 48px;
  border-bottom: 1px solid rgba(255,255,255,0.08);
}

.footer-brand-label {
  font-size: 11px; letter-spacing: 3px; font-weight: 600;
  color: #b73f2a; margin: 0 0 10px;
}

.footer-brand-desc {
  font-size: 14px; color: rgba(255,255,255,0.5);
  line-height: 1.7; margin: 0 0 20px; max-width: 280px;
}

.footer-socials { display: flex; gap: 10px; }

.social-icon {
  width: 36px; height: 36px; border-radius: 50%;
  border: 1px solid rgba(255,255,255,0.15);
  display: flex; align-items: center; justify-content: center;
  color: rgba(255,255,255,0.6); text-decoration: none;
  font-size: 13px; transition: all 0.2s;
}

.social-icon:hover { border-color: #b73f2a; color: #b73f2a; }

.footer-col-label {
  font-size: 10px; letter-spacing: 2.5px; font-weight: 600;
  color: rgba(255,255,255,0.35); margin: 0 0 16px;
}

.footer-link {
  display: block; font-size: 14px; color: rgba(255,255,255,0.6);
  text-decoration: none; margin-bottom: 10px; transition: color 0.2s;
}

.footer-link:hover { color: #fff; }

.footer-contact-line {
  display: flex; align-items: center; gap: 8px;
  font-size: 13.5px; color: rgba(255,255,255,0.55); margin-bottom: 10px;
}

.footer-contact-line i { color: #b73f2a; font-size: 12px; }

.footer-bottom {
  padding: 20px 0; text-align: center;
  font-size: 12.5px; color: rgba(255,255,255,0.25);
}

/* ── Animations ───────────────────────────────────────────────────────── */
@keyframes fadeUp {
  from { opacity: 0; transform: translateY(24px); }
  to   { opacity: 1; transform: translateY(0); }
}

/* ── Responsive ───────────────────────────────────────────────────────── */
.hide-sm { display: inline; }

@media (max-width: 1024px) {
  .team-grid { grid-template-columns: repeat(2, 1fr); }
}

@media (max-width: 900px) {
  .mission-inner { grid-template-columns: 1fr; gap: 40px; }
  .steps-grid { grid-template-columns: 1fr; max-width: 480px; margin: 0 auto; }
  .stat-ribbon { grid-template-columns: repeat(2, 1fr); }
  .footer-inner { grid-template-columns: 1fr 1fr; }
  .about-hero { margin: 0 12px; border-radius: 16px; }
  .cta-section { margin: 0 12px 24px; border-radius: 20px; padding: 56px 24px; }
}

@media (max-width: 600px) {
  .about-hero-content { padding: 60px 20px 100px; }
  .mission-section, .how-section, .team-section { padding: 56px 20px; }
  .team-grid { grid-template-columns: 1fr; }
  .stat-ribbon { grid-template-columns: repeat(2, 1fr); }
  .stat-value { font-size: 24px; }
  .cta-actions { flex-direction: column; align-items: center; }
  .footer-inner { grid-template-columns: 1fr; gap: 32px; }
  .visual-card--mid { margin-left: 0; }
  .hide-sm { display: none; }
}
</style>