<template>
  <div class="page-container">
    <div class="hero-container">
      <!-- Background Image -->
      <img src="/hero.jpeg" class="hero-img" />

      <!-- Overlay -->
      <div class="hero-overlay">
        <h1 class="hero-title">Find <span>your place</span></h1>
        <p class="hero-subtitle">
          Find comfortable, reliable, and affordable homes tailored to your needs.
        </p>

        <!-- Search Bar -->
        <div class="search-bar">
          <div class="search-item">
            <label>Location</label>
            <input type="text" v-model="location" placeholder="Enter location" class="form-control" />
          </div>
          <div class="search-item">
            <label>Type</label>
            <input type="text" v-model="type" placeholder="Enter type" class="form-control" />
            <div v-if="filteredTypeSuggestions.length > 0" class="dropdown-menu show">
              <a v-for="suggestion in filteredTypeSuggestions" :key="suggestion" class="dropdown-item" @click="type = suggestion">{{ suggestion }}</a>
            </div>
          </div>
          <div class="search-item">
            <label>Category</label>
            <input type="text" v-model="category" placeholder="Enter category" class="form-control" />
            <div v-if="filteredCategorySuggestions.length > 0" class="dropdown-menu show">
              <a v-for="suggestion in filteredCategorySuggestions" :key="suggestion" class="dropdown-item" @click="category = suggestion">{{ suggestion }}</a>
            </div>
          </div>
          <button class="search-btn" @click="search">
            <i class="fas fa-search"></i>
          </button>
        </div>
      </div>
    </div>
    
    <!-- Main Content Area (scrollable) -->
<div class="content-area">
    <div class="discover-page">
        <h1 class="text-left mt-4" style="color: black; font-weight: 300px;">Discover</h1>
      <router-link to="/properties" class="see-all-link text-right">See all</router-link>

     <MDBRow :cols="['1', 'md-3']" class="g-4">
      <MDBCol v-for="(card, index) in cards" :key="card.title">
        <MDBCard class="h-100 hover-zoom card-relative">
          <div class="status-overlay">
            <span class="status">{{ card.status }}</span>
          </div>
          <div class="save-overlay">
            <button class="save-btn" @click="toggleSave(card)">
              <i :class="savedCards.includes(card) ? 'fas fa-heart text-danger' : 'far fa-heart'"></i>
            </button>
          </div>
          <div v-if="index === 2" class="arrow-overlay">
            <button class="arrow-btn" @click="goToProperties">
              <i class="fas fa-arrow-right"></i>
            </button>
          </div>
          <MDBCardImg :src="card.img" top alt="..."/>
          <MDBCardBody>
            <MDBCardTitle>{{ card.title }}</MDBCardTitle>
            <MDBCardText>
              {{ card.text }}
            </MDBCardText>
          </MDBCardBody>
        </MDBCard>
      </MDBCol>
    </MDBRow>
    </div>
  </div>
