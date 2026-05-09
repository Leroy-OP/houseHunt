<template>
  <div class="support-page">

    <!-- ── HERO ──────────────────────────────────────────────────────── -->
    <section class="support-hero">
      <div class="support-hero-bg"></div>
      <div class="support-hero-overlay"></div>
      <div class="support-hero-content">
        <p class="hero-eyebrow">SUPPORT HUNTER STREET</p>
        <h1 class="hero-title">Help us build<br/><em>better homes</em><br/>for Nairobi.</h1>
        <p class="hero-subtitle">
          We're a small team with a big mission. Every partnership,<br class="hide-sm"/>
          referral, and conversation moves us forward.
        </p>
        <div class="hero-cta-row">
          <a href="#ways" class="hero-btn hero-btn--primary">See How to Help <i class="fas fa-arrow-down"></i></a>
          <a href="#contact" class="hero-btn hero-btn--ghost">Get in Touch</a>
        </div>
      </div>
      <div class="hero-scroll-indicator">
        <span></span>
      </div>
    </section>

    <!-- ── IMPACT STRIP ───────────────────────────────────────────────── -->
    <div class="impact-strip">
      <div class="impact-item" v-for="item in impact" :key="item.label">
        <i :class="'fas ' + item.icon"></i>
        <div class="impact-text">
          <span class="impact-value">{{ item.value }}</span>
          <span class="impact-label">{{ item.label }}</span>
        </div>
      </div>
    </div>

    <!-- ── WHY SUPPORT ────────────────────────────────────────────────── -->
    <section class="why-section">
      <div class="why-inner">
        <div class="why-visual">
          <div class="why-quote-card">
            <i class="fas fa-quote-left quote-icon"></i>
            <p class="quote-text">
              "Finding a home in Nairobi shouldn't be an ordeal. We're changing that —
              one verified listing at a time."
            </p>
            <div class="quote-author">
              <div class="author-avatar">LK</div>
              <div>
                <p class="author-name">Leroy Keretts</p>
                <p class="author-title">Co-Founder, Hunter Street</p>
              </div>
            </div>
          </div>
          <div class="why-accent-box">
            <p class="accent-stat">73%</p>
            <p class="accent-desc">of Nairobi renters report difficulty finding reliable housing information online.</p>
          </div>
        </div>
        <div class="why-text">
          <p class="section-eyebrow">THE CAUSE</p>
          <h2 class="section-title">Why your support<br/>matters.</h2>
          <p class="why-body">
            The rental market in Nairobi remains fragmented, opaque, and often exploitative.
            Tenants waste weeks on dead-end viewings. Landlords struggle to reach genuine
            leads. Agencies lack a trusted digital presence.
          </p>
          <p class="why-body">
            Hunter Street bridges that gap — but to grow our coverage, improve our tools,
            and keep listings free for renters, we need people who believe in the mission
            to stand behind us.
          </p>
          <div class="why-pillars">
            <div class="pillar" v-for="p in pillars" :key="p.title">
              <div class="pillar-icon"><i :class="'fas ' + p.icon"></i></div>
              <div>
                <p class="pillar-title">{{ p.title }}</p>
                <p class="pillar-desc">{{ p.desc }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- ── WAYS TO SUPPORT ────────────────────────────────────────────── -->
    <section class="ways-section" id="ways">
      <div class="section-head centered">
        <p class="section-eyebrow">GET INVOLVED</p>
        <h2 class="section-title">Ways to support us</h2>
        <p class="section-sub">Pick what works best for you — every action counts.</p>
      </div>
      <div class="ways-grid">
        <div
          class="way-card"
          v-for="(way, i) in ways"
          :key="way.title"
          :class="{ 'way-card--featured': way.featured }"
        >
          <div class="way-badge" v-if="way.featured">Most Impactful</div>
          <div class="way-icon-wrap">
            <i :class="'fas ' + way.icon"></i>
          </div>
          <h3 class="way-title">{{ way.title }}</h3>
          <p class="way-desc">{{ way.desc }}</p>
          <ul class="way-perks">
            <li v-for="perk in way.perks" :key="perk">
              <i class="fas fa-check-circle"></i> {{ perk }}
            </li>
          </ul>
          <a :href="way.href" class="way-btn" :class="{ 'way-btn--solid': way.featured }">
            {{ way.cta }} <i class="fas fa-arrow-right"></i>
          </a>
        </div>
      </div>
    </section>

    <!-- ── PARTNER TIERS ──────────────────────────────────────────────── -->
    <section class="tiers-section">
      <div class="section-head centered">
        <p class="section-eyebrow">AGENCY PARTNERSHIPS</p>
        <h2 class="section-title">Partnership tiers</h2>
        <p class="section-sub">Structured plans for agencies ready to grow with us.</p>
      </div>
      <div class="tiers-grid">
        <div
          class="tier-card"
          v-for="tier in tiers"
          :key="tier.name"
          :class="{ 'tier-card--highlighted': tier.highlighted }"
        >
          <p class="tier-tag" v-if="tier.highlighted">Most Popular</p>
          <p class="tier-name">{{ tier.name }}</p>
          <div class="tier-price">
            <span class="tier-currency">KES</span>
            <span class="tier-amount">{{ tier.price }}</span>
            <span class="tier-period">/mo</span>
          </div>
          <p class="tier-tagline">{{ tier.tagline }}</p>
          <ul class="tier-features">
            <li v-for="f in tier.features" :key="f" :class="{ disabled: f.startsWith('—') }">
              <i :class="f.startsWith('—') ? 'fas fa-minus' : 'fas fa-check'"></i>
              {{ f.replace('—', '') }}
            </li>
          </ul>
          <a href="#contact" class="tier-btn" :class="{ 'tier-btn--solid': tier.highlighted }">
            Get Started <i class="fas fa-arrow-right"></i>
          </a>
        </div>
      </div>
    </section>

    <!-- ── TESTIMONIALS ───────────────────────────────────────────────── -->
    <section class="testimonials-section">
      <div class="section-head centered">
        <p class="section-eyebrow">WHAT THEY SAY</p>
        <h2 class="section-title">Voices from our community</h2>
      </div>
      <div class="testimonials-grid">
        <div class="testi-card" v-for="t in testimonials" :key="t.name">
          <div class="testi-stars">
            <i class="fas fa-star" v-for="n in 5" :key="n"></i>
          </div>
          <p class="testi-text">"{{ t.text }}"</p>
          <div class="testi-author">
            <div class="testi-avatar">{{ t.name[0] }}</div>
            <div>
              <p class="testi-name">{{ t.name }}</p>
              <p class="testi-role">{{ t.role }}</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- ── CONTACT / SUPPORT FORM ─────────────────────────────────────── -->
    <section class="contact-section" id="contact">
      <div class="contact-inner">
        <div class="contact-info">
          <p class="section-eyebrow">REACH OUT</p>
          <h2 class="section-title">Let's talk.</h2>
          <p class="contact-body">
            Whether you're an agency looking to partner, an investor who believes in our vision,
            or simply someone who wants to help — we'd love to hear from you.
          </p>
          <div class="contact-channels">
            <div class="channel" v-for="c in channels" :key="c.label">
              <div class="channel-icon"><i :class="'fas ' + c.icon"></i></div>
              <div>
                <p class="channel-label">{{ c.label }}</p>
                <a :href="c.href" class="channel-value">{{ c.value }}</a>
              </div>
            </div>
          </div>
          <div class="contact-socials">
            <a href="#" class="csocial"><i class="fab fa-facebook-f"></i></a>
            <a href="#" class="csocial"><i class="fab fa-twitter"></i></a>
            <a href="#" class="csocial"><i class="fab fa-instagram"></i></a>
            <a href="#" class="csocial"><i class="fab fa-linkedin-in"></i></a>
          </div>
        </div>

        <div class="contact-form-wrap">
          <div class="form-card">
            <h3 class="form-title">Send us a message</h3>
            <p class="form-sub">We respond within 24 hours.</p>

            <div class="form-row">
              <div class="form-field">
                <label>Full Name</label>
                <input v-model="form.name" type="text" placeholder="Deborah Rotich" />
              </div>
              <div class="form-field">
                <label>Email Address</label>
                <input v-model="form.email" type="email" placeholder="deborah@example.com" />
              </div>
            </div>

            <div class="form-field">
              <label>How would you like to support us?</label>
              <div class="custom-select-wrap">
                <select v-model="form.type">
                  <option value="" disabled>Select an option</option>
                  <option v-for="opt in supportTypes" :key="opt" :value="opt">{{ opt }}</option>
                </select>
                <i class="fas fa-chevron-down select-arrow"></i>
              </div>
            </div>

            <div class="form-field">
              <label>Phone <span class="optional">(optional)</span></label>
              <input v-model="form.phone" type="tel" placeholder="+254 7XX XXX XXX" />
            </div>

            <div class="form-field">
              <label>Message</label>
              <textarea v-model="form.message" rows="4" placeholder="Tell us a bit about yourself and how you'd like to get involved…"></textarea>
            </div>

            <button class="form-submit" @click="submitForm" :disabled="submitting || submitted">
              <span v-if="submitted"><i class="fas fa-check"></i> Message Sent!</span>
              <span v-else-if="submitting"><i class="fas fa-spinner fa-spin"></i> Sending…</span>
              <span v-else>Send Message <i class="fas fa-paper-plane"></i></span>
            </button>

            <p class="form-privacy">
              <i class="fas fa-lock"></i> Your information is never shared with third parties.
            </p>
          </div>
        </div>
      </div>
    </section>

    <!-- ── FAQ ────────────────────────────────────────────────────────── -->
    <section class="faq-section">
      <div class="section-head centered">
        <p class="section-eyebrow">FAQ</p>
        <h2 class="section-title">Common questions</h2>
      </div>
      <div class="faq-list">
        <div
          class="faq-item"
          v-for="(faq, i) in faqs"
          :key="i"
          :class="{ open: openFaq === i }"
          @click="openFaq = openFaq === i ? null : i"
        >
          <div class="faq-q">
            <span>{{ faq.q }}</span>
            <i :class="openFaq === i ? 'fas fa-minus' : 'fas fa-plus'"></i>
          </div>
          <transition name="faq-slide">
            <p class="faq-a" v-if="openFaq === i">{{ faq.a }}</p>
          </transition>
        </div>
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
  name: 'SupportPage',
  data() {
    return {
      openFaq: null,
      submitting: false,
      submitted: false,

      form: {
        name: '',
        email: '',
        type: '',
        phone: '',
        message: '',
      },

      supportTypes: [
        'Agency Partnership',
        'Refer a Landlord / Agency',
        'Investor / Funder',
        'Spread the Word',
        'Volunteer / Intern',
        'Other',
      ],

      impact: [
        { icon: 'fa-home',          value: '500+',  label: 'Listings Hosted' },
        { icon: 'fa-users',         value: '1,500+',  label: 'Renters Helped' },
        { icon: 'fa-building',      value: '140+',    label: 'Agency Partners' },
        { icon: 'fa-map-marker-alt',value: '15+',     label: 'Neighbourhoods' },
        { icon: 'fa-star',          value: '4.8 / 5', label: 'Platform Rating' },
      ],

      pillars: [
        { icon: 'fa-search-dollar', title: 'Free for renters, always', desc: 'Tenants never pay to browse or enquire.' },
        { icon: 'fa-shield-alt',    title: 'Rigorous verification',    desc: 'Every listing is checked before it goes live.' },
        { icon: 'fa-chart-line',    title: 'Growing every month',      desc: 'We\'re expanding to more neighbourhoods weekly.' },
      ],

      ways: [
        {
          icon: 'fa-building',
          title: 'Partner as an Agency',
          desc: 'List your properties on the most trusted rental platform in Nairobi. Reach verified, serious tenants.',
          perks: [
            'Dedicated agency profile page',
            'Unlimited property listings',
            'Direct tenant enquiries',
            'Featured placement options',
          ],
          cta: 'Become a Partner',
          href: '#contact',
          featured: true,
        },
        {
          icon: 'fa-share-alt',
          title: 'Refer Someone',
          desc: 'Know a landlord, agency, or property manager? Send them our way and help grow the network.',
          perks: [
            'Simple referral process',
            'No sign-up required',
            'Help your contacts grow',
            'Build the Nairobi community',
          ],
          cta: 'Refer Now',
          href: '#contact',
          featured: false,
        },
        {
          icon: 'fa-bullhorn',
          title: 'Spread the Word',
          desc: 'Share Hunter Street with tenants, friends, and communities. Word of mouth is our biggest asset.',
          perks: [
            'Share on social media',
            'Mention in community groups',
            'Leave a review or rating',
            'Embed our listings widget',
          ],
          cta: 'Share Hunter Street',
          href: '#',
          featured: false,
        },
        {
          icon: 'fa-handshake',
          title: 'Invest in Our Vision',
          desc: 'We\'re building the definitive housing platform for East Africa. Serious investors are welcome.',
          perks: [
            'Equity or advisory roles',
            'Direct founder access',
            'Impact-focused opportunity',
            'Growing regional market',
          ],
          cta: 'Talk to Us',
          href: '#contact',
          featured: false,
        },
      ],

      tiers: [
        {
          name: 'Starter',
          price: 'Free',
          tagline: 'Perfect for independent landlords.',
          highlighted: false,
          features: [
            'Up to 3 listings',
            'Basic agency profile',
            'Tenant enquiry inbox',
            '— Featured placement',
            '— Priority support',
            '— Analytics dashboard',
          ],
        },
        {
          name: 'Growth',
          price: '2,999',
          tagline: 'For agencies scaling their reach.',
          highlighted: true,
          features: [
            'Up to 25 listings',
            'Full agency profile',
            'Tenant enquiry inbox',
            'Featured placement',
            'Priority support',
            '— Analytics dashboard',
          ],
        },
        {
          name: 'Pro',
          price: '6,999',
          tagline: 'For established agencies that want it all.',
          highlighted: false,
          features: [
            'Unlimited listings',
            'Full agency profile',
            'Tenant enquiry inbox',
            'Featured placement',
            'Priority support',
            'Analytics dashboard',
          ],
        },
      ],

      testimonials: [
        {
          name: 'Walter Ojwang',
          role: 'Tenant — Tumaini',
          text: 'I found my apartment in three days. Every listing I clicked was real and the agency was responsive. Nothing like my previous experiences.',
        },
        {
          name: 'Ignatius Wango',
          role: 'Director, Soothing Realtors',
          text: 'Our agency has seen a 40% increase in qualified leads since listing on Hunter Street. The quality of tenants is noticeably better.',
        },
        {
          name: 'Elly Malit Senteu',
          role: 'Tenant — Masai Lodge',
          text: 'Finally, a platform that respects your time. No fake listings, no unanswered calls. I refer everyone I know.',
        },
      ],

      channels: [
        { icon: 'fa-envelope',      label: 'Email Us',     value: 'info@hunterstreet.co.ke',   href: 'mailto:info@hunterstreet.co.ke' },
        { icon: 'fa-phone',         label: 'Call Us',      value: '+254 700 000 000',           href: 'tel:+254700000000' },
        { icon: 'fa-map-marker-alt',label: 'Visit Us',     value: 'Westlands, Nairobi',         href: '#' },
        { icon: 'fa-clock',         label: 'Office Hours', value: 'Mon – Fri, 8 AM – 6 PM',    href: '#' },
      ],

      faqs: [
        {
          q: 'Is listing on Hunter Street free for renters?',
          a: 'Yes — completely. Renters can browse, save, and contact agencies without paying anything. Our revenue comes entirely from agency partnership plans.',
        },
        {
          q: 'How do you verify listings?',
          a: 'Every listing goes through a manual review by our team before it\'s published. We check photos, pricing accuracy, and confirm agency legitimacy before approval.',
        },
        {
          q: 'What does an agency partnership include?',
          a: 'Partners get a dedicated profile page, the ability to list properties, direct tenant enquiry notifications, and optional featured placement for greater visibility.',
        },
        {
          q: 'Can I list properties in areas outside Nairobi?',
          a: 'Not yet — but it\'s on our roadmap. We\'re currently focused on delivering the best experience across Nairobi before expanding to other cities.',
        },
        {
          q: 'How can I invest in Hunter Street?',
          a: 'We\'re open to conversations with aligned investors and advisors. Please reach out via the contact form and select "Investor / Funder" as your support type.',
        },
        {
          q: 'How quickly will I hear back after submitting the form?',
          a: 'Our team typically responds within 24 hours on weekdays. For urgent matters, calling or WhatsApp-ing our office number is the fastest route.',
        },
      ],
    };
  },
  methods: {
    submitForm() {
      if (!this.form.name || !this.form.email || !this.form.message) return;
      this.submitting = true;
      setTimeout(() => {
        this.submitting = false;
        this.submitted = true;
        this.form = { name: '', email: '', type: '', phone: '', message: '' };
      }, 1800);
    },
  },
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,300;1,400;1,600&family=DM+Sans:wght@300;400;500;600&display=swap');

/* ── Base ─────────────────────────────────────────────────────────────── */
.support-page {
  font-family: 'DM Sans', sans-serif;
  background: #f6f4f1;
  color: #1c1c1c;
  min-height: 100vh;
}

/* ── HERO ─────────────────────────────────────────────────────────────── */
.support-hero {
  position: relative;
  min-height: 88vh;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
  margin: 0 24px;
  border-radius: 30px;
  overflow: hidden;
}

.support-hero-bg {
  position: absolute;
  inset: 0;
  background:
    url('https://images.unsplash.com/photo-1560518883-ce09059eeffa?w=1400&q=80')
    center / cover no-repeat;
  filter: brightness(0.5);
}

.support-hero-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(
    160deg,
    rgba(183,63,42,0.45) 0%,
    rgba(0,0,0,0.55) 60%,
    rgba(0,0,0,0.7) 100%
  );
  z-index: 1;
}

