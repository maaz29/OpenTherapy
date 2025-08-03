RequestsSocket.onopen = function (e) {
        console.log("The connection was set up successfully!");
		RequestsSocket.send(JSON.stringify({ action: "update" }));
    };

    RequestsSocket.onclose = function (e) {
        console.log("Something unexpected happened !");
        RequestsSocket.send(JSON.stringify({ action: "update" }));
    };

    RequestsSocket.onerror = (error) => {
        console.log(error);
        RequestsSocket.send(JSON.stringify({ action: "update" }));
    };

    RequestsSocket.onmessage = function (e) {
    const receivedData = JSON.parse(e.data);
        const targetElement = document.getElementById('requests-list');
        targetElement.innerHTML = '';
        receivedData.therapists.forEach((data) => {
        createAndAppendTherapistProfile(data);
        });
    };

function createAndAppendTherapistProfile(therapist) {
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
    imgProfilePhoto.src = therapist.profile_image;
    imgProfilePhoto.alt = 'user';
    imgProfilePhoto.className = 'profile-photo-lg';

    divProfileImage.appendChild(imgProfilePhoto);

    const divUserInfo = document.createElement('div');
    divUserInfo.className = 'col-md-6 col-sm-6 pt-3';

    const h5ProfileLink = document.createElement('h5');
    h5ProfileLink.className = 'profile-link';
    h5ProfileLink.textContent = `${therapist.first_name} ${therapist.last_name}`;

    const pCity = document.createElement('p');
    pCity.textContent = therapist.city;

    const pCountry = document.createElement('p');
    pCountry.textContent = therapist.country;

    divUserInfo.appendChild(h5ProfileLink);
    divUserInfo.appendChild(pCity);
    divUserInfo.appendChild(pCountry);

    const divActionButtons = document.createElement('div');
    divActionButtons.className = 'col-md-4 col-sm-4 py-5';

    const cancelButton = document.createElement('button');
    cancelButton.type = 'button';
    cancelButton.className = 'btn btn-outline-danger pull-right mx-2';
    cancelButton.textContent = 'Cancel Request';
    cancelButton.setAttribute('data-bs-toggle', 'modal');
    cancelButton.setAttribute('data-bs-target', '#cancelRequestModal');
    cancelButton.setAttribute('data-therapist-username', therapist.username);

    console.log(therapist.client_username);
    console.log(therapist.username);
    console.log(therapist.duration);
    const joinChatButton = document.createElement('a');
    const disabledJoinChatButton = document.createElement('button');
    if (therapist.status === 'accepted') {
    joinChatButton.href = `/chat/chat-room/${therapist.client_username}-${therapist.username}?session_duration=${therapist.duration}`;
    }
    joinChatButton.type = 'button';
    joinChatButton.className = 'btn btn-success pull-right mx-1';
    joinChatButton.textContent = 'Join Chat';
    disabledJoinChatButton.type = 'button';
    disabledJoinChatButton.className = 'btn btn-success pull-right mx-1';
    disabledJoinChatButton.textContent = 'Join Chat';
    if (therapist.status !== 'accepted') {
        disabledJoinChatButton.disabled = true;
    }

    const statusButton = document.createElement('button');
    statusButton.type = 'button';
    statusButton.className = 'btn ml-1';

    if (therapist.status === 'accepted') {
        statusButton.className += ' btn-success';
        statusButton.textContent = 'Accepted';
    } else if (therapist.status === 'pending') {
        statusButton.className += ' btn-warning';
        statusButton.textContent = 'Pending';
    } else {
        statusButton.className += ' btn-danger';
        statusButton.textContent = 'Declined';
    }

    divActionButtons.appendChild(cancelButton);
    if (therapist.status === 'accepted') {
        divActionButtons.appendChild(joinChatButton);
    }
    else{
        divActionButtons.appendChild(disabledJoinChatButton);
    }
    divActionButtons.appendChild(statusButton);

    divRow.appendChild(divProfileImage);
    divRow.appendChild(divUserInfo);
    divRow.appendChild(divActionButtons);

    divNearbyUser.appendChild(divRow);
    divPeopleNearby.appendChild(divNearbyUser);
    divContainer.appendChild(divPeopleNearby);

    const targetElement = document.getElementById('requests-list');
    targetElement.appendChild(divContainer);
}
