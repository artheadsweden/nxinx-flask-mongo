/****************
 the autocomplete function takes one argument, the text field element
 ****************/
function autocomplete(input) {

    let listIndex;

    /*execute a function when someone writes in the text field:*/
    input.addEventListener("input", function (event) {
        let val = this.value;
        if (!val) {
            return false;
        }

        const params = {
            value: val
        }

        fetch('http://127.0.0.1:5000/ajax/all_users', {
            method: 'post',
            headers: {
                'Content-type': 'application/json'
            },
            body: JSON.stringify(params)
        })

        .then(response => response.json())
        .then(arr => {
            /*close any already open lists of autocompleted values*/
            closeAllLists();

            // Set current focus to -1, so we start from top
            // when we use the arrow keys
            listIndex = -1;

            /*create a DIV element that will contain the items (values):*/
            let autoCompleteList = document.createElement("div");
            autoCompleteList.setAttribute("id", input.id + "autocomplete-list");
            autoCompleteList.setAttribute("class", "autocomplete-items");
            /*append the DIV element as a child of the autocomplete container:*/
            input.parentNode.appendChild(autoCompleteList);

            /*for each item in the array...*/
            arr.forEach(user => {
                /*create a DIV element for each matching element:*/
                let listElement = document.createElement("div");
                /*make the matching letters bold:*/
                listElement.innerHTML = "<strong>" + user.substr(0, val.length) + "</strong>";
                listElement.innerHTML += user.substr(val.length);
                /*insert a input field that will hold the current array item's value:*/
                listElement.innerHTML += "<input type='hidden' value='" + user + "'>";
                /*execute a function when someone clicks on the item value (DIV element):*/
                listElement.addEventListener("click", function (e) {
                    /*insert the value for the autocomplete text field:*/
                    input.value = e.target.getElementsByTagName("input")[0].value;
                    /*close the list of autocompleted values,
                    (or any other open lists of autocompleted values:*/
                    closeAllLists();
                });
                autoCompleteList.appendChild(listElement);
            })
        })
        .catch(error => alert(error));

    });

    /*execute a function presses a key on the keyboard:*/
    input.addEventListener("keydown", function (e) {
        let autoCompleteList = document.getElementById(e.target.id + "autocomplete-list");
        if (autoCompleteList) {
            autoCompleteList = autoCompleteList.getElementsByTagName("div");
        }

        if (e.keyCode === 40) {
            /*If the arrow DOWN key is pressed,
            increase the currentFocus variable:*/
            listIndex++;
            /*and and make the current item more visible:*/
            addActive(autoCompleteList);
        } else if (e.keyCode === 38) { //up
            /*If the arrow UP key is pressed,
            decrease the currentFocus variable:*/
            listIndex--;
            /*and and make the current item more visible:*/
            addActive(autoCompleteList);
        } else if (e.keyCode === 13) {
            /*If the ENTER key is pressed, prevent the form from being submitted,*/
            e.preventDefault();
            if (listIndex > -1) {
                /*and simulate a click on the "active" item:*/
                if (autoCompleteList) {
                    autoCompleteList[listIndex].click();
                }
            }
        }
    });

    function addActive(autoCompleteList) {
        /*a function to classify an item as "active":*/
        if (!autoCompleteList) {
            return false;
        }
        /*start by removing the "active" class on all items:*/
        removeActive(autoCompleteList);
        if (listIndex >= autoCompleteList.length) {
            listIndex = 0;
        }

        if (listIndex < 0) {
            listIndex = (autoCompleteList.length - 1);
        }
        /*add class "autocomplete-active":*/
        autoCompleteList[listIndex].classList.add("autocomplete-active");
    }

    function removeActive(autoCompleteList) {
        /*a function to remove the "active" class from all autocomplete items:*/
        for (let item of autoCompleteList) {
            item.classList.remove("autocomplete-active");
        }
    }

    function closeAllLists() {
        /*close all autocomplete lists in the document,
        except the one passed as an argument:*/

        let autoCompleteList = document.getElementsByClassName("autocomplete-items");
        for (let listElement of autoCompleteList) {
            listElement.parentNode.removeChild(listElement);
        }
    }

    /*execute a function when someone clicks in the document:*/
    document.addEventListener("click", function (e) {
        closeAllLists();
    });
}

/*initiate the autocomplete function on the "myInput" element, and pass along the countries array as possible autocomplete values:*/
autocomplete(document.getElementById("userName"));
