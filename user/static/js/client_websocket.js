ClientsSocket.onopen = function (e) {
        console.log("The connection was set up successfully!");
		ClientsSocket.send(JSON.stringify({ action: "update" }));
    };

    ClientsSocket.onclose = function (e) {
        console.log("Something unexpected happened !");
        ClientsSocket.send(JSON.stringify({ action: "update" }));
    };

    ClientsSocket.onerror = (error) => {
        console.log(error);
        ClientsSocket.send(JSON.stringify({ action: "update" }));
    };

    ClientsSocket.onmessage = function (e) {
    const receivedData = JSON.parse(e.data);
        const targetElement = document.getElementById('client-requests-list');
        targetElement.innerHTML = '';
        receivedData.client.forEach((data) => {
        createAndAppendClientProfile(data);
        });
    };

function createAndAppendClientProfile(client) {
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
    imgProfilePhoto.src = client.profile_image;
    imgProfilePhoto.alt = 'user';
    imgProfilePhoto.className = 'profile-photo-lg';

    divProfileImage.appendChild(imgProfilePhoto);

    const divUserInfo = document.createElement('div');
    divUserInfo.className = 'col-md-6 col-sm-6 pt-3';

    const h5ProfileLink = document.createElement('h5');
    h5ProfileLink.className = 'profile-link';
    h5ProfileLink.textContent = `${client.first_name} ${client.last_name}`;

    const pCity = document.createElement('p');
    pCity.textContent = client.city;

    const pCountry = document.createElement('p');
    pCountry.textContent = client.country;

    divUserInfo.appendChild(h5ProfileLink);
    divUserInfo.appendChild(pCity);
    divUserInfo.appendChild(pCountry);

    const divActionButtons = document.createElement('div');
    divActionButtons.className = 'col-md-4 col-sm-4 py-5';

    const declineButton = document.createElement('button');
    declineButton.type = 'button';
    declineButton.className = 'btn btn-outline-danger pull-right mx-2';
    declineButton.textContent = 'Decline';
    declineButton.setAttribute('data-bs-toggle', 'modal');
    declineButton.setAttribute('data-bs-target', '#declineRequestModal');
    declineButton.setAttribute('data-client-username', client.username);

    const acceptButton = document.createElement('button');
    acceptButton.type = 'button';
    acceptButton.className = 'btn btn-success pull-right';
    acceptButton.textContent = 'Accept';
    acceptButton.setAttribute('data-bs-toggle', 'modal');
    acceptButton.setAttribute('data-bs-target', '#acceptRequestModal');
    acceptButton.setAttribute('data-client-username', client.username);

    divActionButtons.appendChild(declineButton);
    divActionButtons.appendChild(acceptButton);

    divRow.appendChild(divProfileImage);
    divRow.appendChild(divUserInfo);
    divRow.appendChild(divActionButtons);

    divNearbyUser.appendChild(divRow);
    divPeopleNearby.appendChild(divNearbyUser);
    divContainer.appendChild(divPeopleNearby);

    const targetElement = document.getElementById('client-requests-list');
    targetElement.appendChild(divContainer);
}
