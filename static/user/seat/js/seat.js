occupiedHandler();
const seats = document.querySelectorAll(".row .seat:not(.occupied)");
const seatContainer = document.querySelector(".row-container");
const count = document.getElementById("count");
const total = document.getElementById("total");
const seatValue = document.getElementById("seatValue");
const movieSelect = document.getElementById("movie");

// old one        // Another Approach

// seats.forEach(function(seat) {
//   seat.addEventListener("click", function(e) {
//     seat.classList.add("selected");
//     const selectedSeats = document.querySelectorAll(".container .selected");
//     selectedSeathLength = selectedSeats.length;
//     count.textContent = selectedSeathLength;
//     let ticketPrice = +movieSelect.value;
//     total.textContent = ticketPrice * selectedSeathLength;
//   });
// });

// localStorage.clear();

// old one

populateUI();

let ticketPrice = +movieSelect.value;

// Save selected movie index and price
function setMovieData(movieIndex, moviePrice) {
    localStorage.setItem("selectedMovieIndex", movieIndex);
    localStorage.setItem("selectedMoviePrice", moviePrice);
}


function updateSelectedCount() {
    let seatNumber = [];
    const selectedSeats = document.querySelectorAll(".container .selected");
    seatsIndex = [...selectedSeats].map(function (seat) {
        seatNumber.push(seat.innerHTML)
        return [...seats].indexOf(seat);

    });
    console.log(seatsIndex);
    console.log(seatNumber);

    localStorage.setItem("selectedSeats", JSON.stringify(seatsIndex));

    let selectedSeatsCount = selectedSeats.length;
    count.textContent = selectedSeatsCount;
    total.textContent = selectedSeatsCount * ticketPrice;
    localStorage.setItem("totalPrice", selectedSeatsCount * ticketPrice);
    localStorage.setItem("seatCount", selectedSeatsCount);
    localStorage.setItem("seatNumber", seatNumber);
    let arragedNumber = "";
    seatNumber.forEach(number => {
        arragedNumber = `${number},${arragedNumber}`
    })
    console.log(arragedNumber);
    seatValue.innerHTML = arragedNumber;

}

// Get data from localstorage and populate
function populateUI() {
    occupiedHandler();
    const selectedSeats = JSON.parse(localStorage.getItem("selectedSeats"));

    if (selectedSeats !== null && selectedSeats.length > 0) {
        seats.forEach(function (seat, index) {
            if (selectedSeats.indexOf(index) > -1) {
                // seat.classList.add("selected");
            }
        });
    }

    const selectedMovieIndex = localStorage.getItem("selectedMovieIndex");

    if (selectedMovieIndex !== null) {
        movieSelect.selectedIndex = selectedMovieIndex;
    }
}

// Movie select event

movieSelect.addEventListener("change", function (e) {
    ticketPrice = +movieSelect.value;
    setMovieData(e.target.selectedIndex, e.target.value);
    console.log(e.target.selectedIndex);
    findSeatSelection(e.target.selectedIndex);
    updateSelectedCount();
});

// Adding selected class to only non-occupied seats on 'click'

seatContainer.addEventListener("click", function (e) {
    let typeOfSeate = localStorage.getItem("typeOfSeat")
    if (
        e.target.classList.contains("seat") &&
        !e.target.classList.contains("occupied") && e.target.classList.contains(typeOfSeate)
    ) {
        e.target.classList.toggle("selected");
        updateSelectedCount();
    } else if (
        e.target.classList.contains("seat") &&
        !e.target.classList.contains("occupied") && e.target.classList.contains(typeOfSeate)
    ) {
        e.target.classList.toggle("selected");
        updateSelectedCount();
    } else if (
        e.target.classList.contains("seat") &&
        !e.target.classList.contains("occupied") && e.target.classList.contains(typeOfSeate)
    ) {
        e.target.classList.toggle("selected");
        updateSelectedCount();
    } else if (
        e.target.classList.contains("seat") &&
        !e.target.classList.contains("occupied") && e.target.classList.contains(typeOfSeate)
    ) {
        e.target.classList.toggle("selected");
        updateSelectedCount();
    } else {

    }
});

// Initial count and total rendering
updateSelectedCount();

let normalSeat = {{ normal_seats }};
let exicutiveSeat = {{ executive_seats }};
let premiumSeat = {{ premium_seats }};
let vipSeat = {{ vip_seats }};

let choiceNormal = document.getElementById("choiceNormal");
let choiceExecutive = document.getElementById("choiceExecutive");
let choicePremium = document.getElementById("choicePremium");
let choiceVip = document.getElementById("choiceVip");

seatArragement();

