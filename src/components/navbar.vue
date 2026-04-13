<template>
  <MDBNavbar
  container
  expand="lg"
  bg="body-tertiary"
  class="d-flex justify-content-between"
  >
    <MDBNavbarBrand>
      <MDBIcon icon="mdb" iconStyle="fab" size="2x" />
    </MDBNavbarBrand>
    <MDBNavbarToggler
      target="#navbarColor01"
      @click="collapse7 = !collapse7"
    ></MDBNavbarToggler>
    <MDBCollapse id="navbarColor01" v-model="collapse7">
      <MDBNavbarNav class="mb-2 mb-lg-0">
        <router-link to="/" class="nav-link">
          <MDBNavbarItem>Home</MDBNavbarItem>
        </router-link>
        <router-link to="/about" class="nav-link">
          <MDBNavbarItem>About Us</MDBNavbarItem>
        </router-link>
        <router-link to="/support" class="nav-link">
          <MDBNavbarItem>Support</MDBNavbarItem>
        </router-link>
      </MDBNavbarNav>
    </MDBCollapse>

    <MDBNavbarNav class="mb-2 mb-lg-0 d-flex flex-row align-items-center ms-auto">
      <MDBNavbarItem
        to="#"
        class="me-3 me-lg-0"
      >
        <MDBIcon icon="bell" />
        <MDBBadge notification color="danger" pill>1</MDBBadge>
      </MDBNavbarItem>
      
      <MDBDropdown class="nav-item me-3" v-model="dropdown6">
        <MDBDropdownToggle tag="a" class="nav-link" @click="dropdown6 = !dropdown6"
          ><img
            src="https://mdbootstrap.com/img/Photos/Avatars/img (31).webp"
            class="rounded-circle"
            height="22"
            alt=""
            loading="lazy"
          />
        </MDBDropdownToggle>
        <MDBDropdownMenu>
          <MDBDropdownItem href="#">My profile</MDBDropdownItem>
          <MDBDropdownItem href="#">Settings</MDBDropdownItem>
          <MDBDropdownItem href="#">Logout</MDBDropdownItem>
        </MDBDropdownMenu>
      </MDBDropdown>
      <MDBNavbarItem class="me-3 me-lg-0">
        <button type="button" class="drawer-icon-btn" @click="drawerOpen = true" aria-label="Open drawer">
          <MDBIcon icon="bars" />
        </button>
      </MDBNavbarItem>
    </MDBNavbarNav>
    <div :class="['drawer-backdrop', { open: drawerOpen }]" @click="drawerOpen = false"></div>
    <aside :class="['right-drawer', { open: drawerOpen }]">
      <div class="drawer-header">
        <h6>Quick drawer</h6>
        <button type="button" class="drawer-close" @click="drawerOpen = false">×</button>
      </div>
      <div class="drawer-body">
        <p>Right-side quick actions and links.</p>
        <a href="#">New message</a>
        <a href="#">Notifications</a>
        <a href="#">Saved items</a>
        <a href="#">Account settings</a>
      </div>
    </aside>
  </MDBNavbar>
</template>

<script>
  import {
    MDBNavbar,
    MDBNavbarItem,
    MDBNavbarBrand,
    MDBNavbarNav,
    MDBNavbarToggler,
    MDBBadge,
    MDBIcon,
    MDBCollapse,
    MDBDropdown,
    MDBDropdownToggle,
    MDBDropdownMenu,
    MDBDropdownItem
  } from 'mdb-vue-ui-kit';
  import { ref } from "vue";

  export default {
    components: {
      MDBNavbar,
      MDBNavbarItem,
      MDBNavbarBrand,
      MDBNavbarNav,
      MDBNavbarToggler,
      MDBBadge,
      MDBIcon,
      MDBCollapse,
      MDBDropdown,
      MDBDropdownToggle,
      MDBDropdownMenu,
      MDBDropdownItem
    },
    setup() {
      const collapse7 = ref(false);
      const dropdown6 = ref(false);
      const drawerOpen = ref(false);

      return {
        collapse7,
        dropdown6,
        drawerOpen
      }
    }
  };
</script>

<style scoped>
.drawer-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.35);
  opacity: 0;
  pointer-events: none;
  transition: opacity 0.25s ease;
  z-index: 1040;
}
.drawer-backdrop.open {
  opacity: 1;
  pointer-events: auto;
}
.right-drawer {
  position: fixed;
  top: 0;
  right: 0;
  width: 280px;
  height: 100%;
  background: #fff;
  box-shadow: -10px 0 30px rgba(0, 0, 0, 0.15);
  transform: translateX(100%);
  transition: transform 0.25s ease;
  z-index: 1050;
  display: flex;
  flex-direction: column;
  padding: 1rem;
}
.right-drawer.open {
  transform: translateX(0);
}
.drawer-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}
.drawer-close {
  border: none;
  background: transparent;
  font-size: 1.5rem;
  line-height: 1;
  cursor: pointer;
}
.drawer-body {
  flex: 1;
  overflow-y: auto;
}
.drawer-body a {
  display: block;
  padding: 0.5rem 0;
  color: #212529;
  text-decoration: none;
}
.drawer-body a:hover {
  color: #0d6efd;
}
.drawer-icon-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  border: 1px solid rgba(13, 110, 253, 0.25);
  border-radius: 50%;
  background: rgba(13, 110, 253, 0.08);
  color: #0d6efd;
  cursor: pointer;
  transition: background 0.2s ease, transform 0.2s ease, border-color 0.2s ease;
}
.drawer-icon-btn:hover {
  background: rgba(13, 110, 253, 0.18);
  border-color: rgba(13, 110, 253, 0.45);
  transform: translateY(-1px);
}
.drawer-icon-btn :global(svg) {
  width: 18px;
  height: 18px;
}
.nav-link::after{
    content: '';
    width: 0%;
    height: 2px;
    background-color: rgb(183, 63, 42);
    display: block;
    margin: auto;
    transition: 0.7s;
}
.nav-link:hover::after{
    width: 100%;
}
</style>