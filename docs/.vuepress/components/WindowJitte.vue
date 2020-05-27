<template>
  <div class="window-jitte" :class="{ shown }">{{ nickname }} 给你发送了一个窗口抖动。</div>
</template>

<script>
export default {
  props: {
    nickname: String
  },

  data: () => ({
    shown: false,
    active: false,
    moving: false
  }),

  watch: {
    active(value) {
      if (!value) return (this.shown = false);
      const prev =
        this.$el.previousElementSibling &&
        this.$el.previousElementSibling.__vue__;
      if (prev && (prev.moving || !prev.shown)) {
        prev.$once("appear", this.appear);
      } else {
        this.appear();
      }
    }
  },

  mounted() {
    this.handleScroll();
    addEventListener("scroll", this.handleScroll);
    addEventListener("resize", this.handleScroll);
  },

  beforeDestroy() {
    removeEventListener("scroll", this.handleScroll);
    removeEventListener("resize", this.handleScroll);
  },

  methods: {
    appear() {
      this.shown = true;
      this.moving = true;
      setTimeout(() => {
        this.moving = false;
        this.$emit("appear");
      }, 100);
    },
    handleScroll() {
      const rect = this.$el.getBoundingClientRect();
      if (rect.top < innerHeight) this.active = true;
    }
  }
};
</script>

<style lang="stylus">
.window-jitte {
  position: relative;
  opacity: 0;
  transform: translateX(-20%);
  transition: transform 0.3s ease-out, opacity 0.3s ease;
  user-select: none;
  font-size: 14px;
  border: 2px;
  background: #e1e2e3;
  border-radius: 6px;
  color: #777777;
  width: fit-content;
  margin: auto;
  padding: 2px 20px;

  &.shown {
    opacity: 1;
    transform: translateX(0);
  }
}
</style>