.support-hero-content {
  position: relative;
  z-index: 2;
  padding: 60px 24px;
  color: #fff;
}

.hero-eyebrow {
  font-size: 11px;
  letter-spacing: 4px;
  font-weight: 600;
  color: rgba(255,255,255,0.65);
  margin-bottom: 20px;
  animation: fadeUp 0.8s ease both;
}

.hero-title {
  font-family: 'Cormorant Garamond', serif;
  font-size: clamp(50px, 7.5vw, 96px);
  font-weight: 300;
  line-height: 1.05;
  color: #fff;
  margin: 0 0 22px;
  animation: fadeUp 0.9s ease 0.1s both;
}

.hero-title em {
  font-style: italic;
  color: #f2c4b8;
}

.hero-subtitle {
  font-size: 16px;
  font-weight: 300;
  color: rgba(255,255,255,0.78);
  line-height: 1.7;
  margin: 0 0 40px;
  animation: fadeUp 1s ease 0.2s both;
}

.hero-cta-row {
  display: flex;
  justify-content: center;
  gap: 14px;
  flex-wrap: wrap;
  animation: fadeUp 1.1s ease 0.3s both;
}

.hero-btn {
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

.hero-btn--primary {
  background: #b73f2a;
  color: #fff;
  box-shadow: 0 10px 30px rgba(183,63,42,0.4);
}

.hero-btn--primary:hover {
  background: #9a3523;
  transform: translateY(-2px);
  box-shadow: 0 14px 36px rgba(183,63,42,0.5);
}

.hero-btn--ghost {
  background: transparent;
  color: #fff;
  border: 1px solid rgba(255,255,255,0.45);
}

.hero-btn--ghost:hover {
  background: rgba(255,255,255,0.09);
  border-color: #fff;
  transform: translateY(-2px);
}

/* Scroll indicator */
.hero-scroll-indicator {
  position: absolute;
  bottom: 30px;
  left: 50%;
  transform: translateX(-50%);
  z-index: 2;
}

.hero-scroll-indicator span {
  display: block;
  width: 1px;
  height: 48px;
  background: linear-gradient(to bottom, rgba(255,255,255,0), rgba(255,255,255,0.5));
  margin: 0 auto;
  animation: scrollPulse 1.8s ease-in-out infinite;
}

@keyframes scrollPulse {
  0%, 100% { opacity: 0.3; transform: scaleY(0.6); }
  50%       { opacity: 1;   transform: scaleY(1);   }
}

/* ── IMPACT STRIP ─────────────────────────────────────────────────────── */
.impact-strip {
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  background: #fff;
  border-bottom: 1px solid #ede9e4;
  padding: 0 32px;
}

.impact-item {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 26px 32px;
  border-right: 1px solid #ede9e4;
}

.impact-item:last-child { border-right: none; }

.impact-item > .fas {
  font-size: 20px;
  color: #b73f2a;
  width: 44px;
  height: 44px;
  background: #fdf5f3;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.impact-text { display: flex; flex-direction: column; }

.impact-value {
  font-family: 'Cormorant Garamond', serif;
  font-size: 26px;
  font-weight: 600;
  color: #111;
  line-height: 1;
}

.impact-label {
  font-size: 11px;
  letter-spacing: 1px;
  color: #999;
  text-transform: uppercase;
  margin-top: 3px;
  font-weight: 500;
}

/* ── WHY SECTION ──────────────────────────────────────────────────────── */
.why-section {
  padding: 96px 48px;
  background: #f6f4f1;
}

.why-inner {
  max-width: 1100px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 72px;
  align-items: center;
}

.why-visual {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.why-quote-card {
  background: #fff;
  border-radius: 20px;
  padding: 36px;
  border: 1px solid #ede9e4;
  box-shadow: 0 4px 24px rgba(0,0,0,0.05);
  position: relative;
}

.quote-icon {
  font-size: 28px;
  color: #f2c4b8;
  margin-bottom: 16px;
  display: block;
}

.quote-text {
  font-family: 'Cormorant Garamond', serif;
  font-size: 20px;
  font-weight: 400;
  font-style: italic;
  color: #333;
  line-height: 1.7;
  margin: 0 0 24px;
}

.quote-author {
  display: flex;
  align-items: center;
  gap: 14px;
}

.author-avatar {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  background: linear-gradient(135deg, #b73f2a, #d4614a);
  color: #fff;
  font-family: 'Cormorant Garamond', serif;
  font-size: 16px;
  font-weight: 600;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.author-name {
  font-size: 14px;
  font-weight: 600;
  color: #111;
  margin: 0 0 2px;
}

.author-title {
  font-size: 12px;
  color: #999;
  margin: 0;
}

.why-accent-box {
  background: linear-gradient(135deg, #b73f2a, #d4614a);
  border-radius: 16px;
  padding: 28px 32px;
  color: #fff;
}

.accent-stat {
  font-family: 'Cormorant Garamond', serif;
  font-size: 56px;
  font-weight: 600;
  color: #fff;
  line-height: 1;
  margin: 0 0 10px;
}

.accent-desc {
  font-size: 14px;
  color: rgba(255,255,255,0.8);
  line-height: 1.6;
  margin: 0;
}

.section-eyebrow {
  font-size: 10px;
  letter-spacing: 3px;
  font-weight: 600;
  color: #b73f2a;
  text-transform: uppercase;
  margin: 0 0 10px;
}

.section-title {
  font-family: 'Cormorant Garamond', serif;
  font-size: clamp(30px, 3.5vw, 44px);
  font-weight: 600;
  color: #111;
  margin: 0 0 24px;
  line-height: 1.15;
}

.why-body {
  font-size: 15px;
  color: #555;
  line-height: 1.8;
  margin: 0 0 18px;
}

.why-pillars {
  display: flex;
  flex-direction: column;
  gap: 16px;
  margin-top: 28px;
}

.pillar {
  display: flex;
  align-items: flex-start;
  gap: 14px;
}

.pillar-icon {
  width: 38px;
  height: 38px;
  border-radius: 10px;
  background: #fdf5f3;
  border: 1px solid #f0d8d3;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #b73f2a;
  font-size: 14px;
  flex-shrink: 0;
  margin-top: 2px;
}

.pillar-title {
  font-size: 14px;
  font-weight: 600;
  color: #111;
  margin: 0 0 3px;
}

.pillar-desc {
  font-size: 13px;
  color: #888;
  margin: 0;
}

/* ── WAYS TO SUPPORT ──────────────────────────────────────────────────── */
.ways-section {
  padding: 88px 48px;
  background: #fff;
}

.section-head.centered {
  text-align: center;
  margin-bottom: 56px;
}

.section-sub {
  font-size: 15px;
  color: #888;
  line-height: 1.7;
  margin-top: 10px;
}

.ways-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
  max-width: 1200px;
  margin: 0 auto;
  align-items: start;
}

.way-card {
  background: #f9f8f6;
  border: 1px solid #ede9e4;
  border-radius: 20px;
  padding: 32px 24px;
  display: flex;
  flex-direction: column;
  gap: 14px;
  position: relative;
  transition: box-shadow 0.25s, transform 0.25s;
}

.way-card:hover {
  box-shadow: 0 14px 40px rgba(0,0,0,0.08);
  transform: translateY(-5px);
}

.way-card--featured {
  background: #111;
  border-color: #111;
  color: #fff;
}

.way-badge {
  position: absolute;
  top: -12px;
  left: 50%;
  transform: translateX(-50%);
  background: #b73f2a;
  color: #fff;
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 1.5px;
  text-transform: uppercase;
  padding: 5px 14px;
  border-radius: 20px;
  white-space: nowrap;
}

.way-icon-wrap {
  width: 52px;
  height: 52px;
  border-radius: 14px;
  background: linear-gradient(135deg, #b73f2a, #d4614a);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  font-size: 20px;
  box-shadow: 0 6px 18px rgba(183,63,42,0.3);
}

.way-title {
  font-family: 'Cormorant Garamond', serif;
  font-size: 22px;
  font-weight: 600;
  margin: 0;
  color: inherit;
}

.way-card--featured .way-title { color: #fff; }

.way-desc {
  font-size: 13.5px;
  line-height: 1.7;
  margin: 0;
  color: #777;
}

.way-card--featured .way-desc { color: rgba(255,255,255,0.6); }

.way-perks {
  list-style: none;
  padding: 0;
  margin: 4px 0 0;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.way-perks li {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  color: #555;
}

.way-card--featured .way-perks li { color: rgba(255,255,255,0.7); }

.way-perks li i {
  color: #b73f2a;
  font-size: 11px;
  flex-shrink: 0;
}

.way-card--featured .way-perks li i { color: #f2c4b8; }

.way-btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  font-weight: 600;
  color: #b73f2a;
  text-decoration: none;
  border-bottom: 1px solid #b73f2a;
  padding-bottom: 2px;
  align-self: flex-start;
  margin-top: auto;
  transition: gap 0.2s, color 0.2s;
}

.way-btn:hover { gap: 12px; }

.way-btn--solid {
  background: #b73f2a;
  color: #fff;
  border: none;
  padding: 12px 22px;
  border-radius: 30px;
  font-size: 13px;
  font-weight: 600;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  align-self: stretch;
  justify-content: center;
  transition: background 0.2s, transform 0.2s;
}

.way-btn--solid:hover { background: #9a3523; transform: translateY(-1px); }

/* ── TIERS ────────────────────────────────────────────────────────────── */
.tiers-section {
  padding: 88px 48px;
  background: #f6f4f1;
}

.tiers-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
  max-width: 960px;
  margin: 0 auto;
  align-items: start;
}

.tier-card {
  background: #fff;
  border: 1px solid #ede9e4;
  border-radius: 20px;
  padding: 36px 28px;
  position: relative;
  transition: box-shadow 0.25s, transform 0.25s;
}

.tier-card:hover {
  box-shadow: 0 12px 36px rgba(0,0,0,0.08);
  transform: translateY(-5px);
}

.tier-card--highlighted {
  background: #111;
  border-color: #111;
  color: #fff;
}

.tier-tag {
  position: absolute;
  top: -12px;
  left: 50%;
  transform: translateX(-50%);
  background: #b73f2a;
  color: #fff;
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 1.5px;
  text-transform: uppercase;
  padding: 5px 14px;
  border-radius: 20px;
  white-space: nowrap;
}

.tier-name {
  font-size: 10px;
  letter-spacing: 2.5px;
  font-weight: 700;
  text-transform: uppercase;
  color: #b73f2a;
  margin: 0 0 16px;
}

.tier-price {
  display: flex;
  align-items: baseline;
  gap: 4px;
  margin-bottom: 6px;
}

.tier-currency {
  font-size: 14px;
  font-weight: 500;
  color: #888;
}

.tier-card--highlighted .tier-currency { color: rgba(255,255,255,0.5); }

.tier-amount {
  font-family: 'Cormorant Garamond', serif;
  font-size: 48px;
  font-weight: 600;
  color: #111;
  line-height: 1;
}

.tier-card--highlighted .tier-amount { color: #fff; }

.tier-period {
  font-size: 14px;
  color: #aaa;
}

.tier-tagline {
  font-size: 13.5px;
  color: #888;
  margin: 0 0 24px;
  padding-bottom: 24px;
  border-bottom: 1px solid #f0f0f0;
}

.tier-card--highlighted .tier-tagline {
  color: rgba(255,255,255,0.5);
  border-color: rgba(255,255,255,0.1);
}

.tier-features {
  list-style: none;
  padding: 0;
  margin: 0 0 28px;
  display: flex;
  flex-direction: column;
  gap: 11px;
}

.tier-features li {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 13.5px;
  color: #444;
}

.tier-card--highlighted .tier-features li { color: rgba(255,255,255,0.75); }

.tier-features li.disabled { color: #ccc; }
.tier-card--highlighted .tier-features li.disabled { color: rgba(255,255,255,0.25); }

.tier-features li i { font-size: 11px; color: #b73f2a; flex-shrink: 0; }
.tier-features li.disabled i { color: #ddd; }

.tier-btn {
  display: block;
  text-align: center;
  padding: 13px;
  border-radius: 30px;
  font-size: 13.5px;
  font-weight: 600;
  text-decoration: none;
  border: 1.5px solid #b73f2a;
  color: #b73f2a;
  transition: all 0.2s;
}

.tier-btn:hover { background: #b73f2a; color: #fff; }

.tier-btn--solid {
  background: #b73f2a;
  color: #fff;
  border-color: #b73f2a;
}

.tier-btn--solid:hover { background: #9a3523; border-color: #9a3523; }

/* ── TESTIMONIALS ─────────────────────────────────────────────────────── */
.testimonials-section {
  padding: 88px 48px;
  background: #fff;
}

.testimonials-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
  max-width: 1100px;
  margin: 0 auto;
}

.testi-card {
  background: #f9f8f6;
  border: 1px solid #ede9e4;
  border-radius: 20px;
  padding: 32px;
  display: flex;
  flex-direction: column;
  gap: 16px;
  transition: box-shadow 0.25s, transform 0.25s;
}

.testi-card:hover {
  box-shadow: 0 12px 36px rgba(0,0,0,0.07);
  transform: translateY(-4px);
}

.testi-stars { display: flex; gap: 4px; }
.testi-stars i { color: #f2a524; font-size: 13px; }

.testi-text {
  font-family: 'Cormorant Garamond', serif;
  font-size: 18px;
  font-style: italic;
  color: #333;
  line-height: 1.7;
  margin: 0;
  flex-grow: 1;
}

.testi-author { display: flex; align-items: center; gap: 12px; }

.testi-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: linear-gradient(135deg, #b73f2a, #d4614a);
  color: #fff;
  font-family: 'Cormorant Garamond', serif;
  font-size: 17px;
  font-weight: 600;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.testi-name { font-size: 14px; font-weight: 600; color: #111; margin: 0 0 2px; }
.testi-role { font-size: 12px; color: #999; margin: 0; }

/* ── CONTACT ──────────────────────────────────────────────────────────── */
.contact-section {
  padding: 88px 48px;
  background: #f6f4f1;
}

.contact-inner {
  max-width: 1100px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: 1fr 1.4fr;
  gap: 64px;
  align-items: start;
}

.contact-body {
  font-size: 15px;
  color: #555;
  line-height: 1.8;
  margin: 0 0 36px;
}

.contact-channels {
  display: flex;
  flex-direction: column;
  gap: 18px;
  margin-bottom: 32px;
}

.channel { display: flex; align-items: center; gap: 16px; }

.channel-icon {
  width: 42px;
  height: 42px;
  border-radius: 11px;
  background: #fdf5f3;
  border: 1px solid #f0d8d3;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #b73f2a;
  font-size: 14px;
  flex-shrink: 0;
}

.channel-label {
  font-size: 11px;
  letter-spacing: 1.5px;
  text-transform: uppercase;
  color: #aaa;
  font-weight: 600;
  margin: 0 0 2px;
}

.channel-value {
  font-size: 14.5px;
  color: #222;
  font-weight: 500;
  text-decoration: none;
  transition: color 0.2s;
}

.channel-value:hover { color: #b73f2a; }

.contact-socials { display: flex; gap: 10px; }

.csocial {
  width: 38px;
  height: 38px;
  border-radius: 50%;
  border: 1.5px solid #ddd;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #888;
  font-size: 13px;
  text-decoration: none;
  transition: all 0.2s;
}

.csocial:hover { border-color: #b73f2a; color: #b73f2a; background: #fdf5f3; }

/* Form */
.form-card {
  background: #fff;
  border-radius: 24px;
  padding: 44px;
  border: 1px solid #ede9e4;
  box-shadow: 0 4px 30px rgba(0,0,0,0.06);
}

.form-title {
  font-family: 'Cormorant Garamond', serif;
  font-size: 28px;
  font-weight: 600;
  color: #111;
  margin: 0 0 4px;
}

.form-sub {
  font-size: 13px;
  color: #aaa;
  margin: 0 0 28px;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

.form-field {
  display: flex;
  flex-direction: column;
  gap: 6px;
  margin-bottom: 16px;
}

.form-field label {
  font-size: 11.5px;
  font-weight: 600;
  letter-spacing: 0.5px;
  color: #555;
  text-transform: uppercase;
}

.optional {
  font-weight: 400;
  color: #bbb;
  text-transform: none;
  letter-spacing: 0;
}

.form-field input,
.form-field textarea,
.form-field select {
  width: 100%;
  padding: 13px 16px;
  border: 1.5px solid #e8e4de;
  border-radius: 12px;
  font-family: 'DM Sans', sans-serif;
  font-size: 14px;
  color: #1c1c1c;
  background: #fafaf9;
  outline: none;
  transition: border-color 0.2s, box-shadow 0.2s;
  box-sizing: border-box;
  appearance: none;
}

.form-field input:focus,
.form-field textarea:focus,
.form-field select:focus {
  border-color: #b73f2a;
  box-shadow: 0 0 0 3px rgba(183,63,42,0.08);
  background: #fff;
}

.form-field textarea { resize: vertical; min-height: 110px; }

.custom-select-wrap { position: relative; }

.select-arrow {
  position: absolute;
  right: 16px;
  top: 50%;
  transform: translateY(-50%);
  color: #aaa;
  font-size: 11px;
  pointer-events: none;
}

.form-submit {
  width: 100%;
  padding: 15px;
  background: #b73f2a;
  color: #fff;
  border: none;
  border-radius: 12px;
  font-family: 'DM Sans', sans-serif;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s, transform 0.2s, box-shadow 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  margin-top: 6px;
}

.form-submit:hover:not(:disabled) {
  background: #9a3523;
  transform: translateY(-1px);
  box-shadow: 0 8px 24px rgba(183,63,42,0.3);
}

.form-submit:disabled { opacity: 0.75; cursor: default; }

.form-privacy {
  display: flex;
  align-items: center;
  gap: 7px;
  font-size: 12px;
  color: #bbb;
  margin: 12px 0 0;
  justify-content: center;
}

.form-privacy i { color: #d4c5c2; }

/* ── FAQ ──────────────────────────────────────────────────────────────── */
.faq-section {
  padding: 88px 48px;
  background: #fff;
}

.faq-list {
  max-width: 760px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 0;
}

.faq-item {
  border-bottom: 1px solid #ede9e4;
  cursor: pointer;
  padding: 22px 0;
  user-select: none;
}

.faq-q {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 20px;
  font-size: 16px;
  font-weight: 500;
  color: #111;
  transition: color 0.2s;
}

.faq-item.open .faq-q { color: #b73f2a; }

.faq-q i {
  font-size: 13px;
  color: #b73f2a;
  flex-shrink: 0;
  transition: transform 0.3s;
}

.faq-a {
  font-size: 14.5px;
  color: #666;
  line-height: 1.8;
  margin: 14px 0 0;
  padding-right: 32px;
}

/* FAQ slide transition */
.faq-slide-enter-active,
.faq-slide-leave-active { transition: opacity 0.25s ease, transform 0.25s ease; }
.faq-slide-enter-from,
.faq-slide-leave-to  { opacity: 0; transform: translateY(-6px); }

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

@media (max-width: 1100px) {
  .ways-grid { grid-template-columns: repeat(2, 1fr); }
}

@media (max-width: 900px) {
  .why-inner,
  .contact-inner { grid-template-columns: 1fr; gap: 40px; }
  .tiers-grid,
  .testimonials-grid { grid-template-columns: 1fr; max-width: 480px; margin: 0 auto; }
  .impact-strip { gap: 0; }
  .impact-item { padding: 20px 20px; border-right: none; border-bottom: 1px solid #ede9e4; width: 100%; }
  .footer-inner { grid-template-columns: 1fr 1fr; }
  .support-hero { margin: 0 12px; border-radius: 16px; }
  .form-row { grid-template-columns: 1fr; }
}

@media (max-width: 600px) {
  .ways-grid { grid-template-columns: 1fr; }
  .why-section, .ways-section, .tiers-section,
  .testimonials-section, .contact-section, .faq-section { padding: 56px 20px; }
  .form-card { padding: 28px 20px; }
  .support-hero { min-height: 100vh; }
  .hero-title { font-size: 44px; }
  .hero-cta-row { flex-direction: column; align-items: center; }
  .footer-inner { grid-template-columns: 1fr; gap: 32px; }
  .hide-sm { display: none; }
}
</style>