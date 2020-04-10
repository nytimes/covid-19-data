import { states } from "./data.js";
import sort from "./sort.js";

let dataParam = "cases";
let dataItems = Object.keys(states.states);
let sortParam = "name";
let sortOrder = "az";

function numberWithCommas(x) {
  return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

const ctx = document.getElementById("dataChart").getContext("2d");
const chart = new Chart(ctx, {
  // The type of chart we want to create
  type: "line",

  // The data for our dataset
  data: { datasets: [] },

  options: {
    legend: {
      display: false,
    },
    aspectRatio: 2,
    scales: {
      xAxes: [
        {
          type: "time",
          time: {
            tooltipFormat: "MMMM D, YYYY",
            unit: "day",
            displayFormats: { day: "MM/D" },
          },
        },
      ],
    },
  },
});

function button(id, color) {
  const str = id.replace(/\s+/g, "-").toLowerCase();
  return `<button value="${id}" id="select-${str}"class="selected-item js-clear-button"style="border:solid 3px ${color};">
  ${id}
  <span class="selected-item__icon" >
  <?xml version="1.0" encoding="utf-8"?>
  <svg
    version="1.1"
    id="Layer_1"
    xmlns="http://www.w3.org/2000/svg"
    xmlns:xlink="http://www.w3.org/1999/xlink"
    x="0px"
    y="0px"
    viewBox="0 0 10 10"
    style="enable-background: new 0 0 10 10;"
    xml:space="preserve"
    height="1em"
  >
    <style type="text/css">
      .st0 {
        fill: currentColor;
      }
    </style>
    <path
      class="st0"
      d="M5,0C2.3,0,0.1,2.3,0.1,5c0,2.7,2.2,4.9,4.9,4.9S9.9,7.7,9.9,5C9.9,2.3,7.7,0,5,0z M8.2,7.4L7.4,8.2L4.9,5.8
L2.5,8.2L1.7,7.4L4.1,5L1.7,2.6l0.8-0.8l2.4,2.4l2.4-2.4l0.8,0.8L5.8,5L8.2,7.4z"
    />
  </svg></span>
</button>`;
}

function selectionGenerate() {
  // const buttonsArr = [];
  // dataItems.map(i => {
  //   buttonsArr.push(button(i));
  // });

  // const selectedContainer = document.querySelector("#chartSelected");
  // selectedContainer.innerHTML = buttonsArr.join("");
  const clearButtons = document.querySelectorAll(".js-clear-button");

  for (const button of clearButtons) {
    button.addEventListener("click", dataClear);
  }
}

function dataGenerate(data) {
  const processedDataArr = data.data.map(d => {
    let dataItem = d[dataParam];
    if (dataParam === "casesPop" || dataParam === "deathsPop") {
      dataItem = d[dataParam].toFixed(4);
    }
    return {
      x: new Date(d.date),
      y: dataItem,
    };
  });
  return {
    label: data.name,
    data: processedDataArr,
    backgroundColor: "rgba(0, 0, 0, 0)",
    borderColor: "#" + Math.floor(Math.random() * 16777215).toString(16),
  };
}

function chartGenerate() {
  const sortedData = dataItems.sort();
  const buttonsArr = [];
  const chartData = sortedData.map(state => {
    const stats = states.states[state];
    const stateData = dataGenerate(stats);

    buttonsArr.push(button(state, stateData.borderColor));
    return stateData;
  });
  chart.data.datasets = chartData;
  const selectedContainer = document.querySelector("#chartSelected");
  selectedContainer.innerHTML = buttonsArr.join("");
  chart.update();
  selectionGenerate();
}

function dataSelectButtons() {
  const selectButtons = document.querySelectorAll(".js-data-select-button");

  for (const button of selectButtons) {
    button.addEventListener("click", dataTypeSet);
  }
}

function dataCards() {
  const statesArr = Object.values(states.states);
  const sortedStates = sort(statesArr, sortParam, sortOrder);
  let statesDisplay = "";
  sortedStates.map(state => {
    const firstCaseDate = moment(state.firstCase).format("MMMM D, YYYY");
    let firstDeathDate = "";
    if (state.firstDeath) {
      firstDeathDate = moment(state.firstDeath).format("MMMM D, YYYY");
    }

    statesDisplay += `
          <div class="data-card" id="${state.name}">
          <details class="data-card__contents" open>
            <summary class="data-card__header">
              <h1 class="data-card__data-title">${state.name}</h1>
            </summary>
            <div class="data-card__stats-container">
              <span class="data-card__stats">Total Cases:</span>
              <span class="data-card__stats data-card__stats--highlighted"
                >${numberWithCommas(state.cases)}</span
              >
            </div>
            <div class="data-card__stats-container">
              <span class="data-card__stats">Total Deaths:</span
              ><span class="data-card__stats data-card__stats--highlighted"
                >${numberWithCommas(state.deaths)}</span
              >
            </div>
            <div class="data-card__stats-container">
              <span class="data-card__stats">First Case:</span
              ><span class="data-card__stats data-card__stats--highlighted"
                >${firstCaseDate}
            </div>
            <div class="data-card__stats-container">
              <span class="data-card__stats">First Death:</span
              >${
                state.firstDeath
                  ? `
                  <span class="data-card__stats data-card__stats--highlighted">
                  ${firstDeathDate}</span>
                 `
                  : `
                  <span class="data-card__stats">
                    (none reported)
                  </span>
                `
              }
            </div>
            <div class="data-card__stats-container">
            <span class="data-card__stats">Population:</span
            ><span class="data-card__stats data-card__stats--highlighted"
              >${state.population > 0 ? state.population : "Not Available"}
          </div>
          <div class="data-card__stats-container">
          <span class="data-card__stats">% Pop Cases:</span
          ><span class="data-card__stats data-card__stats--highlighted"
            >${
              state.casesPop > 0
                ? state.casesPop.toFixed(4) + "%"
                : "Not Available"
            }
        </div>
        <div class="data-card__stats-container">
        <span class="data-card__stats">% Pop Deaths:</span
        ><span class="data-card__stats data-card__stats--highlighted"
          >${
            state.deathsPop > 0
              ? state.deathsPop.toFixed(4) + "%"
              : "Not Available"
          }
      </div>
          </details>
          <button class="data-card__select-button js-select-button" value="${
            state.name
          }">View on chart</button>
          </div>`;
  });
  const cardsContainer = document.querySelector("#cards-container");
  cardsContainer.innerHTML = statesDisplay;
  const cardsButtons = document.querySelectorAll(".js-select-button");

  for (const button of cardsButtons) {
    button.addEventListener("click", dataAdd);
  }
}

function sortSelectButtons() {
  const selectButtons = document.querySelectorAll(".js-sort-button");

  for (const button of selectButtons) {
    button.addEventListener("click", sortTypeSet);
  }
}

function sortTypeSet(event) {
  const id = event.target.value;
  if (sortParam !== id) {
    sortParam = id;
    const activeButton = document.querySelectorAll(".js-sort-button");
    for (const button of activeButton) {
      button.classList.remove("selected-item--selected");
    }

    const selectedButton = document.querySelector(`#${event.target.id}`);
    selectedButton.classList.add("selected-item--selected");
  } else {
    const sortContainer = document.querySelector(".card-sort");
    if (sortOrder === "az") {
      sortOrder = "za";
      sortContainer.classList.add("sort-order--reversed");
    } else {
      sortOrder = "az";
      sortContainer.classList.remove("sort-order--reversed");
    }
  }
  dataCards();
}

function dataAdd(event) {
  const id = event.target.value;
  if (id === "all") {
    const itemList = Object.keys(states.states);
    dataItems = itemList.sort();
    chartGenerate();
  } else if (!dataItems.includes(id)) {
    const stats = states.states[id];
    const dataSeries = dataGenerate(stats);
    const dataSets = [...chart.data.datasets];
    dataSets.push(dataSeries);
    chart.data.datasets = sort(dataSets, "label", "az");
    chart.update();
    const sortedItems = [...dataItems, id];
    dataItems = sortedItems.sort();
    chartGenerate();
    // const card = document.querySelector(`#${id}`);
    // card.classList.add("data-card--selected");
  }
}
function dataTypeSet(event) {
  const id = event.target.value;
  if (dataParam !== id) {
    dataParam = id;
    chartGenerate();
    const activeButton = document.querySelectorAll(".js-data-select-button");
    for (const button of activeButton) {
      button.classList.remove("selected-item--selected");
      button.disabled = false;
    }
    const cardsContainer = document.querySelector(`#${event.target.id}`);
    cardsContainer.classList.add("selected-item--selected");
    cardsContainer.disabled = true;
  }
}

function dataClear(event) {
  const id = event.target.value;
  if (dataItems.includes(id)) {
    const newArr = chart.data.datasets.filter(i => i.label !== id);
    const sortedArr = newArr.sort();
    chart.data.datasets = sortedArr;
    const filteredItems = dataItems.filter(i => i !== id);
    const sortedItems = filteredItems.sort();
    dataItems = sortedItems;
    chart.update();
    const str = id.replace(/\s+/g, "-").toLowerCase();
    const button = document.querySelector(`#select-${str}`);
    button.remove();
    // chartGenerate();
  } else if (id === "clear") {
    chart.data.datasets = [];
    chart.update();
    dataItems = [];
    chartGenerate();
  }
}

function setCollapse() {
  const width = window.innerWidth;
  const details = document.querySelectorAll(".data-card__contents");
  if (width <= 600) {
    for (const item of details) {
      item.open = false;
    }
  } else if (width > 600) {
    for (const item of details) {
      item.open = true;
    }
  }
}

window.onloadend = setCollapse;
window.onresize = setCollapse;

dataCards();
chartGenerate();
dataSelectButtons();
sortSelectButtons();