function findSeatSelection(seatType) {
    let seatCount = 0;
    let typeOfSeate = "";
    if (seatType === 0) {
        seatCount = null;
        typeOfSeate = "";
    } else if (seatType === 1) {
        seatCount = {{ normal_seats }};
    typeOfSeate = "normal";
} else if (seatType === 2) {
    seatCount = {{ executive_seats }};
typeOfSeate = "exicutive";
    } else if (seatType === 3) {
    seatCount = {{ premium_seats }};
typeOfSeate = "premium";
    } else if (seatType === 4) {
    seatCount = {{ vip_seats }};
typeOfSeate = "vip";
    }
console.log(typeOfSeate);
localStorage.setItem("typeOfSeat", typeOfSeate);
console.log(seatCount);
let seat = document.querySelectorAll(".seat")
console.log(seatType);
for (let seatNum = 0; seatNum < {{ totalSeat }}; seatNum++) {
    // console.log(seat[seatNum]);
    if (seatCount === null && seatType === 0) {
        console.log("choice");
        seat[seatNum].style.cursor = "text";
    } else if (seatNum >= 0 && seatNum < seatCount && seatType === 1) {
        seat[seatNum].style.cursor = "pointer"
        console.log("normal");
    } else if (seatNum >= {{ normal_seats }} && seatNum < (seatCount + {{ normal_seats }}) && seatType === 2 ) {
    seat[seatNum].style.cursor = "pointer"
    console.log("exicutive");
} else if (seatNum >= {{ executive_seats }}+{{ normal_seats }} && seatNum < (seatCount + {{ normal_seats }}+{{ executive_seats }}) && seatType === 3) {
    seat[seatNum].style.cursor = "pointer"
    console.log("premium");
} else if (seatNum >= {{ premium_seats }}+{{ normal_seats }}+{{ executive_seats }} && seatNum < (seatCount + {{ normal_seats }}+{{ executive_seats }}+{{ premium_seats }}) && seatType === 4 ) {
    seat[seatNum].style.cursor = "pointer"
    console.log("vip");
} else {
    seat[seatNum].style.cursor = "text"
    console.log("else");
}
}

function choiceHandler(seatType) {
    console.log(seatType);
}

    // normal.style.cursor = "pointer !importent"
    // exicutive.style.cursor = "default !importent"
    // premium.style.cursor = "default !importent"
    // vip.style.cursor = "default !importent"
    // } else if (seatType === "exicutive") {
    //     exicutive.style.cursor = "default"
    // } else if (seatType === "premium") {
    //     premium.style.cursor = "default"
    // } else {
    //     vip.style.cursor = "default"
    // }
}
function seatArragement() {

    let normal = document.getElementById("normal")
    let exicutive = document.getElementById("exicutive")
    let premium = document.getElementById("premium")
    let vip = document.getElementById("vip")
    let seatVal = {{ row_count }};
let seatTolerence = seatVal
let outerValue = {{ row_count }}
console.log('seatTolerence:', seatTolerence, 'outerValue:', outerValue);
for (let outer = outerValue; seatTolerence <= normalSeat;) {
    parentDiv = document.createElement("div");
    parentDiv.classList.add("row");
    for (let inner = 0; inner < seatTolerence; inner++) {
        let childDiv = document.createElement("div");
        childDiv.classList.add("seat");
        childDiv.classList.add("normal");
        // for (let i = 0; i<seatTolerence;i++){
        //     childDiv.innerHTML = rowsCount[i]+i;
        //     console.log(rowsCount[i]+i);
        // }

        // childDiv.innerHTML = rowsCount[inner]+inner;
        // console.log(rowsCount[inner]+inner);

        parentDiv.appendChild(childDiv);
    }
    if (seatTolerence === 0) {
        break;
    }
    normalSeat = normalSeat - seatTolerence
    if (outer < normalSeat) {
        seatTolerence = seatVal
    }
    else {
        seatTolerence = normalSeat
    }
    normal.appendChild(parentDiv);
}
// console.log(normal);

seatTolerence = seatVal
for (let outer = outerValue; seatTolerence <= exicutiveSeat;) {
    parentDiv = document.createElement("div");
    parentDiv.classList.add("row");
    for (let inner = 0; inner < seatTolerence; inner++) {
        let childDiv = document.createElement("div");
        childDiv.classList.add("seat");
        childDiv.classList.add("exicutive");
        parentDiv.appendChild(childDiv);
    }
    if (seatTolerence === 0) {
        break;
    }
    exicutiveSeat = exicutiveSeat - seatTolerence
    if (outer < exicutiveSeat) {
        seatTolerence = seatVal
    }
    else {
        seatTolerence = exicutiveSeat
    }
    exicutive.appendChild(parentDiv);
}
// console.log(exicutive);

seatTolerence = seatVal
for (let outer = outerValue; seatTolerence <= premiumSeat;) {
    parentDiv = document.createElement("div");
    parentDiv.classList.add("row");
    for (let inner = 0; inner < seatTolerence; inner++) {
        let childDiv = document.createElement("div");
        childDiv.classList.add("seat");
        childDiv.classList.add("premium");
        parentDiv.appendChild(childDiv);
    }
    if (seatTolerence === 0) {
        break;
    }
    premiumSeat = premiumSeat - seatTolerence
    if (outer < premiumSeat) {
        seatTolerence = seatVal
    }
    else {
        seatTolerence = premiumSeat
    }
    premium.appendChild(parentDiv);
}
// console.log(premium);

seatTolerence = seatVal
for (let outer = outerValue; seatTolerence <= vipSeat;) {
    parentDiv = document.createElement("div");
    parentDiv.classList.add("row");
    for (let inner = 0; inner < seatTolerence; inner++) {
        let childDiv = document.createElement("div");
        childDiv.classList.add("seat");
        childDiv.classList.add("vip");
        parentDiv.appendChild(childDiv);
    }
    if (seatTolerence === 0) {
        break;
    }
    vipSeat = vipSeat - seatTolerence
    if (outer < vipSeat) {
        seatTolerence = seatVal
    }
    else {
        seatTolerence = vipSeat
    }
    vip.appendChild(parentDiv);
}
// console.log(vip);
seatNumberAssignment();
}