</div>
<div class="content-area">
    <div class="discover-page">
        <h1 class="text-left mt-4" style="color: black; font-weight: 300px;">Reliable Agencies</h1>
      <router-link to="/properties" class="see-all-link text-right">See all</router-link>

     <MDBRow :cols="['1', 'md-3']" class="g-4">
      <MDBCol v-for="(card, index) in cards" :key="card.title">
        <MDBCard class="h-100 hover-zoom card-relative">
          <div class="status-overlay">
            <span class="status">{{ card.status }}</span>
          </div>
          <div class="save-overlay">
            <button class="save-btn" @click="toggleSave(card)">
              <i :class="savedCards.includes(card) ? 'fas fa-heart text-danger' : 'far fa-heart'"></i>
            </button>
          </div>
          <div v-if="index === 2" class="arrow-overlay">
            <button class="arrow-btn" @click="goToProperties">
              <i class="fas fa-arrow-right"></i>
            </button>
          </div>
          <MDBCardImg :src="card.img" top alt="..."/>
          <MDBCardBody>
            <MDBCardTitle>{{ card.title }}</MDBCardTitle>
            <MDBCardText>
              {{ card.text }}
            </MDBCardText>
          </MDBCardBody>
        </MDBCard>
      </MDBCol>
    </MDBRow>
    </div>
  </div>
 <!-- Footer -->
  <MDBFooter :text="['center', 'lg-start', 'muted']">
    <!-- Section: Social media -->
    <section class="
        d-flex
        justify-content-center justify-content-lg-between
        p-4
        border-bottom
      ">
      <!-- Left -->
      <div class="me-5 d-none d-lg-block">
        <span>Get connected with us on social networks:</span>
      </div>
      <!-- Left -->
      <!-- Right -->
      <div>
        <a href="" class="me-4 text-reset">
          <MDBIcon iconStyle="fab" icon="facebook-f"></MDBIcon>
        </a>
        <a href="" class="me-4 text-reset">
          <MDBIcon iconStyle="fab" icon="twitter"></MDBIcon>
        </a>
        <a href="" class="me-4 text-reset">
          <MDBIcon iconStyle="fab" icon="google"></MDBIcon>
        </a>
        <a href="" class="me-4 text-reset">
          <MDBIcon iconStyle="fab" icon="instagram"></MDBIcon>
        </a>
        <a href="" class="me-4 text-reset">
          <MDBIcon iconStyle="fab" icon="linkedin"></MDBIcon>
        </a>
        <a href="" class="me-4 text-reset">
          <MDBIcon iconStyle="fab" icon="github"></MDBIcon>
        </a>
      </div>
      <!-- Right -->
    </section>
    <!-- Section: Social media -->
    <!-- Section: Links  -->
    <section class="">
      <MDBContainer class="text-center text-md-start mt-5">
        <!-- Grid row -->
        <MDBRow class="mt-3">
          <!-- Grid column -->
          <MDBCol md="3" lg="4" xl="3" class="mx-auto mb-4">
            <!-- Content -->
            <h6 class="text-uppercase fw-bold mb-4">
              <i class="fas fa-gem me-3"></i>Hunter Street
            </h6>
            <p>
              Here you can use rows and columns to organize your footer
              content. Lorem ipsum dolor sit amet, consectetur
              adipisicing elit.
            </p>
          </MDBCol>
          <!-- Grid column -->
          <!-- Grid column -->
          <!-- Grid column -->
          <!-- Grid column -->
          <MDBCol md="3" lg="2" xl="2" class="mx-auto mb-4">
            <!-- Links -->
            <h6 class="text-uppercase fw-bold mb-4">Useful links</h6>
            <p>
              <a href="#!" class="text-reset">Pricing</a>
            </p>
            <p>
              <a href="#!" class="text-reset">Settings</a>
            </p>
            <p>
              <a href="#!" class="text-reset">Orders</a>
            </p>
            <p>
              <a href="#!" class="text-reset">Help</a>
            </p>
          </MDBCol>
          <!-- Grid column -->
          <!-- Grid column -->
          <MDBCol md="4" lg="3" xl="3" class="mx-auto mb-md-0 mb-4">
            <!-- Links -->
            <h6 class="text-uppercase fw-bold mb-4">Contact</h6>
            <p>
              <i class="fas fa-home me-3"></i> New York, NY 10012, US
            </p>
            <p>
              <i class="fas fa-envelope me-3"></i>
              info@example.com
            </p>
            <p>
              <MDBIcon icon="phone" class="me-3" /> + 01 234 567 88
            </p>
            <p>
              <MDBIcon icon="print" class="me-3" /> + 01 234 567 89
            </p>
          </MDBCol>
          <!-- Grid column -->
        </MDBRow>
        <!-- Grid row -->
      </MDBContainer>
    </section>
    <!-- Section: Links  -->
    <!-- Copyright -->
    <div class="text-center p-4" style="background-color: rgba(0, 0, 0, 0.05)">
      © 2021 Copyright:
      <a class="text-reset fw-bold" href="https://mdbootstrap.com/">MDBootstrap.com</a>
    </div>
    <!-- Copyright -->
  </MDBFooter>
  <!-- Footer -->
</template>

<script>
  import { MDBCard, MDBCardBody, MDBCardTitle, MDBCardText, MDBCardImg, MDBInput, MDBCardGroup, MDBCol, MDBRow, MDBFooter, MDBIcon, MDBContainer } from "mdb-vue-ui-kit";
  import { ref, computed } from "vue";
  import { useRouter } from "vue-router";
  export default {
    components: {
      MDBCard,
      MDBCardBody,
      MDBCardTitle,
      MDBCardText,
      MDBCardImg,
      MDBInput,
      MDBCardGroup,
      MDBCol,
      MDBRow,
      MDBFooter,
      MDBContainer,
      MDBIcon
    },
    setup() {
      const router = useRouter();
      const location = ref('');
      const type = ref('');
      const category = ref('');
      const typeSuggestions = ['Bedsitters', 'Single Room', 'Studio Apartment'];
      const categorySuggestions = ['Hostels', 'Apartments Outside'];
      const filteredTypeSuggestions = computed(() => {
        if (!type.value) return [];
        return typeSuggestions.filter(s => s.toLowerCase().includes(type.value.toLowerCase()));
      });
      const filteredCategorySuggestions = computed(() => {
        if (!category.value) return [];
        return categorySuggestions.filter(s => s.toLowerCase().includes(category.value.toLowerCase()));
      });
      const cards = ref([
        {
          title: 'Card title 1',
          img: 'https://mdbootstrap.com/img/new/standard/city/041.webp',
          text: 'This is a longer card with supporting text below as a natural lead-in to additional content. This content is a little bit longer.',
          status: 'Available'
        },
        {
          title: 'Card title 2',
          img: 'https://mdbootstrap.com/img/new/standard/city/042.webp',
          text: 'This is a longer card with supporting text below as a natural lead-in to additional content. This content is a little bit longer.',
          status: 'Available'
        },
        {
          title: 'Card title 3',
          img: 'https://mdbootstrap.com/img/new/standard/city/043.webp',
          text: 'This is a longer card with supporting text below as a natural lead-in to additional content.',
          status: 'Available'
        }
      ]);
      const savedCards = ref([]);
      const toggleSave = (card) => {
        const index = savedCards.value.indexOf(card);
        if (index > -1) {
          savedCards.value.splice(index, 1);
        } else {
          savedCards.value.push(card);
        }
      };
      const goToProperties = () => {
        router.push('/properties');
      };
      const search = () => {
        console.log('Searching:', { location: location.value, type: type.value, category: category.value });
        // Add search logic here
      };
      return {
        location,
        type,
        category,
        filteredTypeSuggestions,
        filteredCategorySuggestions,
        cards,
        savedCards,
        toggleSave,
        goToProperties,
        search
      };
    }
  };
