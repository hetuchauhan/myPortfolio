document.addEventListener("DOMContentLoaded", function () {
  // Function to handle the file upload
  document
    .getElementById("file-input")
    .addEventListener("change", function (e) {
      const file = e.target.files[0]; // Get the first file selected

      // Check if the file is a valid JSON file
      if (file && file.type === "application/json") {
        const reader = new FileReader();

        reader.onload = function (event) {
          try {
            const jsonData = JSON.parse(event.target.result); // Parse the JSON data
            populateTable(jsonData); // Populate the table with parsed data
            // Store the parsed data in local storage for future use
            localStorage.setItem("errors", JSON.stringify(jsonData));
          } catch (error) {
            alert("Invalid JSON file."); // Show an error if the file is not valid JSON
          }
        };

        reader.readAsText(file); // Read the file as text
      } else {
        alert("Please upload a valid JSON file."); // Alert for invalid file type
      }
    });

  // Function to populate the table with data
  function populateTable(data) {
    const tableBody = document.getElementById("error-list");

    // Clear previous table rows (if any)
    tableBody.innerHTML = "";

    // Iterate through the data and create a row for each entry
    data.forEach((entry) => {
      const row = document.createElement("tr");
      row.classList.add("hover:bg-gray-100");

      const idCell = document.createElement("td");
      idCell.classList.add(
        "px-4",
        "py-3",
        "text-sm",
        "text-gray-600",
        "border-r",
        "border-black"
      );
      idCell.textContent = entry.id; // Add ID to the first cell
      row.appendChild(idCell);

      const errorsCell = document.createElement("td");
      errorsCell.classList.add(
        "px-4",
        "py-3",
        "text-sm",
        "text-gray-600",
        "border-r",
        "border-black"
      );
      // Check if the error field is an array or string
      errorsCell.textContent = Array.isArray(entry.error)
        ? entry.error.join(", ") // If it's an array, join the errors with commas
        : entry.error; // If it's a string, display it directly
      row.appendChild(errorsCell);

      const probabilityCell = document.createElement("td");
      probabilityCell.classList.add("px-4", "py-3", "text-sm", "text-gray-600");
      probabilityCell.textContent = entry.AcceptanceProbability
        ? (entry.AcceptanceProbability * 100).toFixed(2) + "%" // Format probability as a percentage
        : "N/A"; // Display "N/A" if no probability exists
      row.appendChild(probabilityCell);

      tableBody.appendChild(row); // Append the created row to the table body
    });
  }

  // Check if there is stored data in localStorage and populate the table
  const storedData = JSON.parse(localStorage.getItem("errors"));
  if (storedData) {
    populateTable(storedData); // Populate table with the stored data if it exists
  }

  // Clear button event listener
  document
    .getElementById("clear-button")
    .addEventListener("click", function () {
      // Clear the table
      const tableBody = document.getElementById("error-list");
      tableBody.innerHTML = "";

      // Clear the data in localStorage
      localStorage.removeItem("errors");
    });
});