function seatNumberAssignment() {
    let rowsCount = []
    let seatStatus = [0, {{ normal_seats }}, {{ executive_seats }}, {{ premium_seats }}, {{ vip_seats }}]
let rowIncrementCounter = 1;
let startingCount = 0;
let endingCount = 1;
let seatStatusCount = 0;
seatDiv = document.querySelectorAll(".seat");
console.log(seatStatus);
let seatvl = {{ row_count }};
let ascii = 65;
// let arrayRow = []

for (let index = 0; index < seatvl; index++) {
    let rowVal = String.fromCharCode(ascii);
    rowsCount.push(rowVal)
    ascii++;
}
console.log("array :", rowsCount);

for (let index = 0; index < seatDiv.length;) {

    for (let rowindex = 0; rowindex < rowsCount.length; rowindex++) {
        // console.log(div);
        // index >= seatStatus[startingCount] && 
        if (index < seatStatus[endingCount] + seatStatus[2] + seatStatus[3] + seatStatus[4]) {
            seatDiv[index].innerHTML = rowsCount[rowindex] + rowIncrementCounter;

        }
        index++;
    };
    rowIncrementCounter++;


}
    
}
num = localStorage.getItem("seatNumber")
console.log(typeof num);

document.getElementById("cancelTicket").addEventListener("click", () => {
    localStorage.removeItem("seatCount")
    localStorage.removeItem("totalPrice")
    localStorage.removeItem("seatNumber")
    localStorage.removeItem("typeOfSeat")
    localStorage.removeItem("selectedMoviePrice")
    localStorage.removeItem("selectedMovieIndex")
    localStorage.removeItem("selectedSeats")
})

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

document.getElementById("placeOrder").addEventListener("click", () => {
    $.ajax({
        url: '/checkout/',
        type: 'POST',
        data: {
            seatNumber: localStorage.getItem("seatNumber"),
            csrfmiddlewaretoken: csrftoken,
        },
        dataType: 'json',
        success: function (data) {
            if (data) {
                window.location.href = '/checkout_Ticket/';
            }
        }
    });
})
function occupiedHandler() {
    var seatNumber = localStorage.getItem("seatNumber");
    var seatCount = localStorage.getItem("seatCount");
    var typeOfSeat = localStorage.getItem("typeOfSeat");
    var totalPrice = localStorage.getItem("totalPrice");
    var selectedSeats = localStorage.getItem("selectedSeats");
    var selectedMoviePrice = localStorage.getItem("selectedMoviePrice");
    console.log('seatnumber 1:', seatNumber, seatCount, typeOfSeat, totalPrice, selectedSeats, selectedMoviePrice);
    console.log('inner handler:');
    $.ajax({
        type: 'GET',
        url: '/seatreconnect/',
        dataType: 'json',
        data: {
            'seatNumber': seatNumber,
            'seatCount': seatCount,
            'typeOfSeat': typeOfSeat,
            'totalPrice': totalPrice,
            'selectedSeats': selectedSeats,
            'selectedMoviePrice': selectedMoviePrice,
        },
        success: function (data) {
            if (data) {
                console.log(data);
                let totalSeatIndex = data.split(",");
                let indexOfSeat = document.querySelectorAll(".seat");
                console.log(indexOfSeat[0].innerHTML);
                console.log(totalSeatIndex);
                for (let value = 0; value < indexOfSeat.length; value++) {
                    for (let count = 0; count < totalSeatIndex.length; count++) {
                        if (indexOfSeat[value].innerHTML == totalSeatIndex[count]) {
                            indexOfSeat[count].classList.add("selected")
                            // console.log(indexOfSeat[count]); 

                        }       
                    }                        
                }
                // console.log(indexOfSeat);
            }
        }
    });
}