</script>
<style scoped>
.page-container {
  width: 100%;
  min-height: 100vh;
  overflow-y: auto;
  background: #f5f5f5;
}
.content-area{
    width: 100%;
    background: #f5f5f5;
    min-height: 100vh;
    overflow: auto;
}
.discover-page {
    position: relative;
    overflow: hidden;
    margin: 20px 24px;

}
.hero-container {
  position: relative;
  height: 520px;
  border-radius: 25px;
  overflow: hidden;
  margin: 20px 24px;
}

.hero-img {
  width: 100%;
  height: 100%;
  object-fit: cover;          /* ✅ Clean crop */
}

.hero-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.35); /* subtle dark overlay */
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  color: #fff;
  text-align: center;
  padding: 20px;
}

.hero-title {
  font-size: 70px;
  font-weight: 600;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.hero-title span {
  font-style: italic;
  font-weight: 400;
}

.hero-subtitle {
  margin-top: 10px;
  max-width: 600px;
  font-size: 16px;
  opacity: 0.9;
}

/* SEARCH BAR */
.search-bar {
  margin-top: 30px;
  background: #fff;
  border-radius: 20px;
  padding: 10px;
  display: flex;
  align-items: center;
  gap: 10px;
  width: 80%;
  max-width: 900px;
}

.search-item {
  flex: 1;
  text-align: left;
  padding: 10px;
  position: relative;
}

.search-item label {
  font-size: 12px;
  color: gray;
  display: block;
  margin-bottom: 5px;
}

.search-item input {
  width: 100%;
  border: none;
  outline: none;
  font-weight: 500;
  color: black;
}

.search-item .dropdown-menu {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  background: #fff;
  border: 1px solid #ddd;
  border-radius: 5px;
  z-index: 10;
  max-height: 150px;
  overflow-y: auto;
}

.search-item .dropdown-item {
  padding: 8px 10px;
  color: #333;
  text-decoration: none;
  display: block;
  cursor: pointer;
}

.search-item .dropdown-item:hover {
  background: #f8f9fa;
}

.search-btn {
  background: rgb(183, 63, 42);
  color: white;
  border: none;
  border-radius: 30%;
  width: 50px;
  height: 50px;
  cursor: pointer;
}

.content-area {
  width: 100%;
  background: #f5f5f5;
  min-height: 500px;
}

.card-relative {
  position: relative;
}

.status-overlay {
  position: absolute;
  top: 10px;
  left: 10px;
  background: rgba(255, 255, 255, 0.9);
  border-radius: 20px;
  padding: 5px 10px;
  z-index: 1;
}

.save-overlay {
  position: absolute;
  top: 10px;
  right: 10px;
  background: rgba(255, 255, 255, 0.9);
  border-radius: 20px;
  padding: 5px;
  z-index: 1;
}

.arrow-overlay {
  position: absolute;
  top: 50px;
  right: 10px;
  background: rgba(255, 255, 255, 0.9);
  border-radius: 20px;
  padding: 5px;
  z-index: 1;
  margin-top: 150px;
}

.status {
  font-size: 12px;
  color: #333;
  font-weight: 500;
}

.save-btn {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 16px;
}

.arrow-btn {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 16px;
  color: #333;
}

.text-danger {
  color: #dc3545;
}
.see-all-link {
  display: block;           
  text-align: right;       
  color: blue;
  font-weight: 300;        
  text-decoration: underline;
  margin-bottom: 10px;
}
.see-all-link:hover {
  color: darkblue;
  text-decoration: none;
}
</style>