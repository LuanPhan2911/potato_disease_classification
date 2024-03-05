<script>
import { onMounted, reactive, ref } from "vue";
import SelectImage from "./components/SelectImage.vue";
import axios from "axios";
export default {
  components: { SelectImage },
  setup() {
    const image = ref(null);
    const isLoading = ref(false);
    const prediction = reactive({
      hasValue: false,
      error: false,
      label: "",
      confidence: "",
    });
    const getImage = (file) => {
      image.value = file;
    };
    const predictImage = async () => {
      try {
        if (image.value) {
          isLoading.value = true;
          const form = new FormData();
          form.append("file", image.value);
          let res = await axios.post("/api/predict", form);
          let data = res.data;
          if (data) {
            let { label, confidence } = data;
            prediction.label = label;
            prediction.confidence = confidence;
            prediction.hasValue = true;
            prediction.error = false;
          }
        }
      } catch (error) {
        prediction.error = true;
        prediction.hasValue = false;
      }
      isLoading.value = false;
    };
    onMounted(() => {
      document.title = "Predict Potato Disease";
    });
    return { prediction, isLoading, getImage, predictImage };
  },
};
</script>

<template>
  <div class="main">
    <div class="navbar">
      <div class="container-fluid">
        <div class="navbar-brand text-primary fw-bolder">
          Potato Disease Classification
        </div>
      </div>
    </div>
    <div class="row justify-content-center">
      <div class="col-lg-4 col-md-8">
        <div class="card bg-transparent shadow-lg">
          <div class="card-header bg-light">
            <div class="card-title text-primary fw-bold">
              Predict Potato Disease
            </div>
          </div>
          <div class="card-body">
            <select-image @get-image="getImage" @predict="predictImage" />
          </div>
          <div class="card-footer bg-light" v-if="prediction.hasValue">
            <div class="text-center text-primary" v-if="isLoading">
              Predicting...
            </div>
            <div class="row" v-else>
              <div class="col-lg-6 text-primary fw-bold">
                Class: {{ prediction.label }}
              </div>
              <div class="col-lg-6 text-primary fw-bolder">
                Confidence: {{ prediction.confidence }}%
              </div>
            </div>
          </div>
          <div class="card-footer bg-light" v-if="prediction.error">
            <div class="text-danger fw-bold text-center">Error from server</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<style scoped>
.main {
  background: url("assets/bg.jpg");
  min-height: 100vh;
  overflow: hidden;
}
</style>
