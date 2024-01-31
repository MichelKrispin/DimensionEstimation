("use strict");

// Send a message to the server by clicking on the compute button
document.getElementById("generate-button").onclick = () => {
  // Open up a compute message
  const notification = UIkit.notification({
    message: "<div uk-spinner></div> &nbsp; Computing...",
    pos: "top-center",
    timeout: 0,
  });

  // Measure the time
  const startTime = performance.now();

  // Reset the plot
  document.getElementById("plot").innerHTML = "";

  // Get the values
  let dataFunction = document.getElementById("select-data-function").value;
  let n = document.getElementById("select-n").value;
  let m_n = document.getElementById("select-mn").value;
  let epsilon = document.getElementById("select-epsilon").value;
  let noise = document.getElementById("select-noise").value;

  // Fetch the graph
  fetch(
    "/plot?" +
      new URLSearchParams({
        data_function: dataFunction,
        n: n,
        m_n: m_n,
        epsilon: epsilon,
        noise: noise,
      })
  )
    .then(function (response) {
      return response.json();
    })
    .then(function (data) {
      // Close the notification
      notification.close();

      if ("error" in data) {
        // Display an error
        UIkit.notification({
          message: `<span style="margin-left: 35%;">ERROR</span><br/>${data["error"]}`,
          pos: "top-center",
          status: "danger",
          timeout: 5000,
        });
      } else {
        // Display taken time
        const endTime = performance.now();
        UIkit.notification({
          message: `Computation took ${endTime - startTime} ms`,
          pos: "top-center",
          timeout: 3000,
        });

        // Display the computed intrinsic dimension
        const node = document.getElementById("plot-result");
        const expression =
          "The approximated intrinsic dimension is &nbsp;` \\hat{d} = " +
          `${data["d_hat"].toFixed(3)}` +
          "`";
        node.innerHTML = expression;
        MathJax.typesetPromise([node]);

        // And plot the graph
        return Bokeh.embed.embed_item(data["plot"], "plot");
      }
    })
    .catch((error) => {
      notification.close();
      alert(error);
    });
};
