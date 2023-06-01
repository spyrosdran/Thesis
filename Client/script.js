function capitalizeFirstLetter(string) {
    return string.charAt(0).toUpperCase() + string.slice(1);
  }

  function getSentimentClass(sentiment) {
    if (sentiment === "positive") {
      return "positive";
    } else if (sentiment === "negative") {
      return "negative";
    } else {
      return "neutral";
    }
  }

function createTableRow(word, column1Text, column2Text, column1Class, column2Class) {
    var row = document.createElement("tr");
    var column1 = document.createElement("td");
    var column2 = document.createElement("td");
    column1.textContent = column1Text;
    column2.textContent = column2Text;
    column1.className = column1Class;
    column2.className = column2Class;
    row.innerHTML = `<td>${word}</td>`;
    row.appendChild(column1);
    row.appendChild(column2);
    return row;
}

function sendRequest() {


    var inputData = document.getElementById("text").value;

    fetch("http://127.0.0.1:5000/evaluate?text=" + inputData)
      .then(response => response.json())
      .then(data => {

        var meanSentiment = document.getElementById("mean-sentiment");
        var meanSentimentText = capitalizeFirstLetter(data[0].sentiment);
        meanSentiment.textContent = "Mean Sentiment: " + meanSentimentText;
        meanSentiment.className = getSentimentClass(data[0].sentiment);

        var meanTable = document.getElementById("mean-table");
        meanTable.innerHTML = "";

        for (var i = 0; i < data[0].words.length; i++) {
          var word = data[0].words[i];
          var positivePercentage = (data[0].values[i][0] * 100).toFixed(2);
          var negativePercentage = (data[0].values[i][1] * 100).toFixed(2);

          var row = createTableRow(word, positivePercentage + "%", negativePercentage + "%", "negative", "positive");

          meanTable.appendChild(row);
        }

        var lastRow = createTableRow("Mean", data[0].mean[0].toFixed(2), data[0].mean[1].toFixed(2), "black", "black");

        meanTable.appendChild(lastRow);

        var countSentiment = document.getElementById("count-sentiment");
        var countSentimentText = capitalizeFirstLetter(data[1].sentiment);
        countSentiment.textContent = "Count Sentiment: " + countSentimentText;
        countSentiment.className = getSentimentClass(data[1].sentiment);

        var countTable = document.getElementById("count-table");
        countTable.innerHTML = "";

        for (var i = 0; i < data[1].words.length; i++) {
          var word = data[1].words[i];
          var label = data[1].labels[i];
          var column1Text = label === "negative" ? label : "";
          var column2Text = label === "positive" ? label : "";
          var column1Class = label === "negative" ? "negative" : "";
          var column2Class = label === "positive" ? "positive" : "";

          var row = createTableRow(word, column1Text, column2Text, column1Class, column2Class);

          countTable.appendChild(row);
        }

        var lastRow = createTableRow("Count", data[1].negatives, data[1].positives, "negative", "positive");

        countTable.appendChild(lastRow);

        // Show the results div
        var resultsDiv = document.getElementById("results");
        resultsDiv.style.display = "block";
        resultsDiv.classList.add("fade-in");

        // Hide error message if it was shown previously
        var errorMessage = document.getElementById("error-message");
        errorMessage.textContent = "";
      })
      .catch(error => {
        console.error("Error:", error);

        // Show error message
        var errorMessage = document.getElementById("error-message");
        errorMessage.textContent = "Couldn't analyze the text. Try something else...";

        // Hide the results div
        var resultsDiv = document.getElementById("results");
        resultsDiv.style.display = "none";
      });
}

function handleFormSubmit(event) {
    event.preventDefault(); // Prevent default form submission behavior
    sendRequest();
}

var form = document.querySelector("form");
form.addEventListener("submit", handleFormSubmit);

// Get the button:
let mybutton = document.getElementById("myBtn");

// When the user scrolls down 20px from the top of the document, show the button
window.onscroll = function() {scrollFunction()};

function scrollFunction() {
  if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
    mybutton.style.display = "block";
  } else {
    mybutton.style.display = "none";
  }
}

// When the user clicks on the button, scroll to the top of the document
function topFunction() {
  document.body.scrollTop = 0; // For Safari
  document.documentElement.scrollTop = 0; // For Chrome, Firefox, IE and Opera
  document.getElementById("text").focus();
}