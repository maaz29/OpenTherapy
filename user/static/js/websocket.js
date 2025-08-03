activeTherapistsSocket.onopen = function (e) {
    console.log("The connection was set up successfully!");
    activeTherapistsSocket.send(JSON.stringify({ action: "update" }));
};

activeTherapistsSocket.onclose = function (e) {
    console.log("Something unexpected happened !");
    activeTherapistsSocket.send(JSON.stringify({ action: "update" }));
};

activeTherapistsSocket.onerror = (error) => {
  activeTherapistsSocket.send(JSON.stringify({ action: "update" }));
};

activeTherapistsSocket.onmessage = function (e) {
const receivedData = JSON.parse(e.data);
    const targetElement = document.getElementById('card-list');
    targetElement.innerHTML = '';
    receivedData.therapists.forEach((data) => {
    createAndAppendUserProfile(data);
    });
};


function createAndAppendUserProfile(data) {
    const divContainer = document.createElement('div');
    divContainer.className = 'text-center';

    const divPeopleNearby = document.createElement('div');
    divPeopleNearby.className = 'people-nearby';

    const divNearbyUser = document.createElement('div');
    divNearbyUser.className = 'nearby-user py-2 pull-left';

    const divRow = document.createElement('div');
    divRow.className = 'row';

    const divProfileImage = document.createElement('div');
    divProfileImage.className = 'col-md-2 col-sm-2 py-4';

    const imgProfilePhoto = document.createElement('img');
    imgProfilePhoto.src = data.profile_image;
    imgProfilePhoto.alt = 'user';
    imgProfilePhoto.className = 'profile-photo-lg';

    divProfileImage.appendChild(imgProfilePhoto);

    const divUserInfo = document.createElement('div');
    divUserInfo.className = 'col-md-7 col-sm-7 pt-3';

    const h5ProfileLink = document.createElement('h5');
    h5ProfileLink.className = 'profile-link';
    h5ProfileLink.textContent = `${data.first_name} ${data.last_name}`;

    const pCity = document.createElement('p');
    pCity.textContent = data.city;

    const pCountry = document.createElement('p');
    pCountry.textContent = data.country;

    divUserInfo.appendChild(h5ProfileLink);
    divUserInfo.appendChild(pCity);
    divUserInfo.appendChild(pCountry);

    const divActionButtons = document.createElement('div');
    divActionButtons.className = 'col-md-3 col-sm-3 py-5';

    const button = document.createElement('button');
    button.type = 'button';
    button.className = 'btn btn-primary pull-right';

    if (data.requested_therapists.includes(data.username)) {
        button.textContent = 'Requested';
        button.disabled = true;
    } else {
        button.textContent = 'Request Session';
        button.setAttribute('data-bs-toggle', 'modal');
        button.setAttribute('data-bs-target', '#sessionBookingModal');
        button.setAttribute('data-therapist-first-name', data.first_name);
        button.setAttribute('data-therapist-last-name', data.last_name);
        button.setAttribute('data-therapist-age', data.age);
        button.setAttribute('data-therapist-username', data.username);
    }

    divActionButtons.appendChild(button);

    divRow.appendChild(divProfileImage);
    divRow.appendChild(divUserInfo);
    divRow.appendChild(divActionButtons);

    divNearbyUser.appendChild(divRow);
    divPeopleNearby.appendChild(divNearbyUser);
    divContainer.appendChild(divPeopleNearby);

    const targetElement = document.getElementById('card-list');
    targetElement.appendChild(divContainer);
}
