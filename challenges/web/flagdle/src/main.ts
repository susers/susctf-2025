//! IF ANYTHING IN THIS FILE IS CHANGED MAKE SURE setVersion.js HAS ALSO BEEN UPDATED
import App from "./App.svelte";

const app = new App({
  target: document.body,
  props: {
    version: "114.5.14",
  },
});

export default app;