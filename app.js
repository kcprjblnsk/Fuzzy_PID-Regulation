document.addEventListener("DOMContentLoaded", (event) => {
  let firstLoad = true;
  let inputForms = document.forms["parametry"].getElementsByTagName("input");
  for (let i = 0; i < inputForms.length; i++) {
    inputForms[i].addEventListener("keypress", function (event) {
      if (event.key === "Enter") {
        event.preventDefault();
        document.getElementById("submitForm").click();
      }
    });
  }

  document.querySelectorAll(".dropdown-content a").forEach((element) => {
    element.addEventListener("click", (event) => {
      event.preventDefault();
      localStorage.setItem("selectedRegulator", element.textContent);
      fetchData();
    });
  });

  document.querySelector("form").addEventListener("submit", (event) => {
    event.preventDefault();
    document.getElementById("regulator").value =
      localStorage.getItem("selectedRegulator") || "PID";

    let formData = new FormData(document.querySelector("form"));

    $.ajax({
      type: "POST",
      url: "",
      data: formData,
      processData: false,
      contentType: false,
      success: function (response) {
        fetchData();
      },
      error: function (jqXHR, textStatus, errorThrown) {
        console.error(textStatus, errorThrown);
      },
    });
  });

  async function fetchData() {
    const plik =
      localStorage.getItem("selectedRegulator") == "Fuzzy Logic"
        ? "./fuzzy.json"
        : "./pid.json";
    const tester = document.getElementById("tester");
    const output = document.getElementById("output");
    const zadana = document.getElementById("pozycja");
    const kp = document.getElementById("kp");
    const ti = document.getElementById("ti");
    const td = document.getElementById("td");
    if (firstLoad) {
      output.textContent = "";
      zadana.value = "";
      kp.value = "";
      ti.value = "";
      td.value = "";
      tester.textContent = "";
      zadana.style.display = "";
      kp.style.display = "";
      ti.style.display = "";
      td.style.display = "";
      firstLoad = false;
    } else if (localStorage.getItem("selectedRegulator") == "Fuzzy Logic") {
      zadana.style.display = "";
      kp.style.display = "none";
      ti.style.display = "none";
      td.style.display = "none";
    } else {
      zadana.style.display = "";
      kp.style.display = "";
      ti.style.display = "";
      td.style.display = "";
    }
    document.getElementById("regulatorInfo").textContent =
      localStorage.getItem("selectedRegulator") || "PID";
    try {
      const response = await fetch(plik);
      const data = await response.text();
      const obj = JSON.parse(data);
      console.log(obj);

      let traces = [];

      for (let i = 0; i < obj.length; i++) {
        if (i == obj.length - 1) {
          if (obj[i].hasOwnProperty("zadana")) {
            zadana.value = parseFloat(obj[i].zadana);
          } else {
            zadana.style.display = "none";
          }
          if (obj[i].hasOwnProperty("kp")) {
            kp.value = parseFloat(obj[i].kp);
          } else {
            kp.style.display = "none";
          }
          if (obj[i].hasOwnProperty("ti")) {
            ti.value = parseFloat(obj[i].ti);
          } else {
            ti.style.display = "none";
          }
          if (obj[i].hasOwnProperty("td")) {
            td.value = parseFloat(obj[i].td);
          } else {
            td.style.display = "none";
          }
        }
        traces.push({
          type: "scatter",
          mode: "lines",
          name: i == 0 ? "Symulacja poprzednia" : "Symulacja bieżąca",
          x: obj[i].time,
          y: obj[i].distance,
          line: { color: i == 0 ? "gray" : "blue" },
        });
      }

      const layout = {
        title: "<b> Przebieg lewitacji kulki </b>",
        xaxis: {
          title: "Czas [s]",
          titlefont: {
            size: 18,
            color: "black",
          },
        },
        yaxis: {
          title: "Pozycja kulki [mm]",
          titlefont: {
            size: 18,
            color: "black",
          },
        },
        annotations: [
          {
            x: obj[obj.length - 1].time[obj[obj.length - 1].time.length - 1],
            y: obj[obj.length - 1].distance[
              obj[obj.length - 1].distance.length - 1
            ],
            xref: "x",
            yref: "y",
            text: `Końcowa pozycja = ${
              Math.floor(
                obj[obj.length - 1].distance[
                  obj[obj.length - 1].distance.length - 1
                ] * 100
              ) / 100
            }`,
            showarrow: true,
            arrowhead: 7,
            ax: 0,
            ay: -40,
          },
        ],
      };

      Plotly.newPlot(tester, traces, layout);
    } catch (error) {
      console.error(error);
    }
  }
  fetchData();
});
