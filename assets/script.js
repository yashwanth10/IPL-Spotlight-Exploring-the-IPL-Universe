

// document.addEventListener("DOMContentLoaded", () => {
//     const imageContainers = document.querySelectorAll(".image-container");
//     imageContainers.forEach((container) => {
//         container.addEventListener("mouseover", () => {
//             const teamCode = container.dataset.teamCode;
//             fetch("./data/Logo-hover.csv")  // Assuming data.csv contains your CSV-like data
//                 .then((response) => response.text())
//                 .then((csvText) => {
//                     const data = csvText.split("\n");
//                     const rowData = data.find((row) => row.startsWith(teamCode));
//                     if (rowData) {
//                         const [team, seasons, brandValue, fanBase] = rowData.split(",");
//                         const dataTooltip = container.querySelector(".data-tooltip");
//                         dataTooltip.innerHTML = `
//                             <strong>Team:</strong> ${team}<br>
//                             <strong>Seasons Won:</strong> ${seasons}<br>
//                             <strong>Brand Value:</strong> ${brandValue}<br>
//                             <strong>Fan Base:</strong> ${fanBase}<br>
//                         `;
//                     }
//                 });
//         });
//     });
// });
