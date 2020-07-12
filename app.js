"use strict";

window.addEventListener("load", async (e) => {
  if ("serviceWorker" in navigator) {
    try {
      navigator.serviceWorker.register("sw.js");
      console.log("SW registered");
    } catch (error) {
      console.log("SW registration failed");
    }
  }
});

let today = new Date();
let formatDate = today.toDateString();
let selectedElement = document.getElementById("date");
selectedElement.innerHTML = formatDate;
