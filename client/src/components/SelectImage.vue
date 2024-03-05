<script>
import { computed, ref } from "vue";
import imgDefault from "@/assets/default.png";
export default {
  emits: ["getImage", "predict"],
  setup(props, { emit }) {
    const imgElement = ref(null);
    const previewUrl = ref(null);
    const imageUrl = computed(() => imgDefault);
    const hasImage = computed(() => !!previewUrl.value);
    const previewImage = (event) => {
      let file = event?.target?.files[0];
      emit("getImage", file);
      if (previewUrl.value) {
        URL.revokeObjectURL(previewUrl.value);
      }
      previewUrl.value = URL.createObjectURL(file);
      imgElement.value.src = previewUrl.value;
    };
    const predictImage = () => emit("predict");
    return {
      imageUrl,
      previewUrl,
      imgElement,
      hasImage,
      previewImage,
      predictImage,
    };
  },
};
</script>
<template>
  <div class="mb-3">
    <label
      for="avatar"
      class="d-flex justify-content-center mb-3 cursor-pointer"
    >
      <img :src="imageUrl" class="img" ref="imgElement" />
    </label>
    <div class="fst-italic fw-bold text-center" v-if="!hasImage">
      Click to upload image
    </div>
    <div v-else class="d-flex justify-content-center">
      <button class="btn btn-primary" @click="predictImage">Predict</button>
    </div>
    <input
      class="form-control"
      name="avatar"
      type="file"
      id="avatar"
      accept="image/*"
      hidden
      @change="previewImage"
    />
  </div>
</template>
<style scoped>
.img {
  width: 256px;
  height: 300px;
}
</style>
