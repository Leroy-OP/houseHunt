<template>
  <MDBRow :cols="['1', 'md-3']" class="g-4">
    <MDBCol>
      <MDBCard class="h-100">
        <MDBCardImg
          src="https://mdbootstrap.com/img/new/standard/city/044.webp"
          top
          alt="..."
        />
        <MDBCardBody>
          <MDBCardTitle>Card title</MDBCardTitle>
          <MDBCardText>
            This is a wider card with supporting text below as a natural lead-in to
            additional content. This content is a little bit longer.
          </MDBCardText>
        </MDBCardBody>
        <MDBCardFooter>
          <small class="text-muted">Last updated 3 mins ago</small>
        </MDBCardFooter>
      </MDBCard>
    </MDBCol>
    <MDBCol>
      <MDBCard class="h-100">
        <MDBCardImg
          src="https://mdbootstrap.com/img/new/standard/city/043.webp"
          top
          alt="..."
        />
        <MDBCardBody>
          <MDBCardTitle>Card title</MDBCardTitle>
          <MDBCardText>
            This card has supporting text below as a natural lead-in to additional
            content.
          </MDBCardText>
        </MDBCardBody>
        <MDBCardFooter>
          <small class="text-muted">Last updated 3 mins ago</small>
        </MDBCardFooter>
      </MDBCard>
    </MDBCol>
    <MDBCol>
      <MDBCard class="h-100">
        <MDBCardImg
          src="https://mdbootstrap.com/img/new/standard/city/042.webp"
          top
          alt="..."
        />
        <MDBCardBody>
          <MDBCardTitle>Card title</MDBCardTitle>
          <MDBCardText>
            This is a wider card with supporting text below as a natural lead-in to
            additional content. This card has even longer content than the first to show
            that equal height action.
          </MDBCardText>
        </MDBCardBody>
        <MDBCardFooter>
          <small class="text-muted">Last updated 3 mins ago</small>
        </MDBCardFooter>
      </MDBCard>
    </MDBCol>
  </MDBRow>
</template>
<script>
  import { MDBCol, MDBRow, MDBCardGroup, MDBCard, MDBCardBody, MDBCardTitle, MDBCardText, MDBCardImg, MDBCardFooter } from "mdb-vue-ui-kit";
  export default {
    components: {
      MDBCol,
      MDBRow,
      MDBCardGroup,
      MDBCard,
      MDBCardBody,
      MDBCardTitle,
      MDBCardText,
      MDBCardImg,
      MDBCardFooter
    }
  };
</script>
